import requests

def send_tele(message):
    token = '6434843338:AAEwIju0jLpN1wHzH8ezBP5ZoMlD2zdU9ng'
    chat_id = '6146643575'
    api = f'https://api.telegram.org/bot{token}/sendMessage'
    requests.post(api, json={'chat_id': chat_id, 'text': message})


send_tele("test")


entrypoint: [ "/usr/bin/mongosh", 'mongosh --eval "rs.initiate({_id: \"myReplicaSet\", members: [{_id: 0, host: \"mongo1\"}, {_id: 1, host: \"mongo2\"}, {_id: 2, host: \"mongo3\"}]})"', 'mongosh --eval "rs.status()"' ]