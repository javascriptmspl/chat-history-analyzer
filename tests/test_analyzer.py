import unittest
from datetime import datetime
from src.chat_analyzer.parser import ChatParser
from src.chat_analyzer.analyzer import ChatAnalyzer


class TestChatAnalyzer(unittest.TestCase):

    def setUp(self):
        # Sample messages
        self.messages = [
            {'timestamp': datetime(2023, 1, 1, 10, 0, 0), 'user': 'Alice', 'message': 'Hello world'},
            {'timestamp': datetime(2023, 1, 1, 10, 1, 0), 'user': 'Bob', 'message': 'Hi Alice'},
            {'timestamp': '2023-01-01 10:02:00', 'user': 'Alice', 'message': 'How are you?'},
        ]

    def test_message_count(self):
        analyzer = ChatAnalyzer(self.messages)
        counts = analyzer.get_message_count_per_user()
        self.assertEqual(counts['Alice'], 2)
        self.assertEqual(counts['Bob'], 1)

    def test_average_length(self):
        analyzer = ChatAnalyzer(self.messages)
        avg = analyzer.get_average_message_length()
        expected = (11 + 8 + 12) / 3  # lengths of messages
        self.assertAlmostEqual(avg, expected)


if __name__ == '__main__':
    unittest.main()