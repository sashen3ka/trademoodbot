from ai_helper import get_ai_response
import json

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Ты помощник, который понимает, что хочет пользователь. "
        "Проанализируй его сообщение и верни JSON следующего формата:\n\n"
        "{\n"
        "  \"mode\": \"trade\" или \"general\",\n"
        "  \"asset\": \"название актива, если указано или \"\",\n"
        "  \"date\": \"дата, если есть в тексте, или \"\",\n"
        "  \"emotion\": \"эмоциональное состояние, если упоминается, или \"\"\n"
        "}\n\n"
        "Если пользователь хочет просто поговорить — mode должен быть \"general\". "
        "Если он говорит о сделке, используй mode: \"trade\"."
    )
}

async def parse_user_intent(user_input: str) -> dict:
    messages = [
        SYSTEM_PROMPT,
        {"role": "user", "content": user_input}
    ]

    try:
        content = await get_ai_response(messages, temperature=0.3)
        if isinstance(content, str):
            content = content.strip()
            if content.startswith("```"):
                content = content.strip("`").strip()
                if content.startswith("json"):
                    content = content[4:].strip()
            parsed = json.loads(content)
        else:
            parsed = content
        if isinstance(parsed, dict) and "mode" in parsed:
            return parsed
    except json.JSONDecodeError as e:
        print(f"❌ JSON ошибка: {e} → {content}")
    except Exception as e:
        print(f"❌ Ошибка распознавания намерения: {e}")

    return {"mode": "general", "asset": "", "date": "", "emotion": ""}
