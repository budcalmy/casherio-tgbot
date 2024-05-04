from moduls.Waste import Waste
from datetime import datetime, timedelta

CURRENCY = '$'


def to_string_lastday_statistics(wastes: list[Waste]):
    if not wastes:
        return "*No last day expenses for statistics*"

    res_waste_list = []

    usual_wastes_by_categories = {}

    usual_total = 0
    daily_total = 0
    day_total = 0

    for waste in wastes:
        if waste.type == "usually":
            if waste.category not in usual_wastes_by_categories:
                usual_wastes_by_categories[waste.category] = 0
            usual_wastes_by_categories[waste.category] += waste.sum
            usual_total += waste.sum

        elif waste.type == "daily":
            daily_total += waste.sum

    for category in usual_wastes_by_categories.keys():
        res_waste_list.append(f"*{category}* — {CURRENCY}{round(usual_wastes_by_categories[category], 2)}")
        day_total += usual_wastes_by_categories[category]
    res_waste_list.append(f"\n+ {CURRENCY}{round(daily_total, 2)} *from daily*")
    day_total += daily_total

    res_waste_list.append(f"*\nTotal: {CURRENCY}{round(day_total, 2)}*")

    return "\n".join(res_waste_list)


def to_string_last7_statistics(wastes: list[Waste], start_date: datetime, end_date):
    if not wastes:
        return ["*No expenses for this 7 days*", {}]

    res_waste_list = []
    waste_by_days = {}
    daily_total = 0
    week_total = 0

    for waste in wastes:
        if waste.type == "daily":
            daily_total += waste.sum

    for waste in wastes:
        if waste.type == "usually":
            split_time = waste.time.split()
            time_key = " ".join(split_time[:2])

            if time_key not in waste_by_days:
                waste_by_days[time_key] = daily_total
            waste_by_days[time_key] += waste.sum

    for i in range((end_date - start_date + timedelta(days=1)).days):
        date_key = (start_date + timedelta(days=i)).strftime("%d %b")
        if date_key not in waste_by_days:
            waste_by_days[date_key] = 0
        res_waste_list.append(f"*{date_key}* — {CURRENCY}{round(waste_by_days[date_key], 2)}")
        week_total += waste_by_days[date_key]

    res_waste_list.append(f"\n*Total: {CURRENCY}{round(week_total, 2)}*")

    return ["\n".join(res_waste_list), list(waste_by_days.keys())]


def to_string_last30_statistics(wastes: list[Waste], start_date: datetime, end_date: datetime):
    if not wastes:
        return ["*No expenses for last month*", {}]

    wastes = sorted(wastes, key=lambda x: x.time)

    total_days = (end_date - start_date + timedelta(days=1)).days
    weeks_days = {}

    weeks_list = []

    total_month = 0

    for i in range(total_days // 7):
        start = start_date + timedelta(days=i * 7)
        end = start_date + timedelta(days=(i + 1) * 7 - 1)

        if i == total_days // 7 - 1:
            end = end_date

        start_str = start.strftime("%d %b")
        end_str = end.strftime("%d %b")

        weeks_days[i + 1] = [0, start_str, end_str]

        for waste in wastes:
            waste_datetime = datetime.strptime(waste.time, "%d %b %H:%M").replace(year=2024)

            if (waste.type == "usually" and start <= waste_datetime <= end) \
                    or (waste.type == "daily" and waste_datetime <= end):

                weeks_days[i + 1][0] += waste.sum

    for week_number in sorted(list(weeks_days.keys())):
        weeks_list.append(
            f"*{weeks_days[week_number][1]} to {weeks_days[week_number][2]}* — {CURRENCY}{round(weeks_days[week_number][0], 2)}")
        total_month += weeks_days[week_number][0]

    weeks_list.append(f"\n*Total:* {CURRENCY}{round(total_month, 2)}")

    return ["\n".join(weeks_list), weeks_days]


def to_string_all_expenses(wastes: list[Waste]):

    if not wastes:
        return ["*No wastes for statistics*"]

    wastes = sorted(wastes, key=lambda x: datetime.strptime(x.time, "%d %b %H:%M"))

    wastes_str_list = []
    total_sum = 0

    for waste in wastes:
        wastes_str_list.append(f"*{waste.category}* — {CURRENCY}{round(waste.sum, 2)} {waste.time}")
        total_sum += waste.sum

    wastes_str_list.append(f"\n\n*Total: {CURRENCY}{round(total_sum, 2)}*")

    return wastes_str_list


def find_today_wastes(waste_list):
    if not waste_list:
        return []

    now = datetime.now()
    curr_date_str = now.strftime("%d %b")

    today_wastes = []
    for waste in waste_list:
        waste_time = waste.time.split()
        if waste_time[0] + " " + waste_time[1] == curr_date_str:
            today_wastes.append(waste)
    return today_wastes


def wastes_to_string_home(wastes_list: list[Waste]):
    if not wastes_list:
        return [[], []]

    wastes = []
    daily_wastes = []
    daily_wastes_dict = {}
    for waste in wastes_list:
        if waste.type == "usually":
            wastes.append(
                f"{waste.category} — {CURRENCY}{round(waste.sum, 2)}    {waste.time}"
            )
        else:
            if waste.category not in daily_wastes_dict:
                daily_wastes_dict[waste.category] = 0
            daily_wastes_dict[waste.category] += waste.sum

    for category, sum in daily_wastes_dict.items():
        daily_wastes.append(f"{category} — {CURRENCY}{round(sum, 2)}")

    return [wastes, daily_wastes]
