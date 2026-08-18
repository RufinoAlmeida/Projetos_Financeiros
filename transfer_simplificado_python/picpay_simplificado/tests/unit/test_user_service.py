from app.api.schemas import UserCreateRequest
from app.application.services.user_service import UserService
from app.core.security import verify_password
from app.domain.entities.enums import UserType


def test_password_is_hashed(db):
    user = UserService(db).create_user(
        UserCreateRequest(
            name="Amador Almeida",
            document="12345678909",
            email="amador@example.com",
            password="Senha@123",
            user_type=UserType.COMMON,
        )
    )
    assert user.password_hash != "Senha@123"
    assert verify_password("Senha@123", user.password_hash)
