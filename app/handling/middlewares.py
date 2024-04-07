from app.storage import Patient

from typing import Any, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message


class PatientMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable, message: Message, data: dict[str, Any]) -> Any:
        data['patient'] = await Patient.get_by_id(message.from_user.id)
        return await handler(message, data)
