#!/usr/bin/env python3
"""
Meeting Recorder - Record meetings and get AI-powered answers
"""
import sys
import os
import argparse
from config import Config
from audio_recorder import AudioRecorder
from transcription import Transcriber
from ai_assistant import AIAssistant


class MeetingRecorder:
    """Main application class for meeting recording and analysis."""

    def __init__(self, config=None):
        """
        Initialize the meeting recorder.

        Args:
            config: Configuration object. If None, loads from .env
        """
        self.config = config or Config()
        self.recorder = None
        self.transcriber = None
        self.assistant = None

    def record_meeting(self, duration=None, filename=None):
        """
        Record a meeting.

        Args:
            duration: Duration in seconds. If None, records until user stops.
            filename: Optional filename for the recording.

        Returns:
            str: Path to the recorded audio file
        """
        # Initialize recorder
        self.recorder = AudioRecorder(
            sample_rate=self.config.sample_rate,
            channels=self.config.channels,
            output_dir=self.config.recordings_dir
        )

        if duration:
            # Record for specific duration
            audio_path = self.recorder.record_with_duration(duration, filename)
        else:
            # Record until user stops
            self.recorder.start_recording()
            input("\nPress Enter to stop recording...\n")
            audio_path = self.recorder.stop_recording(filename)

        return audio_path

    def transcribe(self, audio_path):
        """
        Transcribe an audio file.

        Args:
            audio_path: Path to the audio file

        Returns:
            dict: Transcription result
        """
        if not self.transcriber:
            self.transcriber = Transcriber(
                api_key=self.config.openai_api_key,
                output_dir=self.config.transcripts_dir
            )

        return self.transcriber.transcribe_audio(audio_path)

    def start_qa_session(self, transcript_text):
        """
        Start an interactive Q&A session.

        Args:
            transcript_text: The meeting transcript text
        """
        if not self.assistant:
            self.assistant = AIAssistant(
                provider=self.config.ai_provider,
                anthropic_key=self.config.anthropic_api_key,
                openai_key=self.config.openai_api_key
            )

        self.assistant.interactive_qa(transcript_text)

    def generate_summary(self, transcript_text):
        """
        Generate a meeting summary.

        Args:
            transcript_text: The meeting transcript text

        Returns:
            str: Meeting summary
        """
        if not self.assistant:
            self.assistant = AIAssistant(
                provider=self.config.ai_provider,
                anthropic_key=self.config.anthropic_api_key,
                openai_key=self.config.openai_api_key
            )

        return self.assistant.generate_summary(transcript_text)

    def generate_qa_document(self, transcript_text, output_file=None):
        """
        Generate a Q&A document from the transcript.

        Args:
            transcript_text: The meeting transcript text
            output_file: Optional path to save the Q&A document

        Returns:
            str: Q&A document content
        """
        if not self.assistant:
            self.assistant = AIAssistant(
                provider=self.config.ai_provider,
                anthropic_key=self.config.anthropic_api_key,
                openai_key=self.config.openai_api_key
            )

        qa_content = self.assistant.extract_questions_and_answers(transcript_text)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(qa_content)
            print(f"\nQ&A document saved to: {output_file}")

        return qa_content

    def generate_interview_prep(self, transcript_text, output_file=None):
        """
        Generate interview preparation materials.

        Args:
            transcript_text: The interview transcript text
            output_file: Optional path to save the prep materials

        Returns:
            str: Interview prep content
        """
        if not self.assistant:
            self.assistant = AIAssistant(
                provider=self.config.ai_provider,
                anthropic_key=self.config.anthropic_api_key,
                openai_key=self.config.openai_api_key
            )

        prep_content = self.assistant.generate_interview_prep(transcript_text)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(prep_content)
            print(f"\nInterview prep saved to: {output_file}")

        return prep_content

    def full_workflow(self, duration=None):
        """
        Run the complete workflow: record -> transcribe -> analyze.

        Args:
            duration: Optional recording duration in seconds
        """
        print("\n" + "=" * 80)
        print("MEETING RECORDER - Full Workflow")
        print("=" * 80 + "\n")

        # Step 1: Record
        print("STEP 1: Recording Meeting")
        print("-" * 80)
        audio_path = self.record_meeting(duration)

        if not audio_path:
            print("Recording failed. Exiting.")
            return

        # Step 2: Transcribe
        print("\nSTEP 2: Transcribing Audio")
        print("-" * 80)
        result = self.transcribe(audio_path)
        transcript_text = result["text"]
        transcript_path = result.get("file_path")

        print(f"\nTranscript preview (first 500 characters):")
        print("-" * 80)
        print(transcript_text[:500] + "..." if len(transcript_text) > 500 else transcript_text)
        print("-" * 80)

        # Step 3: Analyze
        print("\nSTEP 3: AI Analysis")
        print("-" * 80)
        print("\nWhat would you like to do?")
        print("1. Generate meeting summary")
        print("2. Extract questions and answers")
        print("3. Generate interview prep materials")
        print("4. Start interactive Q&A session")
        print("5. Skip analysis")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            print("\nGenerating summary...")
            summary = self.generate_summary(transcript_text)
            print("\n" + "=" * 80)
            print("MEETING SUMMARY")
            print("=" * 80)
            print(summary)
            print("=" * 80)

        elif choice == "2":
            output_file = f"{os.path.splitext(transcript_path)[0]}_qa.txt"
            print("\nExtracting questions and answers...")
            qa_doc = self.generate_qa_document(transcript_text, output_file)
            print("\n" + "=" * 80)
            print("QUESTIONS & ANSWERS")
            print("=" * 80)
            print(qa_doc)
            print("=" * 80)

        elif choice == "3":
            output_file = f"{os.path.splitext(transcript_path)[0]}_interview_prep.txt"
            print("\nGenerating interview prep materials...")
            prep = self.generate_interview_prep(transcript_text, output_file)
            print("\n" + "=" * 80)
            print("INTERVIEW PREPARATION")
            print("=" * 80)
            print(prep)
            print("=" * 80)

        elif choice == "4":
            self.start_qa_session(transcript_text)

        else:
            print("\nSkipping analysis.")

        print("\n\nWorkflow completed!")
        print(f"Audio file: {audio_path}")
        print(f"Transcript: {transcript_path}")


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="Meeting Recorder - Record meetings and get AI-powered answers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full workflow (record, transcribe, analyze)
  python meeting_recorder.py --workflow

  # Record a meeting for 60 seconds
  python meeting_recorder.py --record --duration 60

  # Transcribe an existing audio file
  python meeting_recorder.py --transcribe recordings/meeting.wav

  # Start Q&A session with a transcript
  python meeting_recorder.py --qa transcripts/meeting_transcript.txt

  # Generate summary from transcript
  python meeting_recorder.py --summary transcripts/meeting_transcript.txt

  # Show configuration
  python meeting_recorder.py --show-config
        """
    )

    parser.add_argument("--workflow", action="store_true",
                        help="Run full workflow: record -> transcribe -> analyze")
    parser.add_argument("--record", action="store_true",
                        help="Record a meeting")
    parser.add_argument("--duration", type=int,
                        help="Recording duration in seconds")
    parser.add_argument("--transcribe", metavar="AUDIO_FILE",
                        help="Transcribe an audio file")
    parser.add_argument("--qa", metavar="TRANSCRIPT_FILE",
                        help="Start Q&A session with a transcript")
    parser.add_argument("--summary", metavar="TRANSCRIPT_FILE",
                        help="Generate summary from transcript")
    parser.add_argument("--extract-qa", metavar="TRANSCRIPT_FILE",
                        help="Extract questions and answers from transcript")
    parser.add_argument("--interview-prep", metavar="TRANSCRIPT_FILE",
                        help="Generate interview prep from transcript")
    parser.add_argument("--show-config", action="store_true",
                        help="Show current configuration")
    parser.add_argument("--list-devices", action="store_true",
                        help="List available audio devices")

    args = parser.parse_args()

    # Load configuration
    try:
        config = Config()
    except Exception as e:
        print(f"Error loading configuration: {e}")
        print("\nPlease create a .env file based on .env.example and set your API keys.")
        return 1

    # Initialize app
    app = MeetingRecorder(config)

    try:
        # Handle commands
        if args.show_config:
            config.print_config()

        elif args.list_devices:
            AudioRecorder.list_audio_devices()

        elif args.workflow:
            app.full_workflow(args.duration)

        elif args.record:
            audio_path = app.record_meeting(args.duration)
            print(f"\nRecording saved: {audio_path}")

        elif args.transcribe:
            if not os.path.exists(args.transcribe):
                print(f"Error: Audio file not found: {args.transcribe}")
                return 1
            result = app.transcribe(args.transcribe)
            print(f"\nTranscript:\n{result['text']}")

        elif args.qa:
            if not os.path.exists(args.qa):
                print(f"Error: Transcript file not found: {args.qa}")
                return 1
            with open(args.qa, 'r', encoding='utf-8') as f:
                transcript = f.read()
            app.start_qa_session(transcript)

        elif args.summary:
            if not os.path.exists(args.summary):
                print(f"Error: Transcript file not found: {args.summary}")
                return 1
            with open(args.summary, 'r', encoding='utf-8') as f:
                transcript = f.read()
            summary = app.generate_summary(transcript)
            print(f"\nSummary:\n{summary}")

        elif args.extract_qa:
            if not os.path.exists(args.extract_qa):
                print(f"Error: Transcript file not found: {args.extract_qa}")
                return 1
            with open(args.extract_qa, 'r', encoding='utf-8') as f:
                transcript = f.read()
            qa_doc = app.generate_qa_document(transcript)
            print(f"\nQuestions & Answers:\n{qa_doc}")

        elif args.interview_prep:
            if not os.path.exists(args.interview_prep):
                print(f"Error: Transcript file not found: {args.interview_prep}")
                return 1
            with open(args.interview_prep, 'r', encoding='utf-8') as f:
                transcript = f.read()
            prep = app.generate_interview_prep(transcript)
            print(f"\nInterview Prep:\n{prep}")

        else:
            parser.print_help()

        return 0

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
