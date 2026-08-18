from enum import StrEnum


class UserType(StrEnum):
    COMMON = "common"
    MERCHANT = "merchant"


class TransferStatus(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"


class OutboxStatus(StrEnum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
