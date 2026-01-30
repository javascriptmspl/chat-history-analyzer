"""
Chat History Analyzer - Analyzer Module
Performs various analyses on parsed chat data.
"""

import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False


class ChatAnalyzer:
    """
    Analyzes parsed chat data and provides various insights.
    """

    def __init__(self, messages: List[Dict[str, Any]]):
        """
        Initialize analyzer with parsed messages.

        Args:
            messages: List of message dictionaries
        """
        self.messages = messages
        self._validate_messages()

    def _validate_messages(self) -> None:
        """Validate that messages have required fields."""
        required_keys = {'sender', 'timestamp', 'message'}
        for msg in self.messages:
            if not isinstance(msg, dict):
                raise ValueError("Each message must be a dictionary")
            if not required_keys.issubset(msg.keys()):
                raise ValueError(f"Message missing required keys: {required_keys - msg.keys()}")

    def get_total_messages_per_user(self) -> Dict[str, int]:
        """
        Calculate total messages per user.

        Returns:
            Dictionary mapping sender names to message counts
        """
        senders = [msg['sender'] for msg in self.messages]
        return dict(Counter(senders))

    def get_messages_per_day(self) -> Dict[str, int]:
        """
        Calculate messages per day.

        Returns:
            Dictionary mapping date strings (YYYY-MM-DD) to message counts
        """
        days = [msg['timestamp'].date().isoformat() for msg in self.messages]
        return dict(Counter(days))

    def get_messages_per_hour(self) -> Dict[int, int]:
        """
        Calculate messages per hour of day (0-23).

        Returns:
            Dictionary mapping hour (0-23) to message counts
        """
        hours = [msg['timestamp'].hour for msg in self.messages]
        return dict(Counter(hours))

    def get_most_common_words(self, top_n: int = 10, ignore_stopwords: bool = True) -> List[Tuple[str, int]]:
        """
        Find most common words across all messages.

        Args:
            top_n: Number of top words to return
            ignore_stopwords: Whether to exclude common stopwords

        Returns:
            List of (word, frequency) tuples
        """
        all_text = ' '.join([msg['message'] for msg in self.messages])
        words = re.findall(r'\b\w+\b', all_text.lower())

        if ignore_stopwords:
            stopwords = self._get_stopwords()
            words = [word for word in words if word not in stopwords and len(word) > 2]

        return Counter(words).most_common(top_n)

    def _get_stopwords(self) -> set:
        """Get set of common English stopwords."""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'i', 'you', 'he',
            'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his',
            'its', 'our', 'their', 'this', 'that', 'these', 'those'
        }

    def get_emoji_usage_frequency(self) -> List[Tuple[str, int]]:
        """
        Calculate emoji usage frequency.

        Returns:
            List of (emoji, frequency) tuples, sorted by frequency
        """
        all_text = ' '.join([msg['message'] for msg in self.messages])

        # Emoji regex pattern (basic implementation)
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002700-\U000027BF"  # dingbats
            "\U0001f926-\U0001f937"  # gestures
            "\U00010000-\U0010ffff"  # other unicode
            "\u2640-\u2642"  # gender symbols
            "\u2600-\u2B55"  # misc symbols
            "\u200d"  # zero width joiner
            "\u23cf"  # eject symbol
            "\u23e9"  # fast forward
            "\u231a"  # watch
            "\ufe0f"  # variation selector
            "\u3030"  # wavy dash
            "]+",
            flags=re.UNICODE
        )

        emojis = emoji_pattern.findall(all_text)
        return sorted(Counter(emojis).items(), key=lambda x: x[1], reverse=True)

    def get_sentiment_analysis(self) -> Dict[str, Dict[str, Any]]:
        """
        Perform sentiment analysis on messages.

        Returns:
            Dictionary with overall sentiment stats and per-user breakdown
        """
        if not TEXTBLOB_AVAILABLE:
            return {"error": "TextBlob not available. Install with: pip install textblob"}

        sentiments = []
        user_sentiments = defaultdict(list)

        for msg in self.messages:
            blob = TextBlob(msg['message'])
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity

            sentiment_data = {
                'polarity': polarity,
                'subjectivity': subjectivity,
                'sentiment': self._classify_sentiment(polarity)
            }

            sentiments.append(sentiment_data)
            user_sentiments[msg['sender']].append(sentiment_data)

        # Overall stats
        overall = {
            'total_messages': len(sentiments),
            'average_polarity': sum(s['polarity'] for s in sentiments) / len(sentiments) if sentiments else 0,
            'average_subjectivity': sum(s['subjectivity'] for s in sentiments) / len(sentiments) if sentiments else 0,
            'sentiment_distribution': self._get_sentiment_distribution(sentiments)
        }

        # Per-user stats
        per_user = {}
        for user, user_sents in user_sentiments.items():
            per_user[user] = {
                'message_count': len(user_sents),
                'average_polarity': sum(s['polarity'] for s in user_sents) / len(user_sents),
                'average_subjectivity': sum(s['subjectivity'] for s in user_sents) / len(user_sents),
                'sentiment_distribution': self._get_sentiment_distribution(user_sents)
            }

        return {
            'overall': overall,
            'per_user': per_user
        }

    def _classify_sentiment(self, polarity: float) -> str:
        """Classify sentiment based on polarity score."""
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'

    def _get_sentiment_distribution(self, sentiments: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get distribution of sentiment classes."""
        classes = [s['sentiment'] for s in sentiments]
        return dict(Counter(classes))

    def get_longest_and_shortest_messages(self) -> Dict[str, Any]:
        """
        Find longest and shortest messages.

        Returns:
            Dictionary with longest and shortest message details
        """
        if not self.messages:
            return {'longest': None, 'shortest': None}

        sorted_by_length = sorted(self.messages, key=lambda x: len(x['message']))

        return {
            'longest': {
                'sender': sorted_by_length[-1]['sender'],
                'timestamp': sorted_by_length[-1]['timestamp'],
                'message': sorted_by_length[-1]['message'],
                'length': len(sorted_by_length[-1]['message'])
            },
            'shortest': {
                'sender': sorted_by_length[0]['sender'],
                'timestamp': sorted_by_length[0]['timestamp'],
                'message': sorted_by_length[0]['message'],
                'length': len(sorted_by_length[0]['message'])
            }
        }

    def get_basic_stats(self) -> Dict[str, Any]:
        """
        Get basic statistics about the chat.

        Returns:
            Dictionary with various basic statistics
        """
        if not self.messages:
            return {}

        timestamps = [msg['timestamp'] for msg in self.messages]
        message_lengths = [len(msg['message']) for msg in self.messages]

        return {
            'total_messages': len(self.messages),
            'unique_senders': len(set(msg['sender'] for msg in self.messages)),
            'date_range': {
                'start': min(timestamps),
                'end': max(timestamps)
            },
            'average_message_length': sum(message_lengths) / len(message_lengths),
            'total_words': sum(len(re.findall(r'\b\w+\b', msg['message'])) for msg in self.messages)
        }