from typing import Sequence
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


def make_keyboard(items: Sequence, count_in_row=5) -> ReplyKeyboardMarkup:

    rows = [items[i:i + count_in_row] for i in range(0, len(items), count_in_row)]

    keyboard = [[KeyboardButton(text=str(item)) for item in r] for r in rows]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


async def answer_with_keyboard(message: Message, text: str, kb_objects: Sequence, has_cancel=True, count_in_row=5):

    if has_cancel:
        text += '\nОтменить: /cancel'

    markup = make_keyboard(kb_objects, count_in_row=count_in_row)

    return await message.answer(text, reply_markup=markup)


async def answer_no_such_button(message: Message, kb_objects: Sequence, has_cancel=True, count_in_row=5):
    return await answer_with_keyboard(message, 'Такого варианта нет. Пожалуйста, выберите вариант из клавиатуры!',
                                      kb_objects, has_cancel, count_in_row)
