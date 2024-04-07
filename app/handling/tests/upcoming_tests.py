from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command('upcoming_tests'))
async def on_start(msg: Message):
    await msg.answer('У вас нет грядущих анализов...')
