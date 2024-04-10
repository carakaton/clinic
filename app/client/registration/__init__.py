from aiogram import Router

from .register import router as register_router
from .card import router as card_router


registration_router = Router()
registration_router.include_routers(
    register_router,
    card_router,
)

__all__ = (
    'registration_router'
)
