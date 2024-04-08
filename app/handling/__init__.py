from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from .appointments import appointment_router
from .registration import registration_router
from .reports import reports_router
from .tests import tests_router
from .middlewares import PatientMiddleware, ContextMiddleware


dispatcher = Dispatcher()
dispatcher.message.outer_middleware(PatientMiddleware())
dispatcher.message.outer_middleware(ContextMiddleware())
dispatcher.include_routers(
    registration_router,
    appointment_router,
    reports_router,
    tests_router,
)


@dispatcher.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Что бы то ни было, мы это отменили!',
        reply_markup=ReplyKeyboardRemove(),
    )


__all__ = (
    'dispatcher'
)
