from aiogram import Router

from .get_tested import router as get_tested_router
from .upcoming_tests import router as upcoming_tests_router


tests_router = Router()
tests_router.include_routers(
    get_tested_router,
    upcoming_tests_router,
)

__all__ = (
    'tests_router'
)
