import requests

q = """
{
    "type": "message_new",
    "object": {
        "message": {
            "date": 1615572070,
            "from_id": 159526068,
            "id": 0,
            "out": 0,
            "peer_id": 2000000001,
            "text": "week",
            "conversation_message_id": 66,
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
    "event_id": "d4d6d10056b9e679f679c2677013cc60ca740967"
}
"""
q_event = """
{
    "type": "message_event",
    "object": {
        "user_id": 159526068,
        "peer_id": 2000000001,
        "event_id": "b483a4d72f40",
        "payload": {
            "payload": "week"
        },
        "conversation_message_id": 62
    },
    "group_id": 203076503,
    "event_id": "50a24d0f1c8f3d3a4132e34e2651877514e850cd"
}
"""
url = "http://127.0.0.1:5000/"
r = requests.post(url, data=q)
print(r.text)