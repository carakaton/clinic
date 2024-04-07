from typing import Iterable

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app import fake_db


T_D1 = 'К врачу какой специальности Вы бы хотели записаться?'
T_D2 = 'Хорошо. Теперь, пожалуйста, выберите врача.'
T_D3 = 'Хорошо. Теперь, пожалуйста, выберите дату.'
T_D4 = 'Хорошо. Теперь, пожалуйста, выберите время.'
T_DS = 'Отлично! Мы записали Вас к {speciality} {doctor}, {date} на {time}'
T_DW = 'Такого варианта нет. Пожалуйста, выберите вариант из клавиатуры!'


def make_row_keyboard(items: Iterable) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=str(item)) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


async def send_variant_is_wrong(message: Message, variants: Iterable):
    await message.answer(text=T_DW, reply_markup=make_row_keyboard(variants))


class MakeAppointmentStates(StatesGroup):
    choosing_speciality = State()
    choosing_doctor = State()
    choosing_date = State()
    choosing_time = State()


router = Router()


@router.message(Command('make_an_appointment'), StateFilter(None))
async def on_make_an_appointment(message: Message, state: FSMContext):
    specialities = await fake_db.Speciality.get_many()
    await message.answer(text=T_D1, reply_markup=make_row_keyboard(specialities))
    await state.set_state(MakeAppointmentStates.choosing_speciality)


@router.message(MakeAppointmentStates.choosing_speciality)
async def on_choosing_speciality(message: Message, state: FSMContext):
    specialities = await fake_db.Speciality.get_many()
    if message.text not in map(str, specialities):
        return await send_variant_is_wrong(message, specialities)

    speciality = [s for s in specialities if str(s) == message.text][0]
    await state.update_data(speciality=speciality)

    doctors = await fake_db.Doctor.get_many(speciality)
    await message.answer(text=T_D2, reply_markup=make_row_keyboard(doctors))
    await state.set_state(MakeAppointmentStates.choosing_doctor)


@router.message(MakeAppointmentStates.choosing_doctor)
async def on_choosing_doctor(message: Message, state: FSMContext):
    data = await state.get_data()
    doctors = await fake_db.Doctor.get_many(data['speciality'])
    if message.text not in map(str, doctors):
        return await send_variant_is_wrong(message, doctors)

    doctor = [d for d in doctors if str(d) == message.text][0]
    await state.update_data(doctor=doctor)

    dates = await fake_db.Date.get_many(data['speciality'], doctor)
    await message.answer(text=T_D3, reply_markup=make_row_keyboard(dates))
    await state.set_state(MakeAppointmentStates.choosing_date)


@router.message(MakeAppointmentStates.choosing_date)
async def on_choosing_date(message: Message, state: FSMContext):
    data = await state.get_data()
    dates = await fake_db.Date.get_many(data['speciality'], data['doctor'])
    if message.text not in map(str, dates):
        return await send_variant_is_wrong(message, dates)

    date = [d for d in dates if str(d) == message.text][0]
    await state.update_data(date=date)

    times = await fake_db.Time.get_many(data['speciality'], data['doctor'], date)
    await message.answer(text=T_D4, reply_markup=make_row_keyboard(times))
    await state.set_state(MakeAppointmentStates.choosing_time)


@router.message(MakeAppointmentStates.choosing_time)
async def on_chosen_time(message: Message, state: FSMContext):
    data = await state.get_data()
    times = await fake_db.Time.get_many(data['speciality'], data['doctor'], data['date'])
    if message.text not in map(str, times):
        return await send_variant_is_wrong(message, times)

    time = [t for t in times if str(t) == message.text][0]

    await message.answer(text=T_DS.format(**data, time=time), reply_markup=ReplyKeyboardRemove())
    await state.clear()
