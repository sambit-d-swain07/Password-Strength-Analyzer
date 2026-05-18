document.addEventListener('DOMContentLoaded', () => {
    const passwordInput = document.getElementById('password-input');
    const toggleBtn = document.getElementById('toggle-visibility');
    const inputWrapper = document.getElementById('input-wrapper');
    const scoreDisplay = document.getElementById('score-display');
    const segments = [
        document.getElementById('seg-1'),
        document.getElementById('seg-2'),
        document.getElementById('seg-3'),
        document.getElementById('seg-4')
    ];
    const diagnosticsContent = document.getElementById('diagnostics-content');
    const generateBtn = document.getElementById('generate-btn');
    const toast = document.getElementById('toast');
    
    // Visibility toggle
    toggleBtn.addEventListener('click', () => {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        if (type === 'text') {
            toggleBtn.innerHTML = `
                <svg class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                    <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
            `;
        } else {
            toggleBtn.innerHTML = `
                <svg class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                </svg>
            `;
        }
    });

    let debounceTimer;
    
    passwordInput.addEventListener('input', (e) => {
        const val = e.target.value;
        
        clearTimeout(debounceTimer);
        
        if (!val) {
            resetUI();
            return;
        }
        
        // Debounce API calls
        debounceTimer = setTimeout(() => {
            analyzePassword(val);
        }, 300);
    });

    async function analyzePassword(password) {
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password })
            });
            
            const data = await response.json();
            updateUI(data.score, data.diagnostics, data.duplicate);
        } catch (error) {
            console.error('Analysis error:', error);
            diagnosticsContent.innerHTML = `<div class="log-line status-error">> ERROR: Unable to contact assessment server.</div>`;
        }
    }

    function resetUI() {
        // Reset classes
        inputWrapper.className = 'input-wrapper';
        scoreDisplay.className = 'telemetry-score';
        scoreDisplay.textContent = 'AWAITING INPUT';
        
        segments.forEach(seg => {
            seg.style.background = 'rgba(255, 255, 255, 0.1)';
            seg.style.boxShadow = 'none';
        });
        
        diagnosticsContent.innerHTML = '<div class="log-line text-muted">> SYSTEM READY. WAITING FOR INPUT...</div>';
    }

    function updateUI(score, diagnostics, isDuplicate) {
        // Update styling
        inputWrapper.className = `input-wrapper tier-${score}`;
        scoreDisplay.className = `telemetry-score tier-${score}`;
        
        let label = '';
        if (isDuplicate) label = 'CONFLICT';
        else if (score <= 1) label = 'CRITICAL RISK';
        else if (score === 2) label = 'LOW ENTROPY';
        else if (score === 3) label = 'ADEQUATE';
        else if (score === 4) label = 'SECURE';
        
        scoreDisplay.textContent = `TIER ${score} - ${label}`;
        
        // Update segments
        const colors = [
            'var(--tier-1)', // 1
            'var(--tier-2)', // 2
            'var(--tier-3)', // 3
            'var(--tier-4)'  // 4
        ];
        
        const activeColor = score === 0 ? 'var(--tier-1)' : colors[score - 1];
        
        segments.forEach((seg, index) => {
            if (score === 0 && index === 0) {
                seg.style.background = activeColor;
                seg.style.boxShadow = `0 0 8px ${activeColor}`;
            } else if (index < score) {
                seg.style.background = activeColor;
                seg.style.boxShadow = `0 0 8px ${activeColor}`;
            } else {
                seg.style.background = 'rgba(255, 255, 255, 0.1)';
                seg.style.boxShadow = 'none';
            }
        });
        
        // Update diagnostics
        diagnosticsContent.innerHTML = '';
        diagnostics.forEach(diag => {
            const line = document.createElement('div');
            line.className = `log-line status-${diag.status}`;
            line.textContent = `> ${diag.message}`;
            diagnosticsContent.appendChild(line);
        });
        
        // Scroll to bottom
        diagnosticsContent.scrollTop = diagnosticsContent.scrollHeight;
    }

    generateBtn.addEventListener('click', async () => {
        generateBtn.classList.add('loading');
        
        try {
            const response = await fetch('/api/generate');
            const data = await response.json();
            
            const newPassword = data.password;
            passwordInput.value = newPassword;
            
            // Trigger analysis for the new password
            analyzePassword(newPassword);
            
            // Copy to clipboard
            navigator.clipboard.writeText(newPassword).then(() => {
                showToast();
            });
            
        } catch (error) {
            console.error('Generation error:', error);
        } finally {
            generateBtn.classList.remove('loading');
        }
    });

    function showToast() {
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
});
