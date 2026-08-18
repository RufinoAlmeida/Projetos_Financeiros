from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database.models import Base, UserModel, WalletModel


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def users(db):
    payer = UserModel(
        name="Payer", document="11111111111", email="payer@example.com", password_hash="hash", user_type="common"
    )
    payee = UserModel(
        name="Payee", document="22222222222", email="payee@example.com", password_hash="hash", user_type="common"
    )
    merchant = UserModel(
        name="Merchant", document="33333333333333", email="merchant@example.com", password_hash="hash", user_type="merchant"
    )
    db.add_all([payer, payee, merchant])
    db.flush()
    db.add_all([
        WalletModel(user_id=payer.id, balance=Decimal("200.00")),
        WalletModel(user_id=payee.id, balance=Decimal("50.00")),
        WalletModel(user_id=merchant.id, balance=Decimal("100.00")),
    ])
    db.commit()
    return payer, payee, merchant
