from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from backend.database import Database
from backend.config import Config
from backend.security.rate_limiter import rate_limit
from backend.security.data_validator import TelegramUpdateValidator, InputValidationError
from backend.cache.decorators import async_cache
import logging
from typing import Optional, Tuple

router = Router()
logger = logging.getLogger(__name__)

# Кэшируем клавиатуру на 1 час
@async_cache(ttl=3600, key_func=lambda user_id: f"ref_kb:{user_id}")
async def get_referral_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    """Генерация кэшированной клавиатуры"""
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🔗 Пригласить друга",
            url=f"t.me/{Config.BOT_USERNAME}?start=ref_{user_id}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="📊 Мои рефералы",
            callback_data=f"ref_stats:{user_id}"
        )
    )
    return builder.as_markup()

@router.message(Command("start"))
@rate_limit(calls=1, period=10, scope="user")  # Лимит: 1 запуск в 10 сек
async def cmd_start(message: types.Message):
    """
    Обработчик команды /start с:
    - Валидацией входящих данных
    - Защитой от спама
    - Кэшированием клавиатуры
    """
    try:
        # Валидация входящего сообщения
        validated_data = TelegramUpdateValidator.validate_message(message)
        user_id = validated_data['user_id']
        
        # Парсинг реферера с проверкой
        referrer_id: Optional[int] = None
        if len(message.text.split()) > 1:
            try:
                _, ref_code = message.text.split()
                if ref_code.startswith("ref_"):
                    referrer_id = int(ref_code.split('_')[1])
            except (ValueError, IndexError):
                logger.warning(f"Invalid ref code from {user_id}")

        # Регистрация в БД
        async with Database() as db:
            if not await db.register_user(
                user_id=user_id,
                username=validated_data['from']['full_name'],
                referrer_id=referrer_id
            ):
                raise InputValidationError("Ошибка регистрации")

            # Отправка сообщения с кэшированной клавиатурой
            await message.answer(
                "🐉 Добро пожаловать в Hype Drakon!\n\n"
                f"Ваш ID: {user_id}\n"
                "Приглашайте друзей и получайте бонусы!",
                reply_markup=await get_referral_keyboard(user_id)
            )

    except InputValidationError as e:
        logger.error(f"Validation error: {e}")
        await message.answer("❌ Ошибка ввода данных")
    except Exception as e:
        logger.critical(f"Start command failed: {e}", exc_info=True)
        await message.answer("⚠️ Произошла системная ошибка")

@router.callback_query(F.data.startswith("ref_stats:"))
@rate_limit(calls=3, period=60)  # Лимит 3 запроса в минуту
async def show_referrals(callback: types.CallbackQuery):
    """Просмотр рефералов с кэшированием"""
    try:
        user_id = int(callback.data.split(':')[1])
        
        # Кэшируем запрос к БД на 5 минут
        @async_cache(ttl=300, key_func=lambda uid: f"ref_stats:{uid}")
        async def get_stats(uid: int) -> Tuple[int, int]:
            async with Database() as db:
                count = await db.get_referrals_count(uid)
                bonus = count * Config.REFERRAL_BONUS
                return count, bonus

        count, bonus = await get_stats(user_id)
        
        await callback.message.edit_text(
            f"📊 Ваши рефералы: {count}\n"
            f"💰 Сумма бонусов: {bonus} монет",
            reply_markup=await get_referral_keyboard(user_id)
        )
    except Exception as e:
        logger.error(f"Referral stats error: {e}")
        await callback.answer("❌ Ошибка загрузки данных")

# Middleware для логирования
@router.message.middleware
async def log_commands_middleware(handler, event, data):
    logger.info(f"Processing {event.text} from {event.from_user.id}")
    return await handler(event, data)