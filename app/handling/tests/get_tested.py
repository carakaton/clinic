from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command('get_tested'))
async def on_start(msg: Message):
    await msg.answer('Сдачи анализов пока не доступны...')

