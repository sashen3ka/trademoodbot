from firebase import db
from aiogram import types
from datetime import datetime, timedelta
from collections import defaultdict
from handlers.steps.constants import EMOTION_DETAILS

async def show_statistics(message: types.Message):
    if message.text == "⬅ Назад":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("➕ Ввести новую сделку", "📊 Посмотреть статистику", "Обсудить с ИИ 🤖")
        await message.answer("📱 Главное меню:", reply_markup=keyboard)
        return

    user_id = str(message.from_user.id)
    text_lower = message.text.lower()

    if "1 день" in text_lower:
        period_label = "1 день"
        days = 1
    elif "месяц" in text_lower:
        period_label = "30 дней"
        days = 30
    else:
        period_label = "7 дней"
        days = 7

    period_start = datetime.utcnow() - timedelta(days=days)

    trades_ref = db.collection("users").document(user_id).collection("trades")
    docs = trades_ref.where("timestamp", ">", period_start).stream()
    trades = [doc.to_dict() for doc in docs]

    if not trades:
        await message.answer(f"📊 За последние {period_label} сделок не найдено.")
        return

    total_trades = len(trades)
    valid_usd = [t["usd_pnl"] for t in trades if isinstance(t.get("usd_pnl"), (int, float))]
    total_usd = round(sum(valid_usd), 2)
    total_pct = sum(t.get("pnl_percent", 0) for t in trades)
    avg_pct = round(total_pct / total_trades, 2)

    emotions = defaultdict(list)
    for t in trades:
        code = t.get("emotion_code")
        if code in EMOTION_DETAILS:
            emotions[code].append(t)

    emotion_breakdown = ""
    for code, group in emotions.items():
        count = len(group)
        total_emotion_usd = sum(t.get("usd_pnl", 0) for t in group)
        avg_emotion_usd = round(total_emotion_usd / count, 2)
        detail = EMOTION_DETAILS[code]
        label = f"{detail['emoji']} {detail['label']}"
        emotion_breakdown += f"{label} → {avg_emotion_usd}$ ({count} сделок)\n"

    text = (
        f"📊 <b>Твоя статистика за {period_label}</b>:\n\n"
        f"Всего сделок: <b>{total_trades}</b>\n"
        f"Средний PNL: <b>{avg_pct}%</b>\n"
        f"Общий результат: <b>{total_usd}$</b>\n\n"
        f"{emotion_breakdown}"
    )

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📅 За 1 день", "🗓 За 7 дней", "📆 За месяц", "⬅ Назад")

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
