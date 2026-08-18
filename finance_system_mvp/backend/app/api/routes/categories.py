from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.session import get_db
from app.models import Category, User
from app.schemas.schemas import CategoryCreate, CategoryOut

router = APIRouter(prefix="/api/categories", tags=["Categorias"])


@router.get("", response_model=list[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return db.scalars(
        select(Category)
        .where(Category.user_id == user.id)
        .order_by(Category.type, Category.name)
    ).all()


@router.post("", response_model=CategoryOut, status_code=201)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if data.type not in {"RECEITA", "DESPESA"}:
        from fastapi import HTTPException
        raise HTTPException(400, "Tipo inválido.")

    category = Category(user_id=user.id, **data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
