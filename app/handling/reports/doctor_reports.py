from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command('doctor_reports'))
async def on_start(msg: Message):
    await msg.answer('Доктора еще ничего не заключили...')
