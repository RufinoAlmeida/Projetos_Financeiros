from decimal import Decimal

import pytest

from app.api.schemas import TransferRequest
from app.application.services.transfer_service import TransferService
from app.domain.exceptions.errors import (
    AuthorizationDeniedError,
    InsufficientBalanceError,
    MerchantCannotPayError,
    UserNotFoundError,
)
from app.infrastructure.database.models import WalletModel


class Authorizer:
    def __init__(self, result=True):
        self.result = result

    def authorize(self):
        if not self.result:
            raise AuthorizationDeniedError("Transfer was not authorized")
        return True


def test_transfer_moves_money_atomically(db, users):
    payer, payee, _ = users
    result = TransferService(db, Authorizer()).execute(
        TransferRequest(value=Decimal("100.00"), payer=payer.id, payee=payee.id)
    )
    db.refresh(payer.wallet)
    db.refresh(payee.wallet)
    assert result.amount == Decimal("100.00")
    assert payer.wallet.balance == Decimal("100.00")
    assert payee.wallet.balance == Decimal("150.00")


def test_transfer_rejects_insufficient_balance(db, users):
    payer, payee, _ = users
    with pytest.raises(InsufficientBalanceError):
        TransferService(db, Authorizer()).execute(
            TransferRequest(value=Decimal("500.00"), payer=payer.id, payee=payee.id)
        )
    db.refresh(payer.wallet)
    db.refresh(payee.wallet)
    assert payer.wallet.balance == Decimal("200.00")
    assert payee.wallet.balance == Decimal("50.00")


def test_merchant_cannot_pay(db, users):
    _, payee, merchant = users
    with pytest.raises(MerchantCannotPayError):
        TransferService(db, Authorizer()).execute(
            TransferRequest(value=Decimal("10.00"), payer=merchant.id, payee=payee.id)
        )


def test_unauthorized_transfer_does_not_change_balance(db, users):
    payer, payee, _ = users
    with pytest.raises(AuthorizationDeniedError):
        TransferService(db, Authorizer(result=False)).execute(
            TransferRequest(value=Decimal("10.00"), payer=payer.id, payee=payee.id)
        )
    db.refresh(payer.wallet)
    db.refresh(payee.wallet)
    assert payer.wallet.balance == Decimal("200.00")
    assert payee.wallet.balance == Decimal("50.00")


def test_inconsistency_rolls_back_debit(db, users):
    payer, payee, _ = users
    db.delete(payee.wallet)
    db.commit()

    with pytest.raises(UserNotFoundError):
        TransferService(db, Authorizer()).execute(
            TransferRequest(value=Decimal("10.00"), payer=payer.id, payee=payee.id)
        )

    db.refresh(payer.wallet)
    assert payer.wallet.balance == Decimal("200.00")
