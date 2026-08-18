from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.database.models import WalletModel


class WalletRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_for_update(self, user_id: int) -> WalletModel | None:
        query = select(WalletModel).where(WalletModel.user_id == user_id).with_for_update()
        return self.db.scalar(query)

    def create(self, wallet: WalletModel) -> WalletModel:
        self.db.add(wallet)
        self.db.flush()
        return wallet
