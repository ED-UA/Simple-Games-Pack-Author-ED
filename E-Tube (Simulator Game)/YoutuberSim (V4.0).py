import random
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============= НАЛАШТУВАННЯ ТА МОВИ =============
class Settings:
    def __init__(self):
        self.language = "en"  # en, ua
        self.difficulty = "normal"  # easy, normal, hard
        self.sound = True
        self.auto_save = True
        self.load_settings()
    
    def load_settings(self):
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r", encoding='utf-8') as f:
                    data = json.load(f)
                    self.language = data.get("language", "en")
                    self.difficulty = data.get("difficulty", "normal")
                    self.sound = data.get("sound", True)
                    self.auto_save = data.get("auto_save", True)
            except:
                pass
    
    def save_settings(self):
        with open("settings.json", "w", encoding='utf-8') as f:
            json.dump({
                "language": self.language,
                "difficulty": self.difficulty,
                "sound": self.sound,
                "auto_save": self.auto_save
            }, f, indent=4)
    
    def get_text(self, key: str) -> str:
        """Отримати текст відповідно до мови"""
        texts = {
            # Головне меню
            "welcome": {"en": "WELCOME TO YOUTUBER SIMULATOR v4.0", "ua": "ЛАСКАВО ПРОСИМО ДО СИМУЛЯТОРА ЮТУБЕРА v4.0"},
            "name_prompt": {"en": "What's your name? ", "ua": "Як вас звати? "},
            "load_save": {"en": "Save found! Load it? (yes/no): ", "ua": "Знайдено збереження! Завантажити? (так/ні): "},
            
            # Статус
            "subscribers": {"en": "Subscribers", "ua": "Підписники"},
            "money": {"en": "Money", "ua": "Гроші"},
            "energy": {"en": "Energy", "ua": "Енергія"},
            "hunger": {"en": "Hunger", "ua": "Голод"},
            "thirst": {"en": "Thirst", "ua": "Спрага"},
            "videos": {"en": "Videos", "ua": "Відео"},
            "fame": {"en": "Fame", "ua": "Слава"},
            "pc_level": {"en": "PC Level", "ua": "Рівень ПК"},
            
            # Меню дій
            "menu": {"en": "MENU", "ua": "МЕНЮ"},
            "make_video": {"en": "Make a video", "ua": "Зняти відео"},
            "rest": {"en": "Rest", "ua": "Відпочити"},
            "eat_drink": {"en": "Eat/Drink", "ua": "Поїсти/Попити"},
            "upgrade_pc": {"en": "Upgrade PC", "ua": "Покращити ПК"},
            "leaderboard": {"en": "Leaderboard", "ua": "Рейтинг"},
            "stats": {"en": "Statistics", "ua": "Статистика"},
            "pc_specs": {"en": "PC Specs", "ua": "Характеристики ПК"},
            "settings": {"en": "Settings", "ua": "Налаштування"},
            "save": {"en": "Save game", "ua": "Зберегти гру"},
            "exit": {"en": "Exit", "ua": "Вийти"},
            
            # Налаштування
            "settings_menu": {"en": "SETTINGS", "ua": "НАЛАШТУВАННЯ"},
            "language": {"en": "Language (English/Ukrainian)", "ua": "Мова (English/Українська)"},
            "difficulty": {"en": "Difficulty (easy/normal/hard)", "ua": "Складність (легка/нормальна/важка)"},
            "sound": {"en": "Sound (on/off)", "ua": "Звук (вкл/викл)"},
            "auto_save": {"en": "Auto-save (on/off)", "ua": "Автозбереження (вкл/викл)"},
        }
        return texts.get(key, {}).get(self.language, key)

settings = Settings()

# ============= КОМПОНЕНТИ ПК (РОЗШИРЕНІ) =============
class PCComponent:
    def __init__(self, name: str, category: str, brands: Dict[int, str], base_price: int):
        self.name = name
        self.category = category
        self.brands = brands  # level -> brand name
        self.level = 1
        self.base_price = base_price
    
    def get_name(self) -> str:
        return self.brands.get(self.level, f"{self.name} Lv.{self.level}")
    
    def get_upgrade_cost(self) -> int:
        return self.base_price * self.level

# ВСІ КОМПОНЕНТИ (20 штук!)
COMPONENTS = {
    # Процесори (15 рівнів)
    "cpu": PCComponent("CPU", "processor", {
        1: "Intel Celeron G5900", 2: "AMD Athlon 3000G", 3: "Intel Pentium Gold", 
        4: "AMD Ryzen 3 3100", 5: "Intel Core i3-10100", 6: "AMD Ryzen 5 3600",
        7: "Intel Core i5-10400", 8: "AMD Ryzen 5 5600X", 9: "Intel Core i7-10700K",
        10: "AMD Ryzen 7 5800X", 11: "Intel Core i9-10900K", 12: "AMD Ryzen 9 5900X",
        13: "Intel Core i9-12900K", 14: "AMD Ryzen 9 7950X", 15: "Intel Core i9-14900KS"
    }, 150),
    
    # Відеокарти
    "gpu": PCComponent("GPU", "graphics", {
        1: "GT 710", 2: "GT 1030", 3: "RX 550", 4: "GTX 1050 Ti", 5: "GTX 1650",
        6: "RX 580", 7: "GTX 1660 Super", 8: "RTX 2060", 9: "RX 5700 XT",
        10: "RTX 3060 Ti", 11: "RX 6800 XT", 12: "RTX 4070 Ti", 13: "RX 7900 XTX",
        14: "RTX 4090", 15: "RTX 5090 Ti"
    }, 200),
    
    # Оперативна пам'ять
    "ram": PCComponent("RAM", "memory", {
        1: "4GB DDR4", 2: "8GB DDR4-2666", 3: "8GB DDR4-3200", 4: "16GB DDR4-3200",
        5: "16GB DDR4-3600", 6: "32GB DDR4-3600", 7: "32GB DDR5-4800", 8: "64GB DDR5-5200",
        9: "64GB DDR5-6000", 10: "128GB DDR5-6400", 11: "128GB DDR5-7200", 12: "256GB DDR5-8000",
        13: "256GB DDR5-8800", 14: "512GB DDR5-9600", 15: "1TB DDR5-10000"
    }, 100),
    
    # Накопичувач
    "storage": PCComponent("Storage", "storage", {
        1: "128GB HDD", 2: "256GB HDD", 3: "256GB SSD", 4: "512GB SSD", 5: "1TB SSD",
        6: "512GB NVMe", 7: "1TB NVMe", 8: "2TB NVMe", 9: "2TB PCIe 4.0", 10: "4TB PCIe 4.0",
        11: "4TB PCIe 5.0", 12: "8TB PCIe 5.0", 13: "8TB PCIe 6.0", 14: "16TB PCIe 7.0", 15: "32TB PCIe 8.0"
    }, 80),
    
    # Материнська плата
    "motherboard": PCComponent("Motherboard", "motherboard", {
        1: "H310M", 2: "B365M", 3: "B460M", 4: "Z490", 5: "B550M", 6: "X570",
        7: "B660M", 8: "Z690", 9: "B760M", 10: "X670E", 11: "Z790", 12: "X670E Extreme",
        13: "Z890", 14: "X990E", 15: "Z1090 Godlike"
    }, 120),
    
    # Охолодження
    "cooler": PCComponent("Cooler", "cooling", {
        1: "Stock Cooler", 2: "Deepcool AK400", 3: "Cooler Master 212", 4: "Noctua NH-U12S",
        5: "be quiet! Dark Rock 4", 6: "Arctic 240mm", 7: "NZXT Kraken X63", 8: "Corsair H100i",
        9: "Noctua NH-D15", 10: "Arctic 360mm", 11: "NZXT Kraken Z73", 12: "Custom Loop",
        13: "Cryo Cooler", 14: "LN2 System", 15: "Quantum Cooling"
    }, 60),
    
    # Блок живлення
    "psu": PCComponent("PSU", "power", {
        1: "300W", 2: "400W Bronze", 3: "450W Bronze", 4: "500W Bronze", 5: "550W Gold",
        6: "650W Gold", 7: "750W Gold", 8: "850W Platinum", 9: "1000W Platinum", 10: "1200W Gold",
        11: "1200W Platinum", 12: "1500W Titanium", 13: "1600W Titanium", 14: "2000W Platinum", 15: "3000W Titanium"
    }, 90),
    
    # Корпус
    "case": PCComponent("Case", "case", {
        1: "Micro-ATX Case", 2: "ATX Case", 3: "Zalman T6", 4: "Deepcool Matrexx", 5: "Corsair 4000D",
        6: "NZXT H510", 7: "Lian Li 215", 8: "Fractal Meshify", 9: "Corsair 5000D", 10: "Lian Li O11",
        11: "Hyte Y60", 12: "Corsair 7000D", 13: "Thermaltake Tower", 14: "InWin 928", 15: "Quantum Chassis"
    }, 70),
    
    # Монітор
    "monitor": PCComponent("Monitor", "display", {
        1: "60Hz 1080p", 2: "75Hz 1080p", 3: "144Hz 1080p", 4: "165Hz 1080p", 5: "240Hz 1080p",
        6: "144Hz 1440p", 7: "165Hz 1440p", 8: "240Hz 1440p", 9: "360Hz 1080p", 10: "165Hz 4K",
        11: "240Hz 4K", 12: "360Hz 1440p", 13: "480Hz 1440p", 14: "540Hz 4K", 15: "1000Hz 8K"
    }, 110),
    
    # Клавіатура
    "keyboard": PCComponent("Keyboard", "peripheral", {
        1: "Membrane KB", 2: "Redragon K552", 3: "Logitech G413", 4: "Corsair K55", 5: "HyperX Alloy",
        6: "Razer BlackWidow", 7: "Logitech G915", 8: "SteelSeries Apex", 9: "Wooting 60HE", 10: "Razer Huntsman",
        11: "Corsair K100", 12: "Optical Pro", 13: "Hall Effect", 14: "NeuroLink", 15: "ThoughtSync"
    }, 50),
    
    # Мишка
    "mouse": PCComponent("Mouse", "peripheral", {
        1: "Office Mouse", 2: "Logitech G203", 3: "Razer DeathAdder", 4: "SteelSeries Rival 3", 5: "Logitech G502",
        6: "Razer Viper Mini", 7: "Glorious Model O", 8: "Logitech G Pro X", 9: "Razer Viper V2", 10: "Finalmouse",
        11: "Logitech G502 X", 12: "Razer Basilisk V3", 13: "Finalmouse TenZ", 14: "Quantum Sensor", 15: "Telepathic"
    }, 40),
    
    # Гарнітура
    "headset": PCComponent("Headset", "audio", {
        1: "Basic Headphones", 2: "HyperX Cloud Stinger", 3: "Logitech G432", 4: "Corsair HS60", 5: "SteelSeries Arctis 5",
        6: "Razer BlackShark", 7: "HyperX Cloud Alpha", 8: "Logitech G Pro X", 9: "SteelSeries Arctis Pro", 10: "Audeze Penrose",
        11: "Sennheiser HD 800", 12: "Quantum Spatial", 13: "Beyerdynamic DT 1990", 14: "Neural Surround", 15: "Brainwave Interface"
    }, 60),
    
    # НОВІ КОМПОНЕНТИ:
    # Звукова карта
    "sound_card": PCComponent("Sound Card", "audio", {
        1: "Realtek onboard", 2: "ASUS Xonar DG", 3: "Creative Sound Blaster", 4: "EVGA Nu Audio", 5: "ASUS Essence STX II",
        6: "Creative AE-5", 7: "EVGA Nu Audio Pro", 8: "ASUS ROG SupremeFX", 9: "Creative AE-9", 10: "Sound Blaster X3",
        11: "GSX 1000", 12: "Mayflower ARC", 13: "Schiit Hel", 14: "Quantum Audio", 15: "Holographic Sound"
    }, 80),
    
    # Мережева карта
    "network_card": PCComponent("Network Card", "network", {
        1: "100Mbps Ethernet", 2: "1Gbps Ethernet", 3: "WiFi 4", 4: "WiFi 5", 5: "2.5Gbps Ethernet",
        6: "WiFi 6", 7: "5Gbps Ethernet", 8: "WiFi 6E", 9: "10Gbps Ethernet", 10: "WiFi 7",
        11: "25Gbps Ethernet", 12: "WiFi 8", 13: "40Gbps Ethernet", 14: "100Gbps Ethernet", 15: "Quantum Link"
    }, 70),
    
    # USB-контролер
    "usb_controller": PCComponent("USB Controller", "connectivity", {
        1: "USB 2.0", 2: "USB 3.0", 3: "USB 3.1", 4: "USB 3.2 Gen1", 5: "USB 3.2 Gen2",
        6: "USB-C 10Gbps", 7: "USB 4.0", 8: "USB-C 20Gbps", 9: "USB-C 40Gbps", 10: "Thunderbolt 3",
        11: "Thunderbolt 4", 12: "USB 5.0", 13: "Thunderbolt 5", 14: "Quantum USB", 15: "Optical Link"
    }, 50),
    
    # RGB-контролер
    "rgb_controller": PCComponent("RGB Controller", "lighting", {
        1: "No RGB", 2: "Basic RGB", 3: "Addressable RGB", 4: "Corsair iCUE", 5: "Razer Chroma",
        6: "ASUS Aura", 7: "MSI Mystic Light", 8: "Gigabyte RGB Fusion", 9: "NZXT CAM", 10: "Thermaltake RGB",
        11: "Full RGB Sync", 12: "Smart RGB", 13: "AI RGB", 14: "Holographic RGB", 15: "Quantum Lighting"
    }, 40),
    
    # Блок розгону
    "overclock_module": PCComponent("OC Module", "performance", {
        1: "No OC", 2: "Auto OC", 3: "Basic OC", 4: "Moderate OC", 5: "Advanced OC",
        6: "Custom OC", 7: "Liquid OC", 8: "Extreme OC", 9: "LN2 OC", 10: "Cryo OC",
        11: "Quantum OC", 12: "AI OC", 13: "Self OC", 14: "Molecular OC", 15: "Subatomic OC"
    }, 100),
    
    # Система моніторингу
    "monitoring": PCComponent("Monitoring", "utility", {
        1: "No display", 2: "Basic LCD", 3: "Temperature display", 4: "Usage monitor", 5: "RGB display",
        6: "OLED panel", 7: "Touch screen", 8: "Stats display", 9: "Smart monitor", 10: "AI monitoring",
        11: "Predictive monitor", 12: "Holographic display", 13: "AR overlay", 14: "VR interface", 15: "Brain interface"
    }, 60)
}

# ============= КОНКУРЕНТИ (20 ШТУК!) =============
COMPETITORS = [
    {"name": "MrBeastUA", "subs": 8000000, "fame": 98, "level": 15, "type": "entertainment"},
    {"name": "GeekGirl", "subs": 2500000, "fame": 85, "level": 14, "type": "tech"},
    {"name": "ProCoder", "subs": 1500000, "fame": 78, "level": 13, "type": "coding"},
    {"name": "GamerOld", "subs": 900000, "fame": 65, "level": 11, "type": "gaming"},
    {"name": "TechReviewer", "subs": 600000, "fame": 58, "level": 10, "type": "reviews"},
    {"name": "FoodieMaster", "subs": 400000, "fame": 48, "level": 9, "type": "food"},
    {"name": "SportLife", "subs": 250000, "fame": 40, "level": 8, "type": "sports"},
    {"name": "ArtWonder", "subs": 150000, "fame": 35, "level": 7, "type": "art"},
    {"name": "MusicMaestro", "subs": 120000, "fame": 32, "level": 7, "type": "music"},
    {"name": "TravelBug", "subs": 90000, "fame": 28, "level": 6, "type": "travel"},
    {"name": "FitnessGuru", "subs": 70000, "fame": 25, "level": 6, "type": "fitness"},
    {"name": "MovieBuff", "subs": 50000, "fame": 22, "level": 5, "type": "movies"},
    {"name": "ScienceLab", "subs": 40000, "fame": 20, "level": 5, "type": "science"},
    {"name": "HistoryBuff", "subs": 30000, "fame": 18, "level": 4, "type": "education"},
    {"name": "CarLover", "subs": 25000, "fame": 16, "level": 4, "type": "automotive"},
    {"name": "MakeupStar", "subs": 20000, "fame": 15, "level": 4, "type": "beauty"},
    {"name": "PetParadise", "subs": 15000, "fame": 13, "level": 3, "type": "animals"},
    {"name": "DanceQueen", "subs": 10000, "fame": 11, "level": 3, "type": "dance"},
    {"name": "ComedyKing", "subs": 8000, "fame": 10, "level": 3, "type": "comedy"},
    {"name": "ASMRWhisper", "subs": 5000, "fame": 8, "level": 2, "type": "asmr"}
]

# ============= НОВІ МЕХАНІКИ =============
class Achievement:
    def __init__(self, name: str, description: str, requirement: str, reward: int):
        self.name = name
        self.description = description
        self.requirement = requirement
        self.reward = reward
        self.unlocked = False

ACHIEVEMENTS = [
    Achievement("First Video", "Upload your first video", "videos>=1", 100),
    Achievement("100 Subs", "Reach 100 subscribers", "subs>=100", 500),
    Achievement("Monetized", "Reach 1000 subscribers", "subs>=1000", 2000),
    Achievement("PC Enthusiast", "Reach PC level 5", "pc_level>=5", 1000),
    Achievement("Tech Guru", "Reach PC level 10", "pc_level>=10", 5000),
    Achievement("Ultimate PC", "Reach PC level 15", "pc_level>=15", 10000),
    Achievement("100 Videos", "Upload 100 videos", "videos>=100", 5000),
    Achievement("500 Videos", "Upload 500 videos", "videos>=500", 20000),
    Achievement("Celebrity", "Reach 100k subscribers", "subs>=100000", 25000),
    Achievement("Superstar", "Reach 1M subscribers", "subs>=1000000", 100000),
]

class DailyQuest:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.quests = [
            {"name": "Make 3 videos", "progress": 0, "target": 3, "reward": 500, "complete": False},
            {"name": "Gain 100 subscribers", "progress": 0, "target": 100, "reward": 1000, "complete": False},
            {"name": "Upgrade PC", "progress": 0, "target": 1, "reward": 800, "complete": False},
        ]
    
    def update(self, action: str, amount: int = 1):
        for quest in self.quests:
            if not quest["complete"]:
                if action == "video" and "Make" in quest["name"]:
                    quest["progress"] += amount
                elif action == "subs" and "Gain" in quest["name"]:
                    quest["progress"] += amount
                elif action == "upgrade" and "Upgrade" in quest["name"]:
                    quest["progress"] += amount
                
                if quest["progress"] >= quest["target"]:
                    quest["complete"] = True
    
    def get_rewards(self) -> int:
        total = 0
        for quest in self.quests:
            if quest["complete"]:
                total += quest["reward"]
        return total

# ============= ОСНОВНИЙ КЛАС ГРИ =============
class YouTuberSimulator:
    def __init__(self, name: str = None):
        self.name = name or "YouTuber"
        self.subscribers = 0
        self.money = 500.0
        self.energy = 100
        self.hunger = 80
        self.thirst = 80
        self.videos_count = 0
        self.fame = 0
        self.play_time = 0
        self.total_earned = 0
        
        # Компоненти ПК
        self.pc = {key: comp for key, comp in COMPONENTS.items()}
        
        # Прогресія
        self.collaboration_chance = 0.05
        self.sponsor_chance = 0.03
        self.collaborations_done = []
        self.sponsors_done = []
        
        # Додаткові механіки
        self.achievements = [Achievement(a.name, a.description, a.requirement, a.reward) for a in ACHIEVEMENTS]
        self.daily_quest = DailyQuest()
        self.current_season = 1
        self.season_progress = 0
        self.streak_days = 0
        self.last_played = datetime.now().strftime("%Y-%m-%d")
        
        # Статистика
        self.stats = self.init_stats()
        self.competitors = [c.copy() for c in COMPETITORS]
        self.games_available = self.calculate_available_games()
        
        # Оновлення шансів
        self.update_progression_rates()
    
    def init_stats(self) -> Dict:
        stats = {}
        categories = ["gaming", "tutorial", "review", "vlog", "challenge", "streaming", 
                     "podcast", "reaction", "unboxing", "tierlist"]
        
        games = ["minecraft", "roblox", "farming", "valorant", "driver", "gta6", 
                "warthunder", "cyberpunk", "quantum", "fortnite", "cod", "amongus"]
        
        for game in games:
            stats[f"gaming_{game}"] = 0
        
        for category in categories:
            if category != "gaming":
                stats[f"{category}"] = 0
        
        return stats
    
    def get_pc_average_level(self) -> float:
        return sum(comp.level for comp in self.pc.values()) / len(self.pc)
    
    def get_video_quality_bonus(self) -> float:
        avg = self.get_pc_average_level()
        return 0.6 + (avg / 15) * 1.4
    
    def get_subscriber_bonus(self) -> float:
        avg = self.get_pc_average_level()
        return 1 + (avg - 1) * 0.15
    
    def update_progression_rates(self):
        """Оновлення шансів колаборацій та спонсорств"""
        self.collaboration_chance = 0.05
        self.sponsor_chance = 0.03
        
        # Бонуси від підписників
        if self.subscribers >= 10000:
            self.collaboration_chance += 0.08
            self.sponsor_chance += 0.05
        if self.subscribers >= 50000:
            self.collaboration_chance += 0.10
            self.sponsor_chance += 0.07
        if self.subscribers >= 100000:
            self.collaboration_chance += 0.12
            self.sponsor_chance += 0.10
        if self.subscribers >= 1000000:
            self.collaboration_chance += 0.20
            self.sponsor_chance += 0.15
        
        # Бонуси від ПК
        pc_avg = self.get_pc_average_level()
        self.collaboration_chance += (pc_avg - 1) * 0.015
        self.sponsor_chance += (pc_avg - 1) * 0.012
        
        # Бонуси від кількості відео
        self.collaboration_chance += min(0.15, self.videos_count / 800)
        self.sponsor_chance += min(0.12, self.videos_count / 1000)
        
        # Обмеження
        self.collaboration_chance = min(0.60, self.collaboration_chance)
        self.sponsor_chance = min(0.50, self.sponsor_chance)
        
        # Складність
        if settings.difficulty == "easy":
            self.collaboration_chance *= 1.2
            self.sponsor_chance *= 1.2
        elif settings.difficulty == "hard":
            self.collaboration_chance *= 0.7
            self.sponsor_chance *= 0.7
    
    def calculate_available_games(self) -> List[str]:
        avg_level = self.get_pc_average_level()
        games = []
        
        all_games = ["minecraft", "roblox", "farming", "valorant", "driver", 
                    "gta6", "warthunder", "fortnite", "cod", "amongus", 
                    "cyberpunk", "quantum"]
        
        thresholds = {
            "minecraft": 1, "roblox": 1, "farming": 2, "valorant": 3,
            "driver": 4, "gta6": 5, "warthunder": 6, "fortnite": 4,
            "cod": 5, "amongus": 2, "cyberpunk": 8, "quantum": 11
        }
        
        for game in all_games:
            if avg_level >= thresholds.get(game, 10):
                games.append(game)
        
        return games
    
    def get_game_display_name(self, game_key: str) -> str:
        names = {
            "minecraft": "🎮 Minecraft", "roblox": "🎮 Roblox", "farming": "🚜 Farming Simulator",
            "valorant": "🔫 Valorant", "driver": "🚗 Driver SF", "gta6": "🏎️ GTA 6",
            "warthunder": "✈️ War Thunder", "fortnite": "🎯 Fortnite", "cod": "🔫 Call of Duty",
            "amongus": "👽 Among Us", "cyberpunk": "🌃 Cyberpunk 2077", "quantum": "⚛️ Quantum Reality"
        }
        return names.get(game_key, game_key)
    
    def check_achievements(self):
        """Перевірка та видача досягнень"""
        rewards = 0
        for ach in self.achievements:
            if not ach.unlocked:
                condition = ach.requirement
                if eval(condition):
                    ach.unlocked = True
                    self.money += ach.reward
                    rewards += ach.reward
                    print(f"\n🏆 ДОСЯГНЕННЯ: {ach.name}!")
                    print(f"   {ach.description} +{ach.reward}$")
        return rewards
    
    def show_status(self):
        pc_avg = self.get_pc_average_level()
        hunger_icon = "🍖" if self.hunger > 70 else "🍗" if self.hunger > 40 else "🍞" if self.hunger > 20 else "⚠️"
        thirst_icon = "💧" if self.thirst > 70 else "🥤" if self.thirst > 40 else "💦" if self.thirst > 20 else "⚠️"
        
        print("\n" + "="*70)
        print(f"👤 {self.name}  |  👥 {self.subscribers:,}  |  💰 {self.money:.0f}$")
        print(f"⚡ {self.energy}%  |  {hunger_icon}{self.hunger}%  |  {thirst_icon}{self.thirst}%  |  🎬 {self.videos_count}")
        print(f"🏆 Слава:{self.fame}  |  💻 ПК:{pc_avg:.1f}  |  🤝 {self.collaboration_chance*100:.0f}%")
        print(f"📅 Сезон:{self.current_season}  |  🔥 Стрік:{self.streak_days}дн  |  📊 Квести:{sum(1 for q in self.daily_quest.quests if q['complete'])}/3")
        print("="*70)
    
    def make_video(self, category: str, sub_category: str = None):
        if self.energy < 15:
            print("\n❌ " + ("Too tired!" if settings.language == "en" else "Занадто втомлений!"))
            return False
        
        if self.hunger < 10 or self.thirst < 10:
            print("\n❌ " + ("Eat/Drink first!" if settings.language == "en" else "Спочатку поїжте/пийте!"))
            return False
        
        # Витрати енергії
        energy_cost = random.randint(10, 20)
        self.energy -= energy_cost
        
        # Оновлення потреб
        self.hunger -= random.randint(3, 8)
        self.thirst -= random.randint(4, 10)
        self.hunger = max(0, self.hunger)
        self.thirst = max(0, self.thirst)
        
        # Штрафи
        penalty = 1.0
        if self.hunger < 20:
            penalty *= 0.7
        elif self.hunger < 40:
            penalty *= 0.9
        if self.thirst < 20:
            penalty *= 0.7
        elif self.thirst < 40:
            penalty *= 0.9
        if self.energy < 20:
            penalty *= 0.6
        
        # Розрахунок переглядів
        base_views = random.randint(2000, 15000)
        multiplier = 1 + (self.videos_count / 200) + (self.fame / 600)
        pc_quality = self.get_video_quality_bonus()
        pc_subs_bonus = self.get_subscriber_bonus()
        
        views = int(base_views * multiplier * pc_quality * penalty * random.uniform(0.8, 1.6))
        
        # Базові підписники
        sub_gain = int(views / 400) + random.randint(0, 15)
        sub_gain = int(sub_gain * pc_subs_bonus)
        
        # Дохід
        income = 0
        if self.subscribers >= 1000:
            income += views * 0.003 * (1 + (self.get_pc_average_level() - 1) * 0.03)
        
        # Бонус категорії
        if category == "challenge":
            views = int(views * 1.5)
            sub_gain = int(sub_gain * 1.3)
        elif category == "streaming":
            income += random.randint(50, 500)
            sub_gain = int(sub_gain * 1.2)
        elif category == "reaction":
            views = int(views * 1.2)
        elif category == "unboxing":
            income += random.randint(30, 300)
        
        # Колаборація
        if random.random() < self.collaboration_chance:
            partner = random.choice(self.competitors)
            collab_subs = int(partner["subs"] * 0.0005) + random.randint(100, 1000)
            collab_money = random.randint(200, 2000)
            sub_gain += collab_subs
            income += collab_money
            self.fame += random.randint(10, 30)
            print(f"\n🤝 КОЛАБОРАЦІЯ з {partner['name']}! +{collab_subs} підс., +{collab_money}$")
        
        # Спонсорство
        if random.random() < self.sponsor_chance and self.subscribers >= 5000:
            sponsors = ["Corsair", "NVIDIA", "AMD", "Red Bull", "Samsung", "Razer", "Logitech"]
            sponsor = random.choice(sponsors)
            sponsor_money = random.randint(500, 5000) * min(5, self.subscribers // 10000 + 1)
            income += sponsor_money
            print(f"\n💼 СПОНСОРСТВО від {sponsor}! +{sponsor_money}$")
        
        # Оновлення
        self.subscribers += sub_gain
        self.money += income
        self.total_earned += income
        self.videos_count += 1
        self.fame += sub_gain // 50
        
        # Статистика
        stat_key = f"{category}_{sub_category}" if sub_category else category
        if stat_key in self.stats:
            self.stats[stat_key] = self.stats.get(stat_key, 0) + 1
        
        # Квести
        self.daily_quest.update("video", 1)
        self.daily_quest.update("subs", sub_gain)
        
        # Досягнення
        self.check_achievements()
        
        # Оновлення шансів
        self.update_progression_rates()
        
        # Виведення результату
        print(f"\n📹 {category.upper()} відео готове!")
        print(f"👁️ Переглядів: {views:,}")
        print(f"➕ Підписників: +{sub_gain}")
        print(f"💵 Зароблено: {income:.2f}$")
        
        # Випадкові події
        if random.random() < 0.1:
            self.special_event()
        
        self.update_competitors()
        return True
    
    def update_competitors(self):
        """Оновлення конкурентів"""
        for comp in self.competitors:
            growth = random.randint(0, max(1, self.videos_count // 60))
            comp["subs"] += growth
            if random.random() < 0.05:
                comp["level"] = min(15, comp.get("level", 1) + 1)
    
    def special_event(self):
        events = [
            ("🔥 Вірусне відео! +1500 підписників!", "subs", 1500),
            ("💸 Мега-спонсор! +5000$!", "money", 5000),
            ("📈 Тренд YouTube! +1000 підписників!", "subs", 1000),
            ("🤝 Коллаб з зіркою! +2000 підс. +2000$!", "both", 2000),
            ("⚡ Збій ПК! -50 енергії!", "energy", -50),
            ("🎁 Топовий донат! +1000$!", "money", 1000),
            ("🏆 Номінація на YouTube Award! +500 слави!", "fame", 500),
            ("🔄 Хейт-хвиля! -500 підписників!", "subs", -500),
        ]
        event, etype, value = random.choice(events)
        print(f"\n✨ {event}")
        
        if etype == "subs":
            self.subscribers = max(0, self.subscribers + value)
        elif etype == "money":
            self.money += value
        elif etype == "both":
            self.subscribers += value
            self.money += 1500
        elif etype == "energy":
            self.energy = max(0, self.energy + value)
        elif etype == "fame":
            self.fame += value
    
    def upgrade_pc(self):
        """Меню прокачки ПК з усіма 20 компонентами"""
        components_list = list(self.pc.items())
        page = 0
        per_page = 8
        
        while True:
            print("\n" + "="*70)
            print("💻 UPGRADE PC - Components (20 total)")
            print("="*70)
            
            start = page * per_page
            end = min(start + per_page, len(components_list))
            
            for i, (key, comp) in enumerate(components_list[start:end], 1):
                if comp.level < 15:
                    cost = comp.get_upgrade_cost()
                    print(f"{i}. {key.upper()}: {comp.get_name()} (Lv.{comp.level}/15) → {cost}$")
                else:
                    print(f"{i}. {key.upper()}: ★ {comp.get_name()} (MAX) ★")
            
            print("\n" + "-"*70)
            print(f"Сторінка {page+1}/{(len(components_list)-1)//per_page + 1}")
            print("0. Назад | N. Наступна | P. Попередня")
            
            choice = input("\nВиберіть компонент: ").strip().lower()
            
            if choice == "0":
                break
            elif choice == "n" and end < len(components_list):
                page += 1
            elif choice == "p" and page > 0:
                page -= 1
            elif choice.isdigit() and 1 <= int(choice) <= len(components_list[start:end]):
                idx = start + int(choice) - 1
                comp_key, comp = components_list[idx]
                if comp.level >= 15:
                    print("❌ Максимальний рівень!")
                    continue
                
                cost = comp.get_upgrade_cost()
                if self.money >= cost:
                    self.money -= cost
                    comp.level += 1
                    print(f"✅ {comp_key.upper()} оновлено до {comp.get_name()} (Lv.{comp.level}/15)!")
                    
                    # Перевірка нових ігор
                    new_games = self.calculate_available_games()
                    if set(new_games) - set(self.games_available):
                        print("🎉 ВІДКРИТО НОВІ ІГРИ!")
                        self.games_available = new_games
                    
                    self.daily_quest.update("upgrade")
                    self.update_progression_rates()
                else:
                    print(f"❌ Потрібно {cost}$, у вас {self.money:.2f}$")
    
    def show_leaderboard(self):
        print("\n" + "="*70)
        print("🏆 E-TUBE LEADERBOARD 🏆")
        print("="*70)
        
        all_creators = [{"name": self.name, "subs": self.subscribers, "fame": self.fame, 
                        "level": self.get_pc_average_level(), "is_player": True}]
        
        for comp in self.competitors[:30]:
            all_creators.append({"name": comp["name"], "subs": comp["subs"], "fame": comp["fame"],
                                "level": comp.get("level", 5), "is_player": False})
        
        all_creators.sort(key=lambda x: x["subs"], reverse=True)
        
        for i, creator in enumerate(all_creators[:20], 1):
            medal = "🥇 " if i == 1 else "🥈 " if i == 2 else "🥉 " if i == 3 else f"{i}. "
            player_mark = " 👈 YOU" if creator["is_player"] else ""
            print(f"{medal}{creator['name']}: {creator['subs']:,} subs (PC Lv.{creator['level']:.1f}){player_mark}")
        print("="*70)
    
    def show_achievements(self):
        print("\n" + "="*70)
        print("🏆 ACHIEVEMENTS 🏆")
        print("="*70)
        
        for ach in self.achievements:
            status = "✅" if ach.unlocked else "❌"
            print(f"{status} {ach.name}: {ach.description} (+{ach.reward}$)")
        print("="*70)
    
    def show_daily_quests(self):
        print("\n" + "="*70)
        print("📅 DAILY QUESTS")
        print("="*70)
        
        total_reward = 0
        for quest in self.daily_quest.quests:
            status = "✅" if quest["complete"] else f"{quest['progress']}/{quest['target']}"
            reward_status = "✓" if quest["complete"] else f"+{quest['reward']}$"
            print(f"{quest['name']}: {status} {reward_status}")
            if quest["complete"]:
                total_reward += quest["reward"]
        
        print(f"\n💰 Total available: {total_reward}$")
        
        if total_reward > 0 and input("\nClaim rewards? (y/n): ").lower() == 'y':
            self.money += total_reward
            print(f"✅ +{total_reward}$ claimed!")
            self.daily_quest.reset()
        print("="*70)
    
    def select_video_topic(self) -> Tuple[Optional[str], Optional[str]]:
        print("\n📹 SELECT VIDEO TYPE:")
        print("1. Gaming 🎮")
        print("2. Tutorials 📚")
        print("3. Reviews 🔍")
        print("4. Vlogs 📹")
        print("5. Challenges 🎯")
        print("6. Streaming 📡")
        print("7. Reactions 😲")
        print("8. Unboxing 📦")
        print("9. Podcasts 🎙️")
        print("10. Tier Lists 📊")
        print("0. Back")
        
        choice = input("\nYour choice: ").strip()
        
        if choice == "1":
            available = self.calculate_available_games()
            if not available:
                print("❌ PC too weak! Upgrade your components.")
                return None, None
            
            print("\n🎮 Available games:")
            for i, game in enumerate(available[:15], 1):
                print(f"{i}. {self.get_game_display_name(game)}")
            
            game_choice = input("Choose game: ").strip()
            if game_choice.isdigit() and 1 <= int(game_choice) <= len(available):
                return "gaming", available[int(game_choice)-1]
        
        elif choice == "2":
            print("\n📚 Tutorials:")
            print("1. Cooking 🍳")
            print("2. Tech 💻")
            print("3. Sports 🏋️")
            print("4. Art 🎨")
            print("5. Music 🎵")
            sub = input("Choose: ").strip()
            subs = {"1":"cooking", "2":"tech", "3":"sport", "4":"art", "5":"music"}
            if sub in subs:
                return "tutorial", subs[sub]
        
        elif choice == "3":
            print("\n🔍 Reviews:")
            print("1. Games 🎮")
            print("2. Food 🍕")
            print("3. YouTubers 📺")
            print("4. Tech 💻")
            print("5. Movies 🎬")
            sub = input("Choose: ").strip()
            subs = {"1":"games", "2":"food", "3":"youtubers", "4":"tech", "5":"movies"}
            if sub in subs:
                return "review", subs[sub]
        
        elif choice == "4":
            return "vlog", None
        elif choice == "5":
            return "challenge", None
        elif choice == "6":
            return "streaming", None
        elif choice == "7":
            return "reaction", None
        elif choice == "8":
            return "unboxing", None
        elif choice == "9":
            return "podcast", None
        elif choice == "10":
            return "tierlist", None
        elif choice == "0":
            return None, None
        
        print("❌ Invalid choice!")
        return None, None
    
    def settings_menu(self):
        while True:
            print("\n" + "="*70)
            print(settings.get_text("settings_menu"))
            print("="*70)
            print(f"1. {settings.get_text('language')} [{settings.language}]")
            print(f"2. {settings.get_text('difficulty')} [{settings.difficulty}]")
            print(f"3. {settings.get_text('sound')} [{'ON' if settings.sound else 'OFF'}]")
            print(f"4. {settings.get_text('auto_save')} [{'ON' if settings.auto_save else 'OFF'}]")
            print("0. Back")
            
            choice = input("\nChoice: ").strip()
            
            if choice == "1":
                new_lang = input("Enter language (en/ua): ").strip().lower()
                if new_lang in ["en", "ua"]:
                    settings.language = new_lang
                    settings.save_settings()
                    print(f"✅ Language changed to {new_lang}")
            
            elif choice == "2":
                new_diff = input("Enter difficulty (easy/normal/hard): ").strip().lower()
                if new_diff in ["easy", "normal", "hard"]:
                    settings.difficulty = new_diff
                    settings.save_settings()
                    self.update_progression_rates()
                    print(f"✅ Difficulty changed to {new_diff}")
            
            elif choice == "3":
                settings.sound = not settings.sound
                settings.save_settings()
                print(f"✅ Sound {'ON' if settings.sound else 'OFF'}")
            
            elif choice == "4":
                settings.auto_save = not settings.auto_save
                settings.save_settings()
                print(f"✅ Auto-save {'ON' if settings.auto_save else 'OFF'}")
            
            elif choice == "0":
                break
    
    def eat_drink(self):
        print("\n🍽️ EAT/DRINK:")
        print("1. Eat (restores hunger 40-60) - 25$")
        print("2. Drink (restores thirst 50-70) - 20$")
        print("3. Full meal (restores both) - 40$")
        print("4. Energy drink (+30 energy) - 50$")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1" and self.money >= 25:
            gain = random.randint(40, 60)
            self.hunger = min(100, self.hunger + gain)
            self.money -= 25
            print(f"🍕 +{gain}% hunger")
        elif choice == "2" and self.money >= 20:
            gain = random.randint(50, 70)
            self.thirst = min(100, self.thirst + gain)
            self.money -= 20
            print(f"🥤 +{gain}% thirst")
        elif choice == "3" and self.money >= 40:
            h_gain = random.randint(40, 60)
            t_gain = random.randint(50, 70)
            self.hunger = min(100, self.hunger + h_gain)
            self.thirst = min(100, self.thirst + t_gain)
            self.money -= 40
            print(f"🍽️ +{h_gain}% hunger, +{t_gain}% thirst")
        elif choice == "4" and self.money >= 50:
            gain = random.randint(25, 35)
            self.energy = min(100, self.energy + gain)
            self.money -= 50
            print(f"⚡ +{gain}% energy")
        elif choice in ["1","2","3","4"]:
            print("❌ Not enough money!")
    
    def rest(self):
        gain = random.randint(20, 45)
        self.energy = min(100, self.energy + gain)
        print(f"\n😴 Restored +{gain}% energy")
    
    def save_game(self):
        save_data = {
            "name": self.name, "subscribers": self.subscribers, "money": self.money,
            "energy": self.energy, "hunger": self.hunger, "thirst": self.thirst,
            "videos_count": self.videos_count, "fame": self.fame, "total_earned": self.total_earned,
            "pc_levels": {key: comp.level for key, comp in self.pc.items()},
            "stats": self.stats, "competitors": self.competitors,
            "current_season": self.current_season, "streak_days": self.streak_days,
            "save_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(YouTuberSimulator.SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=4, ensure_ascii=False)
        print(f"\n💾 Game saved! ({YouTuberSimulator.SAVE_FILE})")
    
    def load_game(self):
        if not os.path.exists(YouTuberSimulator.SAVE_FILE):
            return False
        try:
            with open(YouTuberSimulator.SAVE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.name = data["name"]
            self.subscribers = data["subscribers"]
            self.money = data["money"]
            self.energy = data["energy"]
            self.hunger = data["hunger"]
            self.thirst = data["thirst"]
            self.videos_count = data["videos_count"]
            self.fame = data["fame"]
            self.total_earned = data["total_earned"]
            
            for key, level in data.get("pc_levels", {}).items():
                if key in self.pc:
                    self.pc[key].level = level
            
            self.stats = data.get("stats", self.stats)
            self.competitors = data.get("competitors", self.competitors)
            self.current_season = data.get("current_season", 1)
            self.streak_days = data.get("streak_days", 0)
            
            self.games_available = self.calculate_available_games()
            self.update_progression_rates()
            
            print(f"\n✅ Loaded! (Save from {data['save_date']})")
            return True
        except Exception as e:
            print(f"❌ Load error: {e}")
            return False
    
    def play(self):
        print("\n" + "="*70)
        print("🎬 YOUTUBER SIMULATOR v4.0 - MEGA UPDATE 🎬")
        print("="*70)
        print("NEW FEATURES:")
        print("• 20 PC components (CPU, GPU, RAM, Sound Card, RGB, OC module...)")
        print("• 20 competitors on leaderboard")
        print("• Achievements system with rewards")
        print("• Daily quests for extra money")
        print("• New content: Reactions, Unboxing, Podcasts, Tier Lists")
        print("• New games: Fortnite, Call of Duty, Among Us")
        print("• Settings menu (language, difficulty, auto-save)")
        print("• Improved progression system")
        print("="*70)
        
        while True:
            self.show_status()
            print("\n🎮 MAIN MENU:")
            print("1. Make video")
            print("2. Rest")
            print("3. Eat/Drink")
            print("4. Upgrade PC")
            print("5. Leaderboard")
            print("6. Achievements 🏆")
            print("7. Daily Quests 📅")
            print("8. PC Specs")
            print("9. Settings ⚙️")
            print("10. Save")
            print("11. Exit")
            
            choice = input("\nChoice: ").strip()
            
            if choice == "1":
                cat, sub = self.select_video_topic()
                if cat:
                    self.make_video(cat, sub)
            elif choice == "2":
                self.rest()
            elif choice == "3":
                self.eat_drink()
            elif choice == "4":
                self.upgrade_pc()
            elif choice == "5":
                self.show_leaderboard()
            elif choice == "6":
                self.show_achievements()
            elif choice == "7":
                self.show_daily_quests()
            elif choice == "8":
                self.show_full_pc()
            elif choice == "9":
                self.settings_menu()
            elif choice == "10":
                self.save_game()
            elif choice == "11":
                print(f"\n🏆 Final stats: {self.subscribers:,} subs, {self.total_earned:.2f}$ earned")
                if settings.auto_save or input("Save before exit? (y/n): ").lower() == 'y':
                    self.save_game()
                break
            else:
                print("❌ Invalid choice!")
            
            time.sleep(0.5)
    
    def show_full_pc(self):
        print("\n" + "="*70)
        print("💻 FULL PC SPECIFICATIONS")
        print("="*70)
        
        for key, comp in self.pc.items():
            bar = "█" * (comp.level // 1) + "░" * (15 - comp.level // 1)
            print(f"{key.upper():15}: {comp.get_name():25} [{bar}] Lv.{comp.level}/15")
        
        avg = self.get_pc_average_level()
        print("\n" + "="*70)
        print(f"📊 Average Level: {avg:.2f}/15")
        print(f"🎮 Video Quality: +{(avg-1)*9.3:.0f}%")
        print(f"📈 Subscriber Bonus: +{(avg-1)*15:.0f}%")
        print(f"🎮 Available Games: {', '.join(self.calculate_available_games()[:8])}")
        print("="*70)

# ============= ЗАПУСК =============
SAVE_FILE = "youtuber_save.json"
YouTuberSimulator.SAVE_FILE = SAVE_FILE

def main():
    print("="*70)
    print("🎬 YOUTUBER SIMULATOR v4.0 🎬")
    print("="*70)
    
    game = None
    
    if os.path.exists(SAVE_FILE):
        load = input("Save found! Load it? (yes/no): ").strip().lower()
        if load in ["yes", "y", "так"]:
            game = YouTuberSimulator()
            if game.load_game():
                game.play()
                return
    
    name = input("What's your name? ").strip()
    if not name:
        name = "YouTuber"
    
    game = YouTuberSimulator(name)
    game.play()

if __name__ == "__main__":
    main()