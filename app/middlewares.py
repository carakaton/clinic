from app.storage import Patient

from typing import Any, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class PatientMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable, message: Message, data: dict[str, Any]) -> Any:
        data['patient'] = await Patient.get_by_id(message.from_user.id)
        return await handler(message, data)


class ContextMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable, message: Message, data: dict[str, Any]) -> Any:
        state: FSMContext = data.get('state')
        if state:
            state_data = await state.get_data()
            data.update(state_data)
        return await handler(message, data)
