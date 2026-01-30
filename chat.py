#!/usr/bin/env python3
"""
Chat History Analyzer
A comprehensive tool to analyze chat history files and provide insights.
Supports WhatsApp-like chat formats.
"""

import re
import argparse
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple

try:
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Rich library not found. Install with: pip install rich")
    print("Falling back to plain text output.")

class ChatParser:
    """Parses chat history files into structured data."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse(self) -> List[Dict[str, Any]]:
        """Parse the chat file and return a list of message dictionaries."""
        messages = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

        # Regex pattern for WhatsApp-like format: [DD/MM/YY, HH:MM:SS] User: Message
        pattern = r'\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}:\d{2})\] ([^:]+): (.+)'
        matches = re.findall(pattern, content, re.MULTILINE)

        for match in matches:
            date_str, time_str, user, message = match
            try:
                # Parse date and time
                datetime_str = f"{date_str} {time_str}"
                # Assume format DD/MM/YY
                dt = datetime.strptime(datetime_str, "%d/%m/%y %H:%M:%S")
                messages.append({
                    'timestamp': dt,
                    'user': user.strip(),
                    'message': message.strip()
                })
            except ValueError:
                # Skip invalid lines
                continue

        return messages

class ChatAnalyzer:
    """Analyzes parsed chat data and provides insights."""

    def __init__(self, messages: List[Dict[str, Any]]):
        self.messages = messages

    def get_message_count_per_user(self) -> Dict[str, int]:
        """Return the number of messages per user."""
        users = [msg['user'] for msg in self.messages]
        return dict(Counter(users))

    def get_word_frequency(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Return the most common words across all messages."""
        all_text = ' '.join([msg['message'] for msg in self.messages])
        words = re.findall(r'\b\w+\b', all_text.lower())
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'this', 'that', 'these', 'those'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        return Counter(filtered_words).most_common(top_n)

    def get_messages_per_day(self) -> Dict[str, int]:
        """Return the number of messages per day."""
        days = [msg['timestamp'].date().isoformat() for msg in self.messages]
        return dict(Counter(days))

    def get_average_message_length(self) -> float:
        """Return the average message length in characters."""
        lengths = [len(msg['message']) for msg in self.messages]
        return sum(lengths) / len(lengths) if lengths else 0

    def get_user_activity_over_time(self) -> Dict[str, List[int]]:
        """Return user activity (message count) per hour of day."""
        activity = defaultdict(lambda: [0] * 24)
        for msg in self.messages:
            hour = msg['timestamp'].hour
            activity[msg['user']][hour] += 1
        return dict(activity)

    def generate_report(self, top_words: int = 10) -> str:
        """Generate a text report of the analysis."""
        msg_count = self.get_message_count_per_user()
        word_freq = self.get_word_frequency(top_words)
        avg_len = self.get_average_message_length()
        total_msgs = len(self.messages)

        report = f"""
Chat Analysis Report
====================

Total Messages: {total_msgs}
Average Message Length: {avg_len:.2f} characters

Messages per User:
"""
        for user, count in sorted(msg_count.items(), key=lambda x: x[1], reverse=True):
            report += f"- {user}: {count}\n"

        report += "\nTop Words:\n"
        for word, count in word_freq:
            report += f"- {word}: {count}\n"

        return report

def display_results_rich(analyzer: ChatAnalyzer, top_words: int):
    """Display results using Rich library for beautiful formatting."""
    console = Console()

    console.print("[bold blue]Chat History Analyzer[/bold blue]\n")

    # Message count table
    msg_count = analyzer.get_message_count_per_user()
    table = Table(title="Messages per User")
    table.add_column("User", style="cyan")
    table.add_column("Count", style="magenta")
    for user, count in sorted(msg_count.items(), key=lambda x: x[1], reverse=True):
        table.add_row(user, str(count))
    console.print(table)

    # Top words
    word_freq = analyzer.get_word_frequency(top_words)
    table = Table(title=f"Top {top_words} Words")
    table.add_column("Word", style="cyan")
    table.add_column("Frequency", style="magenta")
    for word, freq in word_freq:
        table.add_row(word, str(freq))
    console.print(table)

    # Stats
    avg_len = analyzer.get_average_message_length()
    console.print(f"\n[green]Total Messages:[/green] {len(analyzer.messages)}")
    console.print(f"[green]Average Message Length:[/green] {avg_len:.2f} characters")

def display_results_plain(analyzer: ChatAnalyzer, top_words: int):
    """Display results in plain text."""
    print("Chat History Analyzer\n")

    # Message count
    msg_count = analyzer.get_message_count_per_user()
    print("Messages per User:")
    for user, count in sorted(msg_count.items(), key=lambda x: x[1], reverse=True):
        print(f"- {user}: {count}")

    # Top words
    word_freq = analyzer.get_word_frequency(top_words)
    print(f"\nTop {top_words} Words:")
    for word, freq in word_freq:
        print(f"- {word}: {freq}")

    # Stats
    avg_len = analyzer.get_average_message_length()
    print(f"\nTotal Messages: {len(analyzer.messages)}")
    print(f"Average Message Length: {avg_len:.2f} characters")

def main():
    parser = argparse.ArgumentParser(
        description="Analyze chat history files and provide insights.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python chat.py chat.txt
  python chat.py chat.txt --output report.txt --top-words 20

Supported format: [DD/MM/YY, HH:MM:SS] User: Message
        """
    )
    parser.add_argument('file', help="Path to the chat history file")
    parser.add_argument('--output', '-o', help="Output file for the report", default=None)
    parser.add_argument('--top-words', '-w', type=int, default=10,
                       help="Number of top words to show (default: 10)")

    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    # Parse the chat
    chat_parser = ChatParser(str(file_path))
    messages = chat_parser.parse()

    if not messages:
        print("No messages found in the file. Check the format.")
        print("Expected format: [DD/MM/YY, HH:MM:SS] User: Message")
        sys.exit(1)

    # Analyze
    analyzer = ChatAnalyzer(messages)

    # Display results
    if RICH_AVAILABLE:
        display_results_rich(analyzer, args.top_words)
    else:
        display_results_plain(analyzer, args.top_words)

    # Generate report
    report = analyzer.generate_report(args.top_words)
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"\nReport saved to '{args.output}'")
        except Exception as e:
            print(f"Error saving report: {e}")
    else:
        print("\nFull Report:")
        print(report)

if __name__ == "__main__":
    main()
