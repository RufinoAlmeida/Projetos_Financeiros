from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.database.models import UserModel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int) -> UserModel | None:
        return self.db.get(UserModel, user_id)

    def get_many_for_update(self, user_ids: list[int]) -> list[UserModel]:
        query = select(UserModel).where(UserModel.id.in_(user_ids)).with_for_update()
        return list(self.db.scalars(query).all())

    def create(self, user: UserModel) -> UserModel:
        self.db.add(user)
        self.db.flush()
        return user
