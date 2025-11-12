"""
Real-time audio processing module for live transcription and question detection.
Processes audio in chunks to enable real-time responses during long meetings/interviews.
"""
import re
import queue
import threading
import time
from collections import deque
from datetime import datetime


class QuestionDetector:
    """Detects questions in transcribed text."""

    # Common question patterns for interviews and meetings
    QUESTION_PATTERNS = [
        r'\b(what|why|how|when|where|who|which)\b.*\?',
        r'\b(tell me about|describe|explain|walk me through)\b.*',
        r'\b(can you|could you|would you|will you)\b.*\?',
        r'\b(have you|do you|did you|are you|were you)\b.*\?',
        r'\b(give me an example of|share an experience)\b.*',
        r'\b(talk about a time when)\b.*',
    ]

    QUESTION_KEYWORDS = [
        'what', 'why', 'how', 'when', 'where', 'who', 'which',
        'tell me', 'describe', 'explain', 'walk me through',
        'can you', 'could you', 'would you',
        'have you', 'do you', 'did you',
        'give me an example', 'share', 'talk about'
    ]

    @staticmethod
    def is_question(text):
        """
        Check if text contains a question.

        Args:
            text: Text to analyze

        Returns:
            bool: True if text appears to be a question
        """
        text_lower = text.lower().strip()

        # Check for question mark
        if '?' in text:
            return True

        # Check patterns
        for pattern in QuestionDetector.QUESTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True

        return False

    @staticmethod
    def extract_questions(text):
        """
        Extract all questions from text.

        Args:
            text: Text to analyze

        Returns:
            list: List of detected questions
        """
        questions = []

        # Split into sentences - more flexible splitting
        sentences = re.split(r'[.!?]+|\n+', text)

        print(f"[QuestionDetector] Analyzing text with {len(sentences)} sentences")

        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:  # Minimum length
                is_q = QuestionDetector.is_question(sentence)
                print(f"[QuestionDetector] '{sentence[:50]}...' -> Question: {is_q}")

                if is_q:
                    # Add question mark if missing
                    if not sentence.endswith('?'):
                        sentence += '?'
                    questions.append(sentence)
                    print(f"[QuestionDetector] ✓ Added question: {sentence[:60]}...")

        print(f"[QuestionDetector] Found {len(questions)} questions total")
        return questions


class RealtimeProcessor:
    """
    Processes audio in real-time for live transcription and answer generation.
    """

    def __init__(self, transcriber, ai_assistant, chunk_duration=10, overlap=2):
        """
        Initialize real-time processor.

        Args:
            transcriber: Transcriber instance
            ai_assistant: AIAssistant instance
            chunk_duration: Duration of each audio chunk in seconds
            overlap: Overlap between chunks in seconds (to avoid word cutoffs)
        """
        self.transcriber = transcriber
        self.ai_assistant = ai_assistant
        self.chunk_duration = chunk_duration
        self.overlap = overlap

        # Audio buffer and processing queue
        self.audio_queue = queue.Queue()
        self.is_processing = False

        # Transcript storage
        self.full_transcript = ""
        self.recent_transcript = deque(maxlen=20)  # Keep last 20 chunks
        self.detected_questions = []

        # Callbacks
        self.on_transcript_update = None
        self.on_question_detected = None
        self.on_answer_ready = None

        # Processing thread
        self.processing_thread = None

    def start(self):
        """Start real-time processing."""
        if self.is_processing:
            return

        self.is_processing = True
        self.processing_thread = threading.Thread(target=self._process_loop, daemon=True)
        self.processing_thread.start()
        print("Real-time processor started")

    def stop(self):
        """Stop real-time processing."""
        self.is_processing = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5)
        print("Real-time processor stopped")

    def add_audio_chunk(self, audio_data, sample_rate):
        """
        Add audio chunk to processing queue.

        Args:
            audio_data: Audio data as numpy array
            sample_rate: Sample rate of audio
        """
        self.audio_queue.put({
            'audio': audio_data,
            'sample_rate': sample_rate,
            'timestamp': time.time()
        })

    def _process_loop(self):
        """Main processing loop (runs in background thread)."""
        print("[RealtimeProcessor] Processing loop started")

        while self.is_processing:
            try:
                # Get audio chunk from queue (with timeout)
                chunk_data = self.audio_queue.get(timeout=1)
                print(f"[RealtimeProcessor] Got audio chunk from queue, size: {len(chunk_data['audio'])}")

                # Transcribe chunk
                print("[RealtimeProcessor] Transcribing chunk...")
                transcript_text = self._transcribe_chunk(
                    chunk_data['audio'],
                    chunk_data['sample_rate']
                )
                print(f"[RealtimeProcessor] Transcription result: '{transcript_text[:100] if transcript_text else 'None'}...'")

                if transcript_text:
                    # Update transcript
                    self._update_transcript(transcript_text)

                    # Detect questions
                    print(f"[RealtimeProcessor] Detecting questions in: '{transcript_text[:60]}...'")
                    questions = QuestionDetector.extract_questions(transcript_text)
                    print(f"[RealtimeProcessor] Detected {len(questions)} questions")

                    for question in questions:
                        self._handle_detected_question(question)

                self.audio_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                print(f"[RealtimeProcessor] Error in processing loop: {e}")
                import traceback
                traceback.print_exc()
                continue

        print("[RealtimeProcessor] Processing loop ended")

    def _transcribe_chunk(self, audio_data, sample_rate):
        """
        Transcribe audio chunk.

        Args:
            audio_data: Audio data
            sample_rate: Sample rate

        Returns:
            str: Transcribed text
        """
        try:
            import soundfile as sf
            import io

            # Convert audio to bytes
            buffer = io.BytesIO()
            sf.write(buffer, audio_data, sample_rate, format='WAV')
            buffer.seek(0)

            # Transcribe using Whisper API
            transcript = self.transcriber.client.audio.transcriptions.create(
                model="whisper-1",
                file=("chunk.wav", buffer, "audio/wav"),
                response_format="text"
            )

            return transcript.strip()

        except Exception as e:
            print(f"Transcription error: {e}")
            return ""

    def _update_transcript(self, text):
        """
        Update transcript with new text.

        Args:
            text: New transcribed text
        """
        if not text:
            return

        # Add to recent transcript
        self.recent_transcript.append(text)

        # Update full transcript
        self.full_transcript += " " + text

        # Notify callback
        if self.on_transcript_update:
            try:
                self.on_transcript_update(text, self.full_transcript)
            except Exception as e:
                print(f"Error in transcript callback: {e}")

    def _handle_detected_question(self, question):
        """
        Handle a detected question.

        Args:
            question: Detected question text
        """
        # Check if we've already processed this question
        if question in self.detected_questions:
            return

        self.detected_questions.append(question)
        print(f"Question detected: {question}")

        # Notify callback
        if self.on_question_detected:
            try:
                self.on_question_detected(question)
            except Exception as e:
                print(f"Error in question callback: {e}")

        # Generate answer in background
        answer_thread = threading.Thread(
            target=self._generate_answer,
            args=(question,),
            daemon=True
        )
        answer_thread.start()

    def _generate_answer(self, question):
        """
        Generate STAR format answer for question.

        Args:
            question: Question to answer
        """
        try:
            # Get recent context (last few transcript chunks)
            context = " ".join(list(self.recent_transcript)[-5:])

            # Use full transcript if available, otherwise use recent context
            transcript_to_use = self.full_transcript if len(self.full_transcript) > 100 else context

            # Generate quick answer (optimized for speed)
            start_time = time.time()
            answer = self.ai_assistant.quick_answer(
                question=question,
                transcript=transcript_to_use,
                format_type="bullets"
            )
            generation_time = int((time.time() - start_time) * 1000)

            # Notify callback
            if self.on_answer_ready:
                try:
                    self.on_answer_ready(question, answer, generation_time)
                except Exception as e:
                    print(f"Error in answer callback: {e}")

        except Exception as e:
            print(f"Error generating answer: {e}")

    def get_statistics(self):
        """
        Get processing statistics.

        Returns:
            dict: Statistics about processing
        """
        return {
            'total_transcript_length': len(self.full_transcript),
            'chunks_processed': len(self.recent_transcript),
            'questions_detected': len(self.detected_questions),
            'queue_size': self.audio_queue.qsize()
        }
