from decimal import Decimal

from sqlalchemy.orm import Session

from app.domain.exceptions.errors import UserNotFoundError
from app.infrastructure.database.models import UserModel, WalletModel


class WalletService:
    def __init__(self, db: Session):
        self.db = db

    def get_wallet(self, user_id: int) -> WalletModel:
        user = self.db.get(UserModel, user_id)
        if not user:
            raise UserNotFoundError("User not found")
        if not user.wallet:
            wallet = WalletModel(user_id=user_id, balance=Decimal("0.00"))
            self.db.add(wallet)
            self.db.commit()
            return wallet
        return user.wallet

    def add_balance(self, user_id: int, amount: Decimal) -> WalletModel:
        wallet = self.db.query(WalletModel).filter(WalletModel.user_id == user_id).with_for_update().first()
        if not wallet:
            raise UserNotFoundError("Wallet not found")
        wallet.balance += amount
        self.db.commit()
        self.db.refresh(wallet)
        return wallet
