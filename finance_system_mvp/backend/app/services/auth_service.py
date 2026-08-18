from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.repositories.user_repository import create, get_by_email


def register(db: Session, name: str, email: str, password: str):
    if get_by_email(db, email):
        raise HTTPException(status_code=409, detail="E-mail já cadastrado.")

    user = User(
        name=name,
        email=email.lower(),
        password_hash=hash_password(password),
    )
    return create(db, user)


def login(db: Session, email: str, password: str):
    user = get_by_email(db, email.lower())

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
        )

    if not user.status:
        raise HTTPException(status_code=403, detail="Usuário inativo.")

    return create_access_token(str(user.id))
