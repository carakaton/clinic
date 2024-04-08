from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.storage import Patient, DoctorVisit


router = Router()


@router.message(Command('upcoming_appointments'))
async def on_upcoming_appointments(msg: Message, patient: Patient):
    appointments = await DoctorVisit.get_all_for(patient)

    if not appointments:
        return await msg.answer('У вас нет грядущих приемов у врачей...')

    for a in appointments:
        await msg.answer(f'У вас будет {a}!')
