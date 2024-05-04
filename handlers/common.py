import logging
from typing import Union

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_keyboard import simple_keyboard
from keyboards.button_text import HOME_PAGE_ACTIONS

from states.States import States

from moduls.User import User
from moduls.wastes_actions import find_today_wastes, wastes_to_string_home

from db.db_queries import find_user_by_id, get_user_name, get_user_wastes

router = Router()

user = User("", 0, [])


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):

    user.id = message.from_user.id
    is_profile = await find_user_by_id(user.id)

    await state.clear()

    if is_profile:

        user.name = await get_user_name(user.id)
        user.wastes = await get_user_wastes(user.id)

        await message.answer(
            text=f"Hi *{user.name}*, I'm a financial accounting bot *Casherio*\n\nYou already have a profile! — /home",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="Markdown"
        )
        await state.set_state(States.user_on_profile)
    else:

        username_from_tg = message.from_user.username

        await message.answer(
            text="Hello, I'm *Casherio* finance accounting bot.\n\nEnter your profile name",
            reply_markup=simple_keyboard([username_from_tg]) if username_from_tg else ReplyKeyboardRemove(),
            parse_mode="Markdown"
        )
        await state.set_state(States.creating_username)


@router.message(Command(commands=["home"]))
async def cmd_home(message: Message, state: FSMContext):

    today_wastes = []
    daily_wastes = []

    try:
        user.id = message.from_user.id
        user.wastes = await get_user_wastes(user.id)
        today_wastes = "\n".join(wastes_to_string_home(find_today_wastes(user.wastes))[0])
        daily_wastes = "\n".join(wastes_to_string_home(user.wastes)[1])
    except Exception as err:
        logging.error(f"[cmd_home action] Failed to find wastes of user with id {user.id}", err)

    await message.answer(
        text=f"*🏠HOME*\n\n*Today wastes:*\n{today_wastes}\n\n*Daily wastes:*\n{daily_wastes}",
        reply_markup=simple_keyboard(HOME_PAGE_ACTIONS),
        parse_mode="Markdown"
    )

    await state.set_state(States.user_on_profile)


@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "cancel")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_state(Union[None])
    await message.answer(
        text="Please wait", reply_markup=ReplyKeyboardRemove()
    )
