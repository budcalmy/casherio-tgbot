from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def inline_keyboard_weeks(buttons_text, callback_text):
    builder = InlineKeyboardBuilder()
    for i in range(len(buttons_text)):
        builder.row(InlineKeyboardButton(
            text=buttons_text[i],
            callback_data=callback_text[i]
        ))

    return builder.as_markup()