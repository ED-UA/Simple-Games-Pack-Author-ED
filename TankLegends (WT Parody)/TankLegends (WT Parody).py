import random
import time
import json
import os
import shutil
from datetime import datetime

class TankCommanderLegends:
    def __init__(self):
        self.version = "1.0.0"
        self.game_name = "TANK COMMANDER: LEGENDS"
        
        # ========== СИСТЕМА МОВ ==========
        self.languages = {
            'en': {
                'name': 'English',
                'welcome': 'WELCOME TO THE GAME',
                'main_menu': 'MAIN MENU',
                'battle': 'BATTLE',
                'stats': 'STATISTICS',
                'exit': 'EXIT',
                'credits': 'CREDITS',
                'gems': 'GEMS',
                'wins': 'WINS',
                'losses': 'LOSSES',
                'level': 'LEVEL',
                'exp': 'EXPERIENCE',
                'settings': 'SETTINGS',
                'language': 'LANGUAGE',
                'sound': 'SOUND',
                'auto_save': 'AUTO SAVE',
                'battle_animations': 'BATTLE ANIMATIONS',
                'back': 'BACK',
                'on': 'ON',
                'off': 'OFF',
                'select_language': 'SELECT LANGUAGE',
                'yes': 'YES',
                'no': 'NO',
                'victory': 'VICTORY',
                'defeat': 'DEFEAT',
                'battle_start': 'BATTLE START',
                'your_vehicle': 'Your vehicle',
                'enemy': 'Enemy',
                'power': 'Power',
                'win_chance': 'Win chance',
                'credits_earned': 'Credits earned',
                'xp_earned': 'XP earned',
                'battle_pass': 'BATTLE PASS',
                'season': 'Season',
                'level_up': 'LEVEL UP',
                'research': 'RESEARCH',
                'purchase': 'PURCHASE',
                'modifications': 'MODIFICATIONS',
                'tech_tree': 'TECH TREE',
                'ships': 'SHIPS',
                'legendary': 'LEGENDARY'
            },
            'uk': {
                'name': 'Українська',
                'welcome': 'ЛАСКАВО ПРОСИМО ДО ГРИ',
                'main_menu': 'ГОЛОВНЕ МЕНЮ',
                'battle': 'БІЙ',
                'stats': 'СТАТИСТИКА',
                'exit': 'ВИХІД',
                'credits': 'КРЕДИТИ',
                'gems': 'САМОЦВІТИ',
                'wins': 'ПЕРЕМОГИ',
                'losses': 'ПОРАЗКИ',
                'level': 'РІВЕНЬ',
                'exp': 'ДОСВІД',
                'settings': 'НАЛАШТУВАННЯ',
                'language': 'МОВА',
                'sound': 'ЗВУК',
                'auto_save': 'АВТОЗБЕРЕЖЕННЯ',
                'battle_animations': 'АНІМАЦІЇ БОЮ',
                'back': 'НАЗАД',
                'on': 'УВІМК.',
                'off': 'ВИМК.',
                'select_language': 'ВИБЕРІТЬ МОВУ',
                'yes': 'ТАК',
                'no': 'НІ',
                'victory': 'ПЕРЕМОГА',
                'defeat': 'ПОРАЗКА',
                'battle_start': 'БІЙ РОЗПОЧИНАЄТЬСЯ',
                'your_vehicle': 'Ваша техніка',
                'enemy': 'Противник',
                'power': 'Сила',
                'win_chance': 'Шанс на перемогу',
                'credits_earned': 'Отримано кредитів',
                'xp_earned': 'Отримано досвіду',
                'battle_pass': 'БОЙОВИЙ ПРОПУСК',
                'season': 'Сезон',
                'level_up': 'ПІДВИЩЕННЯ РІВНЯ',
                'research': 'ДОСЛІДЖЕННЯ',
                'purchase': 'ПОКУПКА',
                'modifications': 'МОДИФІКАЦІЇ',
                'tech_tree': 'ДЕРЕВО ТЕХНІКИ',
                'ships': 'КОРАБЛІ',
                'legendary': 'ЛЕГЕНДАРНІ'
            }
        }
        
        self.current_lang = 'en'
        self.text = self.languages[self.current_lang]
        
        # Налаштування
        self.settings = {
            'language': 'en',
            'sound': True,
            'auto_save': True,
            'battle_animations': True
        }
        
        # ========== БОЙОВИЙ ПРОПУСК ==========
        self.battle_pass = {
            'season': 1,
            'season_name': 'Iron Storm',
            'current_level': 1,
            'current_xp': 0,
            'xp_needed': 100,
            'max_level': 50,
            'rewards': {}
        }
        
        # Генерація нагород
        for level in range(1, 51):
            self.battle_pass['rewards'][level] = {
                'free': {
                    'credits': 500 + (level * 50),
                    'gems': 5 if level % 5 == 0 else 0,
                    'exp': 100 + (level * 10)
                },
                'premium': {
                    'credits': 1000 + (level * 100),
                    'gems': 25 if level % 3 == 0 else 10,
                    'exp': 200 + (level * 20),
                    'vehicle': self.get_battlepass_vehicle(level) if level % 10 == 0 else None
                }
            }
        
        self.player = {
            'name': 'Commander',
            'level': 1,
            'total_exp': 0,
            'wins': 0,
            'losses': 0,
            'credits': 5000,
            'gems': 200,
            'premium_bp': False,
            'current_vehicle': None,
            'current_nation': None,
            'current_type': 'tank'
        }
        
        self.nation_exp = {
            'USSR': 0,
            'Germany': 0,
            'Ukraine': 0,
            'China': 0,
            'USA': 0,
            'UK': 0,
            'France': 0,
            'Japan': 0
        }
        
        # Ініціалізація дерев техніки
        self.tech_tree = self.initialize_tech_tree()
        self.legendary_vehicles = self.initialize_legendary_vehicles()
        
        # Додаємо легендарні машини
        for nation, vehicles in self.legendary_vehicles.items():
            if nation in self.tech_tree:
                self.tech_tree[nation].update(vehicles)
        
        self.ships_tree = self.initialize_ships_tree()
        self.modifications = self.initialize_modifications()
        
        self.owned_vehicles = []
        self.owned_ships = []
        self.research_queue = {}
        self.ship_research_queue = {}
        self.vehicle_mods = {}
        
        # Завантаження
        self.load_settings()
        self.update_language()
        self.migrate_save_file()
        self.load_game()
    
    def update_language(self):
        """Оновити мову"""
        self.text = self.languages.get(self.current_lang, self.languages['en'])
    
    def get_text(self, key):
        """Отримати текст за ключем"""
        return self.text.get(key, key)
    
    def get_battlepass_vehicle(self, level):
        """Отримати техніку за рівень бойового пропуску"""
        vehicles = {
            10: 'M4 Sherman (Elite)',
            20: 'Tiger I (Elite)',
            30: 'T-34-85 (Elite)',
            40: 'Panther (Elite)',
            50: 'Legendary Conqueror'
        }
        return vehicles.get(level)
    
    def initialize_tech_tree(self):
        """Ініціалізація дерева техніки"""
        return {
            'USSR': self.get_ussr_vehicles(),
            'Germany': self.get_germany_vehicles(),
            'Ukraine': self.get_ukraine_vehicles(),
            'China': self.get_china_vehicles(),
            'USA': self.get_usa_vehicles(),
            'UK': self.get_uk_vehicles(),
            'France': self.get_france_vehicles(),
            'Japan': self.get_japan_vehicles()
        }
    
    def initialize_legendary_vehicles(self):
        """Легендарні машини"""
        return {
            'USSR': {
                'IS-9 (Legendary)': {
                    'tier': 8, 'cost': 20000, 'exp_needed': 5000, 'power': 200,
                    'era': 'Legendary', 'year': 1955, 'type': 'tank',
                    'description': 'Legendary heavy tank, the pinnacle of IS series',
                    'legendary': True
                }
            },
            'Germany': {
                'Leopard 2A7V (Legendary)': {
                    'tier': 8, 'cost': 21000, 'exp_needed': 5200, 'power': 205,
                    'era': 'Legendary', 'year': 2015, 'type': 'tank',
                    'description': 'Latest version of the legendary Leopard',
                    'legendary': True
                }
            },
            'Ukraine': {
                'Bulat-M1 (Legendary)': {
                    'tier': 8, 'cost': 19000, 'exp_needed': 4800, 'power': 195,
                    'era': 'Legendary', 'year': 2025, 'type': 'tank',
                    'description': 'Improved version with next-gen protection',
                    'legendary': True
                }
            },
            'China': {
                'ZTZ-99A3 (Legendary)': {
                    'tier': 8, 'cost': 20500, 'exp_needed': 5100, 'power': 202,
                    'era': 'Legendary', 'year': 2020, 'type': 'tank',
                    'description': 'Elite version of main battle tank',
                    'legendary': True
                }
            },
            'USA': {
                'M1A2 Abrams SEPv4 (Legendary)': {
                    'tier': 8, 'cost': 22000, 'exp_needed': 5500, 'power': 210,
                    'era': 'Legendary', 'year': 2023, 'type': 'tank',
                    'description': 'Latest modification of legendary Abrams',
                    'legendary': True
                }
            },
            'UK': {
                'Challenger 3 (Legendary)': {
                    'tier': 8, 'cost': 19500, 'exp_needed': 4900, 'power': 198,
                    'era': 'Legendary', 'year': 2024, 'type': 'tank',
                    'description': 'Next-gen British main battle tank',
                    'legendary': True
                }
            },
            'France': {
                'Leclerc XLR (Legendary)': {
                    'tier': 8, 'cost': 18500, 'exp_needed': 4700, 'power': 192,
                    'era': 'Legendary', 'year': 2022, 'type': 'tank',
                    'description': 'Modernized version of Leclerc',
                    'legendary': True
                }
            },
            'Japan': {
                'Type 10 (Legendary)': {
                    'tier': 8, 'cost': 18800, 'exp_needed': 4750, 'power': 194,
                    'era': 'Legendary', 'year': 2012, 'type': 'tank',
                    'description': 'Japanese main battle tank',
                    'legendary': True
                }
            }
        }
    
    def get_ussr_vehicles(self):
        return {
            'MS-1': {'tier': 1, 'cost': 0, 'exp_needed': 0, 'power': 25, 'era': 'Early', 'year': 1927, 'type': 'tank'},
            'T-26': {'tier': 1, 'cost': 600, 'exp_needed': 150, 'power': 38, 'era': 'Early', 'year': 1931, 'type': 'tank'},
            'BT-5': {'tier': 2, 'cost': 900, 'exp_needed': 300, 'power': 48, 'era': 'Early', 'year': 1933, 'type': 'tank'},
            'T-34 (1940)': {'tier': 3, 'cost': 1500, 'exp_needed': 600, 'power': 70, 'era': 'WWII', 'year': 1940, 'type': 'tank'},
            'KV-1': {'tier': 3, 'cost': 1800, 'exp_needed': 700, 'power': 78, 'era': 'WWII', 'year': 1939, 'type': 'tank'},
            'T-34-85': {'tier': 4, 'cost': 2400, 'exp_needed': 900, 'power': 90, 'era': 'WWII', 'year': 1944, 'type': 'tank'},
            'IS-2': {'tier': 4, 'cost': 2800, 'exp_needed': 1000, 'power': 95, 'era': 'WWII', 'year': 1943, 'type': 'tank'},
            'T-54': {'tier': 5, 'cost': 4500, 'exp_needed': 1500, 'power': 118, 'era': 'Cold War', 'year': 1947, 'type': 'tank'},
            'T-72': {'tier': 6, 'cost': 7000, 'exp_needed': 2400, 'power': 145, 'era': 'Modern', 'year': 1973, 'type': 'tank'},
            'T-90': {'tier': 7, 'cost': 9500, 'exp_needed': 3200, 'power': 170, 'era': 'Modern', 'year': 1992, 'type': 'tank'},
        }
    
    def get_germany_vehicles(self):
        return {
            'A7V': {'tier': 1, 'cost': 0, 'exp_needed': 0, 'power': 28, 'era': 'WWI', 'year': 1918, 'type': 'tank'},
            'Pz.II': {'tier': 1, 'cost': 1000, 'exp_needed': 320, 'power': 50, 'era': 'WWII', 'year': 1935, 'type': 'tank'},
            'Pz.IV': {'tier': 2, 'cost': 1600, 'exp_needed': 550, 'power': 68, 'era': 'WWII', 'year': 1939, 'type': 'tank'},
            'Tiger I': {'tier': 3, 'cost': 2000, 'exp_needed': 750, 'power': 82, 'era': 'WWII', 'year': 1942, 'type': 'tank'},
            'Panther': {'tier': 3, 'cost': 2300, 'exp_needed': 800, 'power': 88, 'era': 'WWII', 'year': 1943, 'type': 'tank'},
            'Tiger II': {'tier': 4, 'cost': 3000, 'exp_needed': 1050, 'power': 100, 'era': 'WWII', 'year': 1944, 'type': 'tank'},
            'Leopard 1': {'tier': 6, 'cost': 7500, 'exp_needed': 2300, 'power': 145, 'era': 'Cold War', 'year': 1965, 'type': 'tank'},
            'Leopard 2A4': {'tier': 6, 'cost': 9000, 'exp_needed': 2800, 'power': 160, 'era': 'Modern', 'year': 1985, 'type': 'tank'},
        }
    
    def get_usa_vehicles(self):
        return {
            'M2 Light': {'tier': 1, 'cost': 0, 'exp_needed': 0, 'power': 32, 'era': 'WWII', 'year': 1935, 'type': 'tank'},
            'M3 Stuart': {'tier': 1, 'cost': 600, 'exp_needed': 180, 'power': 45, 'era': 'WWII', 'year': 1941, 'type': 'tank'},
            'M4 Sherman': {'tier': 2, 'cost': 1500, 'exp_needed': 500, 'power': 72, 'era': 'WWII', 'year': 1942, 'type': 'tank'},
            'M26 Pershing': {'tier': 3, 'cost': 2500, 'exp_needed': 850, 'power': 85, 'era': 'WWII', 'year': 1945, 'type': 'tank'},
            'M60': {'tier': 5, 'cost': 5000, 'exp_needed': 1700, 'power': 120, 'era': 'Cold War', 'year': 1960, 'type': 'tank'},
            'M1 Abrams': {'tier': 6, 'cost': 8000, 'exp_needed': 2800, 'power': 155, 'era': 'Modern', 'year': 1980, 'type': 'tank'},
        }
    
    def get_uk_vehicles(self):
        return {
            'Vickers Mk.VI': {'tier': 1, 'cost': 0, 'exp_needed': 0, 'power': 30, 'era': 'WWII', 'year': 1936, 'type': 'tank'},
            'Matilda II': {'tier': 2, 'cost': 1200, 'exp_needed': 400, 'power': 55, 'era': 'WWII', 'year': 1939, 'type': 'tank'},
            'Cromwell': {'tier': 3, 'cost': 2000, 'exp_needed': 700, 'power': 75, 'era': 'WWII', 'year': 1944, 'type': 'tank'},
            'Centurion Mk.3': {'tier': 4, 'cost': 3500, 'exp_needed': 1200, 'power': 95, 'era': 'Cold War', 'year': 1948, 'type': 'tank'},
            'Challenger 1': {'tier': 6, 'cost': 8500, 'exp_needed': 2800, 'power': 150, 'era': 'Modern', 'year': 1983, 'type': 'tank'},
        }
    
    def get_france_vehicles(self):
        return {
            'Renault FT': {'tier': 1, 'cost': 0, 'exp_needed': 0, 'power': 25, 'era': 'WWI', 'year': 1917, 'type': 'tank'},
            'SOMUA S35': {'tier': 2, 'cost': 1500, 'exp_needed': 500, 'power': 58, 'era': 'WWII', 'year': 1936, 'type': 'tank'},
            'AMX-13': {'tier': 3, 'cost': 2800, 'exp_needed': 900, 'power': 85, 'era': 'Cold War', 'year': 1952, 'type': 'tank'},
            'Leclerc': {'tier': 6, 'cost': 9000, 'exp_needed': 3000, 'power': 160, 'era': 'Modern', 'year': 1992, 'type': 'tank'},
        }
    
    def get_japan_vehicles(self):
        return {
            'Type 89': {'tier': 1, 'cost': 0, 'exp_needed': 0, 'power': 28, 'era': 'WWII', 'year': 1929, 'type': 'tank'},
            'Type 97 Chi-Ha': {'tier': 1, 'cost': 800, 'exp_needed': 250, 'power': 42, 'era': 'WWII', 'year': 1938, 'type': 'tank'},
            'Type 61': {'tier': 3, 'cost': 3000, 'exp_needed': 1000, 'power': 85, 'era': 'Cold War', 'year': 1961, 'type': 'tank'},
            'Type 90': {'tier': 5, 'cost': 7000, 'exp_needed': 2400, 'power': 140, 'era': 'Modern', 'year': 1990, 'type': 'tank'},
        }
    
    def get_ukraine_vehicles(self):
        return {
            'Sich Rifleman': {'tier': 1, 'cost': 0, 'exp_needed': 0, 'power': 27, 'era': 'Early', 'year': 1918, 'type': 'tank'},
            'T-34-76 (Kharkiv)': {'tier': 3, 'cost': 1700, 'exp_needed': 620, 'power': 72, 'era': 'WWII', 'year': 1941, 'type': 'tank'},
            'T-34-85 (Kyiv)': {'tier': 4, 'cost': 2400, 'exp_needed': 900, 'power': 91, 'era': 'WWII', 'year': 1944, 'type': 'tank'},
            'T-64BV (Ukraine)': {'tier': 5, 'cost': 4200, 'exp_needed': 1450, 'power': 118, 'era': 'Modern', 'year': 1985, 'type': 'tank'},
            'Oplot-M': {'tier': 6, 'cost': 7000, 'exp_needed': 2300, 'power': 145, 'era': 'Modern', 'year': 2009, 'type': 'tank'},
        }
    
    def get_china_vehicles(self):
        return {
            'Type 89': {'tier': 1, 'cost': 0, 'exp_needed': 0, 'power': 26, 'era': 'WWII', 'year': 1929, 'type': 'tank'},
            'Type 59': {'tier': 3, 'cost': 1700, 'exp_needed': 650, 'power': 74, 'era': 'Cold War', 'year': 1959, 'type': 'tank'},
            'Type 69': {'tier': 3, 'cost': 2200, 'exp_needed': 820, 'power': 84, 'era': 'Cold War', 'year': 1974, 'type': 'tank'},
            'Type 96': {'tier': 4, 'cost': 3000, 'exp_needed': 1100, 'power': 100, 'era': 'Modern', 'year': 1997, 'type': 'tank'},
            'Type 99': {'tier': 4, 'cost': 4200, 'exp_needed': 1550, 'power': 122, 'era': 'Modern', 'year': 2001, 'type': 'tank'},
        }
    
    def initialize_ships_tree(self):
        return {
            'USA': {
                'USS Fletcher': {'tier': 3, 'cost': 5000, 'exp_needed': 1500, 'power': 110, 'era': 'WWII', 'year': 1942, 'type': 'ship'},
                'USS Iowa': {'tier': 5, 'cost': 12000, 'exp_needed': 3500, 'power': 180, 'era': 'WWII', 'year': 1943, 'type': 'ship'},
            },
            'China': {
                'Type 051': {'tier': 3, 'cost': 4800, 'exp_needed': 1400, 'power': 105, 'era': 'Modern', 'year': 1971, 'type': 'ship'},
                'Type 052D': {'tier': 5, 'cost': 14000, 'exp_needed': 3800, 'power': 185, 'era': 'Modern', 'year': 2014, 'type': 'ship'},
            },
        }
    
    def initialize_modifications(self):
        return {
            'Improved Gun': {'cost': 500, 'power_bonus': 15, 'description': '+15 attack power'},
            'Improved Armor': {'cost': 600, 'defense_bonus': 12, 'description': 'Reduces incoming damage'},
            'High Speed Engine': {'cost': 400, 'speed_bonus': 8, 'description': '+8 initiative'},
            'Explosive Reactive Armor': {'cost': 800, 'defense_bonus': 20, 'description': '+20 defense'},
            'Titan Armor (Legendary)': {'cost': 2000, 'power_bonus': 35, 'description': '+35 power, legendary only', 'legendary_only': True},
        }
    
    def load_settings(self):
        """Завантаження налаштувань"""
        if os.path.exists('tcl_settings.json'):
            try:
                with open('tcl_settings.json', 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
                    self.current_lang = self.settings.get('language', 'en')
                print("⚙️ Settings loaded!")
            except:
                pass
    
    def save_settings(self):
        """Збереження налаштувань"""
        with open('tcl_settings.json', 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)
        print("⚙️ Settings saved!")
    
    def show_settings(self):
        """Показати налаштування"""
        print("\n" + "=" * 50)
        print(f"⚙️ {self.get_text('settings')}")
        print("=" * 50)
        print(f"1. {self.get_text('language')}: {self.languages[self.current_lang]['name']}")
        print(f"2. {self.get_text('sound')}: {self.get_text('on') if self.settings['sound'] else self.get_text('off')}")
        print(f"3. {self.get_text('auto_save')}: {self.get_text('on') if self.settings['auto_save'] else self.get_text('off')}")
        print(f"4. {self.get_text('battle_animations')}: {self.get_text('on') if self.settings['battle_animations'] else self.get_text('off')}")
        print(f"0. {self.get_text('back')}")
        
        choice = input("\n➡️ ")
        
        if choice == '1':
            print(f"\n{self.get_text('select_language')}:")
            print("1. English")
            print("2. Українська")
            lang_choice = input("➡️ ")
            if lang_choice == '1':
                self.current_lang = 'en'
                self.settings['language'] = 'en'
            elif lang_choice == '2':
                self.current_lang = 'uk'
                self.settings['language'] = 'uk'
            self.update_language()
            self.save_settings()
            print(f"\n✅ Language changed to {self.languages[self.current_lang]['name']}")
            input("\nPress Enter to continue...")
        elif choice == '2':
            self.settings['sound'] = not self.settings['sound']
            self.save_settings()
            print(f"\n✅ {self.get_text('sound')}: {self.get_text('on') if self.settings['sound'] else self.get_text('off')}")
            input("\nPress Enter to continue...")
        elif choice == '3':
            self.settings['auto_save'] = not self.settings['auto_save']
            self.save_settings()
            print(f"\n✅ {self.get_text('auto_save')}: {self.get_text('on') if self.settings['auto_save'] else self.get_text('off')}")
            input("\nPress Enter to continue...")
        elif choice == '4':
            self.settings['battle_animations'] = not self.settings['battle_animations']
            self.save_settings()
            print(f"\n✅ {self.get_text('battle_animations')}: {self.get_text('on') if self.settings['battle_animations'] else self.get_text('off')}")
            input("\nPress Enter to continue...")
    
    def show_battlepass(self):
        """Показати бойовий пропуск"""
        print("\n" + "=" * 60)
        print(f"🎖️ {self.get_text('battle_pass')} - {self.get_text('season')} {self.battle_pass['season']}: {self.battle_pass['season_name']}")
        print("=" * 60)
        print(f"Level: {self.battle_pass['current_level']}/{self.battle_pass['max_level']}")
        print(f"XP: {self.battle_pass['current_xp']}/{self.battle_pass['xp_needed']}")
        
        progress = int((self.battle_pass['current_xp'] / self.battle_pass['xp_needed']) * 20)
        print(f"[{'█' * progress}{'░' * (20 - progress)}]")
        
        print(f"\nPremium BP: {'✅ ACTIVE' if self.player['premium_bp'] else '❌ NOT ACTIVE'}")
        if not self.player['premium_bp']:
            print(f"💎 Buy Premium BP for 1000 {self.get_text('gems')} to get 2x rewards!")
        
        print("\n📦 NEXT REWARDS:")
        next_level = self.battle_pass['current_level'] + 1
        if next_level <= self.battle_pass['max_level']:
            rewards = self.battle_pass['rewards'][next_level]
            print(f"  Free: {rewards['free']['credits']}💰 + {rewards['free']['exp']} XP")
            if rewards['free']['gems'] > 0:
                print(f"        + {rewards['free']['gems']}💎")
            if self.player['premium_bp']:
                print(f"  Premium: {rewards['premium']['credits']}💰 + {rewards['premium']['exp']} XP + {rewards['premium']['gems']}💎")
                if rewards['premium']['vehicle']:
                    print(f"           🎁 VEHICLE: {rewards['premium']['vehicle']}")
        
        input("\nPress Enter to continue...")
    
    def add_battlepass_xp(self, xp):
        """Додати XP до бойового пропуску"""
        self.battle_pass['current_xp'] += xp
        
        while self.battle_pass['current_xp'] >= self.battle_pass['xp_needed'] and self.battle_pass['current_level'] < self.battle_pass['max_level']:
            self.battle_pass['current_xp'] -= self.battle_pass['xp_needed']
            self.battle_pass['current_level'] += 1
            
            rewards = self.battle_pass['rewards'][self.battle_pass['current_level']]
            
            print(f"\n🎉 {self.get_text('battle_pass')} {self.get_text('level_up')} {self.battle_pass['current_level']}! 🎉")
            
            self.player['credits'] += rewards['free']['credits']
            self.player['total_exp'] += rewards['free']['exp']
            print(f"  Free: +{rewards['free']['credits']}💰, +{rewards['free']['exp']} XP")
            
            if rewards['free']['gems'] > 0:
                self.player['gems'] += rewards['free']['gems']
                print(f"        +{rewards['free']['gems']}💎")
            
            if self.player['premium_bp']:
                self.player['credits'] += rewards['premium']['credits']
                self.player['total_exp'] += rewards['premium']['exp']
                self.player['gems'] += rewards['premium']['gems']
                print(f"  Premium: +{rewards['premium']['credits']}💰, +{rewards['premium']['exp']} XP, +{rewards['premium']['gems']}💎")
                
                if rewards['premium']['vehicle']:
                    self.owned_vehicles.append({
                        'name': rewards['premium']['vehicle'],
                        'nation': 'USA',
                        'power': 150,
                        'era': 'Premium',
                        'year': 2024,
                        'tier': 6,
                        'type': 'tank',
                        'purchased': True,
                        'premium': True
                    })
                    print(f"        🎁 +{rewards['premium']['vehicle']}")
            
            if self.battle_pass['current_level'] < self.battle_pass['max_level']:
                self.battle_pass['xp_needed'] = int(self.battle_pass['xp_needed'] * 1.1)
    
    def migrate_save_file(self):
        """Міграція файлів зі старих версій"""
        old_files = [
            ('warthunder_save_v220.json', '2.2.0'),
            ('warthunder_save_v211.json', '2.1.1'),
            ('tcl_save.json', '1.0.0')
        ]
        
        new_file = 'tcl_save.json'
        
        if os.path.exists(new_file):
            backup_file = f'tcl_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            shutil.copy(new_file, backup_file)
            print(f"📀 Backup created: {backup_file}")
        
        for old_file, old_version in old_files:
            if os.path.exists(old_file) and old_file != new_file:
                try:
                    with open(old_file, 'r', encoding='utf-8') as f:
                        old_data = json.load(f)
                    
                    print(f"🔄 Migrating from {old_file}...")
                    
                    if 'player' in old_data:
                        if 'money' in old_data['player']:
                            old_data['player']['credits'] = old_data['player'].pop('money')
                        if 'golden_eagles' in old_data['player']:
                            old_data['player']['gems'] = old_data['player'].pop('golden_eagles')
                        self.player.update(old_data['player'])
                    
                    if 'nation_exp' in old_data:
                        nation_mapping = {
                            'СРСР': 'USSR', 'Німеччина': 'Germany',
                            'Україна': 'Ukraine', 'Китай': 'China',
                            'США': 'USA', 'Велика Британія': 'UK',
                            'Франція': 'France', 'Японія': 'Japan'
                        }
                        for old_nation, exp in old_data['nation_exp'].items():
                            new_nation = nation_mapping.get(old_nation, old_nation)
                            self.nation_exp[new_nation] = self.nation_exp.get(new_nation, 0) + exp
                    
                    if 'owned_vehicles' in old_data:
                        self.owned_vehicles = old_data['owned_vehicles']
                    
                    if 'battle_pass' in old_data:
                        self.battle_pass.update(old_data['battle_pass'])
                    
                    os.rename(old_file, f'migrated_{old_file}')
                    print(f"✅ Migration successful!")
                    self.save_game()
                    return
                    
                except Exception as e:
                    print(f"⚠️ Migration error: {e}")
    
    def save_game(self):
        """Збереження гри"""
        data = {
            'version': self.version,
            'game': self.game_name,
            'player': self.player,
            'nation_exp': self.nation_exp,
            'owned_vehicles': self.owned_vehicles,
            'owned_ships': self.owned_ships,
            'research_queue': self.research_queue,
            'ship_research_queue': self.ship_research_queue,
            'vehicle_mods': self.vehicle_mods,
            'battle_pass': self.battle_pass
        }
        with open('tcl_save.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("💾 Game saved!")
    
    def load_game(self):
        """Завантаження гри"""
        save_file = 'tcl_save.json'
        if os.path.exists(save_file):
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.player = data.get('player', self.player)
                    self.nation_exp = data.get('nation_exp', self.nation_exp)
                    self.owned_vehicles = data.get('owned_vehicles', [])
                    self.owned_ships = data.get('owned_ships', [])
                    self.research_queue = data.get('research_queue', {})
                    self.ship_research_queue = data.get('ship_research_queue', {})
                    self.vehicle_mods = data.get('vehicle_mods', {})
                    self.battle_pass = data.get('battle_pass', self.battle_pass)
                print(f"📀 Save loaded!")
            except Exception as e:
                print(f"⚠️ Error loading save: {e}")
                self.init_new_game()
        else:
            self.init_new_game()
    
    def init_new_game(self):
        """Нова гра"""
        self.owned_vehicles = []
        self.owned_ships = []
        self.research_queue = {}
        self.ship_research_queue = {}
        self.vehicle_mods = {}
        
        for nation in self.tech_tree:
            for name, data in self.tech_tree[nation].items():
                if data.get('cost', 0) == 0 and data.get('exp_needed', 0) == 0:
                    self.owned_vehicles.append({
                        'name': name,
                        'nation': nation,
                        'power': data['power'],
                        'era': data['era'],
                        'year': data['year'],
                        'tier': data['tier'],
                        'type': 'tank',
                        'purchased': True
                    })
        
        print(f"✨ New game created!")
        print(f"🎁 Starting bonus: 200 Gems!")
        print(f"🎖️ Battle Pass Season {self.battle_pass['season']} active!")
    
    def battle(self):
        """Бій"""
        if not self.player.get('current_vehicle'):
            print("❌ Select a vehicle first!")
            return
        
        current = None
        all_vehicles = self.owned_vehicles + self.owned_ships
        for v in all_vehicles:
            if v['name'] == self.player['current_vehicle']:
                current = v
                break
        
        if not current:
            print("❌ Vehicle not found!")
            return
        
        is_legendary = 'Legendary' in current['name']
        
        if current['type'] == 'ship':
            final_power = current['power']
            enemies = [
                {'name': 'Patrol Boat', 'power': 60, 'reward_exp': 40, 'reward_credits': 150},
                {'name': 'Destroyer', 'power': 100, 'reward_exp': 70, 'reward_credits': 250},
                {'name': 'Cruiser', 'power': 140, 'reward_exp': 100, 'reward_credits': 400},
            ]
        else:
            final_power = self.get_vehicle_power_with_mods(current)
            enemies = [
                {'name': 'Light Tank', 'power': 30, 'reward_exp': 20, 'reward_credits': 80},
                {'name': 'Medium Tank', 'power': 50, 'reward_exp': 35, 'reward_credits': 120},
                {'name': 'Heavy Tank', 'power': 70, 'reward_exp': 50, 'reward_credits': 160},
                {'name': 'Elite Tank', 'power': 90, 'reward_exp': 70, 'reward_credits': 220},
            ]
        
        enemy = random.choice(enemies)
        
        print("\n" + "=" * 60)
        print(f"⚔️ {self.get_text('battle_start')} ⚔️")
        legendary_tag = " 🌟LEGENDARY🌟" if is_legendary else ""
        print(f"{self.get_text('your_vehicle')}: {current['name']}{legendary_tag}")
        print(f"{self.get_text('power')}: {final_power}")
        print(f"\n{self.get_text('enemy')}: {enemy['name']}")
        print(f"{self.get_text('power')}: {enemy['power']}")
        print("=" * 60)
        
        if self.settings['battle_animations']:
            time.sleep(1)
            print("\n🔫 CALCULATING BATTLE...")
            time.sleep(1.5)
        
        legendary_bonus = 0.05 if is_legendary else 0
        win_chance = 0.65 + (final_power - enemy['power']) / 500 + legendary_bonus
        win_chance = max(0.45, min(0.90, win_chance))
        
        print(f"📊 {self.get_text('win_chance')}: {win_chance*100:.1f}%")
        if is_legendary:
            print("🌟 Legendary bonus: +5% chance!")
        
        bp_xp_gained = random.randint(10, 30)
        
        if random.random() < win_chance:
            reward_credits = random.randint(150, 450) + enemy['reward_credits']
            reward_exp_nation = random.randint(30, 100) + enemy['reward_exp']
            total_exp = random.randint(30, 90)
            
            if is_legendary:
                reward_credits = int(reward_credits * 1.2)
                reward_exp_nation = int(reward_exp_nation * 1.2)
                total_exp = int(total_exp * 1.2)
                bp_xp_gained = int(bp_xp_gained * 1.5)
            
            print(f"\n🎉🎉🎉 {self.get_text('victory')}! 🎉🎉🎉")
            print(f"💰 {self.get_text('credits')}: +{reward_credits}")
            print(f"📚 {self.get_text('exp')} ({current['nation']}): +{reward_exp_nation}")
            print(f"⭐ Total {self.get_text('exp')}: +{total_exp}")
            print(f"🎖️ Battle Pass XP: +{bp_xp_gained}")
            
            self.player['credits'] += reward_credits
            self.nation_exp[current['nation']] += reward_exp_nation
            self.player['total_exp'] += total_exp
            self.player['wins'] += 1
            
            self.add_battlepass_xp(bp_xp_gained)
            
            new_level = 1 + (self.player['total_exp'] // 200)
            if new_level > self.player['level']:
                self.player['level'] = new_level
                print(f"🎊 {self.get_text('level_up')}! Now level {self.player['level']}!")
        else:
            lose_credits = random.randint(20, 60)
            
            print(f"\n💀💀💀 {self.get_text('defeat')}! 💀💀💀")
            print(f"💸 {self.get_text('credits')} lost: {lose_credits}")
            print(f"📚 {self.get_text('exp')} ({current['nation']}): +10")
            print(f"🎖️ Battle Pass XP: +{bp_xp_gained // 2}")
            
            self.player['credits'] = max(0, self.player['credits'] - lose_credits)
            self.nation_exp[current['nation']] += 10
            self.player['losses'] += 1
            
            self.add_battlepass_xp(bp_xp_gained // 2)
        
        if self.settings['battle_animations']:
            time.sleep(1)
        
        self.show_stats()
        if self.settings['auto_save']:
            self.save_game()
        input("\nPress Enter to continue...")
    
    def get_vehicle_power_with_mods(self, vehicle):
        """Розрахувати силу з модифікаціями"""
        mod_key = f"{vehicle['nation']}_{vehicle['name']}"
        current_mods = self.vehicle_mods.get(mod_key, [])
        
        base_power = vehicle['power']
        bonus = 0
        
        for mod_name in current_mods:
            if mod_name in self.modifications:
                mod_data = self.modifications[mod_name]
                if mod_data.get('legendary_only', False):
                    if 'Legendary' in vehicle['name']:
                        bonus += mod_data.get('power_bonus', 0)
                else:
                    bonus += mod_data.get('power_bonus', 0)
        
        return base_power + bonus
    
    def show_stats(self):
        """Показати статистику"""
        print("\n" + "=" * 60)
        print(f"🎮 COMMANDER: {self.player['name']}")
        print(f"🏆 {self.get_text('level')}: {self.player['level']}")
        print(f"⭐ {self.get_text('exp')}: {self.player['total_exp']}")
        print(f"💰 {self.get_text('credits')}: {self.player['credits']}")
        print(f"💎 {self.get_text('gems')}: {self.player['gems']}")
        print(f"📊 {self.get_text('wins')}: {self.player['wins']} | {self.get_text('losses')}: {self.player['losses']}")
        winrate = (self.player['wins'] / (self.player['wins'] + self.player['losses']) * 100) if (self.player['wins'] + self.player['losses']) > 0 else 0
        print(f"📈 WINRATE: {winrate:.1f}%")
        
        if self.player.get('current_vehicle'):
            is_legendary = 'Legendary' in self.player['current_vehicle']
            legendary_tag = " 🌟" if is_legendary else ""
            print(f"🎯 CURRENT VEHICLE: {self.player['current_vehicle']}{legendary_tag}")
        
        legendary_count = len([v for v in self.owned_vehicles if 'Legendary' in v['name']])
        if legendary_count > 0:
            print(f"🌟 LEGENDARY VEHICLES: {legendary_count}")
        
        print(f"\n🎖️ {self.get_text('battle_pass')}: Level {self.battle_pass['current_level']}/{self.battle_pass['max_level']}")
        print("=" * 60)
    
    def show_tech_tree(self, nation):
        """Показати дерево техніки"""
        if nation not in self.tech_tree:
            print("❌ Nation not found!")
            return
        
        print("\n" + "=" * 70)
        print(f"        {self.get_text('tech_tree')} - {nation} (Total: {len(self.tech_tree[nation])} VEHICLES)")
        print("=" * 70)
        
        tiers = {}
        for name, data in self.tech_tree[nation].items():
            tier = data['tier']
            if tier not in tiers:
                tiers[tier] = []
            tiers[tier].append((name, data))
        
        for tier in sorted(tiers.keys()):
            print(f"\n📊 TIER {tier}")
            print("-" * 60)
            for name, data in sorted(tiers[tier], key=lambda x: x[1]['year']):
                legendary_tag = " 🌟" if data.get('legendary', False) else ""
                
                if any(v['name'] == name and v['nation'] == nation for v in self.owned_vehicles):
                    status = "✅ RESEARCHED"
                elif name in self.research_queue.get(nation, {}):
                    status = f"🔬 RESEARCHING ({self.research_queue[nation][name]['current']}/{self.research_queue[nation][name]['needed']})"
                else:
                    available = data['exp_needed'] == 0 or len([v for v in self.owned_vehicles if v['nation'] == nation]) > 0
                    if available:
                        status = f"🔒 AVAILABLE ({data['exp_needed']} XP)"
                    else:
                        status = "🔴 LOCKED"
                
                print(f"  {name}{legendary_tag} ({data['year']}) - 💪Power: {data['power']} | 💰{data['cost']}💰")
                print(f"     {status}")
        
        input("\nPress Enter to continue...")
    
    def research_vehicle(self):
        """Дослідити нову техніку"""
        print(f"\n🔬 {self.get_text('research')}")
        nations = list(self.tech_tree.keys())
        for i, nation in enumerate(nations, 1):
            print(f"{i}. {nation}")
        
        try:
            choice = int(input("Choose nation: "))
            if 1 <= choice <= len(nations):
                nation = nations[choice-1]
                self.show_tech_tree(nation)
                
                vehicle_name = input("\n📝 Enter vehicle name to research: ")
                
                if vehicle_name not in self.tech_tree[nation]:
                    print("❌ Vehicle not found!")
                    input("Press Enter to continue...")
                    return
                
                vehicle_data = self.tech_tree[nation][vehicle_name]
                
                if any(v['name'] == vehicle_name and v['nation'] == nation for v in self.owned_vehicles):
                    print("✅ Already researched!")
                    input("Press Enter to continue...")
                    return
                
                if nation in self.research_queue and vehicle_name in self.research_queue[nation]:
                    print("🔬 Already researching!")
                    input("Press Enter to continue...")
                    return
                
                if self.nation_exp[nation] < vehicle_data['exp_needed']:
                    print(f"❌ Not enough {nation} XP! Need: {vehicle_data['exp_needed']}")
                    input("Press Enter to continue...")
                    return
                
                if nation not in self.research_queue:
                    self.research_queue[nation] = {}
                
                self.research_queue[nation][vehicle_name] = {
                    'current': 0,
                    'needed': vehicle_data['exp_needed']
                }
                
                print(f"🔬 Started researching {vehicle_name}!")
                if vehicle_data.get('legendary', False):
                    print("🌟 LEGENDARY VEHICLE! Worth the effort!")
                input("Press Enter to continue...")
        except:
            print("❌ Invalid input!")
            input("Press Enter to continue...")
    
    def invest_exp(self):
        """Вкласти досвід в дослідження"""
        has_research = any(self.research_queue.values()) or any(self.ship_research_queue.values())
        
        if not has_research:
            print("❌ No active research! Start research first (option 10)")
            input("Press Enter to continue...")
            return
        
        print("\n📚 ACTIVE RESEARCH:")
        
        for nation, vehicles in self.research_queue.items():
            for name, data in vehicles.items():
                legendary_tag = " 🌟" if 'Legendary' in name else ""
                print(f"  🚀 {nation} - {name}{legendary_tag}: {data['current']}/{data['needed']} XP")
        
        for nation, ships in self.ship_research_queue.items():
            for name, data in ships.items():
                print(f"  🚢 {nation} - {name}: {data['current']}/{data['needed']} XP")
        
        print(f"\n💡 Your nation XP:")
        for nation, exp in self.nation_exp.items():
            if exp > 0 or nation in self.tech_tree:
                print(f"  {nation}: {exp} XP")
        
        try:
            amount = int(input("\n✏️ How much XP to invest? (0 - cancel): "))
            if amount <= 0:
                return
            
            print("\nChoose research:")
            options = []
            idx = 1
            
            for nation, vehicles in self.research_queue.items():
                for name, data in vehicles.items():
                    print(f"{idx}. {nation} - {name}")
                    options.append(('tank', nation, name))
                    idx += 1
            
            for nation, ships in self.ship_research_queue.items():
                for name, data in ships.items():
                    print(f"{idx}. {nation} - {name}")
                    options.append(('ship', nation, name))
                    idx += 1
            
            choice = int(input("Your choice: ")) - 1
            if 0 <= choice < len(options):
                obj_type, nation, name = options[choice]
                
                if self.nation_exp[nation] >= amount:
                    self.nation_exp[nation] -= amount
                    
                    if obj_type == 'tank':
                        self.research_queue[nation][name]['current'] += amount
                        print(f"✅ Invested {amount} XP in {name}")
                        
                        if self.research_queue[nation][name]['current'] >= self.research_queue[nation][name]['needed']:
                            print(f"🎉 RESEARCH COMPLETED: {name}!")
                            vehicle_data = self.tech_tree[nation][name]
                            self.owned_vehicles.append({
                                'name': name,
                                'nation': nation,
                                'power': vehicle_data['power'],
                                'era': vehicle_data['era'],
                                'year': vehicle_data['year'],
                                'tier': vehicle_data['tier'],
                                'type': 'tank',
                                'purchased': False
                            })
                            if vehicle_data.get('legendary', False):
                                print("🌟 LEGENDARY VEHICLE UNLOCKED!")
                            del self.research_queue[nation][name]
                            if not self.research_queue[nation]:
                                del self.research_queue[nation]
                    else:
                        self.ship_research_queue[nation][name]['current'] += amount
                        print(f"✅ Invested {amount} XP in ship {name}")
                        
                        if self.ship_research_queue[nation][name]['current'] >= self.ship_research_queue[nation][name]['needed']:
                            print(f"🎉 SHIP RESEARCH COMPLETED: {name}!")
                            ship_data = self.ships_tree[nation][name]
                            self.owned_ships.append({
                                'name': name,
                                'nation': nation,
                                'power': ship_data['power'],
                                'era': ship_data['era'],
                                'year': ship_data['year'],
                                'tier': ship_data['tier'],
                                'type': 'ship',
                                'purchased': False
                            })
                            del self.ship_research_queue[nation][name]
                            if not self.ship_research_queue[nation]:
                                del self.ship_research_queue[nation]
                else:
                    print(f"❌ Not enough {nation} XP!")
            else:
                print("❌ Invalid choice!")
        except:
            print("❌ Invalid input!")
        input("Press Enter to continue...")
    
    def buy_vehicle(self):
        """Купити досліджену техніку"""
        print(f"\n💰 {self.get_text('purchase')}")
        
        not_purchased = [v for v in self.owned_vehicles if not v.get('purchased', True)]
        
        if not not_purchased:
            print("❌ No vehicles available for purchase!")
            input("Press Enter to continue...")
            return
        
        print("\n🛒 RESEARCHED VEHICLES:")
        for i, v in enumerate(not_purchased, 1):
            data = self.tech_tree[v['nation']][v['name']]
            legendary_tag = " 🌟" if data.get('legendary', False) else ""
            print(f"{i}. {v['nation']} - {v['name']}{legendary_tag} (Tier {data['tier']}, 💰 {data['cost']}💰, 💪 {v['power']})")
        
        try:
            choice = int(input("Choose vehicle to purchase (number): "))
            if 1 <= choice <= len(not_purchased):
                vehicle = not_purchased[choice-1]
                data = self.tech_tree[vehicle['nation']][vehicle['name']]
                
                if self.player['credits'] >= data['cost']:
                    self.player['credits'] -= data['cost']
                    vehicle['purchased'] = True
                    print(f"✅ Purchased {vehicle['name']} for {data['cost']}💰!")
                    if data.get('legendary', False):
                        print("🌟 LEGENDARY VEHICLE ACQUIRED!")
                    self.save_game()
                else:
                    print(f"❌ Not enough credits! Need {data['cost']}💰, you have {self.player['credits']}💰")
            else:
                print("❌ Invalid number!")
        except:
            print("❌ Invalid input!")
        input("Press Enter to continue...")
    
    def select_vehicle(self):
        """Вибрати техніку для бою"""
        purchased = [v for v in self.owned_vehicles if v.get('purchased', True)]
        
        if not purchased:
            print("❌ No purchased vehicles!")
            return False
        
        print("\n🚀 YOUR VEHICLES:")
        for i, v in enumerate(purchased, 1):
            final_power = self.get_vehicle_power_with_mods(v)
            legendary_tag = " 🌟" if 'Legendary' in v['name'] else ""
            print(f"{i}. {v['nation']} - {v['name']}{legendary_tag} (💪 {final_power}, 📅 {v['year']})")
        
        try:
            choice = int(input("Choose vehicle for battle (number): "))
            if 1 <= choice <= len(purchased):
                self.player['current_vehicle'] = purchased[choice-1]['name']
                self.player['current_nation'] = purchased[choice-1]['nation']
                self.player['current_type'] = 'tank'
                print(f"✅ Selected: {self.player['current_vehicle']}")
                return True
            else:
                print("❌ Invalid number!")
                return False
        except:
            print("❌ Invalid input!")
            return False
    
    def select_ship(self):
        """Вибрати корабель для бою"""
        purchased = [v for v in self.owned_ships if v.get('purchased', True)]
        
        if not purchased:
            print("❌ No purchased ships!")
            return False
        
        print("\n🚢 YOUR SHIPS:")
        for i, v in enumerate(purchased, 1):
            print(f"{i}. {v['nation']} - {v['name']} (💪 {v['power']}, 📅 {v['year']})")
        
        try:
            choice = int(input("Choose ship for battle (number): "))
            if 1 <= choice <= len(purchased):
                self.player['current_vehicle'] = purchased[choice-1]['name']
                self.player['current_nation'] = purchased[choice-1]['nation']
                self.player['current_type'] = 'ship'
                print(f"✅ Selected: {self.player['current_vehicle']}")
                return True
            else:
                print("❌ Invalid number!")
                return False
        except:
            print("❌ Invalid input!")
            return False
    
    def install_mod(self):
        """Встановити модифікації"""
        if not self.player.get('current_vehicle') or self.player.get('current_type') != 'tank':
            print("❌ Select a vehicle first (option 6)!")
            input("Press Enter to continue...")
            return
        
        current_vehicle = self.player['current_vehicle']
        current_nation = self.player['current_nation']
        is_legendary = 'Legendary' in current_vehicle
        
        mod_key = f"{current_nation}_{current_vehicle}"
        if mod_key not in self.vehicle_mods:
            self.vehicle_mods[mod_key] = []
        
        print(f"\n🔧 {self.get_text('modifications')} FOR {current_vehicle}")
        if is_legendary:
            print("🌟 LEGENDARY VEHICLE - Unique modifications available!")
        
        mod_list = []
        for mod_name, mod_data in self.modifications.items():
            if mod_data.get('legendary_only', False) and not is_legendary:
                continue
            mod_list.append((mod_name, mod_data))
        
        for i, (mod_name, mod_data) in enumerate(mod_list, 1):
            if mod_name in self.vehicle_mods[mod_key]:
                status = "✅ INSTALLED"
            else:
                status = f"💰 {mod_data['cost']}💰"
            legendary_tag = " 🌟" if mod_data.get('legendary_only', False) else ""
            print(f"{i}. {mod_name}{legendary_tag} - {mod_data['description']} - {status}")
        
        try:
            choice = int(input("\nChoose modification (0 - exit): "))
            if 1 <= choice <= len(mod_list):
                mod_name, mod_data = mod_list[choice-1]
                
                if mod_name in self.vehicle_mods[mod_key]:
                    print("❌ Modification already installed!")
                elif self.player['credits'] >= mod_data['cost']:
                    self.player['credits'] -= mod_data['cost']
                    self.vehicle_mods[mod_key].append(mod_name)
                    print(f"✅ Installed {mod_name} on {current_vehicle}!")
                    if mod_data.get('legendary_only', False):
                        print("   🌟 Legendary modification activated!")
                    self.save_game()
                else:
                    print(f"❌ Not enough credits! Need {mod_data['cost']}💰, you have {self.player['credits']}💰")
        except:
            print("❌ Invalid input!")
        input("Press Enter to continue...")
    
    def show_ships_tree(self, nation):
        """Показати дерево кораблів"""
        if nation not in self.ships_tree:
            print("❌ Nation not found!")
            return
        
        print("\n" + "=" * 70)
        print(f"        {self.get_text('ships')} - {nation} (Total: {len(self.ships_tree[nation])} SHIPS)")
        print("=" * 70)
        
        for name, data in sorted(self.ships_tree[nation].items(), key=lambda x: x[1]['tier']):
            if any(v['name'] == name and v['nation'] == nation for v in self.owned_ships):
                status = "✅ RESEARCHED"
            elif name in self.ship_research_queue.get(nation, {}):
                status = f"🔬 RESEARCHING ({self.ship_research_queue[nation][name]['current']}/{self.ship_research_queue[nation][name]['needed']})"
            else:
                status = f"🔒 AVAILABLE ({data['exp_needed']} XP)"
            
            print(f"\n🚢 {name} (Tier {data['tier']}, {data['year']})")
            print(f"   💪 Power: {data['power']} | 💰 {data['cost']}💰")
            print(f"   {status}")
        
        input("\nPress Enter to continue...")
    
    def research_ship(self):
        """Дослідити корабель"""
        print(f"\n🔬 {self.get_text('research')} SHIP")
        nations = list(self.ships_tree.keys())
        for i, nation in enumerate(nations, 1):
            print(f"{i}. {nation}")
        
        try:
            choice = int(input("Choose nation: "))
            if 1 <= choice <= len(nations):
                nation = nations[choice-1]
                self.show_ships_tree(nation)
                
                ship_name = input("\n📝 Enter ship name to research: ")
                
                if ship_name not in self.ships_tree[nation]:
                    print("❌ Ship not found!")
                    input("Press Enter to continue...")
                    return
                
                ship_data = self.ships_tree[nation][ship_name]
                
                if any(v['name'] == ship_name and v['nation'] == nation for v in self.owned_ships):
                    print("✅ Already researched!")
                    input("Press Enter to continue...")
                    return
                
                if nation in self.ship_research_queue and ship_name in self.ship_research_queue[nation]:
                    print("🔬 Already researching!")
                    input("Press Enter to continue...")
                    return
                
                if self.nation_exp[nation] < ship_data['exp_needed']:
                    print(f"❌ Not enough {nation} XP! Need: {ship_data['exp_needed']}")
                    input("Press Enter to continue...")
                    return
                
                if nation not in self.ship_research_queue:
                    self.ship_research_queue[nation] = {}
                
                self.ship_research_queue[nation][ship_name] = {
                    'current': 0,
                    'needed': ship_data['exp_needed']
                }
                
                print(f"🔬 Started researching {ship_name}!")
                input("Press Enter to continue...")
        except:
            print("❌ Invalid input!")
            input("Press Enter to continue...")
    
    def buy_ship(self):
        """Купити досліджений корабель"""
        print(f"\n💰 {self.get_text('purchase')} SHIP")
        
        not_purchased = [v for v in self.owned_ships if not v.get('purchased', True)]
        
        if not not_purchased:
            print("❌ No ships available for purchase!")
            input("Press Enter to continue...")
            return
        
        print("\n🛒 RESEARCHED SHIPS:")
        for i, v in enumerate(not_purchased, 1):
            data = self.ships_tree[v['nation']][v['name']]
            print(f"{i}. {v['nation']} - {v['name']} (Tier {data['tier']}, 💰 {data['cost']}💰, 💪 {v['power']})")
        
        try:
            choice = int(input("Choose ship to purchase (number): "))
            if 1 <= choice <= len(not_purchased):
                ship = not_purchased[choice-1]
                data = self.ships_tree[ship['nation']][ship['name']]
                
                if self.player['credits'] >= data['cost']:
                    self.player['credits'] -= data['cost']
                    ship['purchased'] = True
                    print(f"✅ Purchased {ship['name']} for {data['cost']}💰!")
                    self.save_game()
                else:
                    print(f"❌ Not enough credits! Need {data['cost']}💰, you have {self.player['credits']}💰")
            else:
                print("❌ Invalid number!")
        except:
            print("❌ Invalid input!")
        input("Press Enter to continue...")
    
    def show_legendary_vehicles(self):
        """Показати легендарні машини"""
        print("\n" + "=" * 60)
        print(f"🌟 {self.get_text('legendary')} VEHICLES 🌟")
        print("=" * 60)
        
        for nation, vehicles in self.legendary_vehicles.items():
            for name, data in vehicles.items():
                print(f"\n{nation} - {name}")
                print(f"   📅 {data['year']} | Tier {data['tier']}")
                print(f"   💪 Power: {data['power']} | 💰 {data['cost']}💰")
                print(f"   🔬 Research cost: {data['exp_needed']} XP")
                print(f"   📝 {data['description']}")
        
        print("\n💡 Legendary vehicles have unique modifications!")
        input("\nPress Enter to continue...")
    
    def run(self):
        """Головний цикл гри"""
        print("\n" + "█" * 70)
        print("█" + " " * 68 + "█")
        print("█      🎮 TANK COMMANDER: LEGENDS V1.0.0 🎮      █")
        print("█" + " " * 68 + "█")
        print("█" * 70)
        print("\n✨ WELCOME, COMMANDER!")
        print("   • 🎖️ Battle Pass with 50 levels of rewards")
        print("   • 🌍 8 Nations with vehicles!")
        print("   • 💎 Premium currency: GEMS")
        print("   • 💰 Currency: CREDITS")
        print("   • 🔧 Modification system")
        print("   • 🌟 Legendary vehicles")
        print(f"   • 🌐 Current language: {self.languages[self.current_lang]['name']}")
        
        while True:
            print("\n" + "─" * 70)
            print(self.get_text('main_menu').upper() + ":")
            print("1 ⚔️  " + self.get_text('battle'))
            print("2 🎖️  " + self.get_text('battle_pass'))
            print("3 🌟 " + self.get_text('legendary'))
            print("4 🌲 " + self.get_text('tech_tree') + " - " + self.get_text('tanks'))
            print("5 🚢 " + self.get_text('tech_tree') + " - " + self.get_text('ships'))
            print("6 🚀 " + self.get_text('select') + " " + self.get_text('tank'))
            print("7 🚢 " + self.get_text('select') + " " + self.get_text('ship'))
            print("8 🔧 " + self.get_text('modifications'))
            print("9 📊 " + self.get_text('stats'))
            print("10 🔬 " + self.get_text('research') + " " + self.get_text('tank'))
            print("11 🚢 " + self.get_text('research') + " " + self.get_text('ship'))
            print("12 📚 " + self.get_text('invest') + " " + self.get_text('exp'))
            print("13 💰 " + self.get_text('purchase') + " " + self.get_text('tank'))
            print("14 💰 " + self.get_text('purchase') + " " + self.get_text('ship'))
            print("15 ⚙️ " + self.get_text('settings'))
            print("16 💾 " + self.get_text('save'))
            print("0 🚪 " + self.get_text('exit'))
            print("─" * 70)
            
            choice = input("➡️ " + self.get_text('your') + " " + self.get_text('choice') + ": ")
            
            if choice == '1':
                self.battle()
            elif choice == '2':
                self.show_battlepass()
            elif choice == '3':
                self.show_legendary_vehicles()
            elif choice == '4':
                print("\nSelect nation:")
                nations = list(self.tech_tree.keys())
                for i, nation in enumerate(nations, 1):
                    print(f"{i}. {nation}")
                try:
                    n_choice = int(input("Choice: "))
                    if 1 <= n_choice <= len(nations):
                        self.show_tech_tree(nations[n_choice-1])
                except:
                    print("❌ Invalid input!")
            elif choice == '5':
                print("\nSelect nation:")
                nations = list(self.ships_tree.keys())
                for i, nation in enumerate(nations, 1):
                    print(f"{i}. {nation}")
                try:
                    n_choice = int(input("Choice: "))
                    if 1 <= n_choice <= len(nations):
                        self.show_ships_tree(nations[n_choice-1])
                except:
                    print("❌ Invalid input!")
            elif choice == '6':
                self.select_vehicle()
            elif choice == '7':
                self.select_ship()
            elif choice == '8':
                self.install_mod()
            elif choice == '9':
                self.show_stats()
                input("\nPress Enter to continue...")
            elif choice == '10':
                self.research_vehicle()
            elif choice == '11':
                self.research_ship()
            elif choice == '12':
                self.invest_exp()
            elif choice == '13':
                self.buy_vehicle()
            elif choice == '14':
                self.buy_ship()
            elif choice == '15':
                self.show_settings()
            elif choice == '16':
                self.save_game()
                input("\nPress Enter to continue...")
            elif choice == '0':
                print("\n👋 Thanks for playing TANK COMMANDER: LEGENDS!")
                total_tanks = sum(len(v) for v in self.tech_tree.values())
                total_ships = sum(len(v) for v in self.ships_tree.values())
                researched_tanks = len([v for v in self.owned_vehicles if v.get('purchased', True)])
                researched_ships = len([v for v in self.owned_ships if v.get('purchased', True)])
                legendary_count = len([v for v in self.owned_vehicles if 'Legendary' in v['name']])
                print(f"📊 Researched {researched_tanks}/{total_tanks} tanks & {researched_ships}/{total_ships} ships!")
                print(f"🌟 Legendary vehicles: {legendary_count}")
                print(f"🎖️ Battle Pass Level: {self.battle_pass['current_level']}/{self.battle_pass['max_level']}")
                self.save_game()
                break
            else:
                print("❌ Invalid choice!")

if __name__ == "__main__":
    game = TankCommanderLegends()
    game.run()