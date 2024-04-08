from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.storage import Doctor


DOCS = {475273957}


router = Router()


@router.message(Command('id'))
async def on_id(msg: Message):
    await msg.answer(str(msg.from_user.id))


@router.message(F.from_user.id.in_(DOCS))
async def on_doctor(msg: Message):
    doctor = await Doctor.filter_one(id=msg.from_user.id)

    if not doctor.busy_visits:
        return await msg.answer('К Вам нет записей...')

    for v in doctor.busy_visits.values():
        await msg.answer(f'{v.patient.name} {v.timestamp.strftime('%d.%m в %H:%M')}')
