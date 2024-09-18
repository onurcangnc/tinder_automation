import requests

TELEGRAM_TOKEN = '7197446465:AAGELtqrZ_C3ZdriAOmPvFiP2foLjQfas0c'
CHAT_ID = '649226694'

def send_test_message():
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': 'This is a test message from your bot',
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Test message sent successfully!")
    else:
        print(f"Failed to send test message: {response.status_code} - {response.text}")

send_test_message()
