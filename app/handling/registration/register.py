from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import as_section, Bold

from app.storage import Patient


router = Router()


class RegistrationStates(StatesGroup):
    entering_polis = State()


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

    await Patient(
        tg_id=msg.from_user.id,
        polis=int(msg.text)
    ).create()

    await state.clear()
    await msg.answer('Ваша медкарта создана! Воспользуйтесь кнопкой «Меню» для просмотра доступных услуг.')


@router.message(MagicData(~F.patient))
async def on_user_without_card(msg: Message):
    hello_message = as_section(
        Bold(f'У Вас нет карты, {msg.from_user.first_name}!'),
        f'А ну-ка на /start'
    )
    await msg.answer(**hello_message.as_kwargs())
