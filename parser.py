"""
Chat History Analyzer - Parser Module
Handles parsing of chat history files in .txt and .json formats.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class ChatParser:
    """
    Parses chat history files into structured message data.

    Supports:
    - .txt files (WhatsApp-like format)
    - .json files (structured format)
    """

    def __init__(self, file_path: str):
        """
        Initialize the parser with a file path.

        Args:
            file_path: Path to the chat history file
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def parse(self) -> List[Dict[str, Any]]:
        """
        Parse the chat file and return structured message data.

        Returns:
            List of message dictionaries with keys: sender, timestamp, message

        Raises:
            ValueError: If file format is unsupported or parsing fails
        """
        if self.file_path.suffix.lower() == '.txt':
            return self._parse_txt()
        elif self.file_path.suffix.lower() == '.json':
            return self._parse_json()
        else:
            raise ValueError(f"Unsupported file format: {self.file_path.suffix}")

    def _parse_txt(self) -> List[Dict[str, Any]]:
        """
        Parse WhatsApp-like .txt format.

        Expected format: [DD/MM/YY, HH:MM:SS] Sender: Message
        """
        messages = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            raise ValueError(f"Error reading file: {e}")

        # Regex pattern for WhatsApp format
        pattern = r'\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}:\d{2})\] ([^:]+): (.+)'
        matches = re.findall(pattern, content, re.MULTILINE)

        for match in matches:
            date_str, time_str, sender, message = match
            try:
                # Parse timestamp
                datetime_str = f"{date_str} {time_str}"
                # Try different date formats
                for fmt in ["%d/%m/%y %H:%M:%S", "%d/%m/%Y %H:%M:%S"]:
                    try:
                        timestamp = datetime.strptime(datetime_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # Skip invalid timestamps
                    continue

                messages.append({
                    'sender': sender.strip(),
                    'timestamp': timestamp,
                    'message': message.strip()
                })
            except Exception:
                # Skip malformed lines
                continue

        return messages

    def _parse_json(self) -> List[Dict[str, Any]]:
        """
        Parse .json format.

        Expected format: List of objects with keys: sender, timestamp, message
        timestamp can be ISO string or unix timestamp
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        except Exception as e:
            raise ValueError(f"Error reading JSON file: {e}")

        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list of messages")

        messages = []
        for item in data:
            if not isinstance(item, dict):
                continue

            # Extract required fields
            sender = item.get('sender')
            timestamp_raw = item.get('timestamp')
            message = item.get('message')

            if not all([sender, timestamp_raw, message]):
                continue

            # Parse timestamp
            timestamp = self._parse_timestamp(timestamp_raw)
            if timestamp is None:
                continue

            messages.append({
                'sender': str(sender).strip(),
                'timestamp': timestamp,
                'message': str(message).strip()
            })

        return messages

    def _parse_timestamp(self, timestamp_raw: Any) -> Optional[datetime]:
        """
        Parse timestamp from various formats.

        Args:
            timestamp_raw: Timestamp in string, int, or float format

        Returns:
            datetime object or None if parsing fails
        """
        if isinstance(timestamp_raw, str):
            # Try ISO format first
            try:
                return datetime.fromisoformat(timestamp_raw.replace('Z', '+00:00'))
            except ValueError:
                pass

            # Try common formats
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%d/%m/%Y %H:%M:%S",
                "%m/%d/%Y %H:%M:%S"
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(timestamp_raw, fmt)
                except ValueError:
                    continue

        elif isinstance(timestamp_raw, (int, float)):
            # Unix timestamp
            try:
                return datetime.fromtimestamp(timestamp_raw)
            except (ValueError, OSError):
                pass

        return None