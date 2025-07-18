from .base_client import HttpClient

from tests.rest.models.models import NotificationDto


class NotificationApiClient(HttpClient):
    def get_notifications(self) -> list[NotificationDto]:
        return self.get_list_("/api/notifications", model=NotificationDto)

    def read_notification(self, notification_id: int) -> None:
        self.patch_(f"/api/notifications/{notification_id}/read")

    def read_all_notifications(self) -> None:
        self.patch_("/api/notifications/read-all")

    def delete_all_notifications(self) -> None:
        self.delete_("/api/notifications")