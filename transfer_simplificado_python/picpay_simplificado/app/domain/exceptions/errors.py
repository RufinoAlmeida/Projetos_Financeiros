class DomainError(Exception):
    """Base class for expected business errors."""


class UserNotFoundError(DomainError):
    pass


class InvalidTransferError(DomainError):
    pass


class InsufficientBalanceError(DomainError):
    pass


class MerchantCannotPayError(DomainError):
    pass


class AuthorizationDeniedError(DomainError):
    pass


class ExternalServiceError(DomainError):
    pass
