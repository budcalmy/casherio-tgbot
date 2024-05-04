from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def inline_keyboard_days(buttons_text, callback_text):
    builder = InlineKeyboardBuilder()
    buttons_text = sorted(buttons_text, reverse=True)
    callback_text = sorted(callback_text, reverse=True)

    for _ in range(4):
        row = []
        for _ in range(3):
            if len(buttons_text):
                row.append(InlineKeyboardButton(
                    text=buttons_text.pop(),
                    callback_data=callback_text.pop()
                ))
        builder.row(*row)

    return builder.as_markup()
