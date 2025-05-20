import requests
import time
from datetime import datetime

class Notifier:
    def __init__(self, webhook_url, min_interval=3):
        self.webhook_url = webhook_url
        self.last_sent_time = 0
        self.min_interval = min_interval
        self.last_message = None

    def send(self, message, level="NOTIFY"):
        now = time.time()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"**[{level.upper()}] {timestamp}**\n{message}"
        if formatted == self.last_message or (now - self.last_sent_time < self.min_interval):
            return
        response = requests.post(self.webhook_url, json={"content": formatted})
        if response.status_code != 204:
            raise Exception(f"Discord error {response.status_code}: {response.text}")
        self.last_message = formatted
        self.last_sent_time = now

    def formatter(self, data_dict, title="DATA"):
        lines = [f"**{title.upper()} SUMMARY**"]
        for key, value in data_dict.items():
            lines.append(f"> **{key}:** {value}")
        return "\n".join(lines)
