from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.session import get_db
from app.models import Transaction, User
from app.schemas.schemas import DashboardOut, TransactionCreate, TransactionOut
from app.services.transaction_service import create_transaction, dashboard

router = APIRouter(prefix="/api/transactions", tags=["Transações"])


@router.get("", response_model=list[TransactionOut])
def list_transactions(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return db.scalars(
        select(Transaction)
        .where(Transaction.user_id == user.id)
        .order_by(Transaction.transaction_date.desc(), Transaction.id.desc())
    ).all()


@router.post("", response_model=TransactionOut, status_code=201)
def create(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        return create_transaction(db, user.id, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{transaction_id}", status_code=204)
def delete(
    transaction_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    tx = db.scalar(
        select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user.id,
        )
    )
    if not tx:
        raise HTTPException(404, "Transação não encontrada.")
    db.delete(tx)
    db.commit()


@router.get("/dashboard", response_model=DashboardOut)
def get_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return dashboard(db, user.id)
