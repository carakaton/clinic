from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from app.storage import Patient, TestVisit


router = Router()


@router.message(Command('upcoming_tests'))
async def on_upcoming_tests(msg: Message, patient: Patient):
    tests = await TestVisit.filter(patient=patient)

    if not tests:
        return await msg.answer('У вас не запланировано сдачи анализов...')

    for t in tests:
        await msg.answer(
            text=f'У вас будет {t}!',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Отменить запись', callback_data=f'remtest:{t.id}')]
            ]),
        )


@router.callback_query(F.data.startswith('remtest:'))
async def on_report_button(callback: CallbackQuery):
    test_id = int(callback.data.split(':')[-1])
    test = await TestVisit.get_by_id(test_id)
    await test.laboratory.remove_visit(test)
    await callback.message.delete()
