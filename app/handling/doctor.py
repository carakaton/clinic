from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.storage import Doctor, Report, DoctorVisit


DOCS = {475273957}


class ReportStates(StatesGroup):
    entering_text = State()


router = Router()


@router.message(Command('id'), StateFilter(None))
async def on_id(msg: Message):
    await msg.answer(str(msg.from_user.id))


@router.message(F.from_user.id.in_(DOCS), StateFilter(None))
async def on_doctor(msg: Message):
    doctor = await Doctor.filter_one(id=msg.from_user.id)

    if not doctor.busy_visits:
        return await msg.answer('К Вам нет записей...')

    for v in doctor.busy_visits.values():
        await msg.answer(
            text=f'{v.patient.name} {v.timestamp.strftime('%d.%m в %H:%M')}',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Заключить', callback_data=f'report:{v.id}')]
            ]),
        )


@router.callback_query(F.from_user.id.in_(DOCS), F.data.startswith('report:'))
async def on_report_button(callback: CallbackQuery, state: FSMContext):
    visit_id = int(callback.data.split(':')[-1])
    visit = await DoctorVisit.get_by_id(visit_id)
    await state.update_data(visit=visit, called_message=callback.message)
    await state.set_state(ReportStates.entering_text)
    await callback.message.answer('Отправьте текст заключения.')


@router.message(F.from_user.id.in_(DOCS), ReportStates.entering_text)
async def on_entering_text(msg: Message, state: FSMContext, visit: DoctorVisit, called_message: Message):
    await Report(visit, msg.text).create()
    await visit.doctor.remove_visit(visit)
    await called_message.edit_text('Заключение поставлено.', reply_markup=None)
    await state.clear()
