from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import StateFilter
from states.States import States

from keyboards.button_text import HOME_PAGE_ACTIONS, WASTES_TYPES, STATISTICS_PERIODS
from keyboards.simple_keyboard import simple_keyboard


router = Router()


@router.message(
    StateFilter(States.user_on_profile),
    F.text.in_(HOME_PAGE_ACTIONS),
    F.text.split().len() == 3
)
async def create_an_expense(message: Message, state: FSMContext):
    if message.text.lower() == "create an expense":

        await message.answer(
            text="*Select type of expense:*",
            reply_markup=simple_keyboard(WASTES_TYPES),
            parse_mode="Markdown"
        )

        await state.set_state(States.creating_waste)


@router.message(
    StateFilter(States.user_on_profile),
    F.text.in_(HOME_PAGE_ACTIONS)
)
async def go_to_statistics(message: Message, state: FSMContext):
    if message.text.lower() == "statistics":

        await message.answer(
            text="*Select period of statistics:*",
            reply_markup=simple_keyboard(STATISTICS_PERIODS),
            parse_mode="Markdown"
        )

        await state.set_state(States.show_statistics)
