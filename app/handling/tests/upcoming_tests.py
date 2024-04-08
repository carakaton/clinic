from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.storage import Patient, TestVisit


router = Router()


@router.message(Command('upcoming_tests'))
async def on_upcoming_tests(msg: Message, patient: Patient):
    tests = await TestVisit.filter(patient=patient)

    if not tests:
        return await msg.answer('У вас не запланировано сдачи анализов...')

    for t in tests:
        await msg.answer(f'У вас будет {t}!')
