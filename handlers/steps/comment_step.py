from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from firebase import db
from google.cloud import firestore
from handlers.steps.constants import EMOTION_DETAILS


class TradeStateComment(StatesGroup):
    comment = State()
    comment_text = State()


async def ask_comment(message: types.Message, state: FSMContext):
    await message.answer("📝 Напиши комментарий к сделке:\n\nНапример:\n— «вошёл на автомате»\n— «всё по плану»\n— «эмоции мешали»")
    await TradeStateComment.comment_text.set()


async def process_comment_text(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text.strip())
    await finalize_trade(message, state)


async def finalize_trade(message_or_call, state: FSMContext):
    user_data = await state.get_data()
    user_id = str(message_or_call.from_user.id)
    asset = user_data.get("asset")
    pnl = user_data.get("pnl_percent")
    usd = user_data.get("usd_pnl")
    emotion = user_data.get("emotion_code")
    comment = user_data.get("comment")
    emoji = "📈" if pnl >= 0 else "📉"
    money_label = "Прибыль" if usd >= 0 else "Убыток"

    try:
        db.collection("users").document(user_id).collection("trades").document().set({
            "asset": asset,
            "pnl_percent": pnl,
            "usd_pnl": usd,
            "emotion_code": emotion,
            "comment": comment if comment else None,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

        detail = EMOTION_DETAILS.get(emotion)
        if detail:
            emotion_text = f"{detail['emoji']} {detail['label']}"
        else:
            emotion_text = "❓ Неизвестно"

        text = (
            f"Сделка записана:\n\n"
            f"📌 Актив: <b>{asset}</b>\n"
            f"{emoji} Результат: <b>{pnl}%</b>\n"
            f"💰 {money_label}: <b>{usd}$</b>\n"
            f"🧠 Эмоция: <b>{emotion_text}</b>"
        )

        if comment:
            text += f"\n📝 Комментарий: «{comment}»"

        await message_or_call.answer(text, parse_mode="HTML")

    except Exception as e:
        await message_or_call.answer(f"⚠️ Ошибка при сохранении сделки: {e}")

    await state.finish()
    await message_or_call.answer("Что дальше? Напиши /menu или нажми кнопку👇")


def register_comment_handlers(dp: Dispatcher):
    dp.register_message_handler(process_comment_text, state=TradeStateComment.comment_text)
