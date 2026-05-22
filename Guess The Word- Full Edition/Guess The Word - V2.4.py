import random
import json
import os
import time
from datetime import datetime, timedelta

# --- LANGUAGE SYSTEM ---
class Language:
    def __init__(self):
        self.current_lang = "en"  # За замовчуванням англійська
        self.load_language()
    
    def load_language(self):
        self.strings = {
            "en": {
                # Main menu
                "welcome": "Welcome to {}!",
                "goodbye": "Goodbye, {}! Thanks for playing!",
                "stats": "STATS",
                "inventory": "INVENTORY",
                "shop": "SHOP",
                "bio": "INFO",
                "codes": "CODES",
                "bp": "BATTLE PASS",
                "event": "EVENT",
                "settings": "SETTINGS",
                "exit": "EXIT",
                "unknown_cmd": "Unknown command!",
                "level": "Lvl",
                "wallet": "💰",
                "rank": "Rank",
                "winrate": "Winrate",
                "wins": "Wins",
                "games": "Games",
                "effects": "Effects",
                "enter": "Press Enter...",
                "choice": "Your choice",
                
                # Game modes
                "classic": "Classic",
                "sniper": "Sniper",
                "hard": "Hard",
                "extreme": "Extreme",
                "one_in_hundred": "1 in 100",
                "marathon": "Marathon",
                "sapper": "Sapper",
                "time_attack": "Time Attack",
                "locked": "🔒 Lvl",
                "unlocked": "✅",
                "level_required": "🔒 Level {} required!",
                
                # Gameplay
                "mode": "MODE: {} (1-{})",
                "time_limit": "⏱️ Time limit: {} seconds!",
                "time_out": "💀 Time's up! Number was: {}",
                "no_attempts": "🔥 No attempts left! Use extinguisher? (y/n): ",
                "extinguisher_used": "🔋 Extinguisher used! +5 attempts!",
                "victory": "🏆 VICTORY! +{} XP | +{} 💰",
                "defeat": "💀 Defeat! Number was: {}",
                "higher": "🔼 Higher",
                "lower": "🔽 Lower",
                "invalid_input": "❌ Enter a number or command! Available: ",
                "lucky_trigger": "🍀 Lucky coin triggered! x2 reward!",
                
                # Commands
                "cmd_hint": "hint",
                "cmd_range": "range", 
                "cmd_info": "info",
                "cmd_hack": "hack",
                "cmd_xray": "xray",
                "hint_used": "🔍 Parity: {}",
                "even": "EVEN",
                "odd": "ODD",
                "range_used": "📡 Range: {}-{}",
                "info_used": "📊 Last digit: {}",
                "hack_used": "💻 +2 attempts!",
                "xray_used": "🩻 X-Ray: number between {} and {}",
                
                # Inventory
                "inventory_title": "INVENTORY",
                "normal_cases": "📦 Normal",
                "event_cases": "🎪 Event",
                "devices": "🛠️ Devices",
                "event_items": "🎐 Event Items",
                "open_case": "Open (wood/iron/gold/pumpkin/water) or Exit",
                "case_opened": "🎁 Got: {} 💰",
                "pumpkin_case": "🎃 Got: {}💰 + {}!",
                "water_case": "💧 Got: {}💰 + Bonus 100💰!",
                "case_obtained": "📦 Case obtained!",
                
                # Shop
                "shop_title": "SHOP",
                "devices_section": "🛠️ DEVICES",
                "cosmetics_section": "✨ COSMETICS", 
                "cases_section": "📦 CASES",
                "balance": "Balance",
                "purchased": "✅ Purchased!",
                "insufficient": "❌ Insufficient level or money!",
                "detector": "Detector",
                "extinguisher": "Extinguisher",
                "range_device": "Range",
                "analyst": "Analyst",
                "hack_device": "Hack",
                "xray_device": "X-Ray",
                "lucky_coin": "Lucky Coin",
                "premium": "Premium",
                "gold_nick": "Gold Nick",
                "insider": "Insider",
                "legend_aura": "Legend Aura",
                "rainbow_trail": "Rainbow Trail",
                "fire_effect": "Fire Effect",
                "ice_charm": "Ice Charm",
                "shadow_profile": "Shadow Profile",
                "angel_wings": "Angel Wings",
                
                # Battle Pass
                "bp_title": "BATTLE PASS V2.4",
                "bp_level": "Your level",
                "bp_xp": "BP XP",
                "next_rewards": "NEXT REWARDS",
                "reward_coin": "coins",
                "reward_cosmetic": "✨ Cosmetic",
                "reward_special": "🌟 Special",
                "bp_reward_claimed": "🎁 BATTLE PASS REWARD Level {}!",
                
                # Event
                "event_title": "SUMMER EVENT 2026",
                "event_time_left": "⏰ Time left: {} days {} hours",
                "event_ended": "⚠️ EVENT ENDED!",
                "event_bp": "🎪 EVENT BATTLE PASS",
                "event_level": "Level",
                "event_xp": "XP",
                "daily_missions": "📋 DAILY MISSIONS",
                "season_missions": "🏆 SEASON MISSIONS",
                "mission_complete": "✅ MISSION COMPLETE: {}",
                "mission_reward_xp": "📈 +{} XP",
                "mission_reward_event_xp": "🌞 +{} Event XP",
                "mission_reward_coins": "💰 +{} coins",
                "mission_reward_items": "🛠️ +{} {}",
                "mission_reward_cases": "📦 +{} {} cases",
                "mission_reward_cosmetic": "✨ Got cosmetic: {}",
                "event_bp_reward": "🎪 EVENT BP REWARD Level {}!",
                
                # Profile
                "profile_title": "PLAYER STATS",
                "nick": "Nick",
                "xp_bar": "XP",
                
                # Settings
                "settings_title": "SETTINGS",
                "language": "Language",
                "language_en": "English",
                "language_ua": "Ukrainian",
                "sound": "Sound Effects",
                "sound_on": "🔊 ON",
                "sound_off": "🔇 OFF",
                "animations": "Animations",
                "animations_on": "✨ ON",
                "animations_off": "💨 OFF",
                "difficulty": "Difficulty",
                "difficulty_easy": "Easy",
                "difficulty_normal": "Normal",
                "difficulty_hard": "Hard",
                "auto_save": "Auto-save",
                "auto_save_on": "✅ ON",
                "auto_save_off": "❌ OFF",
                "backup": "Create Backup",
                "reset": "Reset Settings",
                "saved": "✅ Settings saved!",
                "backup_created": "✅ Backup created!",
                "reset_done": "✅ Settings reset to default!",
                
                # Promo codes
                "enter_code": "🔑 CODE: ",
                "code_used": "❌ Code already used!",
                "code_invalid": "❌ Invalid code!",
                "code_success": "✨ {}",
                
                # Migration
                "migration_found": "🔄 Old save detected! Migrating...",
                "migration_success": "🔄 Migration successful! Please restart the game.",
                "migration_error": "❌ Migration error: {}"
            },
            "ua": {
                # Main menu
                "welcome": "Ласкаво просимо до {}!",
                "goodbye": "👋 До побачення, {}! Дякуємо за гру!",
                "stats": "СТАТИСТИКА",
                "inventory": "ІНВЕНТАР",
                "shop": "МАГАЗИН",
                "bio": "ІНФО",
                "codes": "КОДИ",
                "bp": "БП",
                "event": "ІВЕНТ",
                "settings": "НАЛАШТУВАННЯ",
                "exit": "ВИХІД",
                "unknown_cmd": "❌ Невідома команда!",
                "level": "Рівень",
                "wallet": "💰",
                "rank": "Ранг",
                "winrate": "Вінрейт",
                "wins": "Перемог",
                "games": "Ігор",
                "effects": "Ефекти",
                "enter": "Натисніть Enter...",
                "choice": "Ваш вибір",
                
                # Game modes
                "classic": "Класика",
                "sniper": "Снайпер",
                "hard": "Хард",
                "extreme": "Екстрим",
                "one_in_hundred": "1 з 100",
                "marathon": "Марафон",
                "sapper": "Сапер",
                "time_attack": "Часова Атака",
                "locked": "🔒 Рівень",
                "unlocked": "✅",
                "level_required": "🔒 Потрібен {} рівень!",
                
                # Gameplay
                "mode": "🎮 РЕЖИМ: {} (1-{})",
                "time_limit": "⏱️ Ліміт часу: {} секунд!",
                "time_out": "💀 Час вийшов! Число було: {}",
                "no_attempts": "🔥 Спроби вичерпано! Використати вогнегасник? (y/n): ",
                "extinguisher_used": "🔋 Вогнегасник використано! +5 спроб!",
                "victory": "🏆 ПЕРЕМОГА! +{} XP | +{} 💰",
                "defeat": "💀 Програш. Число було: {}",
                "higher": "🔼 Більше",
                "lower": "🔽 Менше",
                "invalid_input": "❌ Введіть число або команду! Доступні: ",
                "lucky_trigger": "🍀 Щаслива монета спрацювала! x2 нагороди!",
                
                # Commands
                "cmd_hint": "hint",
                "cmd_range": "range", 
                "cmd_info": "info",
                "cmd_hack": "hack",
                "cmd_xray": "xray",
                "hint_used": "🔍 Парність: {}",
                "even": "ПАРНЕ",
                "odd": "НЕПАРНЕ",
                "range_used": "📡 Межі: {}-{}",
                "info_used": "📊 Остання цифра: {}",
                "hack_used": "💻 +2 спроби!",
                "xray_used": "🩻 Рентген: число між {} та {}",
                
                # Inventory
                "inventory_title": "ІНВЕНТАР",
                "normal_cases": "📦 Звичайні",
                "event_cases": "🎪 Літні",
                "devices": "🛠️ Девайси",
                "event_items": "🎐 Літні предмети",
                "open_case": "Відкрити (wood/iron/gold/pumpkin/water) або Exit",
                "case_opened": "🎁 Випало: {} 💰",
                "pumpkin_case": "🎃 Випало: {}💰 + {}!",
                "water_case": "💧 Випало: {}💰 + Бонус 100💰!",
                "case_obtained": "📦 Кейс отримано!",
                
                # Shop
                "shop_title": "МАГАЗИН",
                "devices_section": "🛠️ ДЕВАЙСИ",
                "cosmetics_section": "✨ КОСМЕТИКА", 
                "cases_section": "📦 КЕЙСИ",
                "balance": "Баланс",
                "purchased": "✅ Куплено!",
                "insufficient": "❌ Недостатньо рівня або грошей!",
                "detector": "Детектор",
                "extinguisher": "Вогнегасник",
                "range_device": "Діапазон",
                "analyst": "Аналізатор",
                "hack_device": "Злам",
                "xray_device": "Рентген",
                "lucky_coin": "Щаслива Монета",
                "premium": "Преміум",
                "gold_nick": "Золотий Нік",
                "insider": "Інсайдер",
                "legend_aura": "Аура Легенди",
                "rainbow_trail": "Райдужний Слід",
                "fire_effect": "Вогняний Ефект",
                "ice_charm": "Лідяний Шарм",
                "shadow_profile": "Тіньовий Профіль",
                "angel_wings": "Ангельські Крила",
                
                # Battle Pass
                "bp_title": "BATTLE PASS V2.4",
                "bp_level": "Ваш рівень",
                "bp_xp": "BP XP",
                "next_rewards": "НАСТУПНІ НАГОРОДИ",
                "reward_coin": "монет",
                "reward_cosmetic": "✨ Косметика",
                "reward_special": "🌟 Особливе",
                "bp_reward_claimed": "🎁 НАГОРОДА BP {} рівня!",
                
                # Event
                "event_title": "ЛІТНІЙ ІВЕНТ 2026",
                "event_time_left": "⏰ До завершення: {} днів {} годин",
                "event_ended": "⚠️ ІВЕНТ ЗАВЕРШЕНО!",
                "event_bp": "🎪 ЛІТНІЙ BP",
                "event_level": "Рівень",
                "event_xp": "XP",
                "daily_missions": "📋 ЩОДЕННІ ЗАВДАННЯ",
                "season_missions": "🏆 СЕЗОННІ ЗАВДАННЯ",
                "mission_complete": "✅ МІСІЮ ВИКОНАНО: {}",
                "mission_reward_xp": "📈 +{} XP",
                "mission_reward_event_xp": "🌞 +{} літнього XP",
                "mission_reward_coins": "💰 +{} монет",
                "mission_reward_items": "🛠️ +{} {}",
                "mission_reward_cases": "📦 +{} {} кейсів",
                "mission_reward_cosmetic": "✨ Отримано косметику: {}",
                "event_bp_reward": "🎪 НАГОРОДА ЛІТНЬОГО BP {} рівня!",
                
                # Profile
                "profile_title": "СТАТИСТИКА ГРАВЦЯ",
                "nick": "Нік",
                "xp_bar": "XP",
                
                # Settings
                "settings_title": "НАЛАШТУВАННЯ",
                "language": "Мова",
                "language_en": "Англійська",
                "language_ua": "Українська",
                "sound": "Звукові ефекти",
                "sound_on": "🔊 УВІМК.",
                "sound_off": "🔇 ВИМК.",
                "animations": "Анімації",
                "animations_on": "✨ УВІМК.",
                "animations_off": "💨 ВИМК.",
                "difficulty": "Складність",
                "difficulty_easy": "Легка",
                "difficulty_normal": "Нормальна",
                "difficulty_hard": "Важка",
                "auto_save": "Автозбереження",
                "auto_save_on": "✅ УВІМК.",
                "auto_save_off": "❌ ВИМК.",
                "backup": "Створити бекап",
                "reset": "Скинути налаштування",
                "saved": "✅ Налаштування збережено!",
                "backup_created": "✅ Бекап створено!",
                "reset_done": "✅ Налаштування скинуто!",
                
                # Promo codes
                "enter_code": "🔑 КОД: ",
                "code_used": "❌ Код вже використано!",
                "code_invalid": "❌ Невірний код!",
                "code_success": "✨ {}",
                
                # Migration
                "migration_found": "🔄 Виявлено старе збереження! Виконується міграція...",
                "migration_success": "🔄 Міграція успішна! Перезапустіть гру.",
                "migration_error": "❌ Помилка міграції: {}"
            }
        }
    
    def get(self, key, **kwargs):
        text = self.strings[self.current_lang].get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text
    
    def set_language(self, lang):
        if lang in self.strings:
            self.current_lang = lang
            return True
        return False

# --- SETTINGS SYSTEM ---
class GameSettings:
    def __init__(self):
        self.settings_file = "settings_v2_4.json"
        self.language = "en"
        self.sound_enabled = True
        self.animations_enabled = True
        self.difficulty = "normal"
        self.auto_save = True
        self.load_settings()
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.language = data.get("language", "en")
                self.sound_enabled = data.get("sound_enabled", True)
                self.animations_enabled = data.get("animations_enabled", True)
                self.difficulty = data.get("difficulty", "normal")
                self.auto_save = data.get("auto_save", True)
            except:
                pass
    
    def save_settings(self):
        try:
            data = {
                "language": self.language,
                "sound_enabled": self.sound_enabled,
                "animations_enabled": self.animations_enabled,
                "difficulty": self.difficulty,
                "auto_save": self.auto_save
            }
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except:
            pass
    
    def create_backup(self):
        if os.path.exists(self.settings_file):
            backup_file = f"settings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                with open(backup_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                return True
            except:
                return False
        return False
    
    def reset_to_default(self):
        self.language = "en"
        self.sound_enabled = True
        self.animations_enabled = True
        self.difficulty = "normal"
        self.auto_save = True
        self.save_settings()

# --- GAME CONFIGURATION ---
class GameConfiguration:
    NAME = "GUESS THE NUMBER 2.4: Global Edition"
    VERSION = "V2.4"
    DEVELOPER = "ED"
    LANG = Language()

    RANKS = ["Novice", "Apprentice", "Gambler", "Seeker", "Experienced", "Shooter", "Master", "Expert", "Pro", "Elite", "LEGEND", "Titan", "Son of Haidzin", "IMMORTAL"]

    MODES = {
        "1": {"name_key": "classic", "range": 100, "att": float('inf'), "xp": 5, "coin": 7, "lvl": 1, "bp_xp": 10},
        "2": {"name_key": "sniper", "range": 200, "att": 12, "xp": 12, "coin": 20, "lvl": 5, "bp_xp": 20},
        "3": {"name_key": "hard", "range": 100, "att": 25, "xp": 8, "coin": 15, "lvl": 3, "bp_xp": 15},
        "4": {"name_key": "extreme", "range": 100, "att": 8, "xp": 15, "coin": 25, "lvl": 5, "bp_xp": 30},
        "5": {"name_key": "one_in_hundred", "range": 100, "att": 1, "xp": 100, "coin": 300, "lvl": 6, "bp_xp": 100},
        "6": {"name_key": "marathon", "range": 500, "att": 50, "xp": 25, "coin": 45, "lvl": 3, "bp_xp": 35},
        "7": {"name_key": "sapper", "range": 50, "att": 4, "xp": 18, "coin": 35, "lvl": 3, "bp_xp": 25},
        "8": {"name_key": "time_attack", "range": 150, "att": 20, "xp": 30, "coin": 50, "lvl": 4, "bp_xp": 40, "time_limit": 30}
    }

# --- SETTINGS UI ---
def display_settings(settings, lang, player=None):
    while True:
        print(f"\n{'═'*55}")
        print(f"⚙️ {lang.get('settings_title'):^45} ⚙️")
        print(f"{'═'*55}")
        
        print(f"\n1. {lang.get('language')}: {lang.get(f'language_{settings.language}')}")
        print(f"2. {lang.get('sound')}: {lang.get('sound_on') if settings.sound_enabled else lang.get('sound_off')}")
        print(f"3. {lang.get('animations')}: {lang.get('animations_on') if settings.animations_enabled else lang.get('animations_off')}")
        print(f"4. {lang.get('difficulty')}: {lang.get(f'difficulty_{settings.difficulty}')}")
        print(f"5. {lang.get('auto_save')}: {lang.get('auto_save_on') if settings.auto_save else lang.get('auto_save_off')}")
        print(f"\n6. {lang.get('backup')}")
        print(f"7. {lang.get('reset')}")
        print(f"\n0. {lang.get('exit')}")
        
        choice = input(f"\n{lang.get('choice')}: ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            print(f"\n1. {lang.get('language_en')}")
            print(f"2. {lang.get('language_ua')}")
            lang_choice = input(f"{lang.get('choice')}: ").strip()
            if lang_choice == '1':
                settings.language = "en"
                lang.set_language("en")
                print(lang.get('saved'))
            elif lang_choice == '2':
                settings.language = "ua"
                lang.set_language("ua")
                print(lang.get('saved'))
            settings.save_settings()
            input(lang.get('enter'))
        elif choice == '2':
            settings.sound_enabled = not settings.sound_enabled
            settings.save_settings()
            print(lang.get('saved'))
            if settings.sound_enabled and player:
                print("🔊", end=" ")
            input(lang.get('enter'))
        elif choice == '3':
            settings.animations_enabled = not settings.animations_enabled
            settings.save_settings()
            print(lang.get('saved'))
            input(lang.get('enter'))
        elif choice == '4':
            print(f"\n1. {lang.get('difficulty_easy')}")
            print(f"2. {lang.get('difficulty_normal')}")
            print(f"3. {lang.get('difficulty_hard')}")
            diff_choice = input(f"{lang.get('choice')}: ").strip()
            if diff_choice == '1':
                settings.difficulty = "easy"
            elif diff_choice == '2':
                settings.difficulty = "normal"
            elif diff_choice == '3':
                settings.difficulty = "hard"
            settings.save_settings()
            print(lang.get('saved'))
            input(lang.get('enter'))
        elif choice == '5':
            settings.auto_save = not settings.auto_save
            settings.save_settings()
            print(lang.get('saved'))
            input(lang.get('enter'))
        elif choice == '6':
            if settings.create_backup():
                print(lang.get('backup_created'))
            else:
                print("❌ Backup failed!")
            input(lang.get('enter'))
        elif choice == '7':
            if input(f"{lang.get('reset')}? (y/n): ").lower() == 'y':
                settings.reset_to_default()
                lang.set_language(settings.language)
                print(lang.get('reset_done'))
                input(lang.get('enter'))

# --- REST OF THE GAME CLASSES (Player, BattlePass, SummerEvent, etc.) ---
# [Всі інші класи залишаються такими ж, але з використанням lang.get() для текстів]

# --- SAVE MANAGER UPDATED ---
class SaveManager:
    FILE_NAME = "save_v2_4_global.json"
    
    @staticmethod
    def save_progress(player):
        if not GameConfiguration.LANG.get("auto_save"):
            return
        try:
            data = {
                "version": "2.4",
                "name": player.name,
                "lvl": player.level,
                "xp": player.experience,
                "wallet": player.wallet,
                "inventory": player.inventory,
                "statistics": {"wins": player.total_wins, "played": player.total_played},
                "battle_pass": {"level": player.bp_level, "xp": player.bp_experience},
                "event_battle_pass": {"level": player.event_bp.level, "xp": player.event_bp.xp},
                "event_missions": {
                    "daily": [{"name": m["name"], "progress": m["progress"]} for m in player.event.daily_missions],
                    "season": [{"name": m["name"], "progress": m["progress"]} for m in player.event.season_missions]
                },
                "containers": player.cases,
                "redeemed": player.used_codes,
                "event_items": player.event_items,
                "event_cosmetics": player.event_cosmetics,
                "last_event_reset": player.last_event_reset.isoformat() if player.last_event_reset else datetime.now().isoformat()
            }
            with open(SaveManager.FILE_NAME, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"❌ Save error: {e}")
            return False

# --- UPDATED MAIN FUNCTION ---
def main():
    # Завантаження налаштувань
    settings = GameSettings()
    lang = GameConfiguration.LANG
    lang.set_language(settings.language)
    
    player = Player()
    
    if not SaveManager.load_progress(player):
        player.name = input(f"{lang.get('nick')}: ")
        SaveManager.save_progress(player)
    
    print(f"\n🎮 {lang.get('welcome', name=GameConfiguration.NAME)}")
    
    while True:
        # Відображення ніка з ефектами
        name_tag = player.name
        if player.inventory.get("gold", False):
            name_tag = f"✨ {name_tag} ✨"
        if player.inventory.get("shadow", False):
            name_tag = f"🌑{name_tag}🌑"
        if player.inventory.get("ice", False):
            name_tag = f"❄️{name_tag}❄️"
        
        print(f"\n┏{'━'*55}┓")
        print(f"┃{name_tag:^55}┃")
        
        effects = []
        if player.inventory.get("aura", False): effects.append("✨Aura")
        if player.inventory.get("rainbow", False): effects.append("🌈Rainbow")
        if player.inventory.get("fire", False): effects.append("🔥Fire")
        if effects:
            print(f"┃{' '.join(effects):^55}┃")
        
        print(f"┃{lang.get('level')}: {player.level} | BP: {player.bp_level} | 🌞BP: {player.event_bp.level} | {lang.get('wallet')}: {player.wallet:^10}┃")
        print(f"┣{'━'*55}┫")
        
        for k, v in GameConfiguration.MODES.items():
            lock = lang.get('unlocked') if player.level >= v["lvl"] else f"{lang.get('locked')} {v['lvl']}"
            time_tag = " ⏱️" if "time_limit" in v else ""
            mode_name = lang.get(v["name_key"])
            print(f"┃ {k}. {mode_name}{time_tag:<12} | 1-{v['range']:<4} | {lock:>14} ┃")
        
        print(f"┣{'━'*55}┫")
        print(f"┃ {lang.get('shop')} | {lang.get('inventory')} | {lang.get('stats')} | {lang.get('bio')} | {lang.get('codes')} | {lang.get('bp')} | {lang.get('event')} | {lang.get('settings')} | {lang.get('exit')} ┃")
        print(f"┗{'━'*55}┛")
        
        cmd = input(f"\n{lang.get('choice')}: ").lower().strip()
        
        if cmd == 'exit':
            print(f"\n{lang.get('goodbye', name=player.name)}")
            break
        elif cmd == 'stats':
            display_profile(player)
        elif cmd == 'inv':
            display_inventory(player)
        elif cmd == 'shop':
            display_shop(player)
        elif cmd == 'bio':
            print(f"\n🎮 {GameConfiguration.NAME}")
            print(f"👨‍💻 {lang.get('developer')}: {GameConfiguration.DEVELOPER}")
            print(f"📅 {lang.get('version')}: {GameConfiguration.VERSION}")
            print(f"📊 {lang.get('modes_count')}: {len(GameConfiguration.MODES)}")
            input(lang.get('enter'))
        elif cmd == 'codes' or cmd == 'code':
            redeem_gift_code(player)
        elif cmd == 'bp':
            display_battle_pass(player)
        elif cmd == 'event' or cmd == 'summer':
            display_event_menu(player)
        elif cmd == 'settings':
            display_settings(settings, lang, player)
        elif cmd in GameConfiguration.MODES:
            run_game_session(cmd, player)
        else:
            print(lang.get('unknown_cmd'))

# NOTE: Через обмеження довжини, інші функції (Player, BattlePass, SummerEvent,
# display_profile, display_inventory, display_shop, display_battle_pass, 
# display_event_menu, redeem_gift_code, run_game_session, etc.) 
# залишаються такими ж, як у попередній версії, але з використанням lang.get() 
# для всіх текстових рядків.

if __name__ == "__main__":
    main()