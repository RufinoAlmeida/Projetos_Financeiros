import json
import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.domain.entities.enums import OutboxStatus
from app.infrastructure.database.models import OutboxEventModel
from app.infrastructure.external.notification import NotificationGateway

logger = logging.getLogger(__name__)


class OutboxService:
    def __init__(self, db: Session, notification_gateway: NotificationGateway):
        self.db = db
        self.notification_gateway = notification_gateway

    def process_pending(self, limit: int = 20) -> None:
        events = (
            self.db.query(OutboxEventModel)
            .filter(OutboxEventModel.status.in_([OutboxStatus.PENDING.value, OutboxStatus.FAILED.value]))
            .order_by(OutboxEventModel.id)
            .limit(limit)
            .all()
        )
        for event in events:
            payload = json.loads(event.payload)
            try:
                self.notification_gateway.notify(
                    recipient_id=payload["recipient_id"], amount=payload["amount"]
                )
                event.status = OutboxStatus.SENT.value
                event.processed_at = datetime.now(timezone.utc)
                event.last_error = None
            except Exception as exc:
                event.status = OutboxStatus.FAILED.value
                event.attempts += 1
                event.last_error = str(exc)[:1000]
                logger.warning("notification_failed event=%s attempts=%s", event.id, event.attempts)
        self.db.commit()
