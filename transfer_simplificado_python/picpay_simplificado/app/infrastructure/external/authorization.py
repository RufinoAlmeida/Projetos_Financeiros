import logging

import httpx

from app.core.config import Settings
from app.domain.exceptions.errors import AuthorizationDeniedError, ExternalServiceError

logger = logging.getLogger(__name__)


class AuthorizationGateway:
    def authorize(self) -> bool:
        raise NotImplementedError


class HttpAuthorizationGateway(AuthorizationGateway):
    def __init__(self, settings: Settings):
        self.url = settings.authorization_url
        self.timeout = settings.http_timeout_seconds

    def authorize(self) -> bool:
        try:
            response = httpx.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            logger.exception("authorization_service_unavailable")
            raise ExternalServiceError("Authorization service is unavailable") from exc

        authorization = payload.get("data", {}).get("authorization")
        if authorization is not True:
            raise AuthorizationDeniedError("Transfer was not authorized")
        return True
