from app.infrastructure.database.models import Base
from app.infrastructure.database.session import engine


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
