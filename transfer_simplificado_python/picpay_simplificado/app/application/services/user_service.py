from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.schemas import UserCreateRequest
from app.core.security import hash_password
from app.domain.exceptions.errors import DomainError
from app.infrastructure.database.models import UserModel, WalletModel


class DuplicateUserError(DomainError):
    pass


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, request: UserCreateRequest) -> UserModel:
        user = UserModel(
            name=request.name.strip(),
            document=request.document,
            email=str(request.email).lower(),
            password_hash=hash_password(request.password),
            user_type=request.user_type.value,
        )
        self.db.add(user)
        try:
            self.db.flush()
            self.db.add(WalletModel(user_id=user.id, balance=Decimal("0.00")))
            self.db.flush()
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise DuplicateUserError("Email or document is already registered") from exc
        return user
