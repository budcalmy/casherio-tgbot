from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    creating_username = State()
    good_choose = State()
    user_on_profile = State()
    creating_waste = State()
    input_category_of_waste = State()
    input_sum_of_waste = State()
    show_statistics = State()
    on_daily_stat = State()
    on_weekly_stat = State()
    on_monthly_stat = State()
    sending_file = State()