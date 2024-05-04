from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def simple_keyboard(items: list[str]):
    builder = ReplyKeyboardBuilder()
    for btn in [KeyboardButton(text=item) for item in items]:
        builder.add(btn)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)