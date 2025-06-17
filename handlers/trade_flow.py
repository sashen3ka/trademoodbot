from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from firebase import db
from handlers.steps.emotion_step import ask_emotion, register_emotion_handlers
from handlers.steps.comment_step import ask_comment, register_comment_handlers
from handlers.steps.stats import show_statistics


class TradeState(StatesGroup):
    asset = State()
    pnl_percent = State()
    usd_pnl = State()

def register_handlers(dp: Dispatcher):
    register_emotion_handlers(dp)
    register_comment_handlers(dp)

    @dp.message_handler(commands=["add"])
    async def start_trade(message: types.Message, state: FSMContext):
        await message.answer("📌 Введи актив (например: BTCUSDT):")
        await TradeState.asset.set()

    @dp.message_handler(state=TradeState.asset)
    async def process_asset(message: types.Message, state: FSMContext):
        await state.update_data(asset=message.text.strip())
        await message.answer("📈 Какой результат в процентах? (например: +2.5, -1.2, 0.3%)")
        await TradeState.pnl_percent.set()

    @dp.message_handler(state=TradeState.pnl_percent)
    async def process_pnl(message: types.Message, state: FSMContext):
        try:
            text = message.text.strip().replace('%', '').replace(',', '.')
            pnl = float(text)
        except ValueError:
            await message.answer("❗ Введи число в процентах, например +2.5 или -1.2")
            return

        await state.update_data(pnl_percent=pnl)
        await message.answer("💰 Сколько ты заработал или потерял в долларах?\nНапример: +80, -120")
        await TradeState.usd_pnl.set()

    @dp.message_handler(state=TradeState.usd_pnl)
    async def process_usd_pnl(message: types.Message, state: FSMContext):
        try:
            text = message.text.strip().replace(',', '.')
            usd = float(text)
        except ValueError:
            await message.answer("❗ Это не похоже на число. Напиши, сколько ты заработал или потерял в $: например +100, -35, 0.")
            return

        await state.update_data(usd_pnl=usd)

        # Переход к шагу выбора эмоции
        await ask_emotion(message, state)

    @dp.message_handler(commands=["menu"])
    async def show_main_menu(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            types.KeyboardButton("➕ Ввести сделку"),
            types.KeyboardButton("📊 Посмотреть статистику"),
            types.KeyboardButton("Обсудить с ИИ 🤖")
        ]
        keyboard.add(*buttons)
        await message.answer("📱 Главное меню:", reply_markup=keyboard)

    @dp.message_handler(lambda msg: msg.text == "➕ Ввести новую сделку")
    async def start_trade_button(message: types.Message, state: FSMContext):
        await start_trade(message, state)

    @dp.message_handler(lambda msg: msg.text == "📊 Посмотреть статистику")
    async def show_stats_button(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("📅 За 1 день", "🗓 За 7 дней", "📆 За месяц", "⬅ Назад")
        await message.answer("🗓️ Выбери за какой срок хочешь посмотреть статистику:", reply_markup=keyboard)

    @dp.message_handler(lambda msg: msg.text in ["📅 За 1 день", "🗓 За 7 дней", "📆 За месяц", "⬅ Назад"])
    async def handle_period_choice(message: types.Message):
        await show_statistics(message)

    @dp.message_handler(commands=["статистика"])
    async def stats_handler(message: types.Message):
        await show_statistics(message)
