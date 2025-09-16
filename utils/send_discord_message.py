import requests
from config import config

def send_discord_message(message):
    data = {
        "content": message
    }
    response = requests.post(config().get('WEBHOOK_URL'), json=data)

    if response.status_code != 204:
        print(f"Failed to send message. Status code: {response.status_code}")
