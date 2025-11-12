# ⚡ Live Mode Guide - Real-Time Transcription & Question Detection

Your Meeting Recorder now supports **LIVE MODE** - perfect for 30-45 minute interviews and meetings with real-time transcription and instant STAR format answers!

## 🎯 What is Live Mode?

Live Mode processes audio in real-time as you speak, automatically:
- **Transcribes** your conversation every 10 seconds
- **Detects** questions as they're asked
- **Generates** instant STAR format answers
- **Displays** everything live on screen

## 🚀 How to Use Live Mode

### Step 1: Start the App

```bash
uv run python app.py
# or
python app.py
```

Open browser: `http://localhost:5000`

### Step 2: Enable Live Mode

1. **Toggle ON** the "⚡ LIVE MODE" switch (top of page)
2. **Select duration**:
   - 120s (2 min) - for testing
   - 1800s (30 min) - typical interview
   - 2700s (45 min) - extended session
   - Custom - any duration you need

### Step 3: Start Recording

1. Click **"Start Recording"**
2. You'll see:
   - 🔴 **LIVE badge** appear
   - Live transcript section
   - Live Q&A section

### Step 4: Speak Naturally

- Talk normally during your interview/meeting
- Every **10 seconds**, audio is transcribed
- Questions are **automatically detected**
- Answers appear **instantly** (usually under 3 seconds!)

## 📊 What You'll See

### Live Transcript Section
```
⚡ Live Transcript
🔴 LIVE    245 words transcribed...

[Auto-scrolling transcript appears here in real-time]
```

### Live Questions & Answers
```
💡 Live Questions & Instant Answers

❓ Tell me about a challenging situation you faced?

Situation:
- Faced tight deadline on critical project
- Limited resources and team availability

Task:
- Complete project within 2 weeks
- Maintain quality standards

Action:
- Reorganized priorities and workflow
- Implemented daily standups

Result:
- Delivered on time with 95% quality score
- Team productivity increased by 30%

⏱️ 2847ms    🤖 AI Generated
```

## 🎯 Question Detection

The system automatically detects questions like:
- "Tell me about..."
- "Describe a time when..."
- "How do you handle..."
- "What would you do if..."
- "Can you give an example of..."
- "Talk about a situation where..."
- And many more patterns!

## ⚡ Performance

- **Transcription**: Every 10 seconds
- **Question Detection**: Instant
- **Answer Generation**: 1-3 seconds
- **Total Latency**: ~3-5 seconds from question to answer

## 💡 Best Practices

### For Interviews

1. **Enable Live Mode** before starting
2. **Position the app** on a second monitor
3. **Glance at answers** while thinking
4. **Use as reference** for your actual response
5. **Review full transcript** after interview

### For Meetings

1. **Use 30-45 min duration** for full meetings
2. **Let it run continuously** - no need to interact
3. **Questions are detected automatically**
4. **Review Q&A summary** at end
5. **Export transcript** for meeting notes

## 🔧 Technical Details

### Audio Processing
- **Chunk Size**: 10 seconds
- **Overlap**: 2 seconds (prevents word cutoffs)
- **Sample Rate**: 44.1kHz (or configured)
- **Channels**: Mono (most compatible)

### Transcription
- **API**: OpenAI Whisper
- **Model**: whisper-1
- **Format**: Text
- **Latency**: ~2-5 seconds per chunk

### Question Detection
- **Method**: Regex pattern matching
- **Patterns**: 20+ common question formats
- **Accuracy**: High for standard interview questions
- **False Positives**: Minimal

### Answer Generation
- **Format**: STAR (Situation, Task, Action, Result)
- **Style**: Bullet points (for speed)
- **AI**: Claude or ChatGPT (configured)
- **Context**: Uses recent transcript chunks

## 📈 Use Cases

### 1. Technical Interviews (30-45 min)
- Practice behavioral questions
- Get instant STAR answers
- Review your performance
- Identify areas to improve

### 2. Live Presentations
- Capture Q&A automatically
- Get suggested answers
- Review questions later
- Create FAQ document

### 3. Stakeholder Meetings
- Auto-document questions asked
- Track discussion topics
- Generate meeting summary
- Create action items

### 4. Training Sessions
- Capture student questions
- Provide quick answers
- Review common questions
- Improve training content

## ⚠️ Important Notes

### API Usage
- Live mode uses **more API calls** than standard mode
- Whisper API: ~6 calls per minute (for 10-second chunks)
- Claude/ChatGPT: 1 call per detected question
- **Monitor your API usage** on provider dashboards

### Cost Estimation (30-minute session)
- **Whisper**: ~180 chunks × $0.006/min ≈ $0.18
- **Claude/ChatGPT**: ~10 questions × $0.01-0.03 ≈ $0.10-0.30
- **Total**: ~$0.30-0.50 per 30-minute session

### Network Requirements
- **Stable internet** required (streaming to APIs)
- **Bandwidth**: ~50-100 KB/s upload
- **Latency**: Best with <100ms to API servers

## 🎨 UI Features

### Visual Indicators
- 🔴 **Pulsing LIVE badge** - recording active
- ⚡ **Lightning icon** - live mode enabled
- 📊 **Word count** - tracks transcription progress
- ⏱️ **Timing badges** - shows generation speed
- ✨ **Highlight animations** - new content flashes

### Auto-Scrolling
- **Transcript**: Scrolls to bottom automatically
- **Q&A**: New questions appear at top
- **Smooth animations**: Content slides in

### Responsive Design
- Works on desktop, tablet, mobile
- Adapts to screen size
- Optimized for dual-monitor setups

## 🔍 Troubleshooting

### "No transcription appearing"
- Check microphone is working
- Speak clearly and loudly enough
- Wait 10 seconds for first chunk
- Check OpenAI API key is valid

### "Questions not detected"
- Make sure questions are clear
- Use standard question formats
- Add question mark if needed
- Check console for detection logs

### "Answers taking too long"
- Check internet connection
- Verify AI provider API key
- Monitor API rate limits
- Consider switching AI provider

### "Recording stops unexpectedly"
- Check selected duration
- Verify browser doesn't go to sleep
- Keep app window active
- Check system audio permissions

## 💻 System Requirements

### Minimum
- **CPU**: Dual-core 2.0 GHz
- **RAM**: 4 GB
- **Network**: 1 Mbps upload
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+

### Recommended
- **CPU**: Quad-core 2.5 GHz
- **RAM**: 8 GB
- **Network**: 5 Mbps upload
- **Browser**: Latest Chrome or Firefox
- **Display**: Dual monitors (for interview use)

## 🎓 Example Workflow

```
1. Open app → http://localhost:5000
2. Enable ⚡ LIVE MODE toggle
3. Select "30 min" duration
4. Click "Start Recording"
5. See live transcript appear
6. Interviewer asks question
7. Question detected automatically
8. STAR answer appears in 2-3 seconds
9. Glance at answer while thinking
10. Give your actual response
11. Recording continues...
12. After 30 minutes, auto-stops
13. Review full transcript and Q&A
14. Export for future reference
```

## 🚀 Advanced Tips

### Dual Monitor Setup
- **Monitor 1**: Video call/interview
- **Monitor 2**: Live mode app
- **Quick glances** at suggested answers
- **Don't read directly** - use as prompts

### Practice Sessions
- **Record yourself** answering questions
- **Review AI suggestions** after
- **Compare** your answers vs AI
- **Improve** your responses

### Team Meetings
- **Project screen** for all to see
- **Capture Q&A** automatically
- **Generate meeting notes** from transcript
- **Share summary** with team

## 📚 Additional Resources

- **QUICKSTART.md** - Basic setup
- **README.md** - Complete documentation
- **UV_SETUP.md** - Fast installation with UV

## 🆘 Support

Having issues?
1. Check console logs in browser (F12)
2. Check terminal output from server
3. Verify API keys are correct
4. Test with standard mode first
5. Review this guide thoroughly

---

**Ready to go live? Enable ⚡ LIVE MODE and start recording!**

Happy interviewing! 🎙️
