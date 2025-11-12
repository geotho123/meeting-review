#!/usr/bin/env python3
"""
Flask web application for Meeting Recorder with real-time STAR format answers
"""
import os
import time
import json
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sounddevice as sd
import soundfile as sf
import numpy as np
import base64
import io

from config import Config
from transcription import Transcriber
from ai_assistant import AIAssistant

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global state
config = Config()
transcriber = None
ai_assistant = None
recording_state = {
    'is_recording': False,
    'audio_data': [],
    'stream': None,
    'start_time': None,
    'duration': None
}


def init_services():
    """Initialize transcription and AI services."""
    global transcriber, ai_assistant

    if not transcriber:
        transcriber = Transcriber(
            api_key=config.openai_api_key,
            output_dir=config.transcripts_dir
        )

    if not ai_assistant:
        ai_assistant = AIAssistant(
            provider=config.ai_provider,
            anthropic_key=config.anthropic_api_key,
            openai_key=config.openai_api_key
        )


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html', ai_provider=config.ai_provider.upper())


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration."""
    return jsonify({
        'ai_provider': config.ai_provider,
        'sample_rate': config.sample_rate,
        'channels': config.channels
    })


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print('Client connected')
    emit('status', {'message': 'Connected to server', 'type': 'success'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')
    # Stop recording if active
    if recording_state['is_recording']:
        stop_recording_internal()


@socketio.on('start_recording')
def handle_start_recording(data):
    """Start recording audio."""
    duration = data.get('duration', None)  # Duration in seconds

    if recording_state['is_recording']:
        emit('error', {'message': 'Already recording'})
        return

    try:
        recording_state['is_recording'] = True
        recording_state['audio_data'] = []
        recording_state['start_time'] = time.time()
        recording_state['duration'] = duration

        emit('status', {'message': f'Recording started ({duration}s)', 'type': 'success'})

        # Start recording in background thread
        thread = threading.Thread(target=record_audio, args=(duration,))
        thread.daemon = True
        thread.start()

    except Exception as e:
        recording_state['is_recording'] = False
        emit('error', {'message': f'Failed to start recording: {str(e)}'})


def record_audio(duration):
    """Record audio in background thread."""
    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"Audio status: {status}")
        if recording_state['is_recording']:
            recording_state['audio_data'].append(indata.copy())

    try:
        # Create audio stream
        stream = sd.InputStream(
            samplerate=config.sample_rate,
            channels=config.channels,
            callback=audio_callback
        )
        recording_state['stream'] = stream
        stream.start()

        # Record for specified duration
        start_time = time.time()
        while recording_state['is_recording']:
            elapsed = time.time() - start_time

            # Send progress update
            socketio.emit('recording_progress', {
                'elapsed': int(elapsed),
                'duration': duration
            })

            # Stop if duration reached
            if duration and elapsed >= duration:
                socketio.emit('status', {
                    'message': 'Recording duration reached',
                    'type': 'info'
                })
                stop_recording_internal()
                break

            time.sleep(0.1)

    except Exception as e:
        print(f"Recording error: {e}")
        socketio.emit('error', {'message': f'Recording error: {str(e)}'})
        recording_state['is_recording'] = False


@socketio.on('stop_recording')
def handle_stop_recording():
    """Stop recording and process audio."""
    if not recording_state['is_recording']:
        emit('error', {'message': 'Not recording'})
        return

    stop_recording_internal()


def stop_recording_internal():
    """Internal function to stop recording."""
    if not recording_state['is_recording']:
        return

    recording_state['is_recording'] = False

    try:
        # Stop stream
        if recording_state['stream']:
            recording_state['stream'].stop()
            recording_state['stream'].close()

        # Process audio
        if recording_state['audio_data']:
            socketio.emit('status', {
                'message': 'Processing audio...',
                'type': 'info'
            })

            # Save audio file
            audio_array = np.concatenate(recording_state['audio_data'], axis=0)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"meeting_{timestamp}.wav"

            os.makedirs(config.recordings_dir, exist_ok=True)
            filepath = os.path.join(config.recordings_dir, filename)
            sf.write(filepath, audio_array, config.sample_rate)

            socketio.emit('recording_complete', {
                'filename': filename,
                'filepath': filepath,
                'duration': time.time() - recording_state['start_time']
            })

            # Start transcription in background
            thread = threading.Thread(target=transcribe_audio, args=(filepath,))
            thread.daemon = True
            thread.start()
        else:
            socketio.emit('error', {'message': 'No audio data recorded'})

    except Exception as e:
        print(f"Error stopping recording: {e}")
        socketio.emit('error', {'message': f'Error processing audio: {str(e)}'})


def transcribe_audio(filepath):
    """Transcribe audio in background."""
    try:
        init_services()

        socketio.emit('status', {
            'message': 'Transcribing audio...',
            'type': 'info'
        })

        start_time = time.time()
        result = transcriber.transcribe_audio(filepath, save_transcript=True)
        transcription_time = int((time.time() - start_time) * 1000)  # milliseconds

        socketio.emit('transcription_complete', {
            'text': result['text'],
            'file_path': result.get('file_path'),
            'time_ms': transcription_time
        })

    except Exception as e:
        print(f"Transcription error: {e}")
        socketio.emit('error', {'message': f'Transcription failed: {str(e)}'})


@socketio.on('get_answer')
def handle_get_answer(data):
    """Generate STAR format answer for a question."""
    question = data.get('question')
    transcript = data.get('transcript')
    format_type = data.get('format', 'bullets')  # 'bullets' or 'full'

    if not question or not transcript:
        emit('error', {'message': 'Question and transcript required'})
        return

    try:
        init_services()

        emit('status', {
            'message': f'Generating {format_type} STAR answer...',
            'type': 'info'
        })

        start_time = time.time()

        # Generate STAR answer
        result = ai_assistant.generate_star_answer(question, transcript, format_type)

        generation_time = int((time.time() - start_time) * 1000)  # milliseconds

        emit('answer_ready', {
            'question': question,
            'answer': result['full_response'],
            'components': result['components'],
            'format_type': format_type,
            'time_ms': generation_time,
            'provider': config.ai_provider
        })

    except Exception as e:
        print(f"Error generating answer: {e}")
        emit('error', {'message': f'Failed to generate answer: {str(e)}'})


@socketio.on('quick_answer')
def handle_quick_answer(data):
    """Generate a quick answer optimized for speed."""
    question = data.get('question')
    transcript = data.get('transcript')
    format_type = data.get('format', 'bullets')

    if not question or not transcript:
        emit('error', {'message': 'Question and transcript required'})
        return

    try:
        init_services()

        start_time = time.time()
        answer = ai_assistant.quick_answer(question, transcript, format_type)
        generation_time = int((time.time() - start_time) * 1000)

        emit('quick_answer_ready', {
            'question': question,
            'answer': answer,
            'format_type': format_type,
            'time_ms': generation_time,
            'provider': config.ai_provider
        })

    except Exception as e:
        print(f"Error generating quick answer: {e}")
        emit('error', {'message': f'Failed to generate answer: {str(e)}'})


@app.route('/api/test', methods=['GET'])
def test_api():
    """Test API endpoint."""
    return jsonify({
        'status': 'ok',
        'message': 'Meeting Recorder API is running',
        'ai_provider': config.ai_provider
    })


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("Meeting Recorder Web Application")
    print("=" * 80)
    print(f"AI Provider: {config.ai_provider.upper()}")
    print(f"Server starting on http://localhost:5000")
    print("=" * 80 + "\n")

    # Create necessary directories
    os.makedirs(config.recordings_dir, exist_ok=True)
    os.makedirs(config.transcripts_dir, exist_ok=True)

    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
