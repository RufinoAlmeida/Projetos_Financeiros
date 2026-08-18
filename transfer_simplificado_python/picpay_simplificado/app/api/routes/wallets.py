from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.api.schemas import WalletResponse
from app.application.services.wallet_service import WalletService

router = APIRouter(prefix="/wallets", tags=["Wallets"])


class DepositRequest(BaseModel):
    amount: Decimal = Field(gt=0, decimal_places=2, max_digits=18)


@router.get("/{user_id}", response_model=WalletResponse)
def get_wallet(user_id: int, db: Session = Depends(get_db)):
    wallet = WalletService(db).get_wallet(user_id)
    return WalletResponse(user_id=user_id, balance=wallet.balance)


@router.post("/{user_id}/deposit", response_model=WalletResponse)
def demo_deposit(user_id: int, request: DepositRequest, db: Session = Depends(get_db)):
    """Demo-only endpoint used to seed wallet balances for the challenge."""
    wallet = WalletService(db).add_balance(user_id, request.amount)
    return WalletResponse(user_id=user_id, balance=wallet.balance)
