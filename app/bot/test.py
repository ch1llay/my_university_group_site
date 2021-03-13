import requests

q = """
{
    "type": "message_new",
    "object": {
        "message": {
            "date": 1615631085,
            "from_id": 159526068,
            "id": 0,
            "out": 0,
            "peer_id": 2000000001,
            "text": "week",
            "conversation_message_id": 115,
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
    "event_id": "7abe0d3c6fc52decf7cd5b6a0ea552687fc8c70d"
}
"""
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
r = requests.post(url, data=q_event)
print(r.text)