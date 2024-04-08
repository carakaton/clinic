from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.storage import Patient, Report


router = Router()


@router.message(Command('doctor_reports'))
async def on_start(msg: Message, patient: Patient):
    reports = await Report.filter(patient=patient)

    if not reports:
        return await msg.answer('Доктора еще ничего не заключили...')

    for r in reports:
        await msg.answer(str(r))
