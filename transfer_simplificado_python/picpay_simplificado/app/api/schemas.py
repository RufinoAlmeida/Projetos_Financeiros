from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.domain.entities.enums import UserType


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    document: str = Field(min_length=5, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    user_type: UserType = UserType.COMMON

    @field_validator("document")
    @classmethod
    def normalize_document(cls, value: str) -> str:
        return "".join(char for char in value if char.isalnum()).upper()


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    document: str
    email: EmailStr
    user_type: UserType


class WalletResponse(BaseModel):
    user_id: int
    balance: Decimal


class TransferRequest(BaseModel):
    value: Decimal = Field(gt=0, decimal_places=2, max_digits=18)
    payer: int = Field(gt=0)
    payee: int = Field(gt=0)

    @field_validator("value")
    @classmethod
    def normalize_value(cls, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"))


class TransferResponse(BaseModel):
    id: int
    status: str
    value: Decimal
    payer: int
    payee: int
    notification: str


class ErrorResponse(BaseModel):
    error: str
    message: str
