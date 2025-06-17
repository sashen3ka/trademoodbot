import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "deepseek/deepseek-chat-v3-0324:free"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

async def get_ai_response(messages: list[dict], model: str = DEFAULT_MODEL, temperature: float = 0.8, max_tokens: int = 500) -> str:
    """
    Отправляет сообщения в OpenRouter и возвращает ответ от модели.

    :param messages: список сообщений [{"role": "user", "content": "..."}, ...]
    :param model: название модели (по умолчанию deepseek-chat-v3)
    :param temperature: "креативность" модели
    :return: строка-ответ
    """
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(OPENROUTER_URL, headers=HEADERS, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                print("❌ Превышен лимит запросов к OpenRouter")
                return "⚠️ Превышен лимит запросов к ИИ. Подожди немного и попробуй снова."
            else:
                print(f"❌ Ошибка OpenRouter: {e}")
                return "⚠️ Ошибка при обращении к ИИ. Попробуй позже."
        except Exception as e:
            print(f"❌ Неизвестная ошибка OpenRouter: {e}")
            return "⚠️ Ошибка при обращении к ИИ. Попробуй позже.""⚠️ Ошибка при обращении к ИИ. Попробуй позже."
