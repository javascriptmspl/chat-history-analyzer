from collections import Counter, defaultdict
from typing import List, Dict, Any
from datetime import datetime, timedelta
import re


class ChatAnalyzer:
    """Analyzes parsed chat data and provides insights."""

    def __init__(self, messages: List[Dict[str, Any]]):
        self.messages = messages

    def get_message_count_per_user(self) -> Dict[str, int]:
        """Return the number of messages per user."""
        users = [msg['user'] for msg in self.messages]
        return dict(Counter(users))

    def get_word_frequency(self, top_n: int = 10) -> List[tuple]:
        """Return the most common words across all messages."""
        all_text = ' '.join([msg['message'] for msg in self.messages])
        words = re.findall(r'\b\w+\b', all_text.lower())
        # Remove common stop words (basic list)
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

    def generate_report(self) -> str:
        """Generate a text report of the analysis."""
        msg_count = self.get_message_count_per_user()
        word_freq = self.get_word_frequency()
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