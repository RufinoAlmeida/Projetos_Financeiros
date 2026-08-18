import logging

import httpx

from app.core.config import Settings
from app.domain.exceptions.errors import ExternalServiceError

logger = logging.getLogger(__name__)


class NotificationGateway:
    def notify(self, recipient_id: int, amount: str) -> None:
        raise NotImplementedError


class HttpNotificationGateway(NotificationGateway):
    def __init__(self, settings: Settings):
        self.url = settings.notification_url
        self.timeout = settings.http_timeout_seconds

    def notify(self, recipient_id: int, amount: str) -> None:
        payload = {"recipient": recipient_id, "amount": amount}
        try:
            response = httpx.post(self.url, json=payload, timeout=self.timeout)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            logger.warning("notification_service_unavailable recipient=%s", recipient_id)
            raise ExternalServiceError("Notification service is unavailable") from exc
