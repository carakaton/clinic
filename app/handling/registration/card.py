from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command('card'))
async def on_start(msg: Message):
    await msg.answer('Мы пока ищем вашу карту...')
