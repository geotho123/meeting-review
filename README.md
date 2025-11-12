# Meeting Recorder with AI-Powered Q&A

A powerful application that records meetings, transcribes them using OpenAI Whisper, and provides AI-powered answers in **STAR format** (Situation, Task, Action, Result) using Claude or ChatGPT.

## ✨ Features

- **🎙️ Real-Time Audio Recording**: Record meetings with high-quality audio in 60s, 120s, or custom durations
- **🚀 Lightning-Fast Transcription**: Speech-to-text using OpenAI Whisper API with millisecond performance tracking
- **⭐ STAR Format Answers**: Get professional interview-style answers in STAR format
- **💡 Dual Answer Formats**: Choose between bullet points or full paragraph answers
- **🎨 Beautiful Web UI**: Modern, intuitive web interface with real-time updates
- **⚡ Real-Time Processing**: WebSocket-based live updates for recording, transcription, and answer generation
- **🤖 AI Provider Choice**: Use Claude or ChatGPT based on your preference
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices

## 🖥️ Web UI (Recommended)

The easiest way to use the Meeting Recorder is through the web interface!

### Quick Start (Web UI)

1. **Install dependencies** (see Installation section below)

2. **Configure your API keys** in `.env` file

3. **Start the web server**:
   ```bash
   python app.py
   ```

4. **Open your browser** to `http://localhost:5000`

5. **Start recording!**
   - Select duration (60s, 120s, 180s, or custom)
   - Click "Start Recording"
   - Speak naturally
   - Recording stops automatically or click "Stop"
   - Transcription happens automatically
   - Ask questions and get instant STAR format answers!

### Web UI Features

- **Real-time recording** with visual progress indicators
- **Automatic transcription** with performance metrics (shows time in milliseconds)
- **STAR format answers** - perfect for interview preparation
- **Quick question templates** for common interview questions
- **Live status updates** via WebSocket
- **Beautiful gradient UI** with smooth animations

## 📋 Command Line Interface

For advanced users and automation, use the CLI:

### CLI Modes
  - Full workflow (record → transcribe → analyze)
  - Record only
  - Transcribe existing audio
  - Interactive Q&A sessions
  - Generate meeting summaries
  - Extract questions and prepare answers
  - Interview preparation materials

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key (for transcription with Whisper)
- An Anthropic API key (for Claude) OR OpenAI API key (for ChatGPT)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd meeting-review
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration**:
   ```bash
   cp .env.example .env
   ```

4. **Edit `.env` file** and add your API keys:
   ```bash
   # Choose your AI provider: "claude" or "chatgpt"
   AI_PROVIDER=claude

   # Add your API keys
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Getting API Keys

### OpenAI API Key (Required for transcription)
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy the key to your `.env` file

### Anthropic API Key (For Claude)
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key to your `.env` file

## Usage

### Full Workflow (Recommended)

Record a meeting, transcribe it, and analyze it:

```bash
python meeting_recorder.py --workflow
```

With a specific duration (in seconds):
```bash
python meeting_recorder.py --workflow --duration 300
```

### Record Only

Record a meeting:
```bash
python meeting_recorder.py --record
```

Record for a specific duration:
```bash
python meeting_recorder.py --record --duration 60
```

### Transcribe Audio

Transcribe an existing audio file:
```bash
python meeting_recorder.py --transcribe recordings/meeting_20231112_143022.wav
```

### Interactive Q&A Session

Ask questions about a transcript interactively:
```bash
python meeting_recorder.py --qa transcripts/meeting_20231112_143022_transcript.txt
```

Example session:
```
Your Question: What were the main topics discussed?
CLAUDE Answer:
--------------------------------------------------------------------------------
The meeting covered three main topics:
1. Project timeline and milestones
2. Budget allocation for Q4
3. Team resource planning
--------------------------------------------------------------------------------

Your Question: What action items were assigned?
...
```

### Generate Meeting Summary

```bash
python meeting_recorder.py --summary transcripts/meeting_transcript.txt
```

### Extract Questions and Answers

Extract all questions from the meeting and generate professional answers:
```bash
python meeting_recorder.py --extract-qa transcripts/meeting_transcript.txt
```

### Interview Preparation

Generate interview preparation materials from an interview recording:
```bash
python meeting_recorder.py --interview-prep transcripts/interview_transcript.txt
```

### Other Commands

Show current configuration:
```bash
python meeting_recorder.py --show-config
```

List available audio devices:
```bash
python meeting_recorder.py --list-devices
```

Show help:
```bash
python meeting_recorder.py --help
```

## ⭐ STAR Format Answers

The application specializes in generating answers in **STAR format** - perfect for interview preparation!

### What is STAR Format?

STAR stands for:
- **S**ituation: The context or background
- **T**ask: What needed to be accomplished
- **A**ction: The specific steps taken
- **R**esult: The outcome and impact

### Answer Formats

**Bullet Points** (Fast, concise):
```
Situation:
- Key point about context
- Additional background

Task:
- What needed to be done
- Specific objectives

Action:
- Steps taken
- Methods used

Result:
- Measurable outcome
- Impact achieved
```

**Full Paragraphs** (Detailed, professional):
Each section contains 2-4 complete sentences providing comprehensive details.

### Performance

The web UI shows generation time in **milliseconds** for each answer, typically:
- Bullet format: 1-3 seconds
- Full format: 2-5 seconds
- Quick answers: Under 2 seconds

### Example Questions

- "Tell me about a challenging situation you faced"
- "Describe a time you showed leadership"
- "How do you handle conflict in a team?"
- "Describe a project you're proud of"
- "Tell me about a time you failed and what you learned"

## Use Cases

### 1. Meeting Documentation
- Record team meetings
- Get automatic transcripts
- Generate summaries for absent team members
- Extract action items

### 2. Interview Preparation
- Record mock interviews
- Get AI-generated answers to interview questions
- Identify areas for improvement
- Practice responses

### 3. Lecture/Training Notes
- Record lectures or training sessions
- Ask questions about specific topics
- Generate study materials
- Create Q&A documents

### 4. Client Calls
- Record client calls (with permission)
- Generate summaries
- Extract key requirements
- Answer follow-up questions

## Project Structure

```
meeting-review/
├── app.py                   # Flask web application (WEB UI)
├── meeting_recorder.py      # Command-line application
├── audio_recorder.py        # Audio recording module
├── transcription.py         # Speech-to-text module (Whisper API)
├── ai_assistant.py          # AI Q&A module (Claude/ChatGPT + STAR format)
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .env                     # Configuration (you create this)
├── .env.example             # Configuration template
├── templates/               # HTML templates for web UI
│   └── index.html           # Main web interface
├── static/                  # Static web assets
│   ├── css/
│   │   └── style.css        # Web UI styling
│   └── js/
│       └── app.js           # Frontend JavaScript (WebSocket, UI logic)
├── recordings/              # Saved audio files (created automatically)
└── transcripts/             # Saved transcripts (created automatically)
```

## Configuration Options

Edit `.env` file to customize:

```bash
# AI Provider: "claude" or "chatgpt"
AI_PROVIDER=claude

# API Keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Recording Settings
SAMPLE_RATE=44100    # Audio sample rate (Hz)
CHANNELS=2           # 1 for mono, 2 for stereo
```

## Troubleshooting

### Audio Recording Issues

If you encounter audio recording issues:

1. **List audio devices**:
   ```bash
   python meeting_recorder.py --list-devices
   ```

2. **Check microphone permissions** (macOS/Linux):
   - Ensure your terminal has microphone access permissions

3. **Install system dependencies** (Linux):
   ```bash
   sudo apt-get install portaudio19-dev python3-pyaudio
   ```

### API Issues

1. **Check API keys**:
   ```bash
   python meeting_recorder.py --show-config
   ```

2. **Verify API key validity**:
   - Make sure keys are correctly copied (no extra spaces)
   - Check that your API account has credits

3. **Rate limits**:
   - If you hit rate limits, wait a few minutes and try again

## Tips for Best Results

1. **Recording Quality**:
   - Use a good quality microphone
   - Record in a quiet environment
   - Speak clearly and at a moderate pace

2. **Transcription**:
   - Longer audio files take more time to transcribe
   - Clear audio produces better transcripts

3. **AI Answers**:
   - Ask specific questions for better answers
   - Claude tends to be more detailed
   - ChatGPT (GPT-4) is faster but may be more concise

## Cost Considerations

- **OpenAI Whisper**: ~$0.006 per minute of audio
- **Claude (Anthropic)**: Varies by model and usage
- **ChatGPT (GPT-4)**: Varies by model and usage

Monitor your API usage on respective platforms.

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure
- Be mindful of recording permissions and privacy laws
- Don't record sensitive conversations without proper consent

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation (OpenAI/Anthropic)
3. Open an issue on GitHub

## Roadmap

Future enhancements:
- [ ] Real-time transcription during recording
- [ ] Support for multiple languages
- [ ] Web interface
- [ ] Team collaboration features
- [ ] Integration with calendar apps
- [ ] Automatic action item tracking
- [ ] Email summaries

---

**Happy Recording!** 🎙️
