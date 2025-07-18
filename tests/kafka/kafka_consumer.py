from kafka import KafkaConsumer
import json

class OrderKafkaConsumer:
    def __init__(self, topic, bootstrap_servers="localhost:9092", group_id="test-group"):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

    def get_message(self, user_id: int, timeout_sec: int = 10):
        import time
        end_time = time.time() + timeout_sec
        while time.time() < end_time:
            for message in self.consumer.poll(timeout_ms=1000).values():
                for record in message:
                    value = record.value
                    if value.get("userId") == user_id:
                        return value
            time.sleep(0.5)
        return None