from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.infrastructure.database.session import get_db
from app.infrastructure.external.authorization import HttpAuthorizationGateway
from app.infrastructure.external.notification import HttpNotificationGateway


def get_authorization_gateway():
    return HttpAuthorizationGateway(get_settings())


def get_notification_gateway():
    return HttpNotificationGateway(get_settings())
