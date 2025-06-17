from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from google.cloud import firestore
from handlers.steps.comment_step import ask_comment


class TradeStateExtended(StatesGroup):
    emotion = State()

emotions = [
    {"code": "focused_entry", "emoji": "🧘", "label": "Спокоен, уверен"},
    {"code": "doubtful_entry", "emoji": "😰", "label": "В сомнении, тревожно"},
    {"code": "revenge_mode", "emoji": "😡", "label": "Хочу отыграться"},
    {"code": "confused_entry", "emoji": "🌀", "label": "Потерян"},
    {"code": "fomo_entry", "emoji": "🚀", "label": "ФОМО (боялся упустить)"},
    {"code": "overconfident", "emoji": "😎", "label": "Самоуверен"}
]



def get_emotion_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text=f"{e['emoji']} {e['label']}", callback_data=f"emotion:{e['code']}")
        for e in emotions
    ]
    kb.add(*buttons)
    return kb

async def ask_emotion(message: types.Message, state: FSMContext):
    await message.answer("🧠 Какое у тебя было состояние перед или во время сделки?", reply_markup=get_emotion_keyboard())
    await TradeStateExtended.emotion.set()

async def process_emotion(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data.split(":")[1]
    await state.update_data(emotion_code=code)

    # Переход к шагу с комментарием
    await ask_comment(callback_query.message, state)

def register_emotion_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(process_emotion, lambda c: c.data.startswith("emotion:"), state=TradeStateExtended.emotion)
