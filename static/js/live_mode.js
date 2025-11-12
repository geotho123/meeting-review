// Live mode functions for real-time transcription and question detection

let liveTranscript = '';
let detectedQuestions = [];

function updateLiveTranscript(chunk, full) {
    const liveSection = document.getElementById('liveSection');
    const liveDisplay = document.getElementById('liveTranscriptDisplay');
    const liveStats = document.getElementById('liveStats');

    // Show live section if hidden
    if (liveSection.style.display === 'none') {
        liveSection.style.display = 'block';
        liveDisplay.innerHTML = '';  // Clear placeholder
    }

    // Add new chunk
    const chunkDiv = document.createElement('div');
    chunkDiv.className = 'live-transcript-chunk';
    chunkDiv.textContent = chunk;
    liveDisplay.appendChild(chunkDiv);

    // Auto-scroll to bottom
    liveDisplay.scrollTop = liveDisplay.scrollHeight;

    // Update stats
    const wordCount = full.trim().split(/\s+/).length;
    liveStats.textContent = `${wordCount} words transcribed...`;

    // Store full transcript
    liveTranscript = full;
}

function displayDetectedQuestion(question) {
    const qaSection = document.getElementById('liveQASection');
    const container = document.getElementById('liveQuestionsContainer');

    // Show QA section if hidden
    if (qaSection.style.display === 'none') {
        qaSection.style.display = 'block';
        container.innerHTML = '';  // Clear placeholder
    }

    // Create question card
    const questionCard = document.createElement('div');
    questionCard.className = 'live-question-card';
    const timestamp = new Date().getTime();
    questionCard.id = `question-${timestamp}`;

    questionCard.innerHTML = `
        <div class="live-question-text">${question}</div>
        <div class="live-answer-text">
            <div class="loading">
                <div class="spinner"></div>
                <p>Generating STAR answer...</p>
            </div>
        </div>
    `;

    container.insertBefore(questionCard, container.firstChild);

    // Store question
    detectedQuestions.push({question: question, timestamp: timestamp});

    // Show notification
    showMessage(`Question detected: "${question.substring(0, 50)}..."`, 'info');
}

function displayLiveAnswer(question, answer, timeMs) {
    // Find the question card
    const cards = document.querySelectorAll('.live-question-card');
    let targetCard = null;

    for (let card of cards) {
        const questionText = card.querySelector('.live-question-text').textContent;
        if (questionText === question) {
            targetCard = card;
            break;
        }
    }

    if (!targetCard) return;

    // Update answer
    const answerDiv = targetCard.querySelector('.live-answer-text');
    answerDiv.innerHTML = `
        <div>${formatContent(answer, 'bullets')}</div>
        <div class="live-answer-meta">
            <span class="live-badge-small">⏱️ ${timeMs}ms</span>
            <span class="live-badge-small">🤖 AI Generated</span>
        </div>
    `;

    // Highlight briefly
    answerDiv.classList.add('highlight-new');
    setTimeout(() => answerDiv.classList.remove('highlight-new'), 2000);

    // Show notification
    showMessage(`Answer generated in ${timeMs}ms!`, 'success');
}
