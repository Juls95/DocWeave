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
        
        // First, get commits to show progress
        const commitsResponse = await fetch(`/api/commits?repo_path=${encodeURIComponent(repoPath)}&limit=${limit}`);
        if (!commitsResponse.ok) {
            throw new Error('Failed to fetch commits');
        }
        const commits = await commitsResponse.json();
        
        updateProgress(40, `Found ${commits.length} commit(s). Analyzing with Copilot CLI...`);
        
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
    // Show success message
    const resultsContent = document.getElementById('resultsContent');
    resultsContent.innerHTML = `
        <div class="success-message">
            ✅ Successfully analyzed ${result.commits_count} commit(s)!
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
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Health check on load
fetch('/api/health')
    .then(res => res.json())
    .then(data => {
        console.log('DocWeave API is healthy:', data);
    })
    .catch(err => {
        console.error('API health check failed:', err);
    });
