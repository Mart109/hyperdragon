import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)

TOKEN = "8081082371:AAHC8Vgj6t72s-ef1cP64BEdET7-2zWGN38"

router = Router()


# Клавиатура с Web App кнопкой
def web_app_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Открыть приложение", web_app=WebAppInfo(url="https://example.com"))]
        ],
        resize_keyboard=True
    )


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {message.from_user.full_name}!",
        reply_markup=web_app_keyboard()
    )


# Обрабатываем данные из Web App
@router.message(F.web_app_data)
async def web_app_handler(message: Message) -> None:
    try:
        web_app_data = message.web_app_data
        data = json.loads(web_app_data.data)
        await message.answer(f"✅ Получены данные: {data}")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


async def main() -> None:
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())