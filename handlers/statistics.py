from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from states.States import States

from datetime import datetime, timedelta

from keyboards.inline_keyboard_for_weeks import inline_keyboard_weeks
from keyboards.inline_keyboard_for_days import inline_keyboard_days
from keyboards.simple_keyboard import simple_keyboard
from keyboards.button_text import BACK, STATISTICS_PERIODS

from moduls.wastes_actions import to_string_last7_statistics, to_string_last30_statistics, to_string_lastday_statistics, to_string_all_expenses

from db.db_queries import get_expenses_for_period, get_all_expenses


router = Router()


@router.message(
    F.text.lower() == "last day",
    StateFilter(States.show_statistics)
)
async def get_daily_stat(message: Message):
    if message.text.lower() == "last day":

        today_date = datetime.now()

        start_date = today_date.replace(year=2024, hour=0, minute=0, second=0)
        end_date = today_date.replace(year=2024, hour=23, minute=59, second=59)

        str_date_for_ans = today_date.strftime("%d %b %Y")

        expenses = await get_expenses_for_period(user_id=message.from_user.id, start_date=start_date, end_date=end_date)

        await message.answer(
            text=f"*All wastes for the {str_date_for_ans}:*\n\n{to_string_lastday_statistics(expenses)}",
            parse_mode="Markdown"
        )

        await message.answer(
            text="*Home — /home*",
            parse_mode="Markdown"
        )



@router.message(
    F.text.lower() == "last 7 days",
    StateFilter(States.show_statistics)
)
async def get_weekly_stat(message: Message):
    if message.text.lower() == "last 7 days":

        today_date = datetime.now()
        start_date = (today_date - timedelta(days=6)).replace(year=2024, hour=0, minute=0, second=0)
        end_date = today_date.replace(year=2024, hour=23, minute=59, second=59)

        expenses = await get_expenses_for_period(user_id=message.from_user.id, start_date=start_date, end_date=end_date)

        start_date_str_for_ans = start_date.strftime("%d %b")
        end_date_str_for_ans = end_date.strftime("%d %b %Y")

        to_string_days, days_dates = to_string_last7_statistics(expenses, start_date, end_date)

        await message.answer(
            text=f"*All wastes from {start_date_str_for_ans} to {end_date_str_for_ans}:*\n\n{to_string_days}",
            parse_mode="Markdown",
            reply_markup=inline_keyboard_days(days_dates, days_dates)
        )

        await message.answer(
            text="*Home — /home*",
            parse_mode="Markdown"
        )



@router.message(
    F.text.lower() == "last month",
    StateFilter(States.show_statistics)
)
async def get_monthly_stat(message: Message):
    if message.text.lower() == "last month":

        today_date = datetime.now()
        first_day_of_curr_month = today_date.replace(day=1)
        start_date = (first_day_of_curr_month - timedelta(days=1)).replace(day=1, year=2024, hour=0, minute=0, second=0)
        end_date = (first_day_of_curr_month - timedelta(days=1)).replace(year=2024, hour=23, minute=59, second=59)

        month_name = start_date.strftime("%B").capitalize()

        expenses = await get_expenses_for_period(user_id=message.from_user.id, start_date=start_date, end_date=end_date)

        to_string_weeks, week_days_dates = to_string_last30_statistics(expenses, start_date=start_date, end_date=end_date)

        inline_btns_texts = []
        callback_texts = []

        for line in week_days_dates.values():
            start_date, end_date = line[1:]
            inline_btns_texts.append(f"From {start_date} to {end_date}")
            callback_texts.append(f"{'_'.join(start_date.split())}_{'_'.join(end_date.split())}")

        await message.answer(
            text=f"*Wastes for {month_name}:*\n\n"
                 f"{to_string_weeks}",
            parse_mode="Markdown",
            reply_markup=inline_keyboard_weeks(inline_btns_texts, callback_texts)
        )

        await message.answer(
            text="*Home — /home*",
            parse_mode="Markdown"
        )


@router.message(
    F.text.lower() == "all expenses",
    StateFilter(States.show_statistics)
)
async def get_all_stat(message: Message, state: FSMContext):
    all_expenses = await get_all_expenses(user_id=message.from_user.id)

    if len(all_expenses) > 30:
        await message.answer(
            text=f"*Too many expenses lines for tg message*\n"
                 f"I can create for your:\n"
                 f"*/txt* file\n",
            reply_markup=simple_keyboard(BACK),
            parse_mode="Markdown"
        )
        await state.set_state(States.sending_file)
    else:
        await message.answer(
            parse_mode="Markdown",
            text="\n".join(to_string_all_expenses(all_expenses)),
        )

    await message.answer(
        text="*Home — /home*",
        parse_mode="Markdown"
    )


@router.callback_query(F.data.split("_").len() == 4)
async def callback_weekly_stat(query: CallbackQuery):
    date_ranges = query.data.split('_')
    start_date_str, end_date_str = ' '.join(date_ranges[:2]), ' '.join(date_ranges[2:])

    start_date = datetime.strptime(' '.join(date_ranges[:2]), "%d %b").replace(year=2024, hour=0, minute=0, second=0)
    end_date = datetime.strptime(' '.join(date_ranges[2:]), "%d %b").replace(year=2024, hour=23, minute=59, second=59)

    expenses = await get_expenses_for_period(query.from_user.id, start_date, end_date)
    to_string_days, days_dates = to_string_last7_statistics(expenses, start_date, end_date)

    await query.message.answer(
        text=f"*All wastes from {start_date_str} to {end_date_str}:*\n\n{to_string_days}",
        parse_mode="Markdown",
        reply_markup=inline_keyboard_days(days_dates, days_dates)
    )
    await query.message.answer(
        text="*Home — /home*",
        parse_mode="Markdown"
    )


@router.callback_query(F.data.split(" ").len() == 2)
async def callback_day_stat(query: CallbackQuery):
    start_date = datetime.strptime(query.data, "%d %b").replace(year=2024, hour=0, minute=0, second=0)
    end_date = datetime.strptime(query.data, "%d %b").replace(year=2024, hour=23, minute=59, second=59)

    day_date_str_for_ans = start_date.strftime("%d %b %Y")

    expenses = await get_expenses_for_period(user_id=query.from_user.id, start_date=start_date, end_date=end_date)

    await query.message.answer(
        text=f"*All wastes for the {day_date_str_for_ans}:*\n\n{to_string_lastday_statistics(expenses)}",
        parse_mode="Markdown"
    )

    await query.message.answer(
        text="Home — */home*",
        parse_mode="Markdown"
    )

@router.message(
    F.text.lower() == "back"
)
async def back_to_select_stat_period(message: Message):
    await message.answer(
        text="*Select period of statistics:*",
        reply_markup=simple_keyboard(STATISTICS_PERIODS),
        parse_mode="Markdown"
    )

