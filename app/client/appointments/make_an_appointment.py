from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.storage import Patient, Speciality, Doctor, VisitDate
from app.utils import answer_with_keyboard, answer_no_such_button


class MakeAppointmentStates(StatesGroup):
    choosing_speciality = State()
    choosing_doctor = State()
    choosing_date = State()
    choosing_time = State()


router = Router()


@router.message(Command('make_an_appointment'), StateFilter(None))
async def on_make_an_appointment(message: Message, state: FSMContext, patient: Patient):

    is_kid = not patient.is_old
    specialities = await Speciality.filter(for_kids=is_kid, for_sex=None)
    specialities.extend(await Speciality.filter(for_kids=None, for_sex=patient.sex))
    specialities.extend(await Speciality.filter(for_kids=None, for_sex=None))

    await state.set_state(MakeAppointmentStates.choosing_speciality)

    await answer_with_keyboard(message, text='К врачу какой специальности Вы бы хотели записаться?',
                               kb_objects=specialities, count_in_row=2)


@router.message(MakeAppointmentStates.choosing_speciality)
async def on_choosing_speciality(message: Message, state: FSMContext):

    specialities = await Speciality.get_all()
    if not (speciality := specialities.filter_one_by_str(message.text)):
        return await answer_no_such_button(message, specialities, count_in_row=2)

    await state.update_data(speciality=speciality)
    await state.set_state(MakeAppointmentStates.choosing_doctor)

    doctors = await Doctor.filter(speciality=speciality)
    await answer_with_keyboard(message, text='Хорошо. Теперь, пожалуйста, выберите врача.',
                               kb_objects=doctors, count_in_row=3)


@router.message(MakeAppointmentStates.choosing_doctor)
async def on_choosing_doctor(message: Message, state: FSMContext, speciality: Speciality):

    doctors = await Doctor.filter(speciality=speciality)
    if not (doctor := doctors.filter_one_by_str(message.text)):
        return await answer_no_such_button(message, doctors, count_in_row=3)

    await state.update_data(doctor=doctor)
    await state.set_state(MakeAppointmentStates.choosing_date)

    visit_dates = doctor.get_free_visit_dates()
    await answer_with_keyboard(message, text='Хорошо. Теперь, пожалуйста, выберите дату.',
                               kb_objects=visit_dates)


@router.message(MakeAppointmentStates.choosing_date)
async def on_choosing_date(message: Message, state: FSMContext, doctor: Doctor):

    visit_dates = doctor.get_free_visit_dates()
    if not (visit_date := visit_dates.filter_one_by_str(message.text)):
        return await answer_no_such_button(message, visit_dates)

    await state.update_data(visit_date=visit_date)
    await state.set_state(MakeAppointmentStates.choosing_time)

    visit_times = doctor.get_free_visit_times(visit_date.timestamp)
    await answer_with_keyboard(message, text='Хорошо. Теперь, пожалуйста, выберите время.',
                               kb_objects=visit_times)


@router.message(MakeAppointmentStates.choosing_time)
async def on_chosen_time(message: Message, state: FSMContext, patient: Patient, doctor: Doctor, visit_date: VisitDate):

    visit_times = doctor.get_free_visit_times(date=visit_date.timestamp)
    if not (visit_time := visit_times.filter_one_by_str(message.text)):
        return await answer_no_such_button(message, visit_times)

    await state.clear()

    visit = await doctor.add_visit(patient, visit_time.timestamp)
    await message.answer(text=f'Отлично! Мы записали Вас к {visit}', reply_markup=ReplyKeyboardRemove())
