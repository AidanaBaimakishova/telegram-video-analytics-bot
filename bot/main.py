import asyncio
import logging
import socket

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram import F

from core.query_handler import handle_query

socket.setdefaulttimeout(30)

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def start_handler(message: types.Message):
    await message.answer(
        "Привет! 👋\n"
        "Я бот для аналитики по видео.\n\n"
        "Примеры запросов:\n"
        "• Сколько всего просмотров?\n"
        "• Какой прирост просмотров?\n"
        "• Какой прирост просмотров за вчера?"
    )


async def text_handler(message: types.Message):
    try:
        print("TELEGRAM TEXT:", message.text)
        result = handle_query(message.text)
        await message.answer(str(result))
    except Exception:
        await message.answer("Произошла ошибка при обработке запроса")


async def main():
    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())
    dp.message.register(text_handler, F.text)

    logging.info("🤖 Aiogram-бот запущен")
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
