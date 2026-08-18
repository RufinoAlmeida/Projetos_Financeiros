from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.session import Base, engine
from app.api.routes import auth, categories, accounts, transactions
from app.models import models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance System API",
    version="1.0.0",
    description="MVP de controle de receitas e despesas.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(accounts.router)
app.include_router(transactions.router)


@app.get("/health")
def health():
    return {"status": "ok"}
