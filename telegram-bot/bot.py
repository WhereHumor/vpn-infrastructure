import asyncio
import os
from datetime import datetime, timedelta, timezone
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
REMNAWAVE_API_URL = os.getenv("REMNAWAVE_API_URL")
REMNAWAVE_API_TOKEN = os.getenv("REMNAWAVE_API_TOKEN")
SQUAD_UUID = os.getenv("SQUAD_UUID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def get_or_create_user(tg_id: int, username: str):
    """Проверяет, есть ли пользователь. Если есть - выдает ссылку, если нет - создает."""
    user_name = f"tg_{username}_{tg_id}"
    headers = {
        "Authorization": f"Bearer {REMNAWAVE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        # 1. ПЫТАЕМСЯ ПОЛУЧИТЬ ПОЛЬЗОВАТЕЛЯ ПО ИМЕНИ
        # Используем эндпоинт by-username, так как поиск по UUID не сработает
        get_url = f"{REMNAWAVE_API_URL}/api/users/by-username/{user_name}"
        
        async with session.get(get_url, headers=headers, ssl=False) as response:
            if response.status == 200:
                data = await response.json()
                # Пользователь найден, достаем его ссылку
                return data.get("response", {}).get("subscriptionUrl")
            elif response.status == 404:
                pass # Пользователя нет, идем дальше создавать

        # 2. ЕСЛИ НЕ НАЙДЕН (404) - СОЗДАЕМ НОВОГО (POST)
        post_url = f"{REMNAWAVE_API_URL}/api/users"
        expire_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
        payload = {
            "username": user_name,
            "expireAt": expire_date,
            "trafficLimitBytes": 107374182400, # 100 GB
            "trafficLimitStrategy": "MONTH",   # Сброс раз в месяц
            "activeInternalSquads": [SQUAD_UUID],
            "status": "ACTIVE"
        }

        async with session.post(post_url, json=payload, headers=headers, ssl=False) as response:
            if response.status in [200, 201]:
                data = await response.json()
                return data.get("response", {}).get("subscriptionUrl")
            else:
                error_text = await response.text()
                print(f"❌ Ошибка API Remnawave: {response.status} - {error_text}")
                return None

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    waiting_msg = await message.answer("⏳ Секунду обновляю данные...")
    
    username = message.from_user.username or "user"
    tg_id = message.from_user.id
    
    sub_url = await get_or_create_user(tg_id, username)
    
    if sub_url:
        text = (
            f"✅ <b>Твой доступ готов!</b>\n\n"
            f"🔗 <b>Ссылка на подписку:</b>\n<code>{sub_url}</code>\n\n"
            f"📥 Скопируй её и добавь в приложение <b>Happ</b>.\n"
            f"⚠️ <i>Не передавай ссылку третьим лицам!</i>"
        )
        await waiting_msg.edit_text(text, parse_mode="HTML")
    else:
        await waiting_msg.edit_text("❌ Ошибка. Проверь логи на сервере.", parse_mode="HTML")

async def main():
    print("🚀 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
