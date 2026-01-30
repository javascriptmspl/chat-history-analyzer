#!/usr/bin/env python3
"""
Run the Flask web application for Chat History Analyzer
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from chat_analyzer.app import app

if __name__ == '__main__':
    print("\n")
    print("╔═══════════════════════════════════════════╗")
    print("║  💬  CHAT HISTORY ANALYZER - Web UI      ║")
    print("╚═══════════════════════════════════════════╝\n")
    print("🚀 Starting Flask application...\n")
    print("📱 Open your browser and go to: http://localhost:5000\n")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
