from aiogram import Router

from .make_an_appointment import router as make_appointment_router
from .upcoming_appointments import router as upcoming_appointments_router


appointment_router = Router()
appointment_router.include_routers(
    make_appointment_router,
    upcoming_appointments_router,
)

__all__ = (
    'appointment_router'
)
