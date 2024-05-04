from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router
from aiogram.filters import StateFilter

from states.States import States

from datetime import datetime as dt

from keyboards.simple_keyboard import simple_keyboard

from moduls.Waste import Waste

from db.db_queries import insert_user_waste

from keyboards.button_text import DEFAULT_CATEGORIES, WASTES_TYPES

import re


router = Router()
waste = Waste(0, '', '', 0.0, '')


def from_str_to_float(string: str):
    if re.match(r'^[\d.,]+$', string):
        string = string.replace(',', '.')
        return [float(string), True]
    else:
        return ["", False]


@router.message(
    StateFilter(States.creating_waste)
)
async def choose_waste_type(message: Message, state: FSMContext):
    input_type = message.text.lower()
    if input_type == "daily expense":
        waste.type = "daily"
        await message.answer(
            text="Please choose category of expense from given or input yours",
            reply_markup=simple_keyboard(DEFAULT_CATEGORIES)
        )
        await state.set_state(States.input_category_of_waste)
    elif input_type == "usually expense":
        waste.type = "usually"
        await message.answer(
            text="Please choose category of expense from given or input yours",
            reply_markup=simple_keyboard(DEFAULT_CATEGORIES)
        )
        await state.set_state(States.input_category_of_waste)
    else:
        await message.answer(
            text="Please choose from given types",
            reply_markup=simple_keyboard(WASTES_TYPES)
        )



@router.message(
    StateFilter(States.input_category_of_waste))
async def choose_category(message: Message, state: FSMContext):
    chosen_category = message.text.lower()
    waste.user_id = message.from_user.id
    waste.category = chosen_category
    await message.answer(
        text=f"Selected category: {chosen_category}\n"
             f"Enter the sum of expense: ",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(States.input_sum_of_waste)


@router.message(
    StateFilter(States.input_sum_of_waste)
)
async def input_sum_of_waste(message: Message, state: FSMContext):

    input_number, ok = from_str_to_float(message.text.lower())

    if not ok:
        await message.answer(
            text="Please, enter a number",
            reply_markup=ReplyKeyboardRemove()
        )
    else:

        waste.sum = input_number
        await message.answer(
            text=f"Expense successfully added!\n\n"
                 f"Selected category: {waste.category}\n"
                 f"Sum: {waste.sum}\n\n"
                 f"Go home /home",
            reply_markup=simple_keyboard(["/home"])
        )

        now = dt.now()
        waste.time = now.strftime("%d %b %H:%M")

        await insert_user_waste(waste)

        await state.set_state(States.user_on_profile)
