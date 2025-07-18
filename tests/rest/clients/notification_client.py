from .rest_client import RestClient
from tests.rest.models.models import NotificationDto
from typing import List, Optional

class NotificationApiClient:
    def __init__(self, base_url: str = "http://localhost:8080", token: Optional[str] = None):
        self.rest = RestClient(base_url, token)

    def get_notifications(self) -> List[NotificationDto]:
        return self.rest.get_list("/api/notifications", NotificationDto, paginated=True)

    def delete_all_notifications(self):
        return self.rest.delete("/api/notifications")

    def read_notification(self, notification_id: int):
        return self.rest.patch(f"/api/notifications/{notification_id}/read")

    def read_all_notifications(self):
        return self.rest.patch("/api/notifications/read-all") 