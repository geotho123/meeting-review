"""
Speech-to-text transcription module using OpenAI Whisper API.
"""
import os
from openai import OpenAI
from datetime import datetime


class Transcriber:
    """Transcribes audio files to text using OpenAI Whisper API."""

    def __init__(self, api_key=None, output_dir="transcripts"):
        """
        Initialize the transcriber.

        Args:
            api_key: OpenAI API key. If None, reads from environment variable.
            output_dir: Directory to save transcripts
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided and not found in environment")

        self.client = OpenAI(api_key=self.api_key)
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def transcribe_audio(self, audio_file_path, save_transcript=True):
        """
        Transcribe an audio file to text.

        Args:
            audio_file_path: Path to the audio file
            save_transcript: Whether to save the transcript to a file

        Returns:
            dict: Contains 'text' (transcript) and 'file_path' (if saved)
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        print(f"Transcribing audio file: {audio_file_path}")
        print("This may take a moment...")

        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )

            print("Transcription completed!")

            result = {"text": transcript}

            # Save transcript if requested
            if save_transcript:
                transcript_path = self._save_transcript(transcript, audio_file_path)
                result["file_path"] = transcript_path

            return result

        except Exception as e:
            print(f"Error during transcription: {e}")
            raise

    def transcribe_with_timestamps(self, audio_file_path, save_transcript=True):
        """
        Transcribe an audio file with word-level timestamps.

        Args:
            audio_file_path: Path to the audio file
            save_transcript: Whether to save the transcript to a file

        Returns:
            dict: Contains 'text', 'segments', and optionally 'file_path'
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        print(f"Transcribing audio file with timestamps: {audio_file_path}")
        print("This may take a moment...")

        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )

            print("Transcription completed!")

            result = {
                "text": transcript.text,
                "segments": transcript.segments if hasattr(transcript, 'segments') else []
            }

            # Save transcript if requested
            if save_transcript:
                transcript_path = self._save_transcript(transcript.text, audio_file_path)
                result["file_path"] = transcript_path

            return result

        except Exception as e:
            print(f"Error during transcription: {e}")
            raise

    def _save_transcript(self, transcript_text, audio_file_path):
        """
        Save transcript to a text file.

        Args:
            transcript_text: The transcript text
            audio_file_path: Path to the original audio file

        Returns:
            str: Path to the saved transcript file
        """
        # Generate transcript filename based on audio filename
        audio_filename = os.path.basename(audio_file_path)
        audio_name = os.path.splitext(audio_filename)[0]
        transcript_filename = f"{audio_name}_transcript.txt"
        transcript_path = os.path.join(self.output_dir, transcript_filename)

        # Save transcript with metadata
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(f"Transcript for: {audio_filename}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 80 + "\n\n")
            f.write(transcript_text)

        print(f"Transcript saved to: {transcript_path}")
        return transcript_path

    def load_transcript(self, transcript_path):
        """
        Load a transcript from a file.

        Args:
            transcript_path: Path to the transcript file

        Returns:
            str: The transcript text
        """
        with open(transcript_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip metadata lines (first 3 lines)
        lines = content.split("\n")
        if len(lines) > 3 and lines[2].startswith("-" * 20):
            return "\n".join(lines[4:])
        return content
