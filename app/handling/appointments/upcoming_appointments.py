from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.storage import Patient, Appointment


router = Router()


@router.message(Command('upcoming_appointments'))
async def on_start(msg: Message, patient: Patient):
    appointments = await Appointment.get_all_for(patient)

    if not appointments:
        return await msg.answer('У вас нет грядущих приемов у врачей...')

    for a in appointments:
        await msg.answer(f'У вас будет {a}!')
