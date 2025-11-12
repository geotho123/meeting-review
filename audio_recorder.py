"""
Audio recording module for meeting recorder.
"""
import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime
import os
import threading
import time


class AudioRecorder:
    """Records audio from the default microphone."""

    def __init__(self, sample_rate=44100, channels=2, output_dir="recordings"):
        """
        Initialize the audio recorder.

        Args:
            sample_rate: Sample rate in Hz
            channels: Number of audio channels (1=mono, 2=stereo)
            output_dir: Directory to save recordings
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.output_dir = output_dir
        self.recording = False
        self.audio_data = []
        self.stream = None

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def _audio_callback(self, indata, frames, time_info, status):
        """Callback function for audio stream."""
        if status:
            print(f"Status: {status}")
        if self.recording:
            self.audio_data.append(indata.copy())

    def start_recording(self):
        """Start recording audio."""
        if self.recording:
            print("Already recording!")
            return

        print("Starting recording...")
        self.recording = True
        self.audio_data = []

        # Try configured channels first, fallback to mono if needed
        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self._audio_callback
            )
        except Exception as e:
            if self.channels == 2:
                print(f"Stereo recording not supported, falling back to mono: {e}")
                self.channels = 1
                self.stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    callback=self._audio_callback
                )
            else:
                raise

        self.stream.start()
        print("Recording started. Press Enter or call stop_recording() to stop.")

    def stop_recording(self, filename=None):
        """
        Stop recording and save to file.

        Args:
            filename: Optional filename. If not provided, generates timestamp-based name.

        Returns:
            str: Path to the saved audio file
        """
        if not self.recording:
            print("Not recording!")
            return None

        print("Stopping recording...")
        self.recording = False

        if self.stream:
            self.stream.stop()
            self.stream.close()

        # Concatenate all audio chunks
        if not self.audio_data:
            print("No audio data recorded!")
            return None

        audio_array = np.concatenate(self.audio_data, axis=0)

        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"meeting_{timestamp}.wav"

        filepath = os.path.join(self.output_dir, filename)

        # Save audio file
        sf.write(filepath, audio_array, self.sample_rate)
        print(f"Recording saved to: {filepath}")

        return filepath

    def record_with_duration(self, duration_seconds, filename=None):
        """
        Record audio for a specific duration.

        Args:
            duration_seconds: Duration to record in seconds
            filename: Optional filename

        Returns:
            str: Path to the saved audio file
        """
        self.start_recording()

        print(f"Recording for {duration_seconds} seconds...")
        for i in range(duration_seconds, 0, -1):
            print(f"\rTime remaining: {i} seconds  ", end="", flush=True)
            time.sleep(1)
        print()

        return self.stop_recording(filename)

    @staticmethod
    def list_audio_devices():
        """List all available audio devices."""
        print("\nAvailable audio devices:")
        print(sd.query_devices())

    def is_recording(self):
        """Check if currently recording."""
        return self.recording
