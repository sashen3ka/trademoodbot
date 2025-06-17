import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from handlers.trade_flow import register_handlers
from handlers.ai_chat import handle_ai_chat
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

register_handlers(dp)

from aiogram.types import WebAppInfo, KeyboardButton

menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add(
    types.KeyboardButton(
        text="📈 Открыть Mini App",
        web_app=types.WebAppInfo(url="https://trademoodbot.web.app/?_v=3")
    )
)
menu_keyboard.add("➕ Ввести новую сделку", "Обсудить с ИИ 🤖")

@dp.message_handler(commands=["menu", "start"])
async def menu_handler(message: types.Message):
    await message.answer("📱 Главное меню:", reply_markup=menu_keyboard)

dp.register_message_handler(handle_ai_chat, lambda m: m.text == "Обсудить с ИИ 🤖", state=None)

@dp.message_handler(lambda msg: msg.text == "⬅ Назад")
async def back_to_menu(message: types.Message):
    await menu_handler(message)

dp.register_message_handler(handle_ai_chat, lambda m: m.text not in [
    "➕ Ввести новую сделку",
    "Обсудить с ИИ 🤖",
    "⬅ Назад"
], state=None)

@dp.message_handler(content_types=ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    if message.web_app_data.data == "Обсудить с ИИ 🤖":
        await handle_ai_chat(message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
