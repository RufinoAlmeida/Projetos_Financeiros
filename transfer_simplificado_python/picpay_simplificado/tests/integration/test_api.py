from decimal import Decimal

from fastapi.testclient import TestClient

from app.api.dependencies import get_authorization_gateway
from app.infrastructure.database.models import Base
from app.infrastructure.database.session import engine
from app.main import app


class AlwaysAuthorize:
    def authorize(self):
        return True


app.dependency_overrides[get_authorization_gateway] = lambda: AlwaysAuthorize()
client = TestClient(app)


def test_health():
    assert client.get("/health").status_code == 200
