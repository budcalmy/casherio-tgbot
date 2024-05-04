import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import Message

from handlers import common, beg_actions, home, wastes, statistics, sending_files

from aiogram.types.input_file import FSInputFile

from config import FILE_PATH, BOT_TOKEN


path = FILE_PATH


async def main():
    print("Bot started")

    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher()

    dp.include_routers(common.router, beg_actions.router, wastes.router, home.router, statistics.router, sending_files.router)

    @dp.message(Command(commands=["txt"]))
    async def send_txt_file(message: Message):

        await sending_files.send_txt_file(message)

        document = FSInputFile(path)
        await bot.send_document(message.from_user.id, document)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())