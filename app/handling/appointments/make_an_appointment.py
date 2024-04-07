from typing import Sequence

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.storage import Patient, Speciality, Doctor, Appointment, AppointmentPlace


CANCEL = '\nОтменить: /cancel'
T_D1 = 'К врачу какой специальности Вы бы хотели записаться?' + CANCEL
T_D2 = 'Хорошо. Теперь, пожалуйста, выберите врача.' + CANCEL
T_D3 = 'Хорошо. Теперь, пожалуйста, выберите дату.' + CANCEL
T_D4 = 'Хорошо. Теперь, пожалуйста, выберите время.' + CANCEL
T_DS = 'Отлично! Мы записали Вас к {speciality} {doctor}, {date} на {time}'
T_DW = 'Такого варианта нет. Пожалуйста, выберите вариант из клавиатуры!' + CANCEL


def make_keyboard(items: Sequence) -> ReplyKeyboardMarkup:
    chunk_size = 5
    chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
    keyboard = [[KeyboardButton(text=str(item)) for item in c] for c in chunks]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


async def send_variant_is_wrong(message: Message, variants: Sequence):
    await message.answer(text=T_DW, reply_markup=make_keyboard(variants))


class MakeAppointmentStates(StatesGroup):
    choosing_speciality = State()
    choosing_doctor = State()
    choosing_date = State()
    choosing_time = State()


router = Router()


@router.message(Command('make_an_appointment'), StateFilter(None))
async def on_make_an_appointment(message: Message, state: FSMContext):
    specialities = await Speciality.get_all()
    await message.answer(text=T_D1, reply_markup=make_keyboard(specialities))
    await state.set_state(MakeAppointmentStates.choosing_speciality)


@router.message(MakeAppointmentStates.choosing_speciality)
async def on_choosing_speciality(message: Message, state: FSMContext):
    specialities = await Speciality.get_all()
    if message.text not in map(str, specialities):
        return await send_variant_is_wrong(message, specialities)

    speciality = [s for s in specialities if str(s) == message.text][0]
    await state.update_data(speciality=speciality)

    doctors = await Doctor.filter(speciality=speciality)
    await message.answer(text=T_D2, reply_markup=make_keyboard(doctors))
    await state.set_state(MakeAppointmentStates.choosing_doctor)


@router.message(MakeAppointmentStates.choosing_doctor)
async def on_choosing_doctor(message: Message, state: FSMContext):
    data = await state.get_data()
    doctors = await Doctor.filter(speciality=data['speciality'])
    if message.text not in map(str, doctors):
        return await send_variant_is_wrong(message, doctors)

    doctor = [d for d in doctors if str(d) == message.text][0]
    await state.update_data(doctor=doctor)

    date_strings = await AppointmentPlace.get_not_busy_date_strings_for(doctor)
    await message.answer(text=T_D3, reply_markup=make_keyboard(date_strings))
    await state.set_state(MakeAppointmentStates.choosing_date)


@router.message(MakeAppointmentStates.choosing_date)
async def on_choosing_date(message: Message, state: FSMContext):
    data = await state.get_data()
    date_strings = await AppointmentPlace.get_not_busy_date_strings_for(data['doctor'])
    if message.text not in date_strings:
        return await send_variant_is_wrong(message, date_strings)

    date_string = [d for d in date_strings if d == message.text][0]
    await state.update_data(date=date_string)

    places = await AppointmentPlace.filter(doctor=data['doctor'], date_string=date_string, is_busy=False)
    time_strings = [place.time_string for place in places]
    await message.answer(text=T_D4, reply_markup=make_keyboard(time_strings))
    await state.set_state(MakeAppointmentStates.choosing_time)


@router.message(MakeAppointmentStates.choosing_time)
async def on_chosen_time(message: Message, state: FSMContext, patient: Patient):
    data = await state.get_data()
    places = await AppointmentPlace.filter(doctor=data['doctor'], date_string=data['date'], is_busy=False)
    time_strings = [place.time_string for place in places]
    if message.text not in time_strings:
        return await send_variant_is_wrong(message, time_strings)

    place = [p for p in places if p.time_string == message.text][0]
    await Appointment(patient, data['doctor'], place).create()

    await message.answer(text=T_DS.format(**data, time=place.time_string), reply_markup=ReplyKeyboardRemove())
    await state.clear()
