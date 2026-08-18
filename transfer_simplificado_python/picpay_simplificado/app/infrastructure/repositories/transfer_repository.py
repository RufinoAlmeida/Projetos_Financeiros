from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.database.models import TransferModel


class TransferRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, transfer: TransferModel) -> TransferModel:
        self.db.add(transfer)
        self.db.flush()
        return transfer

    def get(self, transfer_id: int) -> TransferModel | None:
        return self.db.get(TransferModel, transfer_id)


class OutboxRepository:
    def __init__(self, db: Session):
        self.db = db
