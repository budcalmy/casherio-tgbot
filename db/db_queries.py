import os
from dotenv import load_dotenv

import asyncpg

import logging

from moduls.Waste import Waste

from datetime import datetime

logging.basicConfig(level=logging.INFO)

load_dotenv()

HOST = os.getenv("HOST")
PASSWRD = os.getenv("PASSWORD")
USER = os.getenv("USER")
PORT = os.getenv("PORT")
DB_NAME = os.getenv("DB_NAME")


async def insert_user(user_id, user_name):
    connection = await asyncpg.connect(
        host=HOST,
        database=DB_NAME,
        user=USER,
        password=PASSWRD
    )

    try:
        await connection.execute(
            "INSERT INTO users (user_id, username) VALUES ($1, $2)",
            user_id, user_name
        )

        logging.info(f"[insert_user] Successfully insert user {user_name} with id {user_id} into db table")

    except Exception as err:
        logging.error(f"[insert_user] Failed to insert {user_name} with id {user_id} into db", err)
    finally:
        await connection.close()


async def find_user_by_id(user_id):
    connection = await asyncpg.connect(
        host=HOST,
        database=DB_NAME,
        user=USER,
        password=PASSWRD
    )

    result = None

    try:
        result = await connection.fetchrow(
            "SELECT * FROM users WHERE user_id = $1",
            user_id
        )

        if result:
            logging.info(f"[find_user_by_id] Successfully find user with id {user_id} in db table")
    except Exception as err:
        logging.error(f"[find_user_by_id] Error finding moduls with id: {user_id}", err)
    finally:
        await connection.close()
    return result


async def get_user_wastes(user_id):

    connection = await asyncpg.connect(
        host=HOST,
        database=DB_NAME,
        user=USER,
        password=PASSWRD
    )

    try:
        rows = await connection.fetch(
            "SELECT * FROM wastes WHERE user_id = $1",
            user_id
        )

        all_wastes = []
        for row in rows:
            all_wastes.append(Waste(
                row['user_id'],
                row['category'],
                row['type'],
                float(row['sum']),
                row['time']))

        if all_wastes:
            logging.info(f"[get_user_wastes] GET EXPENSES FROM DB user_id: {user_id}")

        return all_wastes

    except Exception as err:
        logging.error(f"[get_user_wastes] Failed to get users id: {user_id} wastes", err)
    finally:
        await connection.close()

    return []


async def get_user_name(user_id):

    connection = await asyncpg.connect(
        host=HOST,
        database=DB_NAME,
        user=USER,
        password=PASSWRD
    )

    try:
        row = await connection.fetch("SELECT username FROM users WHERE user_id = $1", user_id)
        user_name = row[0]['username']

        if user_name:
            logging.info(f"[get_user_name] Successfully find username of user_id {user_id}: {user_name}")
    except Exception as err:
        logging.error(f"[get_user_name] Failed to find user_name for user_id {user_id}", err)
        user_name = None
    finally:
        await connection.close()

    return user_name


async def insert_user_waste(waste):
    connection = await asyncpg.connect(
        host=HOST,
        database=DB_NAME,
        user=USER,
        password=PASSWRD
    )

    try:
        await connection.execute(
            '''
            INSERT INTO wastes (user_id, category, type, sum, time)
            VALUES ($1, $2, $3, $4, $5)
            ''',
            waste.user_id, waste.category, waste.type, str(waste.sum), waste.time
        )

        logging.info(f"[insert_user_waste] Successfully insert user expense: user_id - {waste.user_id}")

    except Exception as err:
        logging.error(f"[insert_user_waste] Failed to insert waste in table with user_id {waste.user_id}", err)
    finally:
        await connection.close()


async def get_expenses_for_period(user_id: int, start_date: datetime, end_date: datetime):

    connection = await asyncpg.connect(
        host=HOST,
        database=DB_NAME,
        user=USER,
        password=PASSWRD
    )

    range_expenses = []

    try:

        query = "SELECT * FROM wastes WHERE user_id = $1"
        rows = await connection.fetch(query, user_id)

        for row in rows:
            flag = False
            datetime_time = datetime.strptime(row['time'], "%d %b %H:%M").replace(year=2024)
            if row['type'] == "usually":
                if start_date <= datetime_time <= end_date:
                    flag = True
            elif row['type'] == "daily":
                if datetime_time <= end_date:
                    flag = True

            if flag:
                range_expenses.append(Waste(
                    row['user_id'],
                    row['category'],
                    row['type'],
                    float(row['sum']),
                    row['time']
                ))

        if rows:
            logging.info(f"[get_expenses_for_period] Successfully fetched range expenses from DB")

    except Exception as err:
        logging.error("[get_expenses_for_period] Failed to fetch range expenses from DB", err)
    finally:
        await connection.close()

    return range_expenses


async def get_all_expenses(user_id: int):
    connection = await asyncpg.connect(
        host=HOST,
        database=DB_NAME,
        user=USER,
        password=PASSWRD
    )

    expenses = []

    try:
        rows = await connection.fetch("SELECT * FROM wastes WHERE user_id = $1", user_id)

        for row in rows:
            expenses.append(Waste(
                        row['user_id'],
                        row['category'],
                        row['type'],
                        float(row['sum']),
                        row['time']
                    ))

        if rows:
            logging.info(f"[get_all_expenses] Successfully get all expenses of user_id {user_id}")
    except Exception as err:
        logging.error(f"[get_all_expenses] Failed to fetch all expenses of user_if {user_id}")
    finally:
        await connection.close()

    return expenses



