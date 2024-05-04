from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import StateFilter
from states.States import States

from keyboards.simple_keyboard import simple_keyboard
from keyboards.button_text import BEG_ACTIONS, HOME_PAGE_ACTIONS

import db.db_queries

from handlers.common import user
router = Router()


@router.message(
    StateFilter(States.creating_username)
)
async def get_username(message: Message, state: FSMContext):
    user.name = message.text

    await message.answer(
        text=f"Hi, *{user.name}*!\nYou have no expenses yet.\n"
             f"*Home* — /home\n",
        reply_markup=simple_keyboard(BEG_ACTIONS),
        parse_mode="Markdown"
    )

    await db.db_queries.insert_user(user.id, user.name)

    await state.set_state(States.good_choose)


@router.message(
    F.text.in_(BEG_ACTIONS),
    StateFilter(States.good_choose),
)
async def first_action(message: Message, state: FSMContext):

    if message.text == "Go to profile":
        await message.answer(
            text=f"*🏠HOME*\n\n*Today wastes:*\n\n*Daily wastes:*\n",
            reply_markup=simple_keyboard(HOME_PAGE_ACTIONS),
            parse_mode="Markdown"
        )

        await state.set_state(States.user_on_profile)


@router.message(
    StateFilter(States.good_choose),
)
async def first_action(message: Message):
    await message.answer(
        text="Please select one of the suggested actions",
        reply_markup=simple_keyboard(BEG_ACTIONS)
    )
