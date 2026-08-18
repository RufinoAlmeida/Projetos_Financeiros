from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Account, Category, Transaction


VALID_TYPES = {"RECEITA", "DESPESA"}
VALID_STATUS = {"PAGO", "PENDENTE", "VENCIDO", "CANCELADO"}


def validate_transaction(db: Session, user_id: int, data):
    if data.type not in VALID_TYPES:
        raise ValueError("Tipo deve ser RECEITA ou DESPESA.")
    if data.status not in VALID_STATUS:
        raise ValueError("Status inválido.")

    if data.category_id:
        category = db.scalar(
            select(Category).where(
                Category.id == data.category_id,
                Category.user_id == user_id,
            )
        )
        if not category:
            raise ValueError("Categoria não encontrada.")
        if category.type != data.type:
            raise ValueError("A categoria não pertence ao tipo da transação.")

    if data.account_id:
        account = db.scalar(
            select(Account).where(
                Account.id == data.account_id,
                Account.user_id == user_id,
            )
        )
        if not account:
            raise ValueError("Conta não encontrada.")


def create_transaction(db: Session, user_id: int, data):
    validate_transaction(db, user_id, data)
    tx = Transaction(user_id=user_id, **data.model_dump())
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def dashboard(db: Session, user_id: int):
    receita = db.scalar(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user_id,
            Transaction.type == "RECEITA",
            Transaction.status != "CANCELADO",
        )
    )
    despesa = db.scalar(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user_id,
            Transaction.type == "DESPESA",
            Transaction.status != "CANCELADO",
        )
    )
    pendente = db.scalar(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user_id,
            Transaction.status == "PENDENTE",
        )
    )
    receita = Decimal(str(receita or 0))
    despesa = Decimal(str(despesa or 0))
    pendente = Decimal(str(pendente or 0))
    return {
        "receitas": receita,
        "despesas": despesa,
        "saldo": receita - despesa,
        "pendentes": pendente,
    }
