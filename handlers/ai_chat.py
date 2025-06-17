from aiogram import types
from firebase import db
from google.cloud import firestore
from ai_helper import get_ai_response
from intent_parser import parse_user_intent
from handlers.steps.constants import EMOTION_DETAILS


shown_prompt_users = set()  # временное хранилище

def format_trade(t: dict) -> str:
    asset = t.get("asset", "?")
    pnl = t.get("pnl_percent", 0)
    usd = t.get("usd_pnl", 0)
    emotion_code = t.get("emotion_code", "")
    comment = t.get("comment")

    emoji = EMOTION_DETAILS.get(emotion_code, {}).get("emoji", "")
    emotion_label = EMOTION_DETAILS.get(emotion_code, {}).get("label", "")
    emotion = f"{emoji} {emotion_label}" if emoji else emotion_code

    text = f"📌 Актив: {asset}\n📈 Результат: {pnl}%\n💰 Прибыль: {usd}$"
    if emotion:
        text += f"\n🧠 Эмоция: {emotion}"
    if comment:
        text += f"\n📝 Комментарий: «{comment}»"
    return text


async def handle_ai_chat(message: types.Message):
    # Первое приветствие без вызова ИИ
    if message.from_user.id not in shown_prompt_users:
        shown_prompt_users.add(message.from_user.id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("⬅ Назад")
        await message.answer("🧠 Я готов к разбору твоих сделок. Напиши, что хочешь обсудить.", reply_markup=keyboard)
        return

    if message.text.strip().lower() in ["стоп", "/стоп"]:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("➕ Ввести новую сделку", "📊 Посмотреть статистику", "Обсудить с ИИ 🤖")
        await message.answer("📱 Главное меню:", reply_markup=keyboard)
        shown_prompt_users.discard(message.from_user.id)
        return

    user_id = str(message.from_user.id)
    user_input = message.text.strip()

    intent = await parse_user_intent(user_input)
    mode = intent.get("mode", "general")

    messages = []

    if mode == "trade":
        trades_ref = db.collection("users").document(user_id).collection("trades")
        docs = trades_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(5).stream()
        trades = [doc.to_dict() for doc in docs if doc.exists]

        if trades:
            latest = trades[0]
            history = trades[1:]

            latest_text = format_trade(latest)
            history_lines = []
            for t in history:
                asset = t.get("asset", "?")
                pnl = t.get("pnl_percent", 0)
                usd = t.get("usd_pnl", 0)
                emotion_code = t.get("emotion_code", "")
                emotion_label = EMOTION_DETAILS.get(emotion_code, {}).get("label", emotion_code)
                history_lines.append(f"— {asset}: {pnl}%, {usd}$, {emotion_label}")

            content = f"Вот моя последняя сделка:\n\n{latest_text}"
            if history_lines:
                content += "\n\nПредыдущие сделки:\n" + "\n".join(history_lines)

            content += f"\n\nПользователь написал:\n{user_input}"

            messages = [
                {
                    "role": "system",
                    "content": (
                        "Ты профессиональный финансовый аналитик и коуч. Твоя задача — анализировать поведение трейдера на основе его сделок, "
                        "выявлять эмоциональные и стратегические ошибки, помогать улучшать принятие решений. Клиент занимается краткосрочной торговлей, "
                        "преимущественно спекуляциями на криптовалютах. Также возможны обсуждения по теме финансов, психологии торговли и управления рисками.\n\n"
                        "Отвечай так, как это сделал бы опытный риск-менеджер: строго, сдержанно, аналитично. Не используй эмодзи, markdown, заглавные буквы без необходимости. "
                        "Не пиши вводных лекций или очевидных советов, если об этом не просят. Формулируй чётко и по делу. Ограничь длину ответа: не более 500 символов по умолчанию, если пользователь не попросит детальнее."
                    )
                },
                {"role": "user", "content": content}
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "Ты профессиональный финансовый аналитик и коуч. Анализируй сделки и поведение трейдера. Отвечай строго, логично и без "
                        "эмоциональных украшений. Не используй эмодзи, звёздочки, markdown, заглавные буквы без причины. Пиши просто, "
                        "деловым языком, как эксперт по рискам. Ограничь длину ответа: не более 500 символов по умолчанию, если пользователь не попросит детальнее."
                    )
                },
                {"role": "user", "content": "У пользователя пока нет сделок.\n" + user_input}
            ]
    else:
        messages = [
            {
                "role": "system",
                "content": (
                    "Ты финансовый аналитик. Отвечай строго, логично и сдержанно. Не используй эмодзи, markdown, звёздочки или "
                    "стилистические украшения. Говори по делу, избегай эмоциональности. Ограничь длину ответа: не более 500 символов по умолчанию, если пользователь не попросит детальнее."
                )
            },
            {"role": "user", "content": user_input}
        ]

    max_tokens = 500
    if any(word in user_input.lower() for word in ["подробнее", "разверни", "детальнее", "поясни"]):
        max_tokens = 1200

    reply = await get_ai_response(messages, max_tokens=max_tokens)
    await message.answer(reply)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("⬅ Назад")
    if message.from_user.id not in shown_prompt_users:
        await message.answer("Можешь продолжить или вернуться в меню:", reply_markup=keyboard)
        shown_prompt_users.add(message.from_user.id)
    else:
        await message.answer("", reply_markup=keyboard)


# Регистрировать этот хендлер можно как:
# dp.register_message_handler(handle_ai_chat, state=None)  # или в нужном режиме
