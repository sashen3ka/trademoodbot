# server.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import parse_qsl
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # добавь это в .env файл

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # в проде лучше ограничить
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_signature(init_data: str, bot_token: str) -> bool:
    parsed = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = parsed.pop("hash", None)

    if not received_hash:
        return False

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(computed_hash, received_hash)

@app.post("/verify")
async def verify_telegram(request: Request):
    body = await request.json()
    init_data = body.get("initData", "")

    is_valid = check_signature(init_data, BOT_TOKEN)

    if is_valid:
        parsed = dict(parse_qsl(init_data))
        return { "verified": True, "userId": parsed.get("user", "").split(":")[1].split(",")[0] }
    else:
        return { "verified": False }
