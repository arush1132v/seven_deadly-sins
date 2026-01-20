import json
import os

class GameData:
    """Manages persistent game data"""
    
    def __init__(self):
        self.save_file = "save_data.json"
        self.data = self.load_default_data()
        self.load()
    
    def load_default_data(self):
        """Returns default game data structure"""
        return {
            "player": {
                "points": 0,
                "highest_level": 1,
                "deaths": 0,
                "wins": 0,
                "playtime_seconds": 0
            },
            "inventory": {
                "owned_items": [],  # List of item IDs (1-5)
                "used_items": []    # Items used in current session
            },
            "abilities": {
                "selected": [],  # 2 ability names
                "usage_stats": {
                    "Wolf Vein": 0,
                    "Dragon Heart": 0,
                    "Demon Eye": 0,
                    "Angels Halo": 0,
                    "John Snow": 0
                }
            },
            "statistics": {
                "coins_collected": 0,
                "ghosts_killed": 0,
                "items_collected": 0
            },
            "settings": {
                "audio": {
                    "music": 0.5,
                    "sfx": 0.7
                },
                "keybinds": {
                    "ability_1": 49,  # Key code for '1'
                    "ability_2": 50,  # Key code for '2'
                    "shop_1": 113,    # Key code for 'q'
                    "shop_2": 101     # Key code for 'e'
                }
            }
        }
    
    def load(self):
        """Load data from save file"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    loaded_data = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self._merge_data(self.data, loaded_data)
                    print(f"✓ Loaded save data: {self.data['player']['points']} points")
            except Exception as e:
                print(f"Error loading save: {e}")
        else:
            print("No save file found, using defaults")
    
    def _merge_data(self, default, loaded):
        """Recursively merge loaded data with defaults"""
        for key, value in loaded.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self._merge_data(default[key], value)
                else:
                    default[key] = value
    
    def save(self):
        """Save data to file"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.data, f, indent=2)
            print("✓ Game data saved")
        except Exception as e:
            print(f"Error saving game: {e}")
    
    # --- GETTERS ---
    def get_points(self):
        return self.data["player"]["points"]
    
    def get_inventory(self):
        return self.data["inventory"]["owned_items"]
    
    def get_unused_items(self):
        """Get items that haven't been used this session"""
        owned = self.data["inventory"]["owned_items"]
        used = self.data["inventory"]["used_items"]
        return [item for item in owned if item not in used]
    
    def get_selected_abilities(self):
        return self.data["abilities"]["selected"]
    
    def get_settings(self):
        return self.data["settings"]
    
    # --- SETTERS ---
    def add_points(self, amount):
        self.data["player"]["points"] += amount
    
    def spend_points(self, amount):
        self.data["player"]["points"] = max(0, self.data["player"]["points"] - amount)
    
    def buy_item(self, item_id):
        if item_id not in self.data["inventory"]["owned_items"]:
            self.data["inventory"]["owned_items"].append(item_id)
    
    def use_item(self, item_id):
        if item_id not in self.data["inventory"]["used_items"]:
            self.data["inventory"]["used_items"].append(item_id)
    
    def reset_used_items(self):
        """Reset used items for new level"""
        self.data["inventory"]["used_items"] = []
    
    def set_selected_abilities(self, abilities):
        self.data["abilities"]["selected"] = abilities
    
    def record_ability_use(self, ability_name):
        if ability_name in self.data["abilities"]["usage_stats"]:
            self.data["abilities"]["usage_stats"][ability_name] += 1
    
    def update_highest_level(self, level):
        if level > self.data["player"]["highest_level"]:
            self.data["player"]["highest_level"] = level
    
    def record_death(self):
        self.data["player"]["deaths"] += 1
    
    def complete_level(self):
        self.data["player"]["wins"] += 1
    
    def add_playtime(self, seconds):
        self.data["player"]["playtime_seconds"] += seconds
    
    def add_coins_collected(self, amount):
        self.data["statistics"]["coins_collected"] += amount
    
    def add_ghost_killed(self):
        self.data["statistics"]["ghosts_killed"] += 1
    
    def add_item_collected(self):
        self.data["statistics"]["items_collected"] += 1
    
    def update_audio(self, music_vol, sfx_vol):
        self.data["settings"]["audio"]["music"] = music_vol
        self.data["settings"]["audio"]["sfx"] = sfx_vol
    
    def update_keybind(self, action, key_code):
        self.data["settings"]["keybinds"][action] = key_code
    
    def get_full_report(self):
        """Get full stats report"""
        p = self.data["player"]
        s = self.data["statistics"]
        hours = p["playtime_seconds"] // 3600
        minutes = (p["playtime_seconds"] % 3600) // 60
        
        report = f"""
=== GAME STATISTICS ===
Points: {p['points']}
Highest Level: {p['highest_level']}
Wins: {p['wins']}
Deaths: {p['deaths']}
Playtime: {hours}h {minutes}m

Coins Collected: {s['coins_collected']}
Ghosts Killed: {s['ghosts_killed']}
Items Collected: {s['items_collected']}

Ability Usage:
"""
        for ability, count in self.data["abilities"]["usage_stats"].items():
            report += f"  {ability}: {count}\n"
        
        return report
    
    def restart_game(self):
        """Reset all progress to default state"""
        print("\n" + "="*50)
        print("🔄 RESTARTING GAME - ALL PROGRESS RESET")
        print("="*50)
        
        # Reset to defaults
        self.data = self.load_default_data()
        
        # Save immediately
        self.save()
        
        print("✓ Game has been reset to initial state")
        print("✓ All points, items, and statistics cleared")
        print("="*50 + "\n")

# Singleton instance
_game_data_instance = None

def get_game_data():
    """Get or create the game data singleton"""
    global _game_data_instance
    if _game_data_instance is None:
        _game_data_instance = GameData()
    return _game_data_instance