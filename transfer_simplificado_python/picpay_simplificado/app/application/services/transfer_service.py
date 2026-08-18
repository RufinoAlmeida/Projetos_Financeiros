import json
import logging
from decimal import Decimal

from sqlalchemy.orm import Session

from app.api.schemas import TransferRequest
from app.domain.entities.enums import OutboxStatus, TransferStatus, UserType
from app.domain.exceptions.errors import (
    AuthorizationDeniedError,
    InsufficientBalanceError,
    InvalidTransferError,
    MerchantCannotPayError,
    UserNotFoundError,
)
from app.infrastructure.database.models import OutboxEventModel, TransferModel, UserModel, WalletModel
from app.infrastructure.external.authorization import AuthorizationGateway

logger = logging.getLogger(__name__)


class TransferService:
    def __init__(self, db: Session, authorization_gateway: AuthorizationGateway):
        self.db = db
        self.authorization_gateway = authorization_gateway

    def execute(self, request: TransferRequest) -> TransferModel:
        if request.payer == request.payee:
            raise InvalidTransferError("Payer and payee must be different")

        # Authorization is deliberately outside the DB transaction: a slow external
        # service should not keep financial rows locked unnecessarily.
        self.authorization_gateway.authorize()

        try:
            with self.db.begin():
                users = list(
                    self.db.query(UserModel)
                    .filter(UserModel.id.in_([request.payer, request.payee]))
                    .with_for_update()
                    .all()
                )
                users_by_id = {user.id: user for user in users}

                payer = users_by_id.get(request.payer)
                payee = users_by_id.get(request.payee)
                if not payer or not payee:
                    raise UserNotFoundError("Payer or payee not found")

                if payer.user_type == UserType.MERCHANT.value:
                    raise MerchantCannotPayError("Merchant users cannot send money")

                payer_wallet = (
                    self.db.query(WalletModel)
                    .filter(WalletModel.user_id == payer.id)
                    .with_for_update()
                    .one_or_none()
                )
                payee_wallet = (
                    self.db.query(WalletModel)
                    .filter(WalletModel.user_id == payee.id)
                    .with_for_update()
                    .one_or_none()
                )
                if not payer_wallet or not payee_wallet:
                    raise UserNotFoundError("Payer or payee wallet not found")

                amount = request.value.quantize(Decimal("0.01"))
                if payer_wallet.balance < amount:
                    raise InsufficientBalanceError("Insufficient balance")

                payer_wallet.balance -= amount
                payee_wallet.balance += amount

                transfer = TransferModel(
                    payer_id=payer.id,
                    payee_id=payee.id,
                    amount=amount,
                    status=TransferStatus.COMPLETED.value,
                )
                self.db.add(transfer)
                self.db.flush()

                event = OutboxEventModel(
                    event_type="transfer.completed",
                    aggregate_id=transfer.id,
                    payload=json.dumps(
                        {"transfer_id": transfer.id, "recipient_id": payee.id, "amount": str(amount)}
                    ),
                    status=OutboxStatus.PENDING.value,
                )
                self.db.add(event)
                self.db.flush()

                return transfer
        except Exception:
            logger.exception("transfer_failed payer=%s payee=%s", request.payer, request.payee)
            raise
