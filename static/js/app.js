// Global state
let socket;
let currentTranscript = '';
let selectedDuration = 120;
let selectedFormat = 'bullets';
let liveMode = false;
let liveTranscript = '';
let detectedQuestions = [];

// Initialize socket connection
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - initializing app');
    try {
        initializeSocket();
        setupEventListeners();
        console.log('App initialized successfully');
    } catch (error) {
        console.error('Error initializing app:', error);
        alert('Error initializing app. Please check console for details.');
    }
});

function initializeSocket() {
    socket = io();

    socket.on('connect', function() {
        console.log('Connected to server');
        showMessage('Connected to server', 'success');
    });

    socket.on('disconnect', function() {
        console.log('Disconnected from server');
        showMessage('Disconnected from server', 'error');
    });

    socket.on('status', function(data) {
        console.log('Status:', data);
        updateStatus(data.message, data.type);
    });

    socket.on('error', function(data) {
        console.error('Error:', data);
        showMessage(data.message, 'error');
        resetRecordingUI();
    });

    socket.on('recording_progress', function(data) {
        updateProgress(data.elapsed, data.duration);
    });

    socket.on('recording_complete', function(data) {
        console.log('Recording complete:', data);
        showMessage(`Recording saved: ${data.filename}`, 'success');
        resetRecordingUI();
    });

    socket.on('transcription_complete', function(data) {
        console.log('Transcription complete:', data);
        currentTranscript = data.text;
        displayTranscript(data.text, data.time_ms);
        showQASection();

        let message = `Transcription completed in ${data.time_ms}ms`;
        if (data.questions_detected) {
            message += ` - ${data.questions_detected} questions detected!`;
        }
        showMessage(message, 'success');
    });

    socket.on('auto_answer', function(data) {
        console.log('Auto answer received:', data);
        // Display as a simple answer card - ensure it appears at the top
        const answersContainer = document.getElementById('answersContainer');
        if (!answersContainer) {
            console.error('answersContainer not found');
            return;
        }

        // Clear placeholder if present
        const placeholder = answersContainer.querySelector('.placeholder-text');
        if (placeholder) {
            placeholder.remove();
        }

        const answerCard = document.createElement('div');
        answerCard.className = 'answer-card';
        answerCard.innerHTML = `
            <div class="answer-question">🤖 ${data.question}</div>
            <div class="answer-meta">
                <span class="meta-badge">⚡ Auto-detected</span>
                <span class="meta-badge">⏱️ ${data.time_ms}ms</span>
            </div>
            <div class="star-content">${formatContent(data.answer, 'bullets')}</div>
        `;
        // Insert at top (latest first)
        answersContainer.insertBefore(answerCard, answersContainer.firstChild);
        showMessage(`Auto-answer: "${data.question.substring(0, 40)}..."`, 'info');
    });

    socket.on('answer_ready', function(data) {
        console.log('Answer ready:', data);
        displayAnswer(data);
        showMessage(`Answer generated in ${data.time_ms}ms`, 'success');
    });

    socket.on('quick_answer_ready', function(data) {
        console.log('Quick answer ready:', data);
        displayQuickAnswer(data);
        showMessage(`Quick answer generated in ${data.time_ms}ms`, 'success');
    });

    // Live mode event handlers
    socket.on('live_transcript', function(data) {
        console.log('Live transcript update:', data);
        updateLiveTranscript(data.chunk, data.full);
    });

    socket.on('question_detected', function(data) {
        console.log('Question detected:', data);
        displayDetectedQuestion(data.question);
    });

    socket.on('live_answer', function(data) {
        console.log('Live answer ready:', data);
        displayLiveAnswer(data.question, data.answer, data.time_ms);
    });

    socket.on('live_session_complete', function(data) {
        console.log('Live session complete:', data);
        showMessage(`Session complete! ${data.statistics.questions_detected} questions detected`, 'success');
        currentTranscript = data.full_transcript;
    });
}

function setupEventListeners() {
    console.log('Setting up event listeners...');

    // Duration selection - handle both dropdown and button formats
    const durationSelect = document.getElementById('durationSelect');
    if (durationSelect) {
        // New dropdown format
        durationSelect.addEventListener('change', function() {
            selectedDuration = parseInt(this.value);
            console.log('Duration selected:', selectedDuration);
        });
    } else {
        // Old button format (fallback for compatibility)
        document.querySelectorAll('.duration-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.duration-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                const duration = this.getAttribute('data-duration');
                if (duration === 'custom') {
                    const customInput = document.getElementById('customDuration');
                    if (customInput) customInput.style.display = 'block';
                } else {
                    const customInput = document.getElementById('customDuration');
                    if (customInput) customInput.style.display = 'none';
                    selectedDuration = parseInt(duration);
                }
            });
        });

        // Custom duration input
        const customDuration = document.getElementById('customDuration');
        if (customDuration) {
            customDuration.addEventListener('change', function() {
                selectedDuration = parseInt(this.value);
            });
        }
    }

    // Format selection
    document.querySelectorAll('.format-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.format-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            selectedFormat = this.getAttribute('data-format');
        });
    });

    // Recording controls
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');

    if (startBtn) {
        console.log('Start button found, attaching listener');
        startBtn.addEventListener('click', startRecording);
    } else {
        console.error('Start button not found!');
    }

    if (stopBtn) {
        console.log('Stop button found, attaching listener');
        stopBtn.addEventListener('click', stopRecording);
    } else {
        console.error('Stop button not found!');
    }

    // Q&A - handle optional elements
    const askBtn = document.getElementById('askBtn');
    if (askBtn) {
        askBtn.addEventListener('click', askQuestion);
    }

    const questionInput = document.getElementById('questionInput');
    if (questionInput) {
        questionInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                askQuestion();
            }
        });
    }

    // Quick questions (optional)
    document.querySelectorAll('.quick-question-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = document.getElementById('questionInput');
            if (input) {
                input.value = this.textContent;
                askQuestion();
            }
        });
    });
}

function startRecording() {
    console.log('startRecording() function called');

    const liveModeToggle = document.getElementById('liveModeToggle');
    if (!liveModeToggle) {
        console.error('liveModeToggle element not found!');
        return;
    }

    const liveModeEnabled = liveModeToggle.checked;
    console.log('Starting recording for', selectedDuration, 'seconds', 'Live mode:', liveModeEnabled);

    // Update UI
    document.getElementById('startBtn').disabled = true;
    document.getElementById('stopBtn').disabled = false;

    const statusIndicator = document.querySelector('.status-indicator');
    statusIndicator.classList.add('recording');

    // Show progress bar
    const progressBar = document.getElementById('progressBar');
    progressBar.style.display = 'block';
    document.querySelector('.progress-fill').style.width = '0%';

    // Show live sections if in live mode
    if (liveModeEnabled) {
        // Show old-style sections if they exist
        const liveSection = document.getElementById('liveSection');
        if (liveSection) liveSection.style.display = 'block';

        const liveQASection = document.getElementById('liveQASection');
        if (liveQASection) liveQASection.style.display = 'block';

        // Clear previous data from all live displays
        const liveTranscriptDisplay = document.getElementById('liveTranscriptDisplay');
        if (liveTranscriptDisplay) {
            liveTranscriptDisplay.innerHTML = '<p class="placeholder-text">Listening for speech...</p>';
        }

        const liveQuestionsContainer = document.getElementById('liveQuestionsContainer');
        if (liveQuestionsContainer) {
            liveQuestionsContainer.innerHTML = '<p class="placeholder-text">Questions will appear here...</p>';
        }

        liveTranscript = '';
        detectedQuestions = [];
    }

    // Emit start recording event with live mode
    socket.emit('start_recording', {
        duration: selectedDuration,
        live_mode: liveModeEnabled
    });

    updateStatus(liveModeEnabled ? 'Recording in LIVE mode...' : 'Recording...', 'recording');
}

function stopRecording() {
    console.log('Stopping recording');

    socket.emit('stop_recording');
    resetRecordingUI();
}

function resetRecordingUI() {
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;

    const statusIndicator = document.querySelector('.status-indicator');
    statusIndicator.classList.remove('recording');

    updateStatus('Ready to record', 'ready');
}

function updateProgress(elapsed, duration) {
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.querySelector('.progress-text');

    const percentage = (elapsed / duration) * 100;
    progressFill.style.width = `${percentage}%`;
    progressText.textContent = `${elapsed}s / ${duration}s`;
}

function updateStatus(message, type) {
    const statusText = document.querySelector('.status-text');
    statusText.textContent = message;

    const statusIndicator = document.querySelector('.status-indicator');
    statusIndicator.className = 'status-indicator';

    if (type === 'recording') {
        statusIndicator.classList.add('recording');
    } else if (type === 'processing' || type === 'info') {
        statusIndicator.classList.add('processing');
    }
}

function displayTranscript(text, timeMs) {
    const transcriptSection = document.getElementById('transcriptSection');
    const transcriptDisplay = document.getElementById('transcriptDisplay');
    const transcriptionTime = document.getElementById('transcriptionTime');

    transcriptSection.style.display = 'block';
    transcriptDisplay.innerHTML = `<p>${text}</p>`;
    transcriptionTime.textContent = `Transcribed in ${timeMs}ms`;
}

function showQASection() {
    // Show Q&A sections if they exist (optional in new layout)
    const qaSection = document.getElementById('qaSection');
    if (qaSection) qaSection.style.display = 'block';

    const commonQuestions = document.getElementById('commonQuestions');
    if (commonQuestions) commonQuestions.style.display = 'block';

    const manualQASection = document.getElementById('manualQASection');
    if (manualQASection) manualQASection.style.display = 'block';
}

function askQuestion() {
    const question = document.getElementById('questionInput').value.trim();

    if (!question) {
        showMessage('Please enter a question', 'error');
        return;
    }

    if (!currentTranscript) {
        showMessage('No transcript available. Please record first.', 'error');
        return;
    }

    console.log('Asking question:', question);
    showMessage('Generating STAR format answer...', 'info');

    // Disable ask button temporarily
    const askBtn = document.getElementById('askBtn');
    askBtn.disabled = true;
    setTimeout(() => askBtn.disabled = false, 2000);

    socket.emit('get_answer', {
        question: question,
        transcript: currentTranscript,
        format: selectedFormat
    });
}

function displayAnswer(data) {
    const answersContainer = document.getElementById('answersContainer');

    const answerCard = document.createElement('div');
    answerCard.className = 'answer-card';

    const components = data.components;

    answerCard.innerHTML = `
        <div class="answer-question">${data.question}</div>
        <div class="answer-meta">
            <span class="meta-badge">⏱️ ${data.time_ms}ms</span>
            <span class="meta-badge">🤖 ${data.provider.toUpperCase()}</span>
            <span class="meta-badge">📋 ${data.format_type}</span>
        </div>

        ${components.situation ? `
        <div class="star-section">
            <h4>📍 Situation</h4>
            <div class="star-content">${formatContent(components.situation, data.format_type)}</div>
        </div>` : ''}

        ${components.task ? `
        <div class="star-section">
            <h4>🎯 Task</h4>
            <div class="star-content">${formatContent(components.task, data.format_type)}</div>
        </div>` : ''}

        ${components.action ? `
        <div class="star-section">
            <h4>⚡ Action</h4>
            <div class="star-content">${formatContent(components.action, data.format_type)}</div>
        </div>` : ''}

        ${components.result ? `
        <div class="star-section">
            <h4>🏆 Result</h4>
            <div class="star-content">${formatContent(components.result, data.format_type)}</div>
        </div>` : ''}
    `;

    answersContainer.insertBefore(answerCard, answersContainer.firstChild);
}

function displayQuickAnswer(data) {
    const answersContainer = document.getElementById('answersContainer');

    const answerCard = document.createElement('div');
    answerCard.className = 'answer-card';

    answerCard.innerHTML = `
        <div class="answer-question">${data.question}</div>
        <div class="answer-meta">
            <span class="meta-badge">⚡ Quick Answer</span>
            <span class="meta-badge">⏱️ ${data.time_ms}ms</span>
            <span class="meta-badge">🤖 ${data.provider.toUpperCase()}</span>
        </div>
        <div class="star-content">${formatContent(data.answer, data.format_type)}</div>
    `;

    answersContainer.insertBefore(answerCard, answersContainer.firstChild);
}

function formatContent(content, formatType) {
    if (formatType === 'bullets') {
        // Convert lines starting with - or * to proper list items
        const lines = content.split('\n');
        let formatted = '';
        let inList = false;

        for (let line of lines) {
            line = line.trim();
            if (line.startsWith('-') || line.startsWith('*')) {
                if (!inList) {
                    formatted += '<ul>';
                    inList = true;
                }
                formatted += `<li>${line.substring(1).trim()}</li>`;
            } else if (line) {
                if (inList) {
                    formatted += '</ul>';
                    inList = false;
                }
                formatted += `<p>${line}</p>`;
            }
        }

        if (inList) {
            formatted += '</ul>';
        }

        return formatted || content;
    } else {
        // For full format, just preserve paragraphs
        return content.split('\n').filter(p => p.trim())
            .map(p => `<p>${p.trim()}</p>`).join('');
    }
}

function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => {
        if (msg.parentNode) {
            msg.remove();
        }
    });

    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;

    // Insert at the top of container (try main first, then container)
    let container = document.querySelector('main');
    if (!container) {
        container = document.querySelector('.container');
    }
    if (!container) {
        container = document.body;
    }

    container.insertBefore(messageDiv, container.firstChild);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.remove();
            }
        }, 300);
    }, 5000);
}

// Helper function to format time
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}
