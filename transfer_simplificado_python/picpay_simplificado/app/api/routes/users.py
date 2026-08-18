from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.schemas import UserCreateRequest, UserResponse
from app.api.dependencies import get_db
from app.application.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreateRequest, db: Session = Depends(get_db)):
    return UserService(db).create_user(request)
