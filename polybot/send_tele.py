import requests

def send_tele(message):
    token = 'TOKEN'
    chat_id = 'CHAT ID'
    api = f'https://api.telegram.org/bot{token}/sendMessage'
    requests.post(api, json={'chat_id': chat_id, 'text': message})


send_tele('Message')


