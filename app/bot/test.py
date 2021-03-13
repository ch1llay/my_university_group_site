import requests

q = '''
{
    "type": "message_new",
    "object": {
        "message": {
            "date": 1615632545,
            "from_id": 159526068,
            "id": 0,
            "out": 0,
            "peer_id": 2000000001,
            "text": "Меню",
            "conversation_message_id": 141,
            "fwd_messages": [],
            "important": false,
            "random_id": 0,
            "attachments": [],
            "is_hidden": false
        },
        "client_info": {
            "button_actions": [
                "text",
                "vkpay",
                "open_app",
                "location",
                "open_link",
                "callback",
                "intent_subscribe",
                "intent_unsubscribe"
            ],
            "keyboard": true,
            "inline_keyboard": true,
            "carousel": false,
            "lang_id": 0
        }
    },
    "group_id": 203076503,
    "event_id": "f2c0942a3fd9b1e9567495f8759af64d2d6e88d0"
}
'''.encode("utf-8")
q_event = """
{
    "type": "message_event",
    "object": {
        "user_id": 159526068,
        "peer_id": 2000000001,
        "event_id": "1776a756b921",
        "payload": {
            "payload": "week"
        },
        "conversation_message_id": 130
    },
    "group_id": 203076503,
    "event_id": "9f5a072b366f9529355236c6704e2465c9da9903"
}
"""
url = "http://127.0.0.1:5000/"
r = requests.post(url, data=q)
print(r.text)