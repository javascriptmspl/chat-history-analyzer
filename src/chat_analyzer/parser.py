import re
from datetime import datetime
from typing import List, Dict, Any


class ChatParser:
    """Parses chat history files into structured data."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse(self) -> List[Dict[str, Any]]:
        """Parse the chat file and return a list of message dictionaries."""
        messages = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()

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