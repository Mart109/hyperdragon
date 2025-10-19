import logging
import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from typing import Dict, List

from backend.database.db import Database
from backend.config import Config
from backend.game.combat import Combat

router = Router()
logger = logging.getLogger(__name__)

class GameplayHandlers:
    def __init__(self, db: Database, combat: Combat):
        self.db = db
        self.combat = combat

    async def handle_tap(self, callback: CallbackQuery, state: FSMContext):
        """Обработка тапа по дракону"""
        user_id = callback.from_user.id
        
        try:
            # Получаем игрока и его активного дракона
            player = self.db.get_player(user_id)
            if not player:
                await callback.answer("Сначала зарегистрируйтесь через /start")
                return
            
            dragon = self.db.get_active_dragon(user_id)
            if not dragon:
                await callback.answer("У вас нет активного дракона!")
                return

            # Проверка кулдауна
            last_tap = player.get('last_tap')
            if last_tap:
                last_tap_time = datetime.fromisoformat(last_tap) if isinstance(last_tap, str) else last_tap
                if datetime.now() - last_tap_time < timedelta(seconds=1):
                    await callback.answer("Подождите 1 секунду между тапами!")
                    return

            # Расчет награды
            base_reward = Config.BASE_DAMAGE
            dragon_bonus = dragon.get('attack', 0) * 0.1  # 10% от атаки дракона
            final_reward = max(1, int(base_reward + dragon_bonus))

            # Критический тап
            is_critical = random.random() < Config.CRIT_CHANCE
            if is_critical:
                final_reward *= 2

            # Обновляем данные
            self.db.execute(
                "UPDATE players SET coins = coins + ?, last_tap = ? WHERE user_id = ?",
                (final_reward, datetime.now().isoformat(), user_id)
            )

            # Отправляем результат
            dragon_name = dragon.get('name', 'Дракон')
            dragon_type = dragon.get('type', 'fire')
            
            message = (
                f"🐉 {dragon_name} ({dragon_type}) атакует!\n"
                f"💥 {'КРИТИЧЕСКИЙ ' if is_critical else ''}Удар!\n"
                f"💰 +{final_reward} монет\n"
                f"💎 Всего: {player['coins'] + final_reward} монет"
            )

            await callback.message.edit_text(
                message,
                reply_markup=self._create_main_menu()
            )
            
        except Exception as e:
            logger.error(f"Tap error: {e}")
            await callback.answer("Ошибка при обработке тапа")

    async def handle_dragons_list(self, message: Message):
        """Показать список драконов игрока"""
        user_id = message.from_user.id
        
        try:
            dragons = self.db.get_player_dragons(user_id)
            player = self.db.get_player(user_id)
            active_dragon_id = player.get('active_dragon_id') if player else None

            if not dragons:
                await message.answer(
                    "🐉 У вас пока нет драконов!\n"
                    "Приобретите первого дракона в магазине /shop",
                    reply_markup=self._create_shop_button()
                )
                return

            response = "🐉 Ваши драконы:\n\n"
            keyboard_buttons = []
            
            for dragon in dragons:
                is_active = dragon['id'] == active_dragon_id
                status = "✅ АКТИВЕН" if is_active else "⚪"
                
                response += (
                    f"{status} {dragon['name']} ({dragon['type']})\n"
                    f"⚔️ Атака: {dragon.get('attack', 10)} | "
                    f"🛡️ Защита: {dragon.get('defense', 5)} | "
                    f"❤️ Здоровье: {dragon.get('health', 100)}\n"
                    f"⭐ Уровень: {dragon.get('level', 1)} | "
                    f"📊 Опыт: {dragon.get('experience', 0)}/100\n\n"
                )
                
                if not is_active:
                    keyboard_buttons.append([
                        InlineKeyboardButton(
                            text=f"Выбрать {dragon['name']}",
                            callback_data=f"select_dragon_{dragon['id']}"
                        )
                    ])

            keyboard_buttons.append([
                InlineKeyboardButton(text="🛒 Магазин драконов", callback_data="shop_dragons"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")
            ])

            await message.answer(
                response,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            )
            
        except Exception as e:
            logger.error(f"Dragons list error: {e}")
            await message.answer("Ошибка при загрузке драконов")

    async def handle_select_dragon(self, callback: CallbackQuery):
        """Выбор активного дракона"""
        user_id = callback.from_user.id
        dragon_id = callback.data.replace("select_dragon_", "")
        
        try:
            success = self.db.set_active_dragon(user_id, dragon_id)
            
            if success:
                dragon = self.db.get_dragon(dragon_id)
                await callback.message.edit_text(
                    f"✅ Теперь ваш активный дракон: {dragon['name']} ({dragon['type']})!",
                    reply_markup=self._create_main_menu()
                )
            else:
                await callback.answer("Ошибка выбора дракона")
                
        except Exception as e:
            logger.error(f"Select dragon error: {e}")
            await callback.answer("Произошла ошибка")

    async def handle_pvp_battle(self, callback: CallbackQuery):
        """Начать PvP бой"""
        user_id = callback.from_user.id
        
        try:
            # Проверяем наличие дракона
            dragon = self.db.get_active_dragon(user_id)
            if not dragon:
                await callback.answer("У вас нет активного дракона для боя!")
                return

            # Ищем случайного противника
            all_players = self.db.fetch_all(
                "SELECT user_id FROM players WHERE user_id != ? AND active_dragon_id IS NOT NULL",
                (user_id,)
            )
            
            if not all_players:
                await callback.answer("Сейчас нет доступных противников")
                return

            opponent = random.choice(all_players)
            battle_result = self.combat.pvp_battle(user_id, opponent['user_id'])
            
            if 'error' in battle_result:
                await callback.answer(f"Ошибка боя: {battle_result['error']}")
                return

            # Формируем результат боя
            winner_id = battle_result['winner']
            is_winner = winner_id == user_id
            is_draw = winner_id is None
            
            opponent_dragon = battle_result['player2_dragon']
            battle_log = battle_result['battle_log']
            
            # Создаем красивый отчет о бое
            result_text = self._format_battle_result(
                user_id, opponent['user_id'], 
                dragon, opponent_dragon,
                battle_result, is_winner, is_draw
            )
            
            # Награда за бой
            if is_winner:
                reward = 50
                self.db.execute(
                    "UPDATE players SET coins = coins + ? WHERE user_id = ?",
                    (reward, user_id)
                )
                result_text += f"\n\n🎉 Победа! +{reward} монет"
            elif is_draw:
                reward = 10
                self.db.execute(
                    "UPDATE players SET coins = coins + ? WHERE user_id = ?",
                    (reward, user_id)
                )
                result_text += f"\n\n🤝 Ничья! +{reward} монет"
            else:
                result_text += f"\n\n💔 Поражение! Попробуйте еще раз"

            await callback.message.edit_text(
                result_text,
                reply_markup=self._create_main_menu(),
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"PvP battle error: {e}")
            await callback.answer("Ошибка при запуске боя")

    def _format_battle_result(self, player1_id, player2_id, dragon1, dragon2, battle_result, is_winner, is_draw):
        """Форматирует результат боя в красивый текст"""
        battle_log = battle_result['battle_log']
        
        text = "⚔️ <b>РЕЗУЛЬТАТ БОЯ</b> ⚔️\n\n"
        text += f"🐲 {dragon1['name']} ({dragon1['type']}) vs 🐲 {dragon2['name']} ({dragon2['type']})\n\n"
        
        for round_data in battle_log:
            text += f"🔸 Раунд {round_data['round']}:\n"
            text += f"   {dragon1['name']} → {round_data['player1_damage']} урона\n"
            text += f"   {dragon2['name']} → {round_data['player2_damage']} урона\n"
            text += f"   ❤️ {round_data['player1_health']} vs {round_data['player2_health']}\n\n"
        
        if is_winner:
            text += "🎯 <b>ВЫ ПОБЕДИЛИ!</b> 🎯"
        elif is_draw:
            text += "🤝 <b>НИЧЬЯ!</b> 🤝"
        else:
            text += "💔 <b>ВЫ ПРОИГРАЛИ!</b> 💔"
            
        return text

    def _create_main_menu(self):
        """Создает главное меню"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🐉 Тапнуть дракона", callback_data="tap_dragon"),
                InlineKeyboardButton(text="⚔️ PvP Бой", callback_data="pvp_battle")
            ],
            [
                InlineKeyboardButton(text="📊 Мои драконы", callback_data="my_dragons"),
                InlineKeyboardButton(text="🛒 Магазин", callback_data="shop")
            ],
            [
                InlineKeyboardButton(text="👥 Профиль", callback_data="profile"),
                InlineKeyboardButton(text="📈 Топ игроков", callback_data="leaderboard")
            ]
        ])

    def _create_shop_button(self):
        """Создает кнопку магазина"""
        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🛒 Магазин", callback_data="shop")
        ]])

def register_gameplay_handlers(dp, db: Database, combat: Combat):
    """Регистрация всех обработчиков"""
    handler = GameplayHandlers(db, combat)
    
    # Тап по дракону
    router.callback_query(F.data == "tap_dragon")(handler.handle_tap)
    
    # Драконы
    router.callback_query(F.data == "my_dragons")(handler.handle_dragons_list)
    router.callback_query(F.data.startswith("select_dragon_"))(handler.handle_select_dragon)
    
    # PvP бои
    router.callback_query(F.data == "pvp_battle")(handler.handle_pvp_battle)
    
    dp.include_router(router)