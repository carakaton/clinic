from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.middlewares import ContextMiddleware
from .doctor import router as doctor_router


dispatcher = Dispatcher()
dispatcher.message.outer_middleware(ContextMiddleware())
dispatcher.callback_query.outer_middleware(ContextMiddleware())
dispatcher.include_routers(
    doctor_router,
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
