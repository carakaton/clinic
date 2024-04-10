from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.storage import Doctor, Report, DoctorVisit, Speciality


DOCS = {475273957, 396359672}


class ReportStates(StatesGroup):
    entering_text = State()
    waiting = State()
    entering_docs = State()


router = Router()


@router.message(Command('id'), StateFilter(None))
async def on_id(msg: Message):
    await msg.answer(str(msg.from_user.id))


@router.message(~F.from_user.id.in_(DOCS))
async def on_not_doctor(msg: Message):
    await msg.answer('Вы не доктор! Используйте бота для пациентов: @carakaton_test_bot')


@router.message(Command('patients'), StateFilter(None))
async def on_doctor(msg: Message):
    doctor = await Doctor.filter_one(id=msg.from_user.id)

    if not doctor.busy_visits:
        return await msg.answer('К Вам нет записей...')

    for v in doctor.busy_visits.values():
        await msg.answer(
            text=f'{v.patient.name} {v.timestamp.strftime('%d.%m в %H:%M')}',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text='Начать прием', callback_data=f'report:{v.id}'),
                InlineKeyboardButton(text='Не пришел', callback_data=f'remvisit:{v.id}'),
            ]]),
        )


@router.callback_query(F.data.startswith('remvisit:'))
async def on_report_button(callback: CallbackQuery):
    visit_id = int(callback.data.split(':')[-1])
    visit = await DoctorVisit.get_by_id(visit_id)
    await visit.doctor.remove_visit(visit)
    await callback.message.delete()


@router.callback_query(F.data.startswith('report:'), StateFilter(None))
async def on_report_button(callback: CallbackQuery, state: FSMContext):
    visit_id = int(callback.data.split(':')[-1])
    visit = await DoctorVisit.get_by_id(visit_id)
    await state.update_data(visit=visit, called_message=callback.message)
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(ReportStates.entering_text)
    await callback.message.answer('Отправьте текст заключения.')


@router.message(ReportStates.entering_text)
async def on_entering_text(msg: Message, state: FSMContext):
    await state.update_data(text=msg.text)
    await msg.answer(
        text='Текст заключения принят.',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Отправить заключение', callback_data=f'done')],
                [InlineKeyboardButton(text='Добавить направления', callback_data=f'adddocs')],
        ]))
    await state.set_state(ReportStates.waiting)


@router.callback_query(ReportStates.waiting, F.data == 'done')
async def on_done_button(callback: CallbackQuery, state: FSMContext,
                         visit: DoctorVisit, called_message: Message, text: str):
    await callback.message.delete()
    await Report(visit, text).create()
    await visit.doctor.remove_visit(visit)
    await called_message.edit_text(text=called_message.text + '\n ЗАКЛЮЧЕНО')
    await state.clear()


@router.callback_query(ReportStates.waiting, F.data == 'adddocs')
async def on_add_docs_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text='Отправить заключение', callback_data=f'done'),
        ]])
    )
    await callback.message.answer('Отправьте направления в формате:')
    await callback.message.answer('Специальность врача - ФИО врача\n'
                                  'Специальность врача - ФИО врача\n'
                                  'Специальность врача - ФИО врача')
    await state.set_state(ReportStates.entering_docs)


@router.message(ReportStates.entering_docs)
async def on_entering_docs(msg: Message, state: FSMContext):
    try:
        docs = msg.text.split('\n')
        docs_data = [doc.split(' - ') for doc in docs]
    except Exception:
        return await msg.answer('Неправильный формат направлений. Попробуйте еще раз.')

    for spec_name, doc_name in docs_data:
        if not (spec := await Speciality.filter_one(name=spec_name)):
            spec = await Speciality(name=spec_name).create()
        if not await Doctor.filter_one(name=doc_name):
            await Doctor(doc_name, spec).create()

    await msg.answer('Направления добавлены. Нажмите "Отправить заключение".')
    await state.set_state(ReportStates.waiting)


@router.message()
async def on_unknown_msg(msg: Message):
    await msg.answer('Не поняли Вас, воспользуйтесь меню!')
