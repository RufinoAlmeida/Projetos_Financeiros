from fastapi import FastAPI

from app.api.error_handlers import register_error_handlers
from app.api.routes import health, transfers, users, wallets
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="REST API for the PicPay Simplificado backend challenge.",
)

register_error_handlers(app)
app.include_router(health.router)
app.include_router(users.router)
app.include_router(wallets.router)
app.include_router(transfers.router)
