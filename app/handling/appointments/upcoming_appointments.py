from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from app.storage import Patient, DoctorVisit


router = Router()


@router.message(Command('upcoming_appointments'))
async def on_upcoming_appointments(msg: Message, patient: Patient):
    visits = await DoctorVisit.get_all_for(patient)

    if not visits:
        return await msg.answer('У вас нет грядущих приемов у врачей...')

    for v in visits:
        await msg.answer(
            text=f'У вас будет {v}!',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Отменить запись', callback_data=f'remvisit:{v.id}')]
            ]),
        )


@router.callback_query(F.data.startswith('remvisit:'))
async def on_report_button(callback: CallbackQuery):
    visit_id = int(callback.data.split(':')[-1])
    visit = await DoctorVisit.get_by_id(visit_id)
    await visit.doctor.remove_visit(visit)
    await callback.message.delete()
