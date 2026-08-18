from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.session import get_db
from app.models import Account, User
from app.schemas.schemas import AccountCreate, AccountOut

router = APIRouter(prefix="/api/accounts", tags=["Contas"])


@router.get("", response_model=list[AccountOut])
def list_accounts(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return db.scalars(
        select(Account).where(Account.user_id == user.id)
    ).all()


@router.post("", response_model=AccountOut, status_code=201)
def create_account(
    data: AccountCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    account = Account(user_id=user.id, **data.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account
