from typing import Iterable

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


def make_row_keyboard(items: Iterable[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


class MakeAppointmentStates(StatesGroup):
    choosing_speciality = State()
    choosing_doctor = State()
    choosing_date = State()
    choosing_time = State()


specialities = {'Стоматолог', 'Дермотолог', 'Окулист'}
doctors = {'Иванов', 'Петров', 'Вылцан'}
dates = {'Сегодня', 'Завтра', 'Послезавтра'}
times = {'До обеда', 'В обед', 'После обеда'}


router = Router()


@router.message(Command('make_an_appointment'), StateFilter(None))
async def on_start(message: Message, state: FSMContext):
    await message.answer(
        text='К врачу какой специальности Вы бы хотели записаться?',
        reply_markup=make_row_keyboard(specialities),
    )
    await state.set_state(MakeAppointmentStates.choosing_speciality)


@router.message(MakeAppointmentStates.choosing_speciality, F.text.in_(specialities))
async def food_chosen(message: Message, state: FSMContext):
    # await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text='Хорошо. Теперь, пожалуйста, выберите врача:',
        reply_markup=make_row_keyboard(doctors),
    )
    await state.set_state(MakeAppointmentStates.choosing_doctor)


@router.message(MakeAppointmentStates.choosing_speciality)
async def food_chosen(message: Message):
    await message.answer(
        text='Такой специальности нет. Пожалуйста, выберите выберите специальность из списка ниже!',
        reply_markup=make_row_keyboard(specialities),
    )


@router.message(MakeAppointmentStates.choosing_doctor, F.text.in_(doctors))
async def food_chosen(message: Message, state: FSMContext):
    await message.answer(
        text='Хорошо. Теперь, пожалуйста, выберите дату:',
        reply_markup=make_row_keyboard(dates),
    )
    await state.set_state(MakeAppointmentStates.choosing_date)


@router.message(MakeAppointmentStates.choosing_doctor)
async def food_chosen(message: Message):
    await message.answer(
        text='Такого врача нет. Пожалуйста, выберите выберите врача из списка ниже!',
        reply_markup=make_row_keyboard(doctors),
    )


@router.message(MakeAppointmentStates.choosing_date, F.text.in_(dates))
async def food_chosen(message: Message, state: FSMContext):
    await message.answer(
        text='Хорошо. Теперь, пожалуйста, выберите время:',
        reply_markup=make_row_keyboard(times),
    )
    await state.set_state(MakeAppointmentStates.choosing_time)


@router.message(MakeAppointmentStates.choosing_date)
async def food_chosen(message: Message):
    await message.answer(
        text='Такой даты нет. Пожалуйста, выберите выберите дату из списка ниже!',
        reply_markup=make_row_keyboard(dates),
    )


@router.message(MakeAppointmentStates.choosing_time, F.text.in_(times))
async def food_chosen(message: Message, state: FSMContext):
    await message.answer(
        text='Отлично! Мы записали Вас.',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(MakeAppointmentStates.choosing_time)
async def food_chosen(message: Message):
    await message.answer(
        text='Такого времени нет. Пожалуйста, выберите выберите время из списка ниже!',
        reply_markup=make_row_keyboard(times),
    )
