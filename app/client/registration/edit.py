from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import as_section, Bold

from app.storage import Patient
from app.utils import answer_with_keyboard


router = Router()


class EditStates(StatesGroup):
    entering_polis = State()
    entering_age = State()
    entering_sex = State()


@router.message(Command('edit'), StateFilter(None))
async def on_new_user_start(msg: Message, state: FSMContext):
    hello_message = as_section(
        Bold(f'Начнем вводить новые данные, {msg.from_user.first_name}?'),
        'Отправьте нам номер вашего полиса, пожалуйста.\n',
        'Вот пример:',
    )

    await state.set_state(EditStates.entering_polis)
    await msg.answer(**hello_message.as_kwargs())
    await msg.answer('1234123412340000')


@router.message(EditStates.entering_polis)
async def on_polis_entered(msg: Message, state: FSMContext):
    if len(msg.text) > 16 or not msg.text.isdigit():
        return await msg.answer('Неправильный формат полиса, попробуйте еще раз.')

    polis = int(msg.text)
    if (patient := await Patient.filter_one(polis=polis)) and patient.id != msg.from_user.id:
        return await msg.answer('Аккаунт с таким полисом уже существует.')

    await state.update_data(polis=polis)
    await state.set_state(EditStates.entering_age)
    await msg.answer('Отправьте свой возраст.')


@router.message(EditStates.entering_age)
async def on_entering_age(msg: Message, state: FSMContext):
    if not msg.text.isdigit() or not 0 < int(msg.text) < 150:
        return await msg.answer('Неправильно указан возраст, попробуйте еще раз.')

    await state.update_data(age=int(msg.text))
    await state.set_state(EditStates.entering_sex)
    await answer_with_keyboard(msg, 'Выберите свой пол.', ['Мужской', 'Женский'], has_cancel=False)


@router.message(EditStates.entering_sex)
async def on_entering_sex(msg: Message, state: FSMContext, polis: int, age: int):

    if msg.text not in {'Мужской', 'Женский'}:
        return await msg.answer('Неправильно указан пол, попробуйте еще раз.')

    patient = await Patient.get_by_id(msg.from_user.id)
    patient.name = msg.from_user.id
    patient.polis = polis
    patient.age = age
    patient.sex = 1 if msg.text == 'Мужской' else 0,

    await state.clear()
    await msg.answer('Ваша медкарта обновлена!',
                     reply_markup=ReplyKeyboardRemove())
