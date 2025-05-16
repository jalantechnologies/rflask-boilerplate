from modules.application.errors import AppError


class NotificationNotFoundError(AppError):
    def __init__(self, notification_id: str) -> None:
        super().__init__(
            code="NOTIFICATION_ERR_01",
            http_status_code=404,
            message=f"Notification with id {notification_id} not found.",
        )
