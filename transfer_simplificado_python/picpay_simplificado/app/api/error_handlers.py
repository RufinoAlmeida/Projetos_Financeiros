from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.application.services.user_service import DuplicateUserError
from app.domain.exceptions.errors import (
    AuthorizationDeniedError,
    ExternalServiceError,
    InsufficientBalanceError,
    InvalidTransferError,
    MerchantCannotPayError,
    UserNotFoundError,
)


def register_error_handlers(app: FastAPI) -> None:
    handlers = {
        DuplicateUserError: (status.HTTP_409_CONFLICT, "DUPLICATE_USER"),
        UserNotFoundError: (status.HTTP_404_NOT_FOUND, "USER_NOT_FOUND"),
        InvalidTransferError: (status.HTTP_422_UNPROCESSABLE_ENTITY, "INVALID_TRANSFER"),
        InsufficientBalanceError: (status.HTTP_422_UNPROCESSABLE_ENTITY, "INSUFFICIENT_BALANCE"),
        MerchantCannotPayError: (status.HTTP_422_UNPROCESSABLE_ENTITY, "MERCHANT_CANNOT_PAY"),
        AuthorizationDeniedError: (status.HTTP_403_FORBIDDEN, "TRANSFER_NOT_AUTHORIZED"),
        ExternalServiceError: (status.HTTP_503_SERVICE_UNAVAILABLE, "EXTERNAL_SERVICE_UNAVAILABLE"),
    }

    for exception_type, (http_status, code) in handlers.items():
        async def handler(request: Request, exc: Exception, http_status=http_status, code=code):
            return JSONResponse(
                status_code=http_status,
                content={"error": code, "message": str(exc)},
            )

        app.add_exception_handler(exception_type, handler)
