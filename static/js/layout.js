// Layout management for Interview Mode toggle

document.addEventListener('DOMContentLoaded', function() {
    const layoutToggle = document.getElementById('layoutToggle');
    const contentWrapper = document.getElementById('contentWrapper');

    if (!layoutToggle || !contentWrapper) {
        console.error('Layout toggle elements not found');
        return;
    }

    // Load saved preference
    const savedMode = localStorage.getItem('interviewMode');
    if (savedMode === 'true') {
        enableInterviewMode();
    }

    // Toggle button click handler
    layoutToggle.addEventListener('click', function() {
        if (contentWrapper.classList.contains('interview-mode')) {
            disableInterviewMode();
        } else {
            enableInterviewMode();
        }
    });

    function enableInterviewMode() {
        contentWrapper.classList.add('interview-mode');
        layoutToggle.innerHTML = '<span class="icon">⬅</span> Standard View';
        localStorage.setItem('interviewMode', 'true');

        // Show notification
        if (typeof showMessage === 'function') {
            showMessage('Interview Mode enabled! Position your Zoom/Meet window on the left.', 'info');
        }
    }

    function disableInterviewMode() {
        contentWrapper.classList.remove('interview-mode');
        layoutToggle.innerHTML = '<span class="icon">⚡</span> Interview Mode';
        localStorage.setItem('interviewMode', 'false');

        // Show notification
        if (typeof showMessage === 'function') {
            showMessage('Standard view enabled.', 'info');
        }
    }
});

// Function to toggle section collapse
function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (!section) return;

    const content = section.querySelector('.section-content');
    const btn = section.querySelector('.collapse-btn');

    if (!content) return;

    if (content.style.display === 'none') {
        content.style.display = 'block';
        if (btn) btn.textContent = '−';
    } else {
        content.style.display = 'none';
        if (btn) btn.textContent = '+';
    }
}
