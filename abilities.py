import time
import pygame

class AbilityManager:
    def __init__(self):
        self.data = {
            "Wolf Vein": {"cd": 15, "color": (192, 192, 192), "desc": "10% Speed Boost (5s)", "icon_type": "circle"},
            "Dragon Heart": {"cd": 15, "color": (255, 50, 50), "desc": "Fears nearest ghost (3s)", "icon_type": "heart"},
            "Demon Eye": {"cd": 20, "color": (148, 0, 211), "desc": "Confuses ghost target (5s)", "icon_type": "eye"},
            "Angels Halo": {"cd": 15, "color": (255, 215, 0), "desc": "Invincible Dash", "icon_type": "ring"},
            "John Snow": {"cd": 0, "color": (200, 240, 255), "desc": "Passive: +3% stats on death", "icon_type": "snowflake"}
        }
        self.last_used = {key: 0 for key in self.data}

    def activate(self, name, player, ghosts):
        if name == "John Snow": return
        now = time.time()
        if now - self.last_used[name] < self.data[name]["cd"]: return

        self.last_used[name] = now
        print(f"Activated {name}!")

        if name == "Wolf Vein":
            player.speed_mult = 1.10
            player.buff_timer = 300 # 5 seconds
        elif name == "Dragon Heart":
            for g in ghosts: g.sleep_timer = 180 # Fear effect
        elif name == "Angels Halo":
            player.invincible = True
            player.invincible_timer = 120 # 2 seconds