import time
from typing import Optional, Dict, Any

from kafka import KafkaConsumer
import json

class OrderKafkaConsumer:
    def __init__(
        self,
        topic: str,
        bootstrap_servers: str = "localhost:9092",
        group_id: str = "test-group",
    ) -> None:
        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode()),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )

    def get_message(
        self,
        *,
        user_id: int,
        timeout: int = 10,
    ) -> Optional[Dict[str, Any]]:
        """Poll until a message with matching userId arrives or timeout."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            for records in self._consumer.poll(timeout_ms=1000).values():
                for record in records:
                    if record.value.get("userId") == user_id:
                        return record.value
        return None

    def close(self) -> None:
        self._consumer.close()