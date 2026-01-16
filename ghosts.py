import pygame
import math
import random
import os

# --- CONFIGURATION ---
BASE_SPEED = 2.0  # Base speed for reference
TILE_SIZE = 30    # Size of the ghost

def load_ghost_img(name, color):
    """Helper to load image or return colored block if missing"""
    path = os.path.join("assets", name)
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    except FileNotFoundError:
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surf.fill(color)
        return surf

# ==========================================
# PARENT CLASS
# ==========================================
class BaseGhost(pygame.sprite.Sprite):
    # Inside BaseGhost class in ghosts.py

    def __init__(self, x, y, name, color, img_file):
        super().__init__()
        # ... existing init code ...
        
        # NEW: Status Effect Timers
        self.fear_timer = 0      # Dragon Heart effect
        self.confusion_timer = 0 # Demon Eye effect

    def apply_status(self, status_type, duration):
        if status_type == "fear":
            self.fear_timer = duration
        elif status_type == "confusion":
            self.confusion_timer = duration

    def update_status_effects(self):
        """Decrements timers and returns current state modifiers."""
        modifiers = {"speed": 1.0, "target_override": None}
        
        # [cite_start]Handle Fear (50% Stats Decrease) [cite: 17]
        if self.fear_timer > 0:
            self.fear_timer -= 1
            modifiers["speed"] *= 0.5 
            
        # [cite_start]Handle Confusion (Target other ghosts) [cite: 17]
        if self.confusion_timer > 0:
            self.confusion_timer -= 1
            modifiers["target_override"] = "GHOSTS"
            
        return modifiers

    # UPDATE your existing move_towards or update method to use these modifiers:
    def update_ai_logic(self, player, all_ghosts):
        """Call this in your specific ghost update methods."""
        
        mods = self.update_status_effects()
        
        target_rect = player.rect
        
        # CONFUSION LOGIC: Find a ghost to attack instead of player
        if mods["target_override"] == "GHOSTS":
            nearest_victim = None
            min_dist = 9999
            for other in all_ghosts:
                if other != self:
                    d = self.get_distance(other)
                    if d < min_dist:
                        min_dist = d
                        nearest_victim = other
            
            if nearest_victim:
                target_rect = nearest_victim.rect
            else:
                # [cite_start]If no other ghosts exist, just stop moving (Stun) [cite: 17]
                return 

        # Execute Movement
        self.move_towards(target_rect, speed_mod=mods["speed"])
    def __init__(self, x, y, name, color, img_file):
        super().__init__()
        self.name = name
        self.image = load_ghost_img(img_file, color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = [float(x), float(y)]
        self.speed = BASE_SPEED
        self.state = "CHASE" 
        
        # --- STATUS EFFECTS ---
        self.sleep_timer = 0          # Stunned/Asleep (Envy/Wrath effect)
        self.speed_penalty_timer = 0  # Slowed down (Sloth effect)
        
    def get_distance(self, target):
        return math.hypot(target.rect.centerx - self.rect.centerx, 
                          target.rect.centery - self.rect.centery)

    def move_towards(self, target_rect, speed_mod=1.0):
        # 1. Calculate Direction
        dx = target_rect.centerx - self.rect.centerx
        dy = target_rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        
        if dist != 0:
            dx, dy = dx / dist, dy / dist 
            
            # 2. Calculate Speed
            current_speed = self.speed * speed_mod
            
            # Apply Sloth's Speed Curse (0.25x speed if cursed)
            if self.speed_penalty_timer > 0:
                current_speed *= 0.25
                self.speed_penalty_timer -= 1
            
            # 3. Move
            self.pos[0] += dx * current_speed
            self.pos[1] += dy * current_speed
            self.rect.x = int(self.pos[0])
            self.rect.y = int(self.pos[1])

    def check_status(self):
        """Checks if ghost is asleep/stunned. Returns True if acting normally."""
        if self.sleep_timer > 0:
            self.sleep_timer -= 1
            return False # Ghost is stunned, cannot move
        return True

    def handle_catch(self):
        return "KILL"

    def kill(self):
        super().kill()

# ==========================================
# 1. PRIDE (Invincible & Merciful)
# ==========================================
class PrideGhost(BaseGhost):
    def __init__(self, x, y):
        super().__init__(x, y, "Pride", (148, 0, 211), "ghost_pride.png")
        self.speed = BASE_SPEED * 1.5 
        self.mercy_lives = 3 

    def update(self, player, all_ghosts):
        if not self.check_status(): return
        # Pride is immune to Sloth's speed curse, so we manually reset it if applied
        self.speed_penalty_timer = 0 
        self.move_towards(player.rect)

    def handle_catch(self):
        if self.mercy_lives > 0:
            self.mercy_lives -= 1
            return "SPARE"
        else:
            return "KILL"

    def kill(self):
        pass # Cannot be killed

# ==========================================
# 2. GREED (The Merchant & Assassin)
# ==========================================
class GreedGhost(BaseGhost):
    def __init__(self, x, y):
        super().__init__(x, y, "Greed", (255, 215, 0), "ghost_greed.png")
        self.speed = BASE_SPEED * 1.0
        self.cost_spare = 100
        self.cost_kill_service = 200
        self.hunter_mode = False
        self.hunter_timer = 0
        self.cooldown_timer = 0

    def update(self, player, all_ghosts):
        if not self.check_status(): return 

        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
            return 

        if self.hunter_mode:
            self.hunter_timer -= 1
            if self.hunter_timer <= 0:
                self.hunter_mode = False 
            else:
                target_ghost = None
                min_dist = 9999
                for ghost in all_ghosts:
                    if ghost != self and ghost.name != "Pride":
                        d = self.get_distance(ghost)
                        if d < min_dist:
                            min_dist = d
                            target_ghost = ghost
                
                if target_ghost:
                    self.move_towards(target_ghost.rect)
                else:
                    self.move_towards(player.rect) 
                return

        self.move_towards(player.rect)

    def handle_catch(self):
        return "GREED_EVENT"

    def pay_for_mercy(self):
        self.cost_spare += 50 
        self.cooldown_timer = 180 

    def pay_for_service(self):
        self.hunter_mode = True
        self.hunter_timer = 600 
        self.cooldown_timer = 60 

# ==========================================
# 3. LUST (Relentless Pursuer)
# ==========================================
class LustGhost(BaseGhost):
    def __init__(self, x, y):
        super().__init__(x, y, "Lust", (255, 105, 180), "ghost_lust.png")
        self.speed = BASE_SPEED * 0.75 

    def update(self, player, all_ghosts):
        if not self.check_status(): return
        self.move_towards(player.rect)

# ==========================================
# 4. ENVY (The Betrayer)
# ==========================================
class EnvyGhost(BaseGhost):
    def __init__(self, x, y):
        super().__init__(x, y, "Envy", (0, 255, 0), "ghost_envy.png")
        self.betrayal_cooldown = 0

    def update(self, player, all_ghosts):
        if not self.check_status(): return

        if self.betrayal_cooldown > 0:
            self.betrayal_cooldown -= 1
        else:
            self.betrayal_cooldown = 60 
            for ghost in all_ghosts:
                if ghost != self:
                    dist_to_player = ghost.get_distance(player)
                    if dist_to_player < 200:
                        if ghost.name == "Pride":
                            if random.random() < 0.25:
                                print("Envy tried to betray Pride and DIED!")
                                self.kill() 
                                return 
                        else:
                            roll = random.random()
                            if roll < 0.10:
                                ghost.kill()
                            elif roll < 0.35: 
                                ghost.sleep_timer = 600 

        self.move_towards(player.rect)

# ==========================================
# 5. GLUTTONY (Hungry)
# ==========================================
class GluttonyGhost(BaseGhost):
    def __init__(self, x, y):
        super().__init__(x, y, "Gluttony", (255, 140, 0), "ghost_gluttony.png")

    def update(self, player, all_ghosts):
        if not self.check_status(): return
        self.move_towards(player.rect)

# ==========================================
# 6. WRATH (The Berserker)
# ==========================================
class WrathGhost(BaseGhost):
    def __init__(self, x, y):
        super().__init__(x, y, "Wrath", (220, 20, 60), "ghost_wrath.png")

    def update(self, player, all_ghosts):
        if not self.check_status(): return

        dx = abs(player.rect.centerx - self.rect.centerx)
        dy = abs(player.rect.centery - self.rect.centery)
        speed_mod = 1.0
        charging = False
        
        if dx < 20 or dy < 20: 
            speed_mod = 1.1 
            charging = True

        if charging:
            for ghost in all_ghosts:
                if ghost != self and ghost.name != "Pride":
                    if self.rect.colliderect(ghost.rect):
                        ghost.sleep_timer = 600 

        if random.random() < 0.25: 
            self.pos[0] += random.choice([-5, 5])
            self.pos[1] += random.choice([-5, 5])
            self.rect.x = int(self.pos[0])
            self.rect.y = int(self.pos[1])
            return 

        self.move_towards(player.rect, speed_mod)

# ==========================================
# 7. SLOTH (The Lazy Curse)
# ==========================================
class SlothGhost(BaseGhost):
    def __init__(self, x, y):
        super().__init__(x, y, "Sloth", (0, 255, 255), "ghost_sloth.png")
        self.wake_range = 200 
        self.curse_cooldown = 0 # Timer to prevent constant cursing

    def update(self, player, all_ghosts):
        if not self.check_status(): return

        dist = self.get_distance(player)
        
        # 1. Sleep if out of range
        if dist > self.wake_range:
            return 
            
        # 2. Curse Logic (When in range)
        if self.curse_cooldown > 0:
            self.curse_cooldown -= 1
        else:
            # Trigger Curse!
            self.curse_cooldown = 400 # Cooldown ~6.5 seconds
            
            # A. Curse Player (We set a flag on the player object)
            # 5 seconds * 60 fps = 300 frames
            player.sloth_penalty_timer = 300 
            print("Sloth Cursed the Player! (0.25x Speed)")
            
            # B. Curse 2 Random Ghosts
            # Filter valid targets (Not Self, Not Pride)
            valid_targets = [g for g in all_ghosts if g != self and g.name != "Pride"]
            
            if len(valid_targets) >= 2:
                victims = random.sample(valid_targets, 2)
                for v in victims:
                    v.speed_penalty_timer = 300
                    print(f"Sloth Cursed {v.name}! (0.25x Speed)")
            elif len(valid_targets) == 1:
                valid_targets[0].speed_penalty_timer = 300

        # 3. Move towards player (Normal Speed)
        self.move_towards(player.rect)

# ==========================================
# FACTORY
# ==========================================
def spawn_ghosts(start_x, start_y):
    ghosts = pygame.sprite.Group()
    ghosts.add(PrideGhost(start_x, start_y))
    ghosts.add(GreedGhost(start_x + 30, start_y))
    ghosts.add(LustGhost(start_x - 30, start_y))
    ghosts.add(EnvyGhost(start_x, start_y + 30))
    ghosts.add(GluttonyGhost(start_x + 30, start_y + 30))
    ghosts.add(WrathGhost(start_x - 30, start_y + 30))
    ghosts.add(SlothGhost(start_x, start_y + 60))
    return ghosts