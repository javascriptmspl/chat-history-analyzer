# 💬 Chat History Analyzer

> Unlock the hidden stories in your chat logs! A beautifully designed Python tool to analyze chat history files and reveal insightful statistics.

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![GitHub Stars](https://img.shields.io/badge/⭐-Give%20us%20a%20star!-yellow?style=flat-square)](.)

</div>

## ✨ Features

- 📊 **Parse Chat Logs** - Currently supports WhatsApp-like formats
- 👥 **User Analytics** - Count messages per user with visual progress bars
- 🔤 **Word Frequency** - Discover the most commonly used words
- 📏 **Message Metrics** - Calculate average message length and more
- 📈 **Beautiful Visualizations** - Colored tables and styled output with emojis
- 📄 **Report Generation** - Export detailed analysis reports to files
- 🎨 **Rich CLI Experience** - Gorgeous terminal output with rich formatting

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download** this repository
   ```bash
   git clone <repository-url>
   cd chat-history-analyzer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package**
   ```bash
   pip install -e .
   ```

## 📖 Usage

### Basic Command
```bash
chat-analyzer path/to/chat.txt
```

### With Options
```bash
chat-analyzer data/sample_chat.txt --output report.txt --top-words 20
```

### Available Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Save the report to a file | None |
| `--top-words` | `-w` | Number of top words to display | 10 |

## 📝 Chat File Format

The tool expects chat files in the WhatsApp-like format:

```
[DD/MM/YY, HH:MM:SS] User: Message text
[DD/MM/YY, HH:MM:SS] Another User: Another message
[DD/MM/YY, HH:MM:SS] User: Hello there!
```

### Example:
```
[01/15/24, 10:30:45] Alice: Hey, how are you?
[01/15/24, 10:31:12] Bob: I'm doing great! How about you?
[01/15/24, 10:32:00] Alice: Awesome! Want to grab coffee?
```

## 🎯 What You Get

The analyzer provides:
- 📊 **Message Counts** - See who's the most talkative
- 🔤 **Word Frequency** - Discover conversation patterns
- 📏 **Message Statistics** - Average length and more
- 📄 **Full Reports** - Exportable analysis reports

## 📁 Project Structure

```
chat-history-analyzer/
├── src/
│   └── chat_analyzer/
│       ├── cli.py           # Command-line interface
│       ├── parser.py        # Chat file parser
│       ├── analyzer.py      # Analysis engine
│       └── __init__.py
├── tests/
│   └── test_analyzer.py     # Unit tests
├── data/
│   └── sample_chat.txt      # Sample chat file
├── README.md                # This file
├── requirements.txt         # Dependencies
└── pyproject.toml          # Project configuration
```

## 🛠️ Development

### Running Tests
```bash
python -m pytest tests/
```

### Installing in Development Mode
```bash
pip install -e ".[dev]"
```

## 📦 Dependencies

- **rich** - For beautiful terminal output
- **python** - Core language

See `requirements.txt` for all dependencies.

## 📊 Sample Output

```
╔═══════════════════════════════════════════╗
║  💬  CHAT HISTORY ANALYZER  💬           ║
║     Unlock Your Chat Insights             ║
╚═══════════════════════════════════════════╝

📂 Loading chat file: data/sample_chat.txt
✓ Found 152 messages!

📊 Messages per User
┏━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ 👤 User  ┃ 💬 Count  ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━┩
│ Alice    │ 87 (57%) █████████████ │
│ Bob      │ 65 (43%) ██████████     │
└──────────┴──────────┘

🔤 Top 10 Words
┏━━━━━━━━━━┳━━━━━━━━━━┓
┃ Word    ┃ Frequency┃
┡━━━━━━━━━━╇━━━━━━━━━━┩
│ hello   │ 12 █████ │
│ great   │ 10 ████  │
│ thanks  │ 8  ███   │
└─────────┴─────────┘
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💡 Tips & Tricks

- **Large Files**: For very large chat files, processing may take a moment. Be patient!
- **Format Issues**: Ensure your chat file matches the expected format
- **Word Analysis**: Stop words are automatically excluded for better insights
- **Export Reports**: Use `-o` flag to save reports for later reference

## 🌟 Support

If you find this tool helpful, please consider giving it a star! ⭐

For issues or questions, please open an issue on the repository.

---

<div align="center">

**Made with ❤️ for chat enthusiasts**

</div>

## Sample Data

A sample chat file is provided in the `data/` directory for testing.

## Contributing

Feel free to contribute by adding support for more chat formats, additional analysis features, or visualizations.

## License

MIT License