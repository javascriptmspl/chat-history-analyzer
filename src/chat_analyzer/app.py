"""
Flask web application for Chat History Analyzer
Provides a beautiful web interface for analyzing chat history files
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
from pathlib import Path
from .parser import ChatParser
from .analyzer import ChatAnalyzer
from io import StringIO

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'txt', 'log'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded chat file."""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File must be .txt or .log'}), 400
        
        # Get top words parameter
        top_words = request.form.get('top_words', 10, type=int)
        
        # Read and parse the file
        content = file.read().decode('utf-8')
        
        # Parse using ChatParser logic
        import re
        messages = []
        pattern = r'\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}:\d{2})\] ([^:]+): (.+)'
        matches = re.findall(pattern, content, re.MULTILINE)
        
        if not matches:
            return jsonify({'error': 'No valid chat messages found. Check the file format.'}), 400
        
        for match in matches:
            date_str, time_str, user, message = match
            messages.append({
                'date': date_str,
                'time': time_str,
                'user': user,
                'message': message
            })
        
        # Analyze
        analyzer = ChatAnalyzer(messages)
        
        # Get statistics
        msg_count = analyzer.get_message_count_per_user()
        word_freq = analyzer.get_word_frequency(top_words)
        avg_len = analyzer.get_average_message_length()
        
        # Prepare response data
        response_data = {
            'total_messages': len(messages),
            'active_users': len(msg_count),
            'average_message_length': round(avg_len, 2),
            'messages_per_user': dict(sorted(msg_count.items(), key=lambda x: x[1], reverse=True)),
            'word_frequency': [{'word': word, 'count': count} for word, count in word_freq],
            'report': analyzer.generate_report()
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': f'Error analyzing file: {str(e)}'}), 500

@app.route('/api/sample-format', methods=['GET'])
def sample_format():
    """Return sample chat format."""
    sample = """[01/15/24, 10:30:45] Alice: Hey everyone, how are you?
[01/15/24, 10:31:12] Bob: I'm doing great! How about you?
[01/15/24, 10:32:00] Alice: Awesome! Want to grab coffee?
[01/15/24, 10:33:45] Charlie: That sounds fun! I'm in.
[01/15/24, 10:34:20] Bob: Python projects are going well, data analysis is fun!"""
    return jsonify({'sample': sample})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

def main():
    """Run the Flask web application."""
    print("\n")
    print("╔═══════════════════════════════════════════╗")
    print("║  💬  CHAT HISTORY ANALYZER - Web UI      ║")
    print("╚═══════════════════════════════════════════╝\n")
    print("🚀 Starting Flask application...\n")
    print("📱 Open your browser and go to: http://localhost:5000\n")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
