# 🚀 Chat History Analyzer - Web Interface Guide

## Starting the Web Application

### Option 1: Using the run script (Recommended)
```bash
python run_web.py
```

### Option 2: Using Python module
```bash
python -m src.chat_analyzer.app
```

### Option 3: Using the virtual environment
```bash
./venv/bin/python run_web.py
```

## Accessing the Web UI

Once the Flask app is running, open your browser and navigate to:
- **Local:** http://localhost:5000
- **Network:** http://192.168.1.X:5000 (replace X with your IP)

## Features

### 📂 File Upload
- Drag and drop or click to select your chat file
- Supported formats: `.txt` and `.log` files
- Max file size: 16 MB

### ⚙️ Configuration
- **Top Words:** Adjust the number of top words to display (5-50)
- File format must match: `[DD/MM/YY, HH:MM:SS] User: Message`

### 📊 Analysis Results

Once your file is analyzed, you'll see:

1. **Summary Statistics**
   - Total Messages count
   - Active Users count
   - Average Message Length

2. **Visual Charts**
   - Doughnut chart showing messages per user distribution
   - Horizontal bar chart showing top word frequencies

3. **Detailed Tables**
   - Messages per user with percentages and progress bars
   - Word frequency analysis with visual indicators

4. **Full Report**
   - Complete text report exportable as a file
   - Download as `.txt` file for sharing

## Example Workflow

1. **Open the application** → http://localhost:5000
2. **Select a chat file** → Click the upload area or drag and drop
3. **Configure options** → Adjust top words if needed
4. **Click "🚀 Analyze Chat"** → Wait for results
5. **Review results** → Scroll through analysis and charts
6. **Download report** → Click "⬇ Download Report" button
7. **Analyze another** → Click "↻ Analyze Another File"

## File Format Requirements

Your chat file must follow this exact format:

```
[DD/MM/YY, HH:MM:SS] User: Message text
[DD/MM/YY, HH:MM:SS] Another User: Another message
```

### Valid Example:
```
[01/15/24, 10:30:45] Alice: Hey everyone, how are you?
[01/15/24, 10:31:12] Bob: I'm doing great! How about you?
[01/15/24, 10:32:00] Alice: Awesome! Want to grab coffee?
[01/15/24, 10:33:45] Charlie: That sounds fun! I'm in.
```

### Date Format:
- `DD` = 2-digit day (01-31)
- `MM` = 2-digit month (01-12)
- `YY` or `YYYY` = 2 or 4-digit year

### Time Format:
- `HH:MM:SS` = 24-hour format

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, you can modify the `run_web.py` file:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Change 5000 to 8000
```

### File Format Not Recognized
- Ensure your file follows the exact format
- Check the "Expected File Format" section in the app
- Make sure timestamps are in [DD/MM/YY, HH:MM:SS] format

### Large Files Taking Too Long
- The app has a 16 MB file size limit
- Very large files may take some time to process
- Try a smaller subset of your chat history

### Browser Not Loading
- Make sure the Flask server is running
- Check the terminal output for any errors
- Try accessing from a different browser
- Clear your browser cache

## Features Highlights

✨ **Beautiful UI**
- Modern dark theme with cyan and purple accents
- Responsive design works on desktop, tablet, and mobile
- Smooth animations and transitions

📊 **Rich Visualizations**
- Interactive charts powered by Chart.js
- Progress bars showing distributions
- Color-coded statistics cards

🎯 **User-Friendly**
- Drag-and-drop file upload
- Real-time analysis results
- One-click report download
- Easy file format reference

🚀 **Performance**
- Fast analysis of large files
- Efficient data processing
- Optimized for modern browsers

## System Requirements

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- 50 MB disk space for logs/data
- 512 MB RAM minimum

## Dependencies

The web interface uses:
- **Flask** - Web framework
- **Werkzeug** - WSGI utilities
- **Chart.js** - Interactive charts (loaded from CDN)
- **Rich** - Terminal styling (for CLI analysis)

## Tips & Tricks

💡 **Export Multiple Reports**
- Analyze the same file with different top-word settings
- Download each report for comparison

💡 **Share Analysis Results**
- Download the full report as TXT
- Copy chart images using your browser's screenshot tool

💡 **Bulk Analysis**
- Split large chat files into smaller chunks
- Analyze each separately for detailed insights

💡 **Keep Server Running**
- Run in a terminal window while you work
- Access from multiple devices on the same network

## Support & Issues

If you encounter any issues:
1. Check the terminal output for error messages
2. Verify your file format matches the requirements
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Try with the sample file: `data/sample_chat.txt`

---

**Enjoy analyzing your chats! 🎉**
