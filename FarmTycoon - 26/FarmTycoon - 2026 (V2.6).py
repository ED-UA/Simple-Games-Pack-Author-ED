import json
import os
import random
import time
from datetime import datetime

# Константи
MAX_SAVES = 3
SAVE_DIR = "farm_tycoon_saves"
CONFIG_FILE = "game_config.json"

# ПЕРЕКЛАДИ
TRANSLATIONS = {
    "uk": {
        "game_title": "🚜 FARM TYCOON 2026 V2.6 🚜",
        "save_select": "📁 ВИБІР ЗБЕРЕЖЕННЯ",
        "empty_slot": "📭 Порожній слот",
        "delete_save": "🗑️ Видалити збереження",
        "exit": "Вихід з гри",
        "new_game": "✨ СТВОРЕННЯ НОВОЇ ГРИ",
        "nickname": "Введіть свій нік",
        "difficulty_choice": "Оберіть складність",
        "easy": "🍃 ЛЕГКА",
        "normal": "⭐ НОРМАЛЬНА",
        "hard": "🔥 ХАРД",
        "back": "Назад",
        "money": "💰 Гроші",
        "loan": "💸 Кредит",
        "day": "📅 ДЕНЬ",
        "season": "🌤️ СЕЗОН",
        "fertilizer": "🌱 Добрив",
        "herbicide": "🌿 Гербіцидів",
        "tractor": "🚜 Трактор",
        "harvester": "🌾 Комбайн",
        "cultivator": "🔧 Культиватор",
        "seeder": "🌱 Сівалка",
        "planting": "🌾 Посівна",
        "garage": "🚜 Гараж",
        "shop": "🛒 Магазин",
        "bank": "🏦 Банк",
        "sell": "📦 Продати врожай",
        "bins": "📊 Бункери",
        "animals": "🐄 Тваринництво",
        "stocks": "📈 Портфель акцій",
        "promocodes": "🎁 Промокоди",
        "achievements": "🏆 Досягнення",
        "settings": "⚙️ Налаштування",
        "guide": "📖 Керівництво",
        "save_and_exit": "💾 Зберегти та вийти",
        "language": "🌐 Мова (Language)",
        "ukrainian": "Українська",
        "english": "English",
        "settings_saved": "✅ Налаштування збережено!",
        "invalid_choice": "❌ Невірний вибір!",
        "not_enough_money": "❌ Не вистачає грошей!",
        "success": "✅ Успішно!",
        "sort_by": "📊 Сортувати за:",
        "sort_brand": "За брендом",
        "sort_country": "За країною",
        "sort_tier": "За рівнем",
        "sort_price": "За ціною",
        "buy": "Купити",
        "sell_item": "Продати",
        "equip": "Екіпірувати",
        "repair": "Ремонт",
        "refuel": "Заправка"
    },
    "en": {
        "game_title": "🚜 FARM TYCOON 2026 V2.6 🚜",
        "save_select": "📁 SAVE SELECTION",
        "empty_slot": "📭 Empty slot",
        "delete_save": "🗑️ Delete save",
        "exit": "Exit game",
        "new_game": "✨ CREATE NEW GAME",
        "nickname": "Enter your nickname",
        "difficulty_choice": "Choose difficulty",
        "easy": "🍃 EASY",
        "normal": "⭐ NORMAL",
        "hard": "🔥 HARD",
        "back": "Back",
        "money": "💰 Money",
        "loan": "💸 Loan",
        "day": "📅 DAY",
        "season": "🌤️ SEASON",
        "fertilizer": "🌱 Fertilizer",
        "herbicide": "🌿 Herbicide",
        "tractor": "🚜 Tractor",
        "harvester": "🌾 Harvester",
        "cultivator": "🔧 Cultivator",
        "seeder": "🌱 Seeder",
        "planting": "🌾 Planting",
        "garage": "🚜 Garage",
        "shop": "🛒 Shop",
        "bank": "🏦 Bank",
        "sell": "📦 Sell crops",
        "bins": "📊 Bins",
        "animals": "🐄 Animal farm",
        "stocks": "📈 Stock portfolio",
        "promocodes": "🎁 Promocodes",
        "achievements": "🏆 Achievements",
        "settings": "⚙️ Settings",
        "guide": "📖 Guide",
        "save_and_exit": "💾 Save and exit",
        "language": "🌐 Language",
        "ukrainian": "Українська",
        "english": "English",
        "settings_saved": "✅ Settings saved!",
        "invalid_choice": "❌ Invalid choice!",
        "not_enough_money": "❌ Not enough money!",
        "success": "✅ Success!",
        "sort_by": "📊 Sort by:",
        "sort_brand": "By brand",
        "sort_country": "By country",
        "sort_tier": "By tier",
        "sort_price": "By price",
        "buy": "Buy",
        "sell_item": "Sell",
        "equip": "Equip",
        "repair": "Repair",
        "refuel": "Refuel"
    }
}

# Складність гри
DIFFICULTY_SETTINGS = {
    "легка": {
        "money": 250000,
        "loan_max": 1000000,
        "crop_multiplier": 1.3,
        "price_multiplier": 1.2,
        "exp_multiplier": 1.5,
        "name_uk": "🍃 ЛЕГКА",
        "name_en": "🍃 EASY"
    },
    "нормальна": {
        "money": 150000,
        "loan_max": 500000,
        "crop_multiplier": 1.0,
        "price_multiplier": 1.0,
        "exp_multiplier": 1.0,
        "name_uk": "⭐ НОРМАЛЬНА",
        "name_en": "⭐ NORMAL"
    },
    "хард": {
        "money": 50000,
        "loan_max": 200000,
        "crop_multiplier": 0.7,
        "price_multiplier": 0.8,
        "exp_multiplier": 0.7,
        "name_uk": "🔥 ХАРД",
        "name_en": "🔥 HARD"
    }
}

# Країни-виробники техніки
COUNTRIES = {
    "Soviet": "🇺🇦 СРСР/Україна",
    "Belarus": "🇧🇾 Білорусь",
    "Lovol": "🇨🇳 Китай",
    "New Holland": "🇺🇸 США/Італія",
    "John Deere": "🇺🇸 США",
    "Ukraine": "🇺🇦 Україна",
    "CLAAS": "🇩🇪 Німеччина",
    "Braud": "🇫🇷 Франція",
    "Gregoire": "🇫🇷 Франція",
    "Yanmar": "🇯🇵 Японія",
    "Kubota": "🇯🇵 Японія",
    "Horsch": "🇩🇪 Німеччина",
    "Lemken": "🇩🇪 Німеччина",
    "Case": "🇺🇸 США",
    "Fendt": "🇩🇪 Німеччина",
    "Great Plains": "🇺🇸 США",
    "Vaderstad": "🇸🇪 Швеція"
}

# Базова ціни
BASE_PRICES = {
    "Пшениця": 12,
    "Соняшник": 25,
    "Рапс": 65,
    "Ячмінь": 10,
    "Овес": 8,
    "Рис": 30,
    "Виноград": 120
}

# Культури
CROPS = {
    "Пшениця": {"y": 1.0},
    "Соняшник": {"y": 0.8},
    "Рапс": {"y": 0.3},
    "Ячмінь": {"y": 1.1},
    "Овес": {"y": 1.2},
    "Рис": {"y": 0.9, "special": "потребує багато води"},
    "Виноград": {"y": 0.5, "special": "висока ціна, малий врожай"}
}

# Промокоди
PROMOCODES = {
    "FarmMannager2026": 20000,
    "I_am_in_debt": 45000,
    "STONKS": "price_boost",
    "MECHANIC": "free_repair",
    "FUEL_CRISIS": "free_fuel",
    "Ya_traktor_wihanyayu": 25000,
    "Ya_traktor_vyhanyayu": 25000,
    "Yatraktorwihanyayu": 25000
}

# ДОСЯГНЕННЯ
ACHIEVEMENTS = {
    "first_million": {"name_uk": "💰 Перший мільйон", "name_en": "💰 First Million", "desc_uk": "Заробити 1,000,000 грн", "desc_en": "Earn 1,000,000 UAH", "target": 1000000, "bonus": 50000, "unlocked": False},
    "collector": {"name_uk": "🔧 Колекціонер", "name_en": "🔧 Collector", "desc_uk": "Купити 10 одиниць техніки", "desc_en": "Buy 10 equipment units", "target": 10, "bonus": 25000, "unlocked": False},
    "landowner": {"name_uk": "🏞️ Землевласник", "name_en": "🏞️ Landowner", "desc_uk": "Купити всі 13 полів", "desc_en": "Buy all 13 fields", "target": 13, "bonus": 100000, "unlocked": False},
    "machinist": {"name_uk": "🚜 Машиніст", "name_en": "🚜 Machinist", "desc_uk": "Зібрати врожай з 1000 га", "desc_en": "Harvest 1000 hectares", "target": 1000, "bonus": 30000, "unlocked": False},
    "agrarian": {"name_uk": "🌾 Аграрій", "name_en": "🌾 Agrarian", "desc_uk": "Зібрати 100,000 кг зерна", "desc_en": "Harvest 100,000 kg of grain", "target": 100000, "bonus": 40000, "unlocked": False},
    "debtor": {"name_uk": "💸 Боржник", "name_en": "💸 Debtor", "desc_uk": "Взяти кредит на 500,000 грн", "desc_en": "Take a loan of 500,000 UAH", "target": 500000, "bonus": 20000, "unlocked": False},
    "game_complete": {"name_uk": "🏆 Фермер-легенда", "name_en": "🏆 Farmer Legend", "desc_uk": "Пройти гру на нормальній складності", "desc_en": "Complete the game on Normal difficulty", "target": 500000000, "bonus": 0, "unlocked": False},
    "rice_king": {"name_uk": "🍚 Рисовий король", "name_en": "🍚 Rice King", "desc_uk": "Зібрати 50,000 кг рису", "desc_en": "Harvest 50,000 kg of rice", "target": 50000, "bonus": 75000, "unlocked": False},
    "grape_master": {"name_uk": "🍇 Виноградний магістр", "name_en": "🍇 Grape Master", "desc_uk": "Зібрати 25,000 кг винограду", "desc_en": "Harvest 25,000 kg of grapes", "target": 25000, "bonus": 100000, "unlocked": False}
}

# СЕЗОНИ
SEASONS = ["Весна", "Літо", "Осінь", "Зима"]
SEASONS_EN = ["Spring", "Summer", "Autumn", "Winter"]
SEASON_EFFECTS = {
    "Весна": 1.1,
    "Літо": 1.05,
    "Осінь": 1.0,
    "Зима": 0.0
}

# КАТАЛОГ ТЕХНІКИ
CATALOG = {
    "tractor": [
        {"model": "Т-25", "price": 15000, "fuel_cons": 5, "tank": 40, "tier": 1, "brand": "Soviet", "country": "Soviet"},
        {"model": "МТЗ-82", "price": 45000, "fuel_cons": 10, "tank": 80, "tier": 2, "brand": "Belarus", "country": "Belarus"},
        {"model": "Lovol Foton TE", "price": 30000, "fuel_cons": 8, "tank": 60, "tier": 2, "brand": "Lovol", "country": "Lovol"},
        {"model": "New Holland T5", "price": 80000, "fuel_cons": 14, "tank": 120, "tier": 3, "brand": "New Holland", "country": "New Holland"},
        {"model": "John Deere 8R", "price": 500000, "fuel_cons": 35, "tank": 700, "tier": 5, "brand": "John Deere", "country": "John Deere"}
    ],
    "harvester": [
        {"model": "Нива Ефект", "price": 25000, "cap": 800, "fuel_cons": 15, "tank": 120, "tier": 1, "brand": "Ukraine", "country": "Ukraine"},
        {"model": "Lovol Foton G50", "price": 60000, "cap": 2000, "fuel_cons": 20, "tank": 250, "tier": 2, "brand": "Lovol", "country": "Lovol"},
        {"model": "New Holland CX", "price": 200000, "cap": 9000, "fuel_cons": 45, "tank": 600, "tier": 4, "brand": "New Holland", "country": "New Holland"},
        {"model": "John Deere X9", "price": 1000000, "cap": 45000, "fuel_cons": 95, "tank": 1500, "tier": 7, "brand": "John Deere", "country": "John Deere"},
        {"model": "Lovol Foton G100", "price": 250000, "cap": 12000, "fuel_cons": 55, "tank": 750, "tier": 4, "brand": "Lovol", "country": "Lovol"},
        {"model": "New Holland CR10", "price": 800000, "cap": 35000, "fuel_cons": 80, "tank": 1200, "tier": 6, "brand": "New Holland", "country": "New Holland"},
        {"model": "CLAAS Lexion 8900", "price": 1500000, "cap": 55000, "fuel_cons": 100, "tank": 1600, "tier": 8, "brand": "CLAAS", "country": "CLAAS"},
        {"model": "Braud 9070L", "price": 1200000, "cap": 8000, "fuel_cons": 40, "tank": 500, "tier": 5, "brand": "Braud", "country": "Braud", "special": "виноградний"},
        {"model": "Gregoire G8.120", "price": 1800000, "cap": 12000, "fuel_cons": 50, "tank": 700, "tier": 6, "brand": "Gregoire", "country": "Gregoire", "special": "виноградний"},
        {"model": "Yanmar YH800", "price": 450000, "cap": 5000, "fuel_cons": 25, "tank": 300, "tier": 3, "brand": "Yanmar", "country": "Yanmar", "special": "рисовий"},
        {"model": "Kubota R900", "price": 700000, "cap": 8000, "fuel_cons": 35, "tank": 450, "tier": 4, "brand": "Kubota", "country": "Kubota", "special": "рисовий"}
    ],
    "cultivator": [
        {"model": "КПС-4", "price": 5000, "eff": 1.1, "tier": 1, "brand": "Ukraine", "country": "Ukraine"},
        {"model": "New Holland Ecolo", "price": 25000, "eff": 1.6, "tier": 3, "brand": "New Holland", "country": "New Holland"},
        {"model": "Horsch Tiger", "price": 150000, "eff": 2.2, "tier": 5, "brand": "Horsch", "country": "Horsch"}
    ],
    "seeder": [
        {"model": "СЗ-3.6", "price": 8000, "y_mod": 1.0, "tier": 1, "brand": "Ukraine", "country": "Ukraine"},
        {"model": "New Holland PZ", "price": 35000, "y_mod": 2.0, "tier": 3, "brand": "New Holland", "country": "New Holland"},
        {"model": "John Deere DB120", "price": 500000, "y_mod": 6.5, "tier": 8, "brand": "John Deere", "country": "John Deere"}
    ],
    "fertilizer": [
        {"name_uk": "Органічні добрива", "name_en": "Organic fertilizer", "price": 500, "yield_boost": 0.3, "use_per_ha": 10},
        {"name_uk": "Мінеральні добрива", "name_en": "Mineral fertilizer", "price": 800, "yield_boost": 0.3, "use_per_ha": 8},
        {"name_uk": "Рідкі добрива", "name_en": "Liquid fertilizer", "price": 1200, "yield_boost": 0.35, "use_per_ha": 6}
    ],
    "herbicide": [
        {"name_uk": "Гліфосат", "name_en": "Glyphosate", "price": 300, "protection": 0.85, "use_per_ha": 5},
        {"name_uk": "Раундап", "name_en": "Roundup", "price": 600, "protection": 0.9, "use_per_ha": 4},
        {"name_uk": "Торнадо", "name_en": "Tornado", "price": 1000, "protection": 0.95, "use_per_ha": 3}
    ]
}

# ПОЛЯ
FIELDS_DATA = []
for i in range(10):
    FIELDS_DATA.append({"id": i+1, "name_uk": f"Поле #{i+1}", "name_en": f"Field #{i+1}", "size": 10 + i*5, "price": (i+1)*5000, "owned": False, "type": "звичайне"})

FIELDS_DATA.append({"id": 11, "name_uk": "Рисове поле", "name_en": "Rice field", "size": 40, "price": 80000, "owned": False, "type": "рисове"})
FIELDS_DATA.append({"id": 12, "name_uk": "Виноградник №1", "name_en": "Vineyard #1", "size": 35, "price": 120000, "owned": False, "type": "виноградне"})
FIELDS_DATA.append({"id": 13, "name_uk": "Виноградник №2", "name_en": "Vineyard #2", "size": 35, "price": 120000, "owned": False, "type": "виноградне"})

FIELDS_DATA[0]["owned"] = True

# ТВАРИНИ
ANIMALS = {
    "cow": {"name_uk": "🐄 Корова", "name_en": "🐄 Cow", "price": 500, "daily_income": 50, "max_health": 100, "days_to_mature": 0},
    "pig": {"name_uk": "🐖 Свиня", "name_en": "🐖 Pig", "price": 300, "daily_income": 0, "max_health": 100, "days_to_mature": 10, "sell_price": 800},
    "chicken": {"name_uk": "🐔 Курка", "name_en": "🐔 Chicken", "price": 50, "daily_income": 30, "max_health": 100, "days_to_mature": 0}
}

# АКЦІЇ
STOCKS = {
    "JohnDeere": {"name": "John Deere", "price": 100, "volatility": 0.05},
    "CNH": {"name": "CNH Industrial", "price": 80, "volatility": 0.07},
    "AGCO": {"name": "AGCO", "price": 60, "volatility": 0.06}
}

# ЄВЕНТИ
NEW_EVENTS = {
    "tax": {"chance": 5, "name_uk": "📋 Податкова перевірка", "name_en": "📋 Tax audit", "desc_uk": "Штраф 1,000 грн!", "desc_en": "Fine 1,000 UAH!", "effect": -1000},
    "hail": {"chance": 8, "name_uk": "🌨️ Град", "name_en": "🌨️ Hail", "desc_uk": "Знищує 50% врожаю!", "desc_en": "Destroys 50% of harvest!", "effect": -0.5},
    "exhibition": {"chance": 6, "name_uk": "🏆 Фермерська виставка", "name_en": "🏆 Farming exhibition", "desc_uk": "Ви перемогли! Отримали 10,000 грн!", "desc_en": "You won! Got 10,000 UAH!", "effect": 10000},
    "epidemic": {"chance": 7, "name_uk": "🦠 Епідемія", "name_en": "🦠 Epidemic", "desc_uk": "Хвороби тварин! Втрата 50% здоров'я!", "desc_en": "Animal diseases! 50% health loss!", "effect": "animal_disease"}
}

BUNKER_CAPACITY = 50000

# Глобальні змінні для мови та перекладів
current_language = "en"  # за замовчуванням англійська
current_translations = TRANSLATIONS["en"]

def set_language(lang):
    global current_language, current_translations
    current_language = lang
    current_translations = TRANSLATIONS[lang]

def get_text(key):
    return current_translations.get(key, key)

def print_tractor_song():
    print("\n" + "="*60)
    print("🎵 ПАСХАЛКА - Я ТРАКТОР ВИГАНЯЮ 🎵")
    print("="*60)
    print("\nЯ трактор виганяю,")
    print("До неї під'їжджаю:")
    print("Сідай, мала, не бійся,")
    print("Бо я ся не кусаю!")
    print("Вали куди подалі,")
    print("Я сторіси знімаю,")
    print("В моєму Instagramі")
    print("Тобі місця немає!")
    print("\n" + "="*60)
    print("🎁 +25,000 грн за пасхалку!")
    print("="*60)

def load_config():
    global current_language
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                current_language = config.get("language", "en")
                set_language(current_language)
        except:
            set_language("en")

def save_config():
    config = {"language": current_language}
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def generate_economy():
    crops_dict = {}
    for crop in BASE_PRICES.keys():
        crops_dict[crop] = random.uniform(0.8, 1.2)
    return {
        "crops": crops_dict,
        "equipment": random.uniform(0.85, 1.15),
        "fuel": random.uniform(0.8, 1.2)
    }

def get_season(day):
    season_index = (day // 30) % 4
    if current_language == "uk":
        return SEASONS[season_index]
    else:
        return SEASONS_EN[season_index]

def get_season_effect(season_name):
    season_map = {"Весна": 1.1, "Spring": 1.1, "Літо": 1.05, "Summer": 1.05, 
                  "Осінь": 1.0, "Autumn": 1.0, "Зима": 0.0, "Winter": 0.0}
    return season_map.get(season_name, 1.0)

def get_current_price(base_price, economy_factor):
    return int(base_price * economy_factor)

def get_difficulty_name(difficulty):
    if current_language == "uk":
        return DIFFICULTY_SETTINGS[difficulty]["name_uk"]
    else:
        return DIFFICULTY_SETTINGS[difficulty]["name_en"]

def show_guide():
    """Керівництво по грі"""
    if current_language == "uk":
        print("\n" + "="*60)
        print("📖 КЕРІВНИЦТВО ПО ГРІ")
        print("="*60)
        print("\n🎯 МЕТА ГРИ:")
        print("   Стати найбагатшим фермером! Купуйте техніку,")
        print("   вирощуйте культури, продавайте врожай та інвестуйте.")
        
        print("\n🌾 ОСНОВНІ МЕХАНІКИ:")
        print("   1. Посівна - виберіть поле та культуру для вирощування")
        print("   2. Гараж - керуйте технікою (заправка, ремонт, продаж)")
        print("   3. Магазин - купуйте техніку, добрива, гербіциди")
        print("   4. Банк - беріть кредити або завершуйте гру")
        print("   5. Тваринництво - купуйте тварин для пасивного доходу")
        print("   6. Акції - інвестуйте в компанії")
        
        print("\n🌟 ОСОБЛИВОСТІ:")
        print("   • Сезони впливають на врожайність")
        print("   • Економіка змінюється кожні 7 днів")
        print("   • Випадкові події (град, виставка, податки)")
        print("   • Промокоди дають бонуси")
        print("   • Досягнення нагороджують грошима")
        
        print("\n🎁 ПРОМОКОДИ:")
        print("   • FarmMannager2026 - 20,000 грн")
        print("   • I_am_in_debt - 45,000 грн")
        print("   • STONKS - +50% до ціни на 1 день")
        print("   • MECHANIC - безкоштовний ремонт")
        print("   • FUEL_CRISIS - безкоштовне пальне")
        print("   • Ya_traktor_wihanyayu - ПАСХАЛКА! +25,000 грн")
        
        print("\n💡 ПОРАДИ:")
        print("   • Починайте з легкої складності")
        print("   • Інвестуйте в кращу техніку")
        print("   • Використовуйте добрива для більшого врожаю")
        print("   • Слідкуйте за цінами на ринку")
        print("   • Диверсифікуйте доходи (тварини, акції)")
    else:
        print("\n" + "="*60)
        print("📖 GAME GUIDE")
        print("="*60)
        print("\n🎯 GAME OBJECTIVE:")
        print("   Become the richest farmer! Buy equipment,")
        print("   grow crops, sell harvest and invest.")
        
        print("\n🌾 MAIN MECHANICS:")
        print("   1. Planting - choose a field and crop to grow")
        print("   2. Garage - manage equipment (refuel, repair, sell)")
        print("   3. Shop - buy equipment, fertilizer, herbicides")
        print("   4. Bank - take loans or complete the game")
        print("   5. Animal farming - buy animals for passive income")
        print("   6. Stocks - invest in companies")
        
        print("\n🌟 FEATURES:")
        print("   • Seasons affect yield")
        print("   • Economy changes every 7 days")
        print("   • Random events (hail, exhibition, taxes)")
        print("   • Promocodes give bonuses")
        print("   • Achievements reward money")
        
        print("\n🎁 PROMOCODES:")
        print("   • FarmMannager2026 - 20,000 UAH")
        print("   • I_am_in_debt - 45,000 UAH")
        print("   • STONKS - +50% price for 1 day")
        print("   • MECHANIC - free repair")
        print("   • FUEL_CRISIS - free fuel")
        print("   • Ya_traktor_wihanyayu - EASTER EGG! +25,000 UAH")
        
        print("\n💡 TIPS:")
        print("   • Start with Easy difficulty")
        print("   • Invest in better equipment")
        print("   • Use fertilizer for higher yield")
        print("   • Watch market prices")
        print("   • Diversify income (animals, stocks)")
    
    print("\n" + "="*60)
    input("\n" + (get_text("back") if current_language == "uk" else "Press Enter to continue..."))

def settings_menu():
    """Меню налаштувань"""
    global current_language
    while True:
        print("\n" + "="*50)
        print("⚙️ " + get_text("settings"))
        print("="*50)
        
        print(f"\n1. {get_text('language')}: {'Українська' if current_language == 'uk' else 'English'}")
        print(f"0. {get_text('back')}")
        
        choice = input("\n👉 " + (get_text("back") if current_language == "uk" else "Your choice: "))
        
        if choice == "0":
            save_config()
            break
        elif choice == "1":
            print("\n1. Українська")
            print("2. English")
            lang_choice = input("\n" + (get_text("back") if current_language == "uk" else "Choose language: "))
            if lang_choice == "1":
                set_language("uk")
                print(get_text("settings_saved"))
            elif lang_choice == "2":
                set_language("en")
                print(get_text("settings_saved"))
            else:
                print(get_text("invalid_choice"))
            input("\n" + (get_text("back") if current_language == "uk" else "Press Enter..."))

def sort_equipment_list(equipment_list, sort_by="tier"):
    """Сортування списку техніки"""
    if sort_by == "tier":
        return sorted(equipment_list, key=lambda x: x.get('tier', 0))
    elif sort_by == "price":
        return sorted(equipment_list, key=lambda x: x.get('price', 0))
    elif sort_by == "brand":
        return sorted(equipment_list, key=lambda x: x.get('brand', ''))
    elif sort_by == "country":
        return sorted(equipment_list, key=lambda x: COUNTRIES.get(x.get('country', ''), x.get('country', '')))
    return equipment_list

def show_sorted_equipment(equipment_list, title, data):
    """Показ відсортованої техніки в магазині"""
    print(f"\n📋 {title}:")
    
    print(f"\n{get_text('sort_by')}")
    print("  1. " + get_text("sort_tier"))
    print("  2. " + get_text("sort_price"))
    print("  3. " + get_text("sort_brand"))
    print("  4. " + get_text("sort_country"))
    print("  0. " + get_text("back"))
    
    sort_choice = input("\n" + (get_text("back") if current_language == "uk" else "Your choice: "))
    
    if sort_choice == "1":
        equipment_list = sort_equipment_list(equipment_list, "tier")
    elif sort_choice == "2":
        equipment_list = sort_equipment_list(equipment_list, "price")
    elif sort_choice == "3":
        equipment_list = sort_equipment_list(equipment_list, "brand")
    elif sort_choice == "4":
        equipment_list = sort_equipment_list(equipment_list, "country")
    elif sort_choice == "0":
        return None
    else:
        equipment_list = sort_equipment_list(equipment_list, "tier")
    
    return equipment_list

def check_achievements(data):
    total_equipment = len(data['garage'])
    total_fields = len(data['my_fields'])
    total_harvested_ha = data.get('total_harvested_ha', 0)
    total_harvest = sum(data.get('total_harvest', {}).values())
    rice_harvest = data.get('total_harvest', {}).get("Рис", 0)
    grape_harvest = data.get('total_harvest', {}).get("Виноград", 0)
    
    achievements_unlocked = []
    
    if not ACHIEVEMENTS["first_million"]["unlocked"] and data.get('total_earned', 0) >= 1000000:
        ACHIEVEMENTS["first_million"]["unlocked"] = True
        data['money'] += ACHIEVEMENTS["first_million"]["bonus"]
        achievements_unlocked.append(ACHIEVEMENTS["first_million"])
        name = ACHIEVEMENTS["first_million"]["name_uk"] if current_language == "uk" else ACHIEVEMENTS["first_million"]["name_en"]
        print(f"\n🏆 {name}!")
        print(f"   +{ACHIEVEMENTS['first_million']['bonus']:,} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}!")
    
    if not ACHIEVEMENTS["collector"]["unlocked"] and total_equipment >= 10:
        ACHIEVEMENTS["collector"]["unlocked"] = True
        data['money'] += ACHIEVEMENTS["collector"]["bonus"]
        achievements_unlocked.append(ACHIEVEMENTS["collector"])
        name = ACHIEVEMENTS["collector"]["name_uk"] if current_language == "uk" else ACHIEVEMENTS["collector"]["name_en"]
        print(f"\n🏆 {name}!")
        print(f"   +{ACHIEVEMENTS['collector']['bonus']:,} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}!")
    
    if not ACHIEVEMENTS["landowner"]["unlocked"] and total_fields >= 13:
        ACHIEVEMENTS["landowner"]["unlocked"] = True
        data['money'] += ACHIEVEMENTS["landowner"]["bonus"]
        achievements_unlocked.append(ACHIEVEMENTS["landowner"])
        name = ACHIEVEMENTS["landowner"]["name_uk"] if current_language == "uk" else ACHIEVEMENTS["landowner"]["name_en"]
        print(f"\n🏆 {name}!")
        print(f"   +{ACHIEVEMENTS['landowner']['bonus']:,} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}!")
    
    if not ACHIEVEMENTS["machinist"]["unlocked"] and total_harvested_ha >= 1000:
        ACHIEVEMENTS["machinist"]["unlocked"] = True
        data['money'] += ACHIEVEMENTS["machinist"]["bonus"]
        achievements_unlocked.append(ACHIEVEMENTS["machinist"])
        name = ACHIEVEMENTS["machinist"]["name_uk"] if current_language == "uk" else ACHIEVEMENTS["machinist"]["name_en"]
        print(f"\n🏆 {name}!")
        print(f"   +{ACHIEVEMENTS['machinist']['bonus']:,} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}!")
    
    if not ACHIEVEMENTS["agrarian"]["unlocked"] and total_harvest >= 100000:
        ACHIEVEMENTS["agrarian"]["unlocked"] = True
        data['money'] += ACHIEVEMENTS["agrarian"]["bonus"]
        achievements_unlocked.append(ACHIEVEMENTS["agrarian"])
        name = ACHIEVEMENTS["agrarian"]["name_uk"] if current_language == "uk" else ACHIEVEMENTS["agrarian"]["name_en"]
        print(f"\n🏆 {name}!")
        print(f"   +{ACHIEVEMENTS['agrarian']['bonus']:,} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}!")
    
    if not ACHIEVEMENTS["debtor"]["unlocked"] and data.get('max_loan_taken', 0) >= 500000:
        ACHIEVEMENTS["debtor"]["unlocked"] = True
        data['money'] += ACHIEVEMENTS["debtor"]["bonus"]
        achievements_unlocked.append(ACHIEVEMENTS["debtor"])
        name = ACHIEVEMENTS["debtor"]["name_uk"] if current_language == "uk" else ACHIEVEMENTS["debtor"]["name_en"]
        print(f"\n🏆 {name}!")
        print(f"   +{ACHIEVEMENTS['debtor']['bonus']:,} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}!")
    
    if not ACHIEVEMENTS["rice_king"]["unlocked"] and rice_harvest >= 50000:
        ACHIEVEMENTS["rice_king"]["unlocked"] = True
        data['money'] += ACHIEVEMENTS["rice_king"]["bonus"]
        achievements_unlocked.append(ACHIEVEMENTS["rice_king"])
        name = ACHIEVEMENTS["rice_king"]["name_uk"] if current_language == "uk" else ACHIEVEMENTS["rice_king"]["name_en"]
        print(f"\n🏆 {name}!")
        print(f"   +{ACHIEVEMENTS['rice_king']['bonus']:,} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}!")
    
    if not ACHIEVEMENTS["grape_master"]["unlocked"] and grape_harvest >= 25000:
        ACHIEVEMENTS["grape_master"]["unlocked"] = True
        data['money'] += ACHIEVEMENTS["grape_master"]["bonus"]
        achievements_unlocked.append(ACHIEVEMENTS["grape_master"])
        name = ACHIEVEMENTS["grape_master"]["name_uk"] if current_language == "uk" else ACHIEVEMENTS["grape_master"]["name_en"]
        print(f"\n🏆 {name}!")
        print(f"   +{ACHIEVEMENTS['grape_master']['bonus']:,} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}!")
    
    return achievements_unlocked

def show_achievements():
    print("\n" + "="*50)
    print("🏆 " + get_text("achievements"))
    print("="*50)
    
    for key, ach in ACHIEVEMENTS.items():
        status = "✅" if ach["unlocked"] else "❌"
        name = ach["name_uk"] if current_language == "uk" else ach["name_en"]
        desc = ach["desc_uk"] if current_language == "uk" else ach["desc_en"]
        print(f"{status} {name}: {desc} (+{ach['bonus']:,} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')})")
    print("="*50)

def update_animals(data):
    if not data.get('animals'):
        return
    
    total_income = 0
    for animal in data['animals']:
        if animal['type'] == 'cow':
            income = ANIMALS['cow']['daily_income']
            total_income += income
            name = ANIMALS['cow']["name_uk"] if current_language == "uk" else ANIMALS['cow']["name_en"]
            print(f"   {name} +{income} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}")
        elif animal['type'] == 'chicken':
            income = ANIMALS['chicken']['daily_income']
            total_income += income
            name = ANIMALS['chicken']["name_uk"] if current_language == "uk" else ANIMALS['chicken']["name_en"]
            print(f"   {name} +{income} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}")
        elif animal['type'] == 'pig':
            animal['days'] = animal.get('days', 0) + 1
            if animal['days'] >= ANIMALS['pig']['days_to_mature'] and not animal.get('ready', False):
                animal['ready'] = True
                sell_price = ANIMALS['pig']['sell_price']
                print(f"   🐖 {get_text('sell_item')} {sell_price} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}!")
    
    if total_income > 0:
        data['money'] += total_income
        print(f"   💰 +{total_income} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}!")

def update_stocks(data):
    if 'stocks' not in data or not data['stocks']:
        data['stocks'] = {}
        for key, stock in STOCKS.items():
            data['stocks'][key] = stock['price']
        return
    
    changes = []
    for key in STOCKS:
        if key not in data['stocks']:
            data['stocks'][key] = STOCKS[key]['price']
        old_price = data['stocks'][key]
        change = random.uniform(-STOCKS[key]['volatility'], STOCKS[key]['volatility'])
        new_price = int(old_price * (1 + change))
        new_price = max(10, new_price)
        data['stocks'][key] = new_price
        changes.append((STOCKS[key]['name'], old_price, new_price))
    
    if changes:
        print("\n📊 " + (get_text("stocks") if current_language == "uk" else "STOCK MARKET:"))
        for name, old, new in changes:
            diff = ((new - old) / old) * 100
            if diff >= 0:
                print(f"   {name}: {old} → {new} (+{diff:+.1f}%)")
            else:
                print(f"   {name}: {old} → {new} ({diff:+.1f}%)")

def trigger_new_event(data, harvest_amount):
    rand = random.randint(1, 100)
    cumulative = 0
    
    for event_key, event_data in NEW_EVENTS.items():
        cumulative += event_data["chance"]
        if rand <= cumulative:
            name = event_data["name_uk"] if current_language == "uk" else event_data["name_en"]
            desc = event_data["desc_uk"] if current_language == "uk" else event_data["desc_en"]
            print(f"\n{'='*50}")
            print(f"{name} - {desc}")
            print(f"{'='*50}")
            
            if event_key == "tax":
                data['money'] -= 1000
                print(f"💰 -1,000 {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}!")
                return harvest_amount
            elif event_key == "hail":
                harvest_amount = int(harvest_amount * 0.5)
                print(f"🌾 {get_text('sell_item')}: {harvest_amount:,} kg!")
                return harvest_amount
            elif event_key == "exhibition":
                data['money'] += 10000
                print(f"💰 +10,000 {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}!")
                return harvest_amount
            elif event_key == "epidemic":
                if data.get('animals'):
                    for animal in data['animals']:
                        animal['health'] = max(0, animal['health'] - 50)
                    print(f"🦠 -50% {get_text('animals') if current_language == 'uk' else 'animal health'}!")
                return harvest_amount
    
    return harvest_amount

def get_equipped_units(data):
    eq = {}
    for eq_type, idx in data['equipped_ids'].items():
        if idx is not None and 0 <= idx < len(data['garage']):
            eq[eq_type] = data['garage'][idx]
        else:
            eq[eq_type] = None
    return eq

def show_bins(data):
    print("\n" + "="*50)
    print("🌾 " + get_text("bins"))
    print("="*50)
    
    for crop, amount in data['bins'].items():
        percent = (amount / BUNKER_CAPACITY) * 100
        bar_length = int(percent / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        crop_factor = data["economy"]["crops"].get(crop, 1.0)
        current_price = get_current_price(BASE_PRICES.get(crop, 10), crop_factor)
        
        special_marker = ""
        if crop == "Рис":
            special_marker = " 🍚"
        elif crop == "Виноград":
            special_marker = " 🍇"
        
        print(f"{crop:12}{special_marker} {bar} {amount:,} / {BUNKER_CAPACITY:,} kg - {current_price} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}/kg")
    
    total = sum(data['bins'].values())
    print("-"*50)
    print(f"📊 {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}: {total:,} kg")

def show_animals_status(data):
    if not data.get('animals'):
        print("🐄 " + (get_text("animals") if current_language == "uk" else "No animals on farm"))
        return
    
    cows = sum(1 for a in data['animals'] if a['type'] == 'cow')
    pigs = sum(1 for a in data['animals'] if a['type'] == 'pig')
    chickens = sum(1 for a in data['animals'] if a['type'] == 'chicken')
    ready_pigs = sum(1 for a in data['animals'] if a['type'] == 'pig' and a.get('ready', False))
    
    print("\n🐄 " + (get_text("animals") if current_language == "uk" else "FARM STATUS:"))
    cow_name = ANIMALS['cow']["name_uk"] if current_language == "uk" else ANIMALS['cow']["name_en"]
    pig_name = ANIMALS['pig']["name_uk"] if current_language == "uk" else ANIMALS['pig']["name_en"]
    chicken_name = ANIMALS['chicken']["name_uk"] if current_language == "uk" else ANIMALS['chicken']["name_en"]
    print(f"   {cow_name}: {cows} (50 {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}/day)")
    print(f"   {pig_name}: {pigs} ({get_text('sell_item') if current_language == 'uk' else 'ready to sell'}: {ready_pigs})")
    print(f"   {chicken_name}: {chickens} (30 {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}/day)")

def show_portfolio(data):
    if not data.get('portfolio'):
        print("📈 " + (get_text("stocks") if current_language == "uk" else "No stocks in portfolio"))
        return
    
    print("\n📊 " + (get_text("stocks") if current_language == "uk" else "STOCK PORTFOLIO:"))
    total = 0
    for key, amount in data['portfolio'].items():
        if key in data['stocks']:
            current_price = data['stocks'][key]
            value = amount * current_price
            total += value
            print(f"   {STOCKS[key]['name']}: {amount} x {current_price} = {value:,} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}")
        else:
            print(f"   {STOCKS.get(key, {}).get('name', key)}: {amount} (price unknown)")
    print(f"   {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}: {total:,} {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}")

def ensure_save_dir():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def get_save_files():
    ensure_save_dir()
    saves = []
    for i in range(1, MAX_SAVES + 1):
        save_path = os.path.join(SAVE_DIR, f"save_{i}.json")
        if os.path.exists(save_path):
            try:
                with open(save_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                saves.append({
                    "slot": i,
                    "nickname": data.get("nickname", "Unknown"),
                    "difficulty": data.get("difficulty", "нормальна"),
                    "money": data.get("money", 0),
                    "day": data.get("day", 1),
                    "exists": True
                })
            except:
                saves.append({"slot": i, "exists": False, "nickname": None})
        else:
            saves.append({"slot": i, "exists": False, "nickname": None})
    return saves

def create_new_game(slot, nickname, difficulty):
    ensure_save_dir()
    diff_settings = DIFFICULTY_SETTINGS[difficulty]
    
    starter_equipment = []
    if difficulty == "легка":
        starter_equipment = [
            {"model": "Т-25", "price": 15000, "fuel_cons": 5, "tank": 40, "tier": 1, "brand": "Soviet", "country": "Soviet", "type": "tractor", "cond": 100, "fuel": 40, "buy_day": 1},
            {"model": "Нива Ефект", "price": 25000, "cap": 800, "fuel_cons": 15, "tank": 120, "tier": 1, "brand": "Ukraine", "country": "Ukraine", "type": "harvester", "cond": 100, "fuel": 120, "buy_day": 1},
            {"model": "КПС-4", "price": 5000, "eff": 1.1, "tier": 1, "brand": "Ukraine", "country": "Ukraine", "type": "cultivator", "cond": 100, "buy_day": 1},
            {"model": "СЗ-3.6", "price": 8000, "y_mod": 1.0, "tier": 1, "brand": "Ukraine", "country": "Ukraine", "type": "seeder", "cond": 100, "buy_day": 1}
        ]
        starter_money = diff_settings["money"]
    else:
        starter_equipment = []
        starter_money = diff_settings["money"]
    
    data = {
        "slot": slot,
        "nickname": nickname,
        "difficulty": difficulty,
        "money": starter_money,
        "day": 1,
        "garage": starter_equipment,
        "bins": {crop: 0 for crop in CROPS.keys()},
        "my_fields": [f for f in FIELDS_DATA if f["owned"]],
        "equipped_ids": {"tractor": 0 if starter_equipment else None, 
                        "harvester": 1 if len(starter_equipment) > 1 else None,
                        "cultivator": 2 if len(starter_equipment) > 2 else None,
                        "seeder": 3 if len(starter_equipment) > 3 else None},
        "loan": 0,
        "max_loan_taken": 0,
        "economy": generate_economy(),
        "used_promocodes": [],
        "active_effects": {},
        "fertilizer_stock": 0,
        "herbicide_stock": 0,
        "last_economy_day": 1,
        "total_earned": 0,
        "total_harvested_ha": 0,
        "total_harvest": {crop: 0 for crop in CROPS.keys()},
        "animals": [],
        "stocks": {key: stock["price"] for key, stock in STOCKS.items()},
        "portfolio": {},
        "game_completed": False,
        "cheat_mode": False
    }
    
    for key in ACHIEVEMENTS:
        data[key] = False
    
    save_game(data)
    return data

def save_game(data):
    ensure_save_dir()
    save_path = os.path.join(SAVE_DIR, f"save_{data['slot']}.json")
    save_data = data.copy()
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=4)

def load_game_from_slot(slot):
    save_path = os.path.join(SAVE_DIR, f"save_{slot}.json")
    if os.path.exists(save_path):
        with open(save_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for key in ACHIEVEMENTS:
            ACHIEVEMENTS[key]["unlocked"] = data.get(key, False)
        
        if 'economy' in data and 'crops' in data['economy']:
            for crop in CROPS.keys():
                if crop not in data['economy']['crops']:
                    data['economy']['crops'][crop] = 1.0
        else:
            data['economy'] = generate_economy()
        
        if 'my_fields' in data:
            existing_field_names = [f.get("name_uk", f.get("name_en", "")) for f in data['my_fields']]
            for field in FIELDS_DATA:
                field_name = field["name_uk"] if current_language == "uk" else field["name_en"]
                if field["owned"] and field_name not in existing_field_names:
                    data['my_fields'].append(field)
        
        if 'stocks' not in data or not data['stocks']:
            data['stocks'] = {key: stock["price"] for key, stock in STOCKS.items()}
        
        for crop in CROPS.keys():
            if crop not in data['bins']:
                data['bins'][crop] = 0
            if crop not in data['total_harvest']:
                data['total_harvest'][crop] = 0
        
        return data
    return None

def delete_save(slot):
    save_path = os.path.join(SAVE_DIR, f"save_{slot}.json")
    if os.path.exists(save_path):
        os.remove(save_path)
        return True
    return False

def select_save_menu():
    while True:
        print("\n" + "="*60)
        print(get_text("game_title"))
        print("="*60)
        print("\n" + get_text("save_select"))
        
        saves = get_save_files()
        
        for save in saves:
            if save["exists"]:
                diff_name = get_difficulty_name(save["difficulty"])
                print(f"\n  {save['slot']}. 👤 {save['nickname']} | {diff_name} | {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}: {save['money']:,} | {get_text('day').split()[1] if ' ' in get_text('day') else get_text('day')}: {save['day']}")
            else:
                print(f"\n  {save['slot']}. {get_text('empty_slot')}")
        
        print(f"\n  4. {get_text('delete_save')}")
        print(f"  0. {get_text('exit')}")
        
        choice = input(f"\n👉 {get_text('back') if current_language == 'uk' else 'Your choice'}: ")
        
        if choice == "0":
            return None, None, None
        elif choice == "4":
            try:
                del_slot = int(input("Slot number (1-3): "))
                if 1 <= del_slot <= MAX_SAVES:
                    if delete_save(del_slot):
                        print(f"✅ Save {del_slot} deleted!")
                    else:
                        print(f"❌ Slot {del_slot} is empty!")
                else:
                    print(get_text("invalid_choice"))
            except:
                print(get_text("invalid_choice"))
            input("Press Enter...")
            continue
        else:
            try:
                slot = int(choice)
                if 1 <= slot <= MAX_SAVES:
                    save_data = get_save_files()[slot - 1]
                    if save_data["exists"]:
                        data = load_game_from_slot(slot)
                        if data:
                            difficulty = data.get("difficulty", "нормальна")
                            return data, difficulty, data.get("nickname", "Farmer")
                    else:
                        print("\n" + get_text("new_game"))
                        nickname = input(get_text("nickname") + ": ").strip()
                        if not nickname:
                            nickname = f"Farmer{slot}"
                        
                        print(f"\n{get_text('difficulty_choice')}:")
                        for i, (key, settings) in enumerate(DIFFICULTY_SETTINGS.items(), 1):
                            diff_name = settings["name_en"] if current_language == "en" else settings["name_uk"]
                            print(f"  {i}. {diff_name} - {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}: {settings['money']:,}")
                        
                        diff_choice = input(f"\n👉 {get_text('back') if current_language == 'uk' else 'Your choice'}: ")
                        diff_map = {"1": "легка", "2": "нормальна", "3": "хард"}
                        difficulty = diff_map.get(diff_choice, "нормальна")
                        
                        data = create_new_game(slot, nickname, difficulty)
                        return data, difficulty, nickname
                else:
                    print(get_text("invalid_choice"))
            except:
                print(get_text("invalid_choice"))
            input("Press Enter...")

def complete_game(data):
    if data.get("difficulty") != "нормальна":
        print("\n❌ " + (get_text("invalid_choice") if current_language == "uk" else "Only NORMAL difficulty can complete the game with 500 million UAH!"))
        input("Press Enter...")
        return False
    
    if data.get("game_completed"):
        print("\n🏆 " + (get_text("achievements") if current_language == "uk" else "You already completed the game! CHEAT MODE enabled!"))
        return True
    
    if data.get("money", 0) >= 500000000:
        print("\n" + "="*60)
        print("🏆 " + (get_text("achievements") if current_language == "uk" else "CONGRATULATIONS! YOU COMPLETED THE GAME!") + " 🏆")
        print("="*60)
        print(f"\n👤 {get_text('tractor') if current_language == 'uk' else 'Farmer'}: {data['nickname']}")
        print(f"📅 {get_text('day').split()[1] if ' ' in get_text('day') else get_text('day')}: {data['day']}")
        print(f"💰 {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}: {data.get('total_earned', 0):,} UAH")
        print("\n🎁 " + (get_text("success") if current_language == "uk" else "YOU RECEIVED:"))
        print("   🏆 " + (ACHIEVEMENTS["game_complete"]["name_uk"] if current_language == "uk" else ACHIEVEMENTS["game_complete"]["name_en"]))
        print("   🔓 " + (get_text("settings") if current_language == "uk" else "SECRET MODE - CHEAT MODE!"))
        
        ACHIEVEMENTS["game_complete"]["unlocked"] = True
        data["game_completed"] = True
        data["cheat_mode"] = True
        save_game(data)
        
        print("\n" + (get_text("settings_saved") if current_language == "uk" else "Now in CHEAT MODE you can enter 'CHEATMONEY' promo code to get money!"))
        input("\nPress Enter...")
        return True
    
    print(f"\n❌ {get_text('not_enough_money') if current_language == 'uk' else 'Need'} {500000000 - data['money']:,} UAH {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')} {get_text('back') if current_language == 'uk' else 'more'}!")
    input("Press Enter...")
    return False

def bank_menu(data):
    while True:
        print(f"\n--- " + (get_text("bank") if current_language == "uk" else "CENTRAL BANK") + " ---")
        print(f"{get_text('money')}: {data['money']:,} UAH")
        print(f"{get_text('loan')}: {data['loan']:,} UAH (5% " + (get_text("day").split()[1] if ' ' in get_text("day") else get_text("day")) + ")")
        
        diff_settings = DIFFICULTY_SETTINGS.get(data.get("difficulty", "нормальна"), DIFFICULTY_SETTINGS["нормальна"])
        max_loan = diff_settings["loan_max"]
        
        menu_options = "\n1. " + (get_text("buy") if current_language == "uk" else "Take loan") + f" (max {max_loan:,})"
        menu_options += " | 2. " + (get_text("sell_item") if current_language == "uk" else "Repay loan") + " | 3. " + (get_text("exit") if current_language == "uk" else "Complete game") + " (500 mil)"
        if data.get("cheat_mode"):
            menu_options += " | 4. CHEAT: " + (get_text("buy") if current_language == "uk" else "Get money")
        
        c = input(f"{menu_options} | 0. {get_text('back') if current_language == 'uk' else 'Back'}: ")
        
        if c == "0":
            break
        elif c == "1":
            try:
                amount = int(input((get_text("buy") if current_language == "uk" else "Loan amount") + ": "))
                if data['loan'] + amount <= max_loan and amount > 0:
                    data['loan'] += amount
                    data['money'] += amount
                    if data['loan'] > data.get('max_loan_taken', 0):
                        data['max_loan_taken'] = data['loan']
                    print(f"✅ +{amount:,} UAH!")
                else:
                    print(f"❌ Max: {max_loan - data['loan']:,} UAH")
            except:
                print(get_text("invalid_choice"))
        elif c == "2":
            try:
                pay = int(input((get_text("sell_item") if current_language == "uk" else "Amount to repay") + ": "))
                if pay <= data['money'] and pay <= data['loan'] and pay > 0:
                    data['money'] -= pay
                    data['loan'] -= pay
                    print(get_text("success"))
                else:
                    print(get_text("not_enough_money"))
            except:
                print(get_text("invalid_choice"))
        elif c == "3":
            complete_game(data)
        elif c == "4" and data.get("cheat_mode"):
            print("\n🎁 CHEAT MODE ACTIVATED!")
            try:
                cheat_amount = int(input("How much money to give yourself? "))
                if cheat_amount > 0:
                    data['money'] += cheat_amount
                    print(f"✅ +{cheat_amount:,} UAH!")
            except:
                print(get_text("invalid_choice"))

def planting_menu(data):
    diff_settings = DIFFICULTY_SETTINGS.get(data.get("difficulty", "нормальна"), DIFFICULTY_SETTINGS["нормальна"])
    season = get_season(data['day'])
    season_effect = get_season_effect(season)
    
    if season == "Зима" or season == "Winter":
        print("\n❌ " + (get_text("invalid_choice") if current_language == "uk" else "Cannot plant in winter! Wait for spring."))
        print("   " + (get_text("animals") if current_language == "uk" else "Take care of animals or trade stocks."))
        input("Press Enter...")
        return
    
    eq_check = get_equipped_units(data)
    missing = [t for t in ['tractor', 'harvester', 'cultivator', 'seeder'] if eq_check[t] is None]
    if missing:
        print(f"❌ " + (get_text("invalid_choice") if current_language == "uk" else f"Missing equipment: {', '.join(missing)}"))
        input("Press Enter...")
        return
    
    print(f"\n🌤️ {get_text('season')}: {season} ({get_text('sell_item') if current_language == 'uk' else 'effect'}: {season_effect*100:.0f}%)")
    print(f"⭐ {get_text('difficulty_choice').split(':')[0] if ':' in get_text('difficulty_choice') else get_text('difficulty_choice')}: {get_difficulty_name(data['difficulty'])} (x{int(diff_settings['crop_multiplier']*100)}%)")
    
    print("\n📋 " + (get_text("back") if current_language == "uk" else "Your fields:"))
    for i, f in enumerate(data['my_fields']):
        field_name = f["name_uk"] if current_language == "uk" else f["name_en"]
        field_type_marker = ""
        if f.get("type") == "рисове":
            field_type_marker = " 🌾🍚"
        elif f.get("type") == "виноградне":
            field_type_marker = " 🍇"
        print(f"{i+1}. {field_name}{field_type_marker} - {f['size']} ha")
    
    try:
        field_idx = int(input("\n" + (get_text("back") if current_language == "uk" else "Choose field number") + ": ")) - 1
        if field_idx < 0 or field_idx >= len(data['my_fields']):
            print(get_text("invalid_choice"))
            return
        field = data['my_fields'][field_idx]
    except:
        print(get_text("invalid_choice"))
        return
    
    print("\n🌱 " + (get_text("fertilizer") if current_language == "uk" else "Crops:"))
    crops_list = list(CROPS.keys())
    
    if field.get("type") == "рисове":
        available_crops = ["Рис"]
        print("⚠️ " + (get_text("fertilizer") if current_language == "uk" else "This is a rice field! Only rice can be grown here."))
    elif field.get("type") == "виноградное" or field.get("type") == "виноградне":
        available_crops = ["Виноград"]
        print("⚠️ " + (get_text("fertilizer") if current_language == "uk" else "This is a vineyard! Only grapes can be grown here."))
    else:
        available_crops = [c for c in crops_list if c not in ["Рис", "Виноград"]]
    
    for i, crop in enumerate(available_crops, 1):
        crop_factor = data["economy"]["crops"].get(crop, 1.0)
        current_price = get_current_price(BASE_PRICES.get(crop, 10), crop_factor)
        special_info = f" ({CROPS[crop].get('special', '')})" if CROPS[crop].get('special') else ""
        print(f"{i}. {crop}{special_info} - {current_price} UAH/kg (yield: {CROPS[crop]['y']}x)")
    
    crop_choice = input((get_text("back") if current_language == "uk" else "Your choice") + ": ")
    try:
        crop_idx = int(crop_choice) - 1
        if crop_idx < 0 or crop_idx >= len(available_crops):
            print(get_text("invalid_choice"))
            return
        crop = available_crops[crop_idx]
    except:
        print(get_text("invalid_choice"))
        return
    
    use_fertilizer = input("\n" + (get_text("fertilizer") if current_language == "uk" else "Use fertilizer? (+30%) (yes/no): ")).lower() in ["yes", "так", "y", "1"]
    fertilizer_boost = 1.0
    
    if use_fertilizer and data['fertilizer_stock'] >= field['size'] * 8:
        data['fertilizer_stock'] -= int(field['size'] * 8)
        fertilizer_boost = 1.3
        print(get_text("success"))
    elif use_fertilizer:
        print(get_text("not_enough_money"))
        fertilizer_boost = 1.0
    
    use_herbicide = input((get_text("herbicide") if current_language == "uk" else "Use herbicide? (yes/no): ")).lower() in ["yes", "так", "y", "1"]
    if use_herbicide and data['herbicide_stock'] >= field['size'] * 4:
        data['herbicide_stock'] -= int(field['size'] * 4)
        print(get_text("success"))
    elif use_herbicide:
        print(get_text("not_enough_money"))
        use_herbicide = False
    
    tractor = eq_check['tractor']
    harvester = eq_check['harvester']
    
    tractor_fuel = field['size'] * tractor['fuel_cons'] * 0.4
    harvester_fuel = field['size'] * harvester['fuel_cons'] * 0.6
    
    if tractor.get('fuel', 0) < tractor_fuel:
        print(f"❌ " + (get_text("tractor") if current_language == "uk" else "Tractor needs more fuel!"))
        return
    if harvester.get('fuel', 0) < harvester_fuel:
        print(f"❌ " + (get_text("harvester") if current_language == "uk" else "Harvester needs more fuel!"))
        return
    
    if data['loan'] > 0:
        interest = int(data['loan'] * 0.05)
        data['loan'] += interest
        print(f"🏦 " + (get_text("bank") if current_language == "uk" else "Bank charged") + f" {interest} UAH {get_text('fertilizer').split()[1] if ' ' in get_text('fertilizer') else get_text('interest')}!")
    
    tier_sum = (tractor.get('tier', 1) + harvester.get('tier', 1) + 
               eq_check['cultivator'].get('tier', 1) + eq_check['seeder'].get('tier', 1))
    avg_tier = tier_sum / 4
    
    base_yield = field['size'] * 150
    harvest = int(base_yield * CROPS[crop]['y'] * eq_check['seeder'].get('y_mod', 1.0) * 
                  (1 + (avg_tier - 1) * 0.1) * fertilizer_boost * season_effect * diff_settings['crop_multiplier'])
    
    if not use_herbicide and random.random() < 0.3:
        harvest = int(harvest * 0.7)
        print("🌿 " + (get_text("herbicide") if current_language == "uk" else "Weeds destroyed 30% of the harvest!"))
    
    harvest = trigger_new_event(data, harvest)
    harvest = min(harvest, harvester.get('cap', 1000))
    
    if data['bins'][crop] + harvest > BUNKER_CAPACITY:
        harvest = BUNKER_CAPACITY - data['bins'][crop]
        if harvest <= 0:
            print("❌ " + (get_text("bins") if current_language == "uk" else "Bin is full!"))
            return
    
    tractor['fuel'] = max(0, tractor.get('fuel', 0) - int(tractor_fuel))
    harvester['fuel'] = max(0, harvester.get('fuel', 0) - int(harvester_fuel))
    tractor['cond'] = max(0, tractor.get('cond', 100) - 8)
    harvester['cond'] = max(0, harvester.get('cond', 100) - 10)
    
    data['bins'][crop] += harvest
    if 'total_harvest' not in data:
        data['total_harvest'] = {crop: 0 for crop in CROPS.keys()}
    data['total_harvest'][crop] = data['total_harvest'].get(crop, 0) + harvest
    data['total_harvested_ha'] = data.get('total_harvested_ha', 0) + field['size']
    data['day'] += 1
    
    update_animals(data)
    update_stocks(data)
    
    crop_factor = data["economy"]["crops"].get(crop, 1.0)
    current_price = get_current_price(BASE_PRICES.get(crop, 10), crop_factor)
    print(f"\n✅ " + (get_text("sell_item") if current_language == "uk" else "Harvested") + f" {harvest:,} kg {crop}!")
    print(f"💰 {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}: {harvest * current_price:,} UAH")
    input("Press Enter...")

def sell_crops(data):
    total = 0
    print("\n📦 " + (get_text("sell") if current_language == "uk" else "SELL CROPS"))
    
    for crop, amount in data['bins'].items():
        if amount > 0:
            crop_factor = data["economy"]["crops"].get(crop, 1.0)
            price = get_current_price(BASE_PRICES.get(crop, 10), crop_factor)
            value = amount * price
            total += value
            special_marker = ""
            if crop == "Рис":
                special_marker = " 🍚"
            elif crop == "Виноград":
                special_marker = " 🍇"
            print(f"{crop}{special_marker}: {amount:,} kg x {price} = {value:,} UAH")
    
    if total > 0:
        confirm = input(f"\n" + (get_text("sell") if current_language == "uk" else "Sell all crops for") + f" {total:,} UAH? (yes/no): ")
        if confirm.lower() in ["yes", "так", "y", "1"]:
            data['money'] += total
            data['total_earned'] = data.get('total_earned', 0) + total
            data['bins'] = {crop: 0 for crop in CROPS.keys()}
            check_achievements(data)
            print(f"✅ {get_text('sell') if current_language == 'uk' else 'Sold for'} {total:,} UAH!")
    else:
        print("❌ " + (get_text("sell") if current_language == "uk" else "No crops to sell!"))
    input("Press Enter...")

def shop_menu(data):
    while True:
        print("\n" + "="*50)
        print("🛒 " + get_text("shop"))
        print("="*50)
        print(f"{get_text('money')}: {data['money']:,} UAH")
        print("\n1. 🚜 " + get_text("tractor"))
        print("2. 🌱 " + get_text("fertilizer") + " (+30% " + (get_text("sell") if current_language == "uk" else "to yield") + ")")
        print("3. 🌿 " + get_text("herbicide") + " (85% " + (get_text("sell") if current_language == "uk" else "protection") + ")")
        print("4. 🐄 " + get_text("animals"))
        print("5. 📈 " + get_text("stocks"))
        print("6. 🏞️ " + (get_text("buy") if current_language == "uk" else "Buy field"))
        print("7. 🍚 " + (get_text("buy") if current_language == "uk" else "Buy specialized field") + " (Rice/Grapes)")
        print("0. " + get_text("back"))
        
        choice = input("\n" + (get_text("back") if current_language == "uk" else "Your choice") + ": ")
        
        if choice == "0":
            break
        elif choice == "1":
            equipment_shop(data)
        elif choice == "2":
            fertilizer_shop(data)
        elif choice == "3":
            herbicide_shop(data)
        elif choice == "4":
            buy_animal(data)
        elif choice == "5":
            buy_stock_menu(data)
        elif choice == "6":
            buy_field_menu(data)
        elif choice == "7":
            buy_special_field_menu(data)

def buy_special_field_menu(data):
    print("\n🍚 " + (get_text("buy") if current_language == "uk" else "SPECIALIZED FIELDS"))
    
    special_fields = [f for f in FIELDS_DATA if not f["owned"] and f["id"] > 10]
    if not special_fields:
        print("🎉 " + (get_text("success") if current_language == "uk" else "You already own all specialized fields!"))
        input("Press Enter...")
        return
    
    print("\n" + (get_text("buy") if current_language == "uk" else "Available specialized fields") + ":")
    for i, field in enumerate(special_fields, 1):
        field_name = field["name_uk"] if current_language == "uk" else field["name_en"]
        field_emoji = "🌾🍚" if field["type"] == "рисове" else "🍇"
        print(f"{i}. {field_emoji} {field_name} - {field['size']} ha - {field['price']:,} UAH")
    
    try:
        choice = int(input("\n" + (get_text("back") if current_language == "uk" else "Choose field (0 to cancel)") + ": "))
        if choice == 0:
            return
        field = special_fields[choice - 1]
        
        if data['money'] >= field['price']:
            data['money'] -= field['price']
            field['owned'] = True
            data['my_fields'].append(field)
            field_name = field["name_uk"] if current_language == "uk" else field["name_en"]
            print(f"✅ " + (get_text("buy") if current_language == "uk" else "Bought") + f" {field_name}!")
        else:
            print(f"❌ " + (get_text("not_enough_money") if current_language == "uk" else f"Need {field['price'] - data['money']:,} UAH more!"))
    except:
        print(get_text("invalid_choice"))
    input("Press Enter...")

def equipment_shop(data):
    print("\n🚜 " + (get_text("shop") if current_language == "uk" else "EQUIPMENT SHOP"))
    print(f"💰 {get_text('money').split()[1] if ' ' in get_text('money') else get_text('money')}: {data['economy']['equipment']*100:.0f}%")
    
    print("\n1. " + (get_text("tractor") if current_language == "uk" else "Tractors"))
    print("2. " + (get_text("harvester") if current_language == "uk" else "Harvesters"))
    print("3. " + (get_text("cultivator") if current_language == "uk" else "Cultivators"))
    print("4. " + (get_text("seeder") if current_language == "uk" else "Seeders"))
    print("0. " + get_text("back"))
    
    cat_choice = input((get_text("back") if current_language == "uk" else "Your choice") + ": ")
    
    if cat_choice == "0":
        return
    
    cat_map = {"1": "tractor", "2": "harvester", "3": "cultivator", "4": "seeder"}
    if cat_choice not in cat_map:
        print(get_text("invalid_choice"))
        return
    
    cat = cat_map[cat_choice]
    cat_title = get_text(cat) if cat in ["tractor", "harvester", "cultivator", "seeder"] else cat
    
    equipment_list = CATALOG[cat].copy()
    sorted_list = show_sorted_equipment(equipment_list, cat_title, data)
    if sorted_list is None:
        return
    elif sorted_list:
        equipment_list = sorted_list
    
    print(f"\n📋 {cat_title}:")
    for i, item in enumerate(equipment_list):
        current_price = get_current_price(item['price'], data["economy"]["equipment"])
        brand_info = f"[{COUNTRIES.get(item.get('country', ''), item.get('brand', 'Unknown'))}]"
        special_info = f" 🍇" if item.get('special') == "виноградний" else (f" 🍚" if item.get('special') == "рисовий" else "")
        print(f"{i+1}. {brand_info}{special_info} {item['model']} - {current_price:,} UAH (tier {item['tier']})")
    
    try:
        idx = int(input("\n" + (get_text("buy") if current_language == "uk" else "Choose number (0 to cancel)") + ": ")) - 1
        if idx < 0:
            return
        if idx >= len(equipment_list):
            print(get_text("invalid_choice"))
            return
        
        item = equipment_list[idx].copy()
        current_price = get_current_price(item['price'], data["economy"]["equipment"])
        
        if data['money'] >= current_price:
            item['price'] = current_price
            item['type'] = cat
            item['cond'] = 100
            item['fuel'] = item.get('tank', 0)
            item['buy_day'] = data['day']
            data['garage'].append(item)
            data['money'] -= current_price
            print(f"✅ " + (get_text("buy") if current_language == "uk" else "Bought") + f" {item['model']}!")
        else:
            print(f"❌ " + (get_text("not_enough_money") if current_language == "uk" else f"Need {current_price - data['money']:,} UAH more!"))
    except:
        print(get_text("invalid_choice"))
    input("Press Enter...")

def fertilizer_shop(data):
    print("\n🌱 " + (get_text("fertilizer") if current_language == "uk" else "FERTILIZER"))
    print(f"{get_text('fertilizer').split()[1] if ' ' in get_text('fertilizer') else get_text('stock')}: {data['fertilizer_stock']} kg")
    
    for i, item in enumerate(CATALOG["fertilizer"], 1):
        name = item["name_uk"] if current_language == "uk" else item["name_en"]
        print(f"{i}. {name} - {item['price']} UAH ({item['use_per_ha']} kg/ha)")
    
    try:
        choice = int(input("\n" + (get_text("back") if current_language == "uk" else "Choose (0 to cancel)") + ": "))
        if choice == 0:
            return
        item = CATALOG["fertilizer"][choice - 1]
        amount = int(input("How many kg to buy? "))
        total_cost = int((amount / item['use_per_ha']) * item['price'])
        
        if total_cost <= data['money'] and amount > 0:
            data['money'] -= total_cost
            data['fertilizer_stock'] += amount
            print(f"✅ " + (get_text("buy") if current_language == "uk" else "Bought") + f" {amount} kg!")
        else:
            print(get_text("not_enough_money"))
    except:
        print(get_text("invalid_choice"))
    input("Press Enter...")

def herbicide_shop(data):
    print("\n🌿 " + (get_text("herbicide") if current_language == "uk" else "HERBICIDE"))
    print(f"{get_text('herbicide').split()[1] if ' ' in get_text('herbicide') else get_text('stock')}: {data['herbicide_stock']} L")
    
    for i, item in enumerate(CATALOG["herbicide"], 1):
        name = item["name_uk"] if current_language == "uk" else item["name_en"]
        print(f"{i}. {name} - {item['price']} UAH ({item['use_per_ha']} L/ha)")
    
    try:
        choice = int(input("\n" + (get_text("back") if current_language == "uk" else "Choose (0 to cancel)") + ": "))
        if choice == 0:
            return
        item = CATALOG["herbicide"][choice - 1]
        amount = int(input("How many liters to buy? "))
        total_cost = int((amount / item['use_per_ha']) * item['price'])
        
        if total_cost <= data['money'] and amount > 0:
            data['money'] -= total_cost
            data['herbicide_stock'] += amount
            print(f"✅ " + (get_text("buy") if current_language == "uk" else "Bought") + f" {amount} L!")
        else:
            print(get_text("not_enough_money"))
    except:
        print(get_text("invalid_choice"))
    input("Press Enter...")

def buy_field_menu(data):
    print("\n🏞️ " + (get_text("buy") if current_language == "uk" else "BUY FIELD"))
    
    available = [f for f in FIELDS_DATA if not f["owned"] and f["id"] <= 10]
    if not available:
        print("🎉 " + (get_text("success") if current_language == "uk" else "You already own all standard fields!"))
        print("💡 " + (get_text("buy") if current_language == "uk" else "Try buying specialized fields (option 7 in shop)!"))
        input("Press Enter...")
        return
    
    for i, field in enumerate(available, 1):
        field_name = field["name_uk"] if current_language == "uk" else field["name_en"]
        print(f"{i}. {field_name} - {field['size']} ha - {field['price']:,} UAH")
    
    try:
        choice = int(input("\n" + (get_text("back") if current_language == "uk" else "Choose (0 to cancel)") + ": "))
        if choice == 0:
            return
        field = available[choice - 1]
        
        if data['money'] >= field['price']:
            data['money'] -= field['price']
            field['owned'] = True
            data['my_fields'].append(field)
            field_name = field["name_uk"] if current_language == "uk" else field["name_en"]
            print(f"✅ " + (get_text("buy") if current_language == "uk" else "Bought") + f" {field_name}!")
        else:
            print(f"❌ " + (get_text("not_enough_money") if current_language == "uk" else f"Need {field['price'] - data['money']:,} UAH more!"))
    except:
        print(get_text("invalid_choice"))
    input("Press Enter...")

def buy_animal(data):
    print("\n" + "="*50)
    print("🐄 " + (get_text("animals") if current_language == "uk" else "ANIMAL FARM"))
    print("="*50)
    
    cow_name = ANIMALS['cow']["name_uk"] if current_language == "uk" else ANIMALS['cow']["name_en"]
    pig_name = ANIMALS['pig']["name_uk"] if current_language == "uk" else ANIMALS['pig']["name_en"]
    chicken_name = ANIMALS['chicken']["name_uk"] if current_language == "uk" else ANIMALS['chicken']["name_en"]
    
    print(f"1. {cow_name} - {ANIMALS['cow']['price']} UAH (50 UAH/day)")
    print(f"2. {pig_name} - {ANIMALS['pig']['price']} UAH (10 days → sell for {ANIMALS['pig']['sell_price']} UAH)")
    print(f"3. {chicken_name} - {ANIMALS['chicken']['price']} UAH (30 UAH/day)")
    print("0. " + get_text("back"))
    
    choice = input("\n" + (get_text("back") if current_language == "uk" else "Your choice") + ": ")
    
    animal_map = {
        "1": ("cow", ANIMALS['cow']['price']),
        "2": ("pig", ANIMALS['pig']['price']),
        "3": ("chicken", ANIMALS['chicken']['price'])
    }
    
    if choice in animal_map:
        animal_type, price = animal_map[choice]
        try:
            animal_name = ANIMALS[animal_type]["name_uk"] if current_language == "uk" else ANIMALS[animal_type]["name_en"]
            amount = int(input(f"How many {animal_name} to buy? "))
            total_cost = price * amount
            if data['money'] >= total_cost:
                data['money'] -= total_cost
                if 'animals' not in data:
                    data['animals'] = []
                for _ in range(amount):
                    data['animals'].append({
                        'type': animal_type,
                        'health': ANIMALS[animal_type]['max_health'],
                        'days': 0,
                        'ready': False
                    })
                print(f"✅ " + (get_text("buy") if current_language == "uk" else "Bought") + f" {amount} {animal_name} for {total_cost:,} UAH!")
            else:
                print(f"❌ " + (get_text("not_enough_money") if current_language == "uk" else f"Need {total_cost - data['money']:,} UAH more!"))
        except:
            print(get_text("invalid_choice"))
    input("Press Enter...")

def sell_animals(data):
    if not data.get('animals'):
        print("❌ " + (get_text("sell") if current_language == "uk" else "No animals to sell!"))
        input("Press Enter...")
        return
    
    pigs_to_sell = [a for a in data['animals'] if a['type'] == 'pig' and a.get('ready', False)]
    
    print("\n🐖 " + (get_text("sell") if current_language == "uk" else "Ready to sell pigs:"))
    print(f"   {len(pigs_to_sell)} x {ANIMALS['pig']['sell_price']} = {len(pigs_to_sell) * ANIMALS['pig']['sell_price']} UAH")
    
    if pigs_to_sell:
        confirm = input((get_text("sell") if current_language == "uk" else "Sell all ready pigs? (yes/no): ")).lower()
        if confirm in ["yes", "так", "y", "1"]:
            earnings = len(pigs_to_sell) * ANIMALS['pig']['sell_price']
            data['money'] += earnings
            data['animals'] = [a for a in data['animals'] if not (a['type'] == 'pig' and a.get('ready', False))]
            print(f"✅ " + (get_text("sell") if current_language == "uk" else "Sold pigs for") + f" {earnings:,} UAH!")
    else:
        print("❌ " + (get_text("sell") if current_language == "uk" else "No ready pigs to sell!"))
    
    input("Press Enter...")

def buy_stock_menu(data):
    if 'stocks' not in data or not data['stocks']:
        data['stocks'] = {key: stock["price"] for key, stock in STOCKS.items()}
    
    print("\n" + "="*50)
    print("📈 " + (get_text("stocks") if current_language == "uk" else "BUY STOCKS"))
    print("="*50)
    
    for key, stock in STOCKS.items():
        current_price = data['stocks'].get(key, stock['price'])
        print(f"{stock['name']} ({key}): {current_price} UAH")
    
    print("\n" + (get_text("buy") if current_language == "uk" else "Available companies") + ": JohnDeere, CNH, AGCO")
    choice = input("\n" + (get_text("buy") if current_language == "uk" else "Choose company") + ": ").strip()
    
    if choice not in STOCKS:
        print(get_text("invalid_choice"))
        input("Press Enter...")
        return
    
    try:
        amount = int(input("How many shares to buy? "))
        if amount <= 0:
            print(get_text("invalid_choice"))
            input("Press Enter...")
            return
        
        current_price = data['stocks'].get(choice, STOCKS[choice]['price'])
        total_cost = current_price * amount
        
        if data['money'] >= total_cost:
            data['money'] -= total_cost
            if 'portfolio' not in data:
                data['portfolio'] = {}
            data['portfolio'][choice] = data['portfolio'].get(choice, 0) + amount
            print(f"✅ " + (get_text("buy") if current_language == "uk" else "Bought") + f" {amount} {STOCKS[choice]['name']} {get_text('stocks').split()[1] if ' ' in get_text('stocks') else get_text('shares')} for {total_cost:,} UAH!")
        else:
            print(f"❌ " + (get_text("not_enough_money") if current_language == "uk" else f"Need {total_cost - data['money']:,} UAH more!"))
    except ValueError:
        print(get_text("invalid_choice"))
    input("Press Enter...")

def sell_stocks(data):
    if not data.get('portfolio'):
        print("❌ " + (get_text("sell") if current_language == "uk" else "No stocks to sell!"))
        input("Press Enter...")
        return
    
    if 'stocks' not in data or not data['stocks']:
        data['stocks'] = {key: stock["price"] for key, stock in STOCKS.items()}
    
    print("\n" + "="*50)
    print("📉 " + (get_text("sell") if current_language == "uk" else "SELL STOCKS"))
    print("="*50)
    
    total_value = 0
    for key, amount in data['portfolio'].items():
        if key in STOCKS:
            current_price = data['stocks'].get(key, STOCKS[key]['price'])
            value = amount * current_price
            total_value += value
            print(f"{STOCKS[key]['name']}: {amount} x {current_price} = {value:,} UAH")
        else:
            print(f"Unknown company {key}: {amount} shares")
    
    if total_value > 0:
        confirm = input(f"\n" + (get_text("sell") if current_language == "uk" else "Sell all shares for") + f" {total_value:,} UAH? (yes/no): ").lower()
        if confirm in ["yes", "так", "y", "1"]:
            data['money'] += total_value
            data['portfolio'] = {}
            print(f"✅ " + (get_text("sell") if current_language == "uk" else "Sold shares for") + f" {total_value:,} UAH!")
    input("Press Enter...")

def garage_menu(data):
    fuel_price = get_current_price(45, data["economy"]["fuel"])
    
    while True:
        print(f"\n--- " + get_text("garage") + " ---")
        print(f"{get_text('money')}: {data['money']:,} UAH | " + (get_text("fuel") if current_language == "uk" else "Fuel price") + f": {fuel_price} UAH/L")
        
        if not data['garage']:
            print("🚜 " + (get_text("garage") if current_language == "uk" else "Garage is empty"))
            input("Press Enter...")
            break
        
        for i, u in enumerate(data['garage']):
            is_eq = any(val == i for val in data.get('equipped_ids', {}).values())
            marker = "✅" if is_eq else "⭕"
            special_marker = ""
            if u.get('special') == "виноградний":
                special_marker = " 🍇"
            elif u.get('special') == "рисовий":
                special_marker = " 🍚"
            country_name = COUNTRIES.get(u.get('country', ''), u.get('brand', '?'))
            fuel_info = f" | " + (get_text("fuel") if current_language == "uk" else "Fuel") + f": {u.get('fuel',0)}/{u.get('tank',0)}L" if 'tank' in u else ""
            print(f"{i+1}. {marker} [{country_name}]{special_marker} {u['model']} | " + (get_text("repair") if current_language == "uk" else "Condition") + f": {u.get('cond',100)}%{fuel_info}")
        
        cmd = input(f"\n(№-" + (get_text("buy") if current_language == "uk" else "Action") + "): 1-" + (get_text("refuel") if current_language == "uk" else "Refuel") + ", 2-" + (get_text("repair") if current_language == "uk" else "Repair") + ", 3-" + (get_text("sell_item") if current_language == "uk" else "Sell") + ", 4-" + (get_text("equip") if current_language == "uk" else "Equip") + " | 0-" + get_text("back") + ": ")
        if cmd == "0": 
            break
        
        try:
            parts = cmd.split("-")
            if len(parts) != 2:
                print(get_text("invalid_choice"))
                continue
            idx = int(parts[0]) - 1
            act = int(parts[1])
            
            if idx < 0 or idx >= len(data['garage']):
                print(get_text("invalid_choice"))
                continue
                
            unit = data['garage'][idx]
            
            if act == 1:
                if 'tank' in unit:
                    need = unit['tank'] - unit.get('fuel', 0)
                    if need <= 0:
                        print("✅ " + (get_text("refuel") if current_language == "uk" else "Tank is full!"))
                        continue
                    cost = need * fuel_price
                    if data['money'] >= cost:
                        data['money'] -= cost
                        unit['fuel'] = unit['tank']
                        print(f"✅ " + (get_text("refuel") if current_language == "uk" else "Refueled for") + f" {cost:,} UAH")
                    else:
                        print(f"❌ " + (get_text("not_enough_money") if current_language == "uk" else f"Need {cost - data['money']:,} UAH more!"))
            elif act == 2:
                need = 100 - unit.get('cond', 100)
                if need <= 0:
                    print("✅ " + (get_text("repair") if current_language == "uk" else "Equipment is in perfect condition!"))
                    continue
                cost = need * 250
                if data['money'] >= cost:
                    data['money'] -= cost
                    unit['cond'] = 100
                    print(f"✅ " + (get_text("repair") if current_language == "uk" else "Repaired for") + f" {cost:,} UAH")
                else:
                    print(f"❌ " + (get_text("not_enough_money") if current_language == "uk" else f"Need {cost - data['money']:,} UAH more!"))
            elif act == 3:
                price = int(unit['price'] * 0.45)
                data['money'] += price
                for k, v in data.get('equipped_ids', {}).items():
                    if v == idx:
                        data['equipped_ids'][k] = None
                    elif v is not None and v > idx:
                        data['equipped_ids'][k] -= 1
                data['garage'].pop(idx)
                print(f"✅ " + (get_text("sell_item") if current_language == "uk" else "Sold for") + f" {price:,} UAH")
            elif act == 4:
                if unit.get('type') in data.get('equipped_ids', {}):
                    data['equipped_ids'][unit['type']] = idx
                    print(f"✅ {unit['model']} " + (get_text("equip") if current_language == "uk" else "equipped!"))
        except Exception as e:
            print(f"❌ " + (get_text("invalid_choice") if current_language == "uk" else f"Error: {e}"))

def promocode_menu(data):
    print("\n🎁 " + (get_text("promocodes") if current_language == "uk" else "PROMOCODE ACTIVATION"))
    print("Available promo codes:")
    print("  • FarmMannager2026 - 20,000 UAH")
    print("  • I_am_in_debt - 45,000 UAH")
    print("  • STONKS - +50% price for 1 day")
    print("  • MECHANIC - free repair")
    print("  • FUEL_CRISIS - free fuel")
    print("  • Ya_traktor_wihanyayu - EASTER EGG! +25,000 UAH")
    
    if data.get("cheat_mode"):
        print("🔓 CHEAT MODE: CHEATMONEY - +1,000,000 UAH")
    
    code = input("\n🔑 " + (get_text("promocodes") if current_language == "uk" else "Promo code") + ": ").strip()
    
    easter_egg_variants = ["Ya_traktor_wihanyayu", "Ya_traktor_vyhanyayu", "Yatraktorwihanyayu", "ya_traktor_wihanyayu"]
    
    if code in data["used_promocodes"] and code not in easter_egg_variants and code != "CHEATMONEY":
        print(get_text("invalid_choice"))
        input("Press Enter...")
        return
    
    if code in easter_egg_variants:
        print_tractor_song()
        data["money"] += 25000
        if code not in data["used_promocodes"]:
            data["used_promocodes"].append(code)
    elif code == "FarmMannager2026":
        data["money"] += 20000
        data["used_promocodes"].append(code)
        print("✅ +20,000 UAH!")
    elif code == "I_am_in_debt":
        data["money"] += 45000
        data["used_promocodes"].append(code)
        print("✅ +45,000 UAH!")
    elif code == "STONKS":
        data['active_effects']['price_boost'] = data['day']
        data["used_promocodes"].append(code)
        print("✅ ACTIVATED! +50% PRICE TODAY!")
    elif code == "MECHANIC":
        for unit in data['garage']:
            unit['cond'] = 100
        data["used_promocodes"].append(code)
        print("✅ ALL EQUIPMENT REPAIRED!")
    elif code == "FUEL_CRISIS":
        for unit in data['garage']:
            if 'tank' in unit:
                unit['fuel'] = unit['tank']
        data["used_promocodes"].append(code)
        print("✅ ALL EQUIPMENT REFUELED!")
    elif code == "CHEATMONEY" and data.get("cheat_mode"):
        data["money"] += 1000000
        print("✅ CHEAT MODE: +1,000,000 UAH!")
    else:
        print(get_text("invalid_choice"))
    
    input("Press Enter...")

def update_economy(data):
    if data["day"] - data.get("last_economy_day", 0) >= 7:
        old_economy = data["economy"]
        data["economy"] = generate_economy()
        data["last_economy_day"] = data["day"]
        
        print("\n" + "="*50)
        print("📊 " + (get_text("stocks") if current_language == "uk" else "MARKET CHANGES:"))
        print("="*50)
        
        for crop in BASE_PRICES.keys():
            old_factor = old_economy["crops"].get(crop, 1.0)
            new_factor = data["economy"]["crops"].get(crop, 1.0)
            change = ((new_factor - old_factor) / old_factor) * 100
            symbol = "📈" if change > 0 else "📉"
            print(f"{symbol} {crop}: {change:+.1f}%")
        
        equip_change = ((data["economy"]["equipment"] - old_economy["equipment"]) / old_economy["equipment"]) * 100
        symbol = "📈" if equip_change > 0 else "📉"
        print(f"{symbol} " + (get_text("equip") if current_language == "uk" else "Equipment") + f": {equip_change:+.1f}%")
        
        fuel_change = ((data["economy"]["fuel"] - old_economy["fuel"]) / old_economy["fuel"]) * 100
        symbol = "📈" if fuel_change > 0 else "📉"
        print(f"{symbol} " + (get_text("fuel") if current_language == "uk" else "Fuel") + f": {fuel_change:+.1f}%")
        print("="*50)
        input("Press Enter...")

def main():
    load_config()
    
    data, difficulty, nickname = select_save_menu()
    
    if data is None:
        print("\n👋 " + (get_text("exit") if current_language == "uk" else "Goodbye!"))
        return
    
    for key in ACHIEVEMENTS:
        ACHIEVEMENTS[key]["unlocked"] = data.get(key, False)
    
    diff_settings = DIFFICULTY_SETTINGS[difficulty]
    
    print("="*60)
    print(get_text("game_title"))
    print("="*60)
    print(f"👤 {get_text('tractor') if current_language == 'uk' else 'Farmer'}: {nickname}")
    print(f"⭐ {get_text('difficulty_choice').split(':')[0] if ':' in get_text('difficulty_choice') else get_text('difficulty_choice')}: {get_difficulty_name(difficulty)}")
    if data.get("cheat_mode"):
        print("🔓 " + (get_text("settings") if current_language == "uk" else "CHEAT MODE ACTIVATED! (enter CHEATMONEY)"))
    print("="*60)
    
    while True:
        update_economy(data)
        
        season = get_season(data['day'])
        eq = get_equipped_units(data)
        
        print(f"\n{get_text('day')}: {data['day']} | {get_text('season')}: {season}")
        print(f"{get_text('money')}: {data['money']:,} UAH | {get_text('loan')}: {data['loan']:,} UAH")
        print(f"{get_text('fertilizer')}: {data['fertilizer_stock']} kg | {get_text('herbicide')}: {data['herbicide_stock']} L")
        print(f"{get_text('tractor')}: {eq['tractor']['model'] if eq['tractor'] else '❌ " + (get_text("back") if current_language == "uk" else "NO") + "'}")
        print(f"{get_text('harvester')}: {eq['harvester']['model'] if eq['harvester'] else '❌ " + (get_text("back") if current_language == "uk" else "NO") + "'}")
        
        print(f"\n1. {get_text('planting')}")
        print(f"2. {get_text('garage')}")
        print(f"3. {get_text('shop')}")
        print(f"4. {get_text('bank')}")
        print(f"5. {get_text('sell')}")
        print(f"6. {get_text('bins')}")
        print(f"7. {get_text('animals')}")
        print(f"8. {get_text('stocks')}")
        print(f"9. {get_text('promocodes')}")
        print(f"10. {get_text('achievements')}")
        print(f"11. {get_text('settings')}")
        print(f"12. {get_text('guide')}")
        print(f"13. {get_text('save_and_exit')}")
        
        choice = input("\n" + (get_text("back") if current_language == "uk" else "Your choice") + ": ")
        
        if choice == "1":
            planting_menu(data)
        elif choice == "2":
            garage_menu(data)
        elif choice == "3":
            shop_menu(data)
        elif choice == "4":
            bank_menu(data)
        elif choice == "5":
            sell_crops(data)
        elif choice == "6":
            show_bins(data)
            input("Press Enter...")
        elif choice == "7":
            show_animals_status(data)
            print("\n1. " + (get_text("buy") if current_language == "uk" else "Buy animals") + " | 2. " + (get_text("sell") if current_language == "uk" else "Sell pigs") + " | 0. " + get_text("back"))
            animal_choice = input((get_text("back") if current_language == "uk" else "Your choice") + ": ")
            if animal_choice == "1":
                buy_animal(data)
            elif animal_choice == "2":
                sell_animals(data)
        elif choice == "8":
            show_portfolio(data)
            print("\n1. " + (get_text("buy") if current_language == "uk" else "Buy stocks") + " | 2. " + (get_text("sell") if current_language == "uk" else "Sell stocks") + " | 0. " + get_text("back"))
            stock_choice = input((get_text("back") if current_language == "uk" else "Your choice") + ": ")
            if stock_choice == "1":
                buy_stock_menu(data)
            elif stock_choice == "2":
                sell_stocks(data)
        elif choice == "9":
            promocode_menu(data)
        elif choice == "10":
            show_achievements()
            input("Press Enter...")
        elif choice == "11":
            settings_menu()
        elif choice == "12":
            show_guide()
        elif choice == "13":
            save_game(data)
            print(f"\n💾 " + (get_text("settings_saved") if current_language == "uk" else "Game saved! Thanks for playing FARM TYCOON 2026 V2.6!"))
            break
        else:
            print(get_text("invalid_choice"))

if __name__ == "__main__":
    main()