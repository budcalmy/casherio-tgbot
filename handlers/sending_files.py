from aiogram import Router
from aiogram.types import Message

import os

from dotenv import load_dotenv

from moduls.wastes_actions import to_string_all_expenses
from db.db_queries import get_all_expenses


router = Router()
load_dotenv()

path = os.getenv("FILE_PATH")


async def send_txt_file(message: Message):
    with open(path, "w") as file:
        all_expenses = await get_all_expenses(message.from_user.id)
        file.write("\n".join(to_string_all_expenses(all_expenses)))

    await message.answer(
        text="*Home — /home*",
        parse_mode="Markdown"
    )