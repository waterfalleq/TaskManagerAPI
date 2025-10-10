import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.first_name}!")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))