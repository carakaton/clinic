from aiogram import Router

from .doctor_reports import router as doctor_reports_router


reports_router = Router()
reports_router.include_routers(
    doctor_reports_router,
)

__all__ = (
    'reports_router'
)
