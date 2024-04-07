from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import as_section, Bold

router = Router()


@router.message(CommandStart())
async def on_start(msg: Message):
    hello_message = as_section(
        Bold(f'Добро пожаловать, {msg.from_user.first_name}!'),
        f'Где сегодня болит? Воспользуйтесь кнопкой «Меню».'
    )
    await msg.answer(**hello_message.as_kwargs())


@router.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено.",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command('get_tested'))
async def on_start(msg: Message):
    await msg.answer('Сдачи анализов пока не доступны...')


@router.message(Command('upcoming_appointments'))
async def on_start(msg: Message):
    await msg.answer('У вас нет грядущих приемов у врачей...')


@router.message(Command('upcoming_tests'))
async def on_start(msg: Message):
    await msg.answer('У вас нет грядущих анализов...')


@router.message(Command('doctor_reports'))
async def on_start(msg: Message):
    await msg.answer('Доктора еще ничего не заключили...')


@router.message(Command('card'))
async def on_start(msg: Message):
    await msg.answer('Мы пока ищем вашу карту...')


