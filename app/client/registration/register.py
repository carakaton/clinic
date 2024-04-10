from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import as_section, Bold

from app.storage import Patient
from app.utils import answer_with_keyboard


router = Router()


class RegistrationStates(StatesGroup):
    entering_polis = State()
    entering_age = State()
    entering_sex = State()


@router.message(CommandStart(), StateFilter(None), MagicData(F.patient))
async def on_existing_user_start(msg: Message):
    hello_message = as_section(
        Bold(f'Где сегодня болит, {msg.from_user.first_name}?'),
        f'Воспользуйтесь кнопкой «Меню».'
    )
    await msg.answer(**hello_message.as_kwargs())


@router.message(CommandStart(), StateFilter(None))
async def on_new_user_start(msg: Message, state: FSMContext):
    hello_message = as_section(
        Bold(f'Вы у нас в первый раз, {msg.from_user.first_name}?'),
        'Пора завести медкарту! Отправьте нам номер вашего полиса, пожалуйста.\n',
        'Вот пример:',
    )

    await state.set_state(RegistrationStates.entering_polis)
    await msg.answer(**hello_message.as_kwargs())
    await msg.answer('1234123412340000')


@router.message(RegistrationStates.entering_polis)
async def on_polis_entered(msg: Message, state: FSMContext):
    if len(msg.text) > 16 or not msg.text.isdigit():
        return await msg.answer('Неправильный формат полиса, попробуйте еще раз.')

    polis = int(msg.text)
    if await Patient.filter(polis=polis):
        return await msg.answer('Аккаунт с таким полисом уже существует.')

    await state.update_data(polis=polis)
    await state.set_state(RegistrationStates.entering_age)
    await msg.answer('Отправьте свой возраст.')


@router.message(RegistrationStates.entering_age)
async def on_entering_age(msg: Message, state: FSMContext):
    if not msg.text.isdigit() or not 0 < int(msg.text) < 150:
        return await msg.answer('Неправильно указан возраст, попробуйте еще раз.')

    await state.update_data(age=int(msg.text))
    await state.set_state(RegistrationStates.entering_sex)
    await answer_with_keyboard(msg, 'Выберите свой пол.', ['Мужской', 'Женский'], has_cancel=False)


@router.message(RegistrationStates.entering_sex)
async def on_entering_sex(msg: Message, state: FSMContext, polis: int, age: int):

    if msg.text not in {'Мужской', 'Женский'}:
        return await msg.answer('Неправильно указан пол, попробуйте еще раз.')

    await Patient(
        tg_id=msg.from_user.id,
        name=msg.from_user.first_name,
        polis=polis,
        age=age,
        sex=1 if msg.text == 'Мужской' else 0,
    ).create()

    await state.clear()
    await msg.answer('Ваша медкарта создана! Воспользуйтесь кнопкой «Меню» для просмотра доступных услуг.',
                     reply_markup=ReplyKeyboardRemove())


@router.message(MagicData(~F.patient))
async def on_user_without_card(msg: Message):
    hello_message = as_section(
        Bold(f'У Вас нет карты, {msg.from_user.first_name}!'),
        f'А ну-ка на /start'
    )
    await msg.answer(**hello_message.as_kwargs())
