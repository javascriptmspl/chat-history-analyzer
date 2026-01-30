// Chart instances
let messagesChart = null;
let wordsChart = null;

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    setupFormHandler();
    loadSampleFormat();
});

// Load sample format
function loadSampleFormat() {
    fetch('/api/sample-format')
        .then(response => response.json())
        .then(data => {
            document.getElementById('sampleExample').textContent = data.sample;
        });
}

// Setup form handler
function setupFormHandler() {
    const uploadForm = document.getElementById('uploadForm');
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        analyzeChat();
    });

    // Show file name when selected
    const fileInput = document.getElementById('fileInput');
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            const fileName = this.files[0].name;
            const label = this.parentElement;
            label.querySelector('span:nth-of-type(2)').textContent = '✓ ' + fileName;
        }
    });
}

// Analyze chat
function analyzeChat() {
    const fileInput = document.getElementById('fileInput');
    const topWords = document.getElementById('topWords').value;

    if (!fileInput.files.length) {
        showError('Please select a file');
        return;
    }

    // Show loading
    showLoading();

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('top_words', topWords);

    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Analysis failed');
            });
        }
        return response.json();
    })
    .then(data => {
        displayResults(data);
    })
    .catch(error => {
        showError(error.message);
    });
}

// Show loading state
function showLoading() {
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'flex';
}

// Show error
function showError(message) {
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'block';
    document.getElementById('errorMessage').textContent = '✗ ' + message;
}

// Display results
function displayResults(data) {
    // Update stats
    document.getElementById('totalMessages').textContent = data.total_messages;
    document.getElementById('activeUsers').textContent = data.active_users;
    document.getElementById('avgLength').textContent = data.average_message_length + ' chars';

    // Update report
    document.getElementById('fullReport').textContent = data.report;

    // Build messages per user table
    const messagesTableBody = document.getElementById('messagesTableBody');
    messagesTableBody.innerHTML = '';
    const totalMessages = data.total_messages;
    
    for (const [user, count] of Object.entries(data.messages_per_user)) {
        const percentage = ((count / totalMessages) * 100).toFixed(1);
        const row = `
            <tr>
                <td>${user}</td>
                <td>${count}</td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${percentage}%"></div>
                    </div>
                    ${percentage}%
                </td>
            </tr>
        `;
        messagesTableBody.innerHTML += row;
    }

    // Build word frequency table
    const wordsTableBody = document.getElementById('wordsTableBody');
    wordsTableBody.innerHTML = '';
    const maxWordCount = data.word_frequency.length > 0 ? data.word_frequency[0].count : 1;
    
    for (const wordObj of data.word_frequency) {
        const percentage = ((wordObj.count / maxWordCount) * 100).toFixed(1);
        const row = `
            <tr>
                <td>${wordObj.word}</td>
                <td>${wordObj.count}</td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${percentage}%"></div>
                    </div>
                    ${percentage}%
                </td>
            </tr>
        `;
        wordsTableBody.innerHTML += row;
    }

    // Update charts
    updateCharts(data);

    // Show results
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';

    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

// Update charts
function updateCharts(data) {
    const users = Object.keys(data.messages_per_user);
    const messageCounts = Object.values(data.messages_per_user);
    const words = data.word_frequency.map(w => w.word);
    const wordCounts = data.word_frequency.map(w => w.count);

    // Messages chart
    const messagesCtx = document.getElementById('messagesChart').getContext('2d');
    
    if (messagesChart) {
        messagesChart.destroy();
    }

    messagesChart = new Chart(messagesCtx, {
        type: 'doughnut',
        data: {
            labels: users,
            datasets: [{
                data: messageCounts,
                backgroundColor: [
                    '#00d4ff',
                    '#ff006e',
                    '#8338ec',
                    '#ffbe0b',
                    '#06ffa5',
                    '#fb5607'
                ],
                borderColor: '#0a0e27',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#ecf0f1',
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                }
            }
        }
    });

    // Words chart
    const wordsCtx = document.getElementById('wordsChart').getContext('2d');
    
    if (wordsChart) {
        wordsChart.destroy();
    }

    wordsChart = new Chart(wordsCtx, {
        type: 'bar',
        data: {
            labels: words,
            datasets: [{
                label: 'Frequency',
                data: wordCounts,
                backgroundColor: [
                    '#00d4ff',
                    '#ff006e',
                    '#8338ec',
                    '#ffbe0b',
                    '#06ffa5',
                    '#fb5607',
                    '#00d4ff',
                    '#ff006e',
                    '#8338ec',
                    '#ffbe0b'
                ].slice(0, words.length),
                borderColor: '#00d4ff',
                borderWidth: 2
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#ecf0f1',
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#ecf0f1'
                    },
                    grid: {
                        color: 'rgba(0, 212, 255, 0.1)'
                    }
                },
                y: {
                    ticks: {
                        color: '#ecf0f1'
                    },
                    grid: {
                        color: 'rgba(0, 212, 255, 0.1)'
                    }
                }
            }
        }
    });
}

// Reset analysis
function resetAnalysis() {
    document.getElementById('uploadForm').reset();
    document.getElementById('fileInput').parentElement.querySelector('span:nth-of-type(2)').textContent = 'Choose a chat file (TXT or LOG)';
    document.getElementById('uploadSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'none';
    
    // Scroll to top
    document.querySelector('.header').scrollIntoView({ behavior: 'smooth' });
}

// Download report
function downloadReport() {
    const report = document.getElementById('fullReport').textContent;
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(report));
    element.setAttribute('download', 'chat_analysis_report.txt');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}
