from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.storage import Patient


router = Router()


@router.message(Command('card'))
async def on_start(msg: Message):
    patient = await Patient.get_by_id(msg.from_user.id)
    await msg.answer(str(patient))
