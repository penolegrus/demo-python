# import json
# import time
# import uuid
# from queue import Queue, Empty
#
# import pytest
# import stomp
#
# WS_URL = "ws://localhost:8080/ws-live/websocket"
# SEND_DESTINATION = "/app/chat.send"
# SUBSCRIBE_DESTINATION = "/topic/messages"
#
#
# class StompListener(stomp.ConnectionListener):
#     def __init__(self, q: Queue) -> None:
#         self.q = q
#
#     def on_message(self, headers, body):
#         try:
#             self.q.put(json.loads(body))
#         except Exception as e:
#             print("Parse error:", e)
#
#     def on_error(self, headers, body):
#         print("STOMP error:", body)
#
#     def on_disconnected(self):
#         print("STOMP disconnected")
#
#
# def stomp_connection(jwt: str) -> stomp.WSStompConnection:
#     conn = stomp.WSStompConnection(ws=[WS_URL])
#     conn.connect(
#         wait=True,
#         headers={
#             "Authorization": f"Bearer {jwt}",
#             "accept-version": "1.2"
#         }
#     )
#     return conn
#
#
# @pytest.mark.timeout(30)
# def test_user1_sends_multiple_messages_user2_receives_all(random_user):
#     user1 = random_user(user_type="seller")
#     user2 = random_user(user_type="customer")
#
#     inbox = Queue()
#
#     # user2: подключение + подписка
#     conn2 = stomp_connection(user2.token)
#     listener2 = StompListener(inbox)
#     conn2.set_listener("", listener2)
#     conn2.subscribe(destination=SUBSCRIBE_DESTINATION, id=str(uuid.uuid4()), ack="auto")
#
#     # user1: подключение
#     conn1 = stomp_connection(user1.token)
#
#     contents = ["Message 1", "Message 2", "Message 3"]
#     for text in contents:
#         conn1.send(
#             destination=SEND_DESTINATION,
#             body=json.dumps({
#                 "senderId": user1.user.id,
#                 "receiverId": user2.user.id,
#                 "content": text
#             }),
#             headers={
#                 "content-type": "application/json",
#                 "content-length": str(len(json.dumps({"senderId": user1.user.id, "receiverId": user2.user.id, "content": text})))
#             }
#         )
#         time.sleep(0.2)
#
#     # получение
#     received = [inbox.get(timeout=5) for _ in contents]
#     assert [m["content"] for m in received] == contents
#
#     conn1.disconnect()
#     conn2.disconnect()
#     # закрыть underlying socket
#     conn1.transport.close()
#     conn2.transport.close()