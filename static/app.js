// DocWeave Frontend Application

let mermaidInitialized = false;

// Initialize Mermaid
if (typeof mermaid !== 'undefined') {
    mermaid.initialize({ 
        startOnLoad: true,
        theme: 'dark',
        themeVariables: {
            primaryColor: '#238636',
            primaryTextColor: '#c9d1d9',
            primaryBorderColor: '#30363d',
            lineColor: '#30363d',
            secondaryColor: '#161b22',
            tertiaryColor: '#0d1117'
        }
    });
    mermaidInitialized = true;
}

// Form submission handler
document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const repoPath = formData.get('repoPath');
    const limit = parseInt(formData.get('limit')) || 10;
    const daysBack = formData.get('daysBack') ? parseInt(formData.get('daysBack')) : null;
    
    // Hide previous results
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    
    // Show progress
    document.getElementById('progressSection').style.display = 'block';
    updateProgress(0, 'Starting analysis...');
    
    // Disable button
    const btn = document.getElementById('analyzeBtn');
    btn.disabled = true;
    btn.querySelector('.btn-text').style.display = 'none';
    btn.querySelector('.btn-loader').style.display = 'inline';
    
    try {
        updateProgress(20, 'Analyzing repository structure...');
        
        // Check if it's a GitHub URL
        if (repoPath.startsWith('http://') || repoPath.startsWith('https://')) {
            if (repoPath.includes('github.com')) {
                throw new Error('GitHub URLs are not supported directly. Please clone the repository first:\n\n' +
                    `git clone ${repoPath}\n` +
                    'Then use the local path (e.g., the repository folder name)');
            } else {
                throw new Error('URLs are not supported. Please provide a local file path to a git repository.');
            }
        }
        
        // First, get commits to show progress
        const commitsResponse = await fetch(`/api/commits?repo_path=${encodeURIComponent(repoPath)}&limit=${limit}`);
        if (!commitsResponse.ok) {
            const errorData = await commitsResponse.json().catch(() => ({ detail: 'Failed to fetch commits' }));
            let errorMsg = errorData.detail || 'Failed to fetch commits. Please ensure the path is a valid git repository.';
            
            // Add helpful hints for common errors
            if (errorMsg.includes('does not exist')) {
                errorMsg += '\n\n💡 Tip: Use "." for current directory, or provide an absolute path like "/path/to/repo"';
            } else if (errorMsg.includes('not a git repository')) {
                errorMsg += '\n\n💡 Tip: Make sure you\'re in a directory with a .git folder, or initialize with: git init';
            }
            
            throw new Error(errorMsg);
        }
        const commits = await commitsResponse.json();
        
        // Check Copilot status
        const copilotCheck = await fetch('/api/copilot/check');
        const copilotStatus = await copilotCheck.json();
        const copilotMsg = copilotStatus.installed 
            ? `Found ${commits.length} commit(s). Analyzing with GitHub Copilot CLI...`
            : `Found ${commits.length} commit(s). Analyzing (using fallback - Copilot CLI not available)...`;
        updateProgress(40, copilotMsg);
        
        // Now run full analysis
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                repo_path: repoPath,
                limit: limit,
                days_back: daysBack
            })
        });
        
        updateProgress(80, 'Generating documentation...');
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }
        
        const result = await response.json();
        
        updateProgress(100, 'Analysis complete!');
        
        // Show results
        await displayResults(commits, result);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        // Re-enable button
        btn.disabled = false;
        btn.querySelector('.btn-text').style.display = 'inline';
        btn.querySelector('.btn-loader').style.display = 'none';
        document.getElementById('progressSection').style.display = 'none';
    }
});

function updateProgress(percent, message) {
    document.getElementById('progressFill').style.width = percent + '%';
    document.getElementById('progressText').textContent = message;
}

async function displayResults(commits, result) {
        // Show success message with Copilot usage info
        const resultsContent = document.getElementById('resultsContent');
        const copilotInfo = result.message.includes('Copilot CLI used') 
            ? '<br>🤖 <strong>GitHub Copilot CLI was used for AI-powered analysis</strong>'
            : result.message.includes('fallback')
            ? '<br>⚠️ <strong>Using fallback analysis</strong> (Copilot CLI not available)'
            : '';
        
        resultsContent.innerHTML = `
            <div class="success-message">
                ✅ ${result.message}
                ${copilotInfo}
                ${result.documentation_path ? `<br>Documentation saved to: <code>${result.documentation_path}</code>` : ''}
            </div>
            <h3>Recent Commits</h3>
            <div id="commitsList"></div>
        `;
    
    // Display commits
    const commitsList = document.getElementById('commitsList');
    commits.forEach(commit => {
        const commitEl = document.createElement('div');
        commitEl.className = 'commit-item';
        commitEl.innerHTML = `
            <div class="commit-header">
                <span class="commit-sha">${commit.sha}</span>
                <span class="commit-meta">
                    ${commit.additions} additions, ${commit.deletions} deletions
                </span>
            </div>
            <div class="commit-message">${escapeHtml(commit.message.split('\n')[0])}</div>
            <div class="commit-meta">
                <span>👤 ${escapeHtml(commit.author)}</span>
                <span>📅 ${new Date(commit.date).toLocaleString()}</span>
                <span>📁 ${commit.files_changed.length} file(s) changed</span>
            </div>
            ${commit.files_changed.length > 0 ? `
                <details style="margin-top: 10px;">
                    <summary style="cursor: pointer; color: var(--text-secondary);">Files changed</summary>
                    <ul style="margin-top: 10px; padding-left: 20px;">
                        ${commit.files_changed.slice(0, 10).map(f => `<li><code>${escapeHtml(f)}</code></li>`).join('')}
                        ${commit.files_changed.length > 10 ? `<li><em>... and ${commit.files_changed.length - 10} more</em></li>` : ''}
                    </ul>
                </details>
            ` : ''}
        `;
        commitsList.appendChild(commitEl);
    });
    
    // Fetch and display documentation
    if (result.documentation_path) {
        await loadDocumentation(result.documentation_path);
    }
    
    // Show results section
    document.getElementById('resultsSection').style.display = 'block';
}

async function loadDocumentation(docsPath) {
    try {
        // In a real app, you'd fetch these files via API
        // For now, we'll show a message
        const docContent = document.getElementById('documentationContent');
        docContent.innerHTML = `
            <div class="success-message">
                📝 Documentation has been generated in the repository's <code>docs/</code> folder.
            </div>
            <p style="margin-top: 15px; color: var(--text-secondary);">
                The following files have been created:
            </p>
            <ul style="margin-top: 10px; padding-left: 20px;">
                <li><code>CHANGES.md</code> - Detailed commit analysis</li>
                <li><code>NARRATIVE.md</code> - Development narrative</li>
                <li><code>DIAGRAMS.md</code> - Mermaid diagrams</li>
                <li><code>NEXT_STEPS.md</code> - Suggested next steps</li>
            </ul>
        `;
        
        // Try to load diagrams if available
        // In production, you'd have an API endpoint to fetch these
        document.getElementById('diagramsContent').innerHTML = `
            <p style="color: var(--text-secondary);">
                Diagrams have been generated in <code>DIAGRAMS.md</code>. 
                Open the file in your repository to view them, or use a Mermaid-compatible viewer.
            </p>
        `;
        
    } catch (error) {
        console.error('Error loading documentation:', error);
    }
}

function showError(message) {
    const errorEl = document.getElementById('errorMessage');
    // Handle multi-line messages and preserve formatting
    if (message.includes('\n')) {
        errorEl.innerHTML = message.split('\n').map(line => {
            if (line.trim().startsWith('💡')) {
                return `<div style="margin-top: 10px; color: var(--text-secondary);">${escapeHtml(line)}</div>`;
            }
            return `<div>${escapeHtml(line)}</div>`;
        }).join('');
    } else {
        errorEl.textContent = message;
    }
    document.getElementById('errorSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Check Copilot CLI status and health on load
async function checkCopilotStatus() {
    try {
        const healthResponse = await fetch('/api/health');
        const health = await healthResponse.json();
        
        const copilotResponse = await fetch('/api/copilot/check');
        const copilot = await copilotResponse.json();
        
        // Display Copilot status in the UI
        const statusBanner = document.createElement('div');
        statusBanner.className = copilot.installed ? 'success-message' : 'error-card';
        statusBanner.style.marginBottom = '20px';
        statusBanner.style.padding = '15px';
        statusBanner.innerHTML = copilot.installed 
            ? '✅ <strong>GitHub Copilot CLI is available</strong> - AI-powered analysis will be used'
            : `⚠️ <strong>GitHub Copilot CLI not available</strong> - Using fallback analysis. <details style="margin-top: 10px;"><summary style="cursor: pointer;">Show installation instructions</summary><pre style="margin-top: 10px; white-space: pre-wrap;">${copilot.instructions || 'Install GitHub CLI and Copilot extension'}</pre></details>`;
        
        const main = document.querySelector('main');
        if (main && !document.getElementById('copilotStatus')) {
            statusBanner.id = 'copilotStatus';
            main.insertBefore(statusBanner, main.firstChild);
        }
        
        console.log('Copilot CLI status:', copilot);
    } catch (err) {
        console.error('Error checking Copilot status:', err);
    }
}

// Tutorial/Guide Functions
let currentStep = 1;
const totalSteps = 5;

function showStep(step) {
    // Hide all steps
    document.querySelectorAll('.tutorial-step').forEach(s => {
        s.classList.remove('active');
    });
    
    // Show current step
    const stepElement = document.querySelector(`.tutorial-step[data-step="${step}"]`);
    if (stepElement) {
        stepElement.classList.add('active');
    }
    
    // Update progress
    const progressEl = document.getElementById('tutorialProgress');
    if (progressEl) {
        progressEl.textContent = `Step ${step} of ${totalSteps}`;
    }
    
    // Update button states
    const prevBtn = document.querySelector('.tutorial-nav .tutorial-btn:first-child');
    const nextBtn = document.querySelector('.tutorial-nav .tutorial-btn:last-child');
    
    if (prevBtn) prevBtn.disabled = step === 1;
    if (nextBtn) nextBtn.disabled = step === totalSteps;
}

function nextStep() {
    if (currentStep < totalSteps) {
        currentStep++;
        showStep(currentStep);
    }
}

function previousStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
    }
}

function toggleTutorial() {
    const content = document.getElementById('tutorialContent');
    const toggle = document.querySelector('.tutorial-toggle');
    
    if (content && toggle) {
        if (content.style.display === 'none') {
            content.style.display = 'block';
            toggle.textContent = 'Hide Guide';
        } else {
            content.style.display = 'none';
            toggle.textContent = 'Show Guide';
        }
    }
}

// Initialize tutorial on load
document.addEventListener('DOMContentLoaded', () => {
    showStep(1);
});

// Run checks on page load
checkCopilotStatus();
