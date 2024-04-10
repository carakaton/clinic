from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.storage import Patient, TestType, Laboratory
from app.utils import answer_with_keyboard, answer_no_such_button


class GetTestedStates(StatesGroup):
    choosing_test_type = State()
    choosing_laboratory = State()
    choosing_date = State()


router = Router()


@router.message(Command('get_tested'), StateFilter(None))
async def on_get_tested(message: Message, state: FSMContext):

    test_types = await TestType.get_all()

    await state.set_state(GetTestedStates.choosing_test_type)

    await answer_with_keyboard(message, text='Какой анализ Вы хотите сделать?',
                               kb_objects=test_types, count_in_row=3)


@router.message(GetTestedStates.choosing_test_type)
async def on_choosing_test_type(message: Message, state: FSMContext):

    test_types = await TestType.get_all()
    if not (test_type := test_types.filter_one_by_str(message.text)):
        return await answer_no_such_button(message, test_types, count_in_row=3)

    await state.update_data(test_type=test_type)
    await state.set_state(GetTestedStates.choosing_laboratory)

    labs = await Laboratory.filter(test_type=test_type)
    await answer_with_keyboard(message, text='Хорошо. Теперь, пожалуйста, выберите лабораторию.',
                               kb_objects=labs, count_in_row=2)


@router.message(GetTestedStates.choosing_laboratory)
async def on_choosing_laboratory(message: Message, state: FSMContext, test_type: TestType):

    labs = await Laboratory.filter(test_type=test_type)
    if not (lab := labs.filter_one_by_str(message.text)):
        return await answer_no_such_button(message, labs, count_in_row=2)

    await state.update_data(lab=lab)
    await state.set_state(GetTestedStates.choosing_date)

    visit_dates = lab.get_free_visit_dates()
    await answer_with_keyboard(message, text='Хорошо. Теперь, пожалуйста, выберите дату.',
                               kb_objects=visit_dates)


@router.message(GetTestedStates.choosing_date)
async def on_choosing_date(message: Message, state: FSMContext, patient: Patient, lab: Laboratory):

    visit_dates = lab.get_free_visit_dates()
    if not (visit_date := visit_dates.filter_one_by_str(message.text)):
        return await answer_no_such_button(message, visit_dates)

    await state.clear()

    visit = await lab.add_visit(patient, visit_date.timestamp)
    await message.answer(text=f'Отлично! Мы записали Вас в {visit}', reply_markup=ReplyKeyboardRemove())
