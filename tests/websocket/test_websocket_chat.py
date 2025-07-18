import json
import time
import uuid
from queue import Queue, Empty
import pytest
import stomp

WS_URL = "ws://localhost:8080/ws-live/websocket"
SEND_DESTINATION = "/app/chat.send"
SUBSCRIBE_DESTINATION = "/topic/messages"


class StompTestListener(stomp.ConnectionListener):
    def __init__(self, q: Queue):
        self.q = q

    def on_message(self, headers, body):
        try:
            self.q.put(json.loads(body))
        except Exception as e:
            print("Parse error:", e)

    def on_error(self, headers, body):
        print("STOMP error:", body)

    def on_disconnected(self):
        print("STOMP disconnected")


def connect_stomp_client(jwt: str) -> stomp.WSStompConnection:
    """
    ВАЖНО: передаём WebSocket-URL целиком через параметр ws=[...]
    """
    conn = stomp.WSStompConnection(ws=[WS_URL])
    conn.connect(wait=True, headers={"Authorization": f"Bearer {jwt}"})
    return conn


@pytest.mark.timeout(30)
def test_user1_sends_multiple_messages_user2_receives_all(random_user):
    user1 = random_user(user_type="seller")
    user2 = random_user(user_type="customer")

    received = Queue()

    # user2 подключается и подписывается
    conn2 = connect_stomp_client(user2.token)
    listener2 = StompTestListener(received)
    conn2.set_listener("user2", listener2)
    conn2.subscribe(
        destination=SUBSCRIBE_DESTINATION,
        id=f"sub-{uuid.uuid4()}",
        ack="auto"
    )
    time.sleep(0.5)

    # user1 подключается и отправляет сообщения
    conn1 = connect_stomp_client(user1.token)

    contents = ["Message 1", "Message 2", "Message 3"]
    for content in contents:
        payload = {
            "senderId": user1.user.id,
            "receiverId": user2.user.id,
            "content": content
        }
        conn1.send(
            destination=SEND_DESTINATION,
            body=json.dumps(payload),
            headers={"content-type": "application/json"}
        )
        time.sleep(0.2)

    # Ждём и проверяем сообщения
    msgs = []
    for _ in contents:
        try:
            msgs.append(received.get(timeout=5))
        except Empty:
            pytest.fail("Message not received in time")

    assert [m["content"] for m in msgs] == contents

    conn1.disconnect()
    conn2.disconnect()