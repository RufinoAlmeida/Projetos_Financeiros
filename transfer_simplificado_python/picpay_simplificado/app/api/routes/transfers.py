from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_authorization_gateway, get_db, get_notification_gateway
from app.api.schemas import TransferRequest, TransferResponse
from app.application.services.outbox_service import OutboxService
from app.application.services.transfer_service import TransferService
from app.infrastructure.external.authorization import AuthorizationGateway
from app.infrastructure.external.notification import NotificationGateway
from app.infrastructure.database.session import SessionLocal

router = APIRouter(tags=["Transfers"])


def process_notifications() -> None:
    db = SessionLocal()
    try:
        OutboxService(db, get_notification_gateway()).process_pending()
    finally:
        db.close()


@router.post("/transfer", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
def transfer(
    request: TransferRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    authorization_gateway: AuthorizationGateway = Depends(get_authorization_gateway),
):
    transfer_result = TransferService(db, authorization_gateway).execute(request)
    background_tasks.add_task(process_notifications)

    return TransferResponse(
        id=transfer_result.id,
        status=transfer_result.status,
        value=transfer_result.amount,
        payer=transfer_result.payer_id,
        payee=transfer_result.payee_id,
        notification="queued",
    )
