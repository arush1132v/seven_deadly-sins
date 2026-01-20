import time
import pygame
import math

class AbilityManager:
    def __init__(self):
        self.data = {
            "Wolf Vein": {
                "cd": 15, 
                "color": (192, 192, 192), 
                "desc": "10% Speed Boost (5s)", 
                "icon_type": "circle"
            },
            "Dragon Heart": {
                "cd": 15, 
                "color": (255, 50, 50), 
                "desc": "Fears nearest ghost (3s)", 
                "icon_type": "heart"
            },
            "Demon Eye": {
                "cd": 20, 
                "color": (148, 0, 211), 
                "desc": "Confuses nearest ghost (5s)", 
                "icon_type": "eye"
            },
            "Angels Halo": {
                "cd": 15, 
                "color": (255, 215, 0), 
                "desc": "Dash 20 blocks, break walls", 
                "icon_type": "ring"
            },
            "John Snow": {
                "cd": 0, 
                "color": (200, 240, 255), 
                "desc": "Passive: +3% stats on death", 
                "icon_type": "snowflake"
            }
        }
        self.last_used = {key: 0 for key in self.data}

    def activate(self, name, player, ghosts, walls=None):
        """Activate an ability with proper effects"""
        
        # John Snow is passive only
        if name == "John Snow": 
            return
        
        now = time.time()
        if now - self.last_used[name] < self.data[name]["cd"]: 
            return

        self.last_used[name] = now
        print(f"✓ Activated {name}!")

        if name == "Wolf Vein":
            self._activate_wolf_vein(player)
            
        elif name == "Dragon Heart":
            self._activate_dragon_heart(player, ghosts)
            
        elif name == "Demon Eye":
            self._activate_demon_eye(player, ghosts)
            
        elif name == "Angels Halo":
            self._activate_angels_halo(player, walls)

    def _activate_wolf_vein(self, player):
        """10% Speed boost for 5 seconds"""
        player.speed_buff_timer = 300  # 5 seconds at 60 FPS
        print("  → Speed boosted by 10% for 5 seconds!")

    def _activate_dragon_heart(self, player, ghosts):
        """Fear the nearest ghost for 3 seconds (50% speed reduction)"""
        nearest_ghost = None
        min_distance = float('inf')
        
        # Find nearest ghost to player
        for ghost in ghosts:
            distance = math.hypot(
                ghost.rect.centerx - player.rect.centerx,
                ghost.rect.centery - player.rect.centery
            )
            if distance < min_distance:
                min_distance = distance
                nearest_ghost = ghost
        
        if nearest_ghost:
            # Apply fear status effect (3 seconds)
            nearest_ghost.fear_timer = 180  # 3 seconds at 60 FPS
            print(f"  → {nearest_ghost.name} is FEARED for 3 seconds! (50% speed)")
        else:
            print("  → No ghosts nearby to fear!")

    def _activate_demon_eye(self, player, ghosts):
        """Confuse nearest ghost to attack other ghosts for 5 seconds"""
        nearest_ghost = None
        min_distance = float('inf')
        
        # Find nearest ghost to player
        for ghost in ghosts:
            distance = math.hypot(
                ghost.rect.centerx - player.rect.centerx,
                ghost.rect.centery - player.rect.centery
            )
            if distance < min_distance:
                min_distance = distance
                nearest_ghost = ghost
        
        if nearest_ghost:
            # Apply confusion status effect (5 seconds)
            nearest_ghost.confusion_timer = 300  # 5 seconds at 60 FPS
            print(f"  → {nearest_ghost.name} is CONFUSED for 5 seconds! (Attacks other ghosts)")
        else:
            print("  → No ghosts nearby to confuse!")

    def _activate_angels_halo(self, player, walls):
        """
        Invincible dash 20 blocks in movement direction.
        Breaks any walls in path.
        """
        player.start_dash(walls)  # Pass walls to break them
        print("  → Dashing 20 blocks with invincibility! Breaking walls!")

    def apply_john_snow_passive(self, player):
        """Called when player dies - grants +3% permanent stat boost"""
        player.stats_multiplier += 0.03
        print(f"  → John Snow Passive: Stats increased to {player.stats_multiplier * 100:.1f}%!")
        return player.stats_multiplier


class AbilityEffectTracker:
    """
    Tracks active ability effects for visual indicators
    Used by HUD to show which abilities are currently active
    """
    
    def __init__(self):
        self.active_effects = {
            "Wolf Vein": 0,
            "Dragon Heart": 0,
            "Demon Eye": 0,
            "Angels Halo": 0
        }
    
    def update(self, player, ghosts):
        """Update timers based on game state"""
        
        # Wolf Vein - check player speed buff
        if hasattr(player, 'speed_buff_timer') and player.speed_buff_timer > 0:
            self.active_effects["Wolf Vein"] = player.speed_buff_timer
        else:
            self.active_effects["Wolf Vein"] = 0
        
        # Dragon Heart - check if any ghost is feared
        max_fear = 0
        for ghost in ghosts:
            if hasattr(ghost, 'fear_timer'):
                max_fear = max(max_fear, ghost.fear_timer)
        self.active_effects["Dragon Heart"] = max_fear
        
        # Demon Eye - check if any ghost is confused
        max_confusion = 0
        for ghost in ghosts:
            if hasattr(ghost, 'confusion_timer'):
                max_confusion = max(max_confusion, ghost.confusion_timer)
        self.active_effects["Demon Eye"] = max_confusion
        
        # Angels Halo - check if player is dashing
        if hasattr(player, 'is_dashing') and player.is_dashing:
            self.active_effects["Angels Halo"] = player.dash_timer
        else:
            self.active_effects["Angels Halo"] = 0
    
    def get_active_effect_time(self, ability_name):
        """Get remaining time for an ability effect in frames"""
        return self.active_effects.get(ability_name, 0)
    
    def is_active(self, ability_name):
        """Check if ability effect is currently active"""
        return self.active_effects.get(ability_name, 0) > 0