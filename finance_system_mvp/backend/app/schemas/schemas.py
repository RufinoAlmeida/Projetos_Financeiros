from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    status: bool


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: str
    description: str | None = None


class CategoryOut(CategoryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    status: bool


class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    bank: str | None = None
    type: str
    initial_balance: Decimal = Decimal("0")


class AccountOut(AccountCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    status: bool


class TransactionCreate(BaseModel):
    description: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0)
    type: str
    transaction_date: date
    due_date: date | None = None
    status: str = "PAGO"
    payment_method: str | None = None
    notes: str | None = None
    category_id: int | None = None
    account_id: int | None = None


class TransactionOut(TransactionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int


class DashboardOut(BaseModel):
    receitas: Decimal
    despesas: Decimal
    saldo: Decimal
    pendentes: Decimal
