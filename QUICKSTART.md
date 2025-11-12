# 🚀 Quick Start Guide

Get up and running with the Meeting Recorder in under 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Get API Keys

### OpenAI API Key (Required)
1. Go to https://platform.openai.com/api-keys
2. Create an account or log in
3. Click "Create new secret key"
4. Copy the key

### Claude API Key (Optional - for Claude AI)
1. Go to https://console.anthropic.com/
2. Create an account or log in
3. Navigate to "API Keys"
4. Create a new key
5. Copy the key

## Step 3: Configure

```bash
# Copy the example configuration
cp .env.example .env

# Edit .env with your favorite editor
nano .env
# or
vim .env
```

Add your API keys:
```bash
AI_PROVIDER=claude  # or "chatgpt"
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here
```

## Step 4: Launch Web UI

```bash
python app.py
```

You'll see:
```
================================================================================
Meeting Recorder Web Application
================================================================================
AI Provider: CLAUDE
Server starting on http://localhost:5000
================================================================================
```

## Step 5: Open Browser

Open your browser to: **http://localhost:5000**

## Step 6: Record & Analyze!

1. **Select Duration**: Click 60s, 120s, 180s, or custom
2. **Start Recording**: Click the big "Start Recording" button
3. **Speak Naturally**: Talk about your meeting, interview, or topic
4. **Auto-transcription**: Happens automatically when recording stops
5. **Ask Questions**: Type a question or click a quick template
6. **Get STAR Answers**: Receive formatted answers in seconds!

## Example Workflow

```
1. Click "120s" duration
2. Click "Start Recording"
3. Speak for 2 minutes about a project
4. Recording auto-stops
5. Wait ~10-30 seconds for transcription
6. Type: "Describe a challenging situation"
7. Click "Get STAR Answer"
8. Receive formatted answer with Situation, Task, Action, Result!
```

## Common Questions

**Q: Which AI provider should I use?**
- **Claude**: More detailed, comprehensive answers
- **ChatGPT**: Faster, more concise answers

**Q: How long does transcription take?**
- Usually 10-30 seconds for a 2-minute recording
- Displayed in milliseconds on screen

**Q: What's the difference between bullet and full format?**
- **Bullets**: Quick, scannable, great for notes
- **Full**: Complete sentences, better for presentations

**Q: Can I use it offline?**
- No, requires API keys and internet connection for AI processing

**Q: Is my data stored?**
- Audio files saved locally in `recordings/` folder
- Transcripts saved in `transcripts/` folder
- Nothing sent to servers except API calls

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "API key not found" error
Check your `.env` file has the correct keys

### Recording not working
- Check microphone permissions
- Try: `python meeting_recorder.py --list-devices`

### Port 5000 already in use
```bash
# Kill the process using port 5000
lsof -ti:5000 | xargs kill -9
# Or change port in app.py
```

## Next Steps

- Try different question types
- Experiment with 60s vs 120s recordings
- Compare bullet vs full format answers
- Record actual meetings (with permission!)
- Use for interview preparation

## Need Help?

- Check the full README.md for detailed documentation
- Review the troubleshooting section
- Check API provider documentation

---

**Happy Recording! 🎙️**
