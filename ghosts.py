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
    def __init__(self, x, y, name, color, img_file):
        super().__init__()
        self.name = name
        self.color = color  # Store color for name label
        self.image = load_ghost_img(img_file, color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = [float(x), float(y)]
        self.speed = BASE_SPEED
        self.state = "CHASE" 
        
        # --- STATUS EFFECTS ---
        self.sleep_timer = 0          # Stunned/Asleep (Envy/Wrath effect)
        self.speed_penalty_timer = 0  # Slowed down (Sloth effect)
        self.fear_timer = 0           # Dragon Heart effect (50% speed)
        self.confusion_timer = 0      # Demon Eye effect (attack other ghosts)
        
        # --- NAME LABEL ---
        self.font = pygame.font.SysFont("arial", 12, bold=True)
        self.name_surface = self.font.render(self.name, True, (255, 255, 255))
        self.name_bg = pygame.Surface((self.name_surface.get_width() + 6, self.name_surface.get_height() + 4), pygame.SRCALPHA)
        self.name_bg.fill((0, 0, 0, 180))  # Semi-transparent black background
        
        # Status indicator font
        self.status_font = pygame.font.SysFont("arial", 10, bold=True)

    def apply_status(self, status_type, duration):
        """Apply a status effect to this ghost"""
        if status_type == "fear":
            self.fear_timer = duration
            print(f"  {self.name} is now FEARED for {duration/60:.1f}s")
        elif status_type == "confusion":
            self.confusion_timer = duration
            print(f"  {self.name} is now CONFUSED for {duration/60:.1f}s")

    def update_status_effects(self):
        """
        Decrements timers and returns current state modifiers.
        Returns: dict with 'speed' multiplier and 'target_override'
        """
        modifiers = {"speed": 1.0, "target_override": None}
        
        # Handle Fear (50% Speed Decrease)
        if self.fear_timer > 0:
            self.fear_timer -= 1
            modifiers["speed"] *= 0.5 
            
        # Handle Confusion (Target other ghosts)
        if self.confusion_timer > 0:
            self.confusion_timer -= 1
            modifiers["target_override"] = "GHOSTS"
            
        return modifiers

    def get_distance(self, target):
        return math.hypot(target.rect.centerx - self.rect.centerx, 
                          target.rect.centery - self.rect.centery)

    def move_towards(self, target_rect, speed_mod=1.0):
        """Move towards a target with optional speed modifier"""
        # Calculate Direction
        dx = target_rect.centerx - self.rect.centerx
        dy = target_rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        
        if dist != 0:
            dx, dy = dx / dist, dy / dist 
            
            # Calculate Speed
            current_speed = self.speed * speed_mod
            
            # Apply Sloth's Speed Curse (0.25x speed if cursed)
            if self.speed_penalty_timer > 0:
                current_speed *= 0.25
                self.speed_penalty_timer -= 1
            
            # Move
            self.pos[0] += dx * current_speed
            self.pos[1] += dy * current_speed
            self.rect.x = int(self.pos[0])
            self.rect.y = int(self.pos[1])

    def update_with_ai(self, player, all_ghosts):
        """
        Standard AI update that handles status effects.
        Call this from child class update() methods.
        """
        if not self.check_status(): 
            return False  # Ghost is stunned
        
        # Get status effect modifiers
        mods = self.update_status_effects()
        target_rect = player.rect
        
        # CONFUSION LOGIC: Target other ghosts instead of player
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
                # No other ghosts - just stop moving
                return False
        
        # Execute Movement with fear modifier
        self.move_towards(target_rect, speed_mod=mods["speed"])
        return True

    def check_status(self):
        """Checks if ghost is asleep/stunned. Returns True if acting normally."""
        if self.sleep_timer > 0:
            self.sleep_timer -= 1
            return False # Ghost is stunned, cannot move
        return True

    def handle_catch(self):
        return "KILL"

    def draw_name(self, surface, camera):
        """Draw ghost name above their head"""
        # Calculate screen position
        screen_x = self.rect.centerx + camera.camera.x
        screen_y = self.rect.top + camera.camera.y - 18
        
        # Draw background
        bg_rect = self.name_bg.get_rect(center=(screen_x, screen_y))
        surface.blit(self.name_bg, bg_rect)
        
        # Draw name text
        text_rect = self.name_surface.get_rect(center=(screen_x, screen_y))
        surface.blit(self.name_surface, text_rect)
        
        # Draw status indicators
        self.draw_status_icons(surface, camera)
    
    def draw_status_icons(self, surface, camera):
        """Draw icons for active status effects"""
        screen_x = self.rect.centerx + camera.camera.x
        screen_y = self.rect.bottom + camera.camera.y + 5
        offset = 0
        
        # Fear indicator (red skull)
        if self.fear_timer > 0:
            fear_text = self.status_font.render("😱", True, (255, 0, 0))
            surface.blit(fear_text, (screen_x - 15 + offset, screen_y))
            offset += 15
        
        # Confusion indicator (purple swirl)
        if self.confusion_timer > 0:
            conf_text = self.status_font.render("😵", True, (148, 0, 211))
            surface.blit(conf_text, (screen_x - 15 + offset, screen_y))
            offset += 15
        
        # Sleep indicator (zzz)
        if self.sleep_timer > 0:
            sleep_text = self.status_font.render("💤", True, (100, 100, 255))
            surface.blit(sleep_text, (screen_x - 15 + offset, screen_y))
            offset += 15
        
        # Slow indicator (snowflake)
        if self.speed_penalty_timer > 0:
            slow_text = self.status_font.render("❄️", True, (0, 255, 255))
            surface.blit(slow_text, (screen_x - 15 + offset, screen_y))

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
        
        # Pride is immune to Sloth's speed curse
        self.speed_penalty_timer = 0
        
        # Use AI with status effects
        self.update_with_ai(player, all_ghosts)

    def handle_catch(self):
        if self.mercy_lives > 0:
            self.mercy_lives -= 1
            print(f"Pride showed mercy! {self.mercy_lives} mercies left")
            return "SPARE"
        else:
            return "KILL"

    def kill(self):
        pass # Cannot be killed

# ==========================================
# 2. GREED (The Merchant & Assassin)
# ==========================================
# Replace the GreedGhost class in ghosts.py with this updated version:

class GreedGhost(BaseGhost):
    def __init__(self, x, y):
        super().__init__(x, y, "Greed", (255, 215, 0), "ghost_greed.png")
        self.speed = BASE_SPEED * 1.0
        self.cost_spare = 100
        self.cost_kill_service = 200
        self.hunter_mode = False
        self.hunter_timer = 0
        self.target_ghost = None  # Specific ghost to hunt
        self.cooldown_timer = 0
        self.trade_active = False
        self.trade_proximity = 80
        self.passive_timer = 0  # Timer for being passive after trade

    def update(self, player, all_ghosts):
        if not self.check_status(): 
            return 

        # If in passive mode (after trade), don't attack player
        if self.passive_timer > 0:
            self.passive_timer -= 1
            # Just wander around slowly, don't chase player
            if self.passive_timer % 60 == 0:  # Change direction every second
                import random
                self.pos[0] += random.choice([-2, 0, 2])
                self.pos[1] += random.choice([-2, 0, 2])
                self.rect.x = int(self.pos[0])
                self.rect.y = int(self.pos[1])
            return

        # Check if close enough for trade
        dist_to_player = self.get_distance(player)
        if dist_to_player < self.trade_proximity and self.cooldown_timer == 0:
            self.trade_active = True
        else:
            self.trade_active = False

        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
            return 

        if self.hunter_mode:
            self.hunter_timer -= 1
            if self.hunter_timer <= 0:
                self.hunter_mode = False
                self.target_ghost = None
                print("Greed's assassination contract expired!")
            else:
                # Check if target still exists
                if self.target_ghost and self.target_ghost in all_ghosts:
                    # Move toward target
                    self.move_towards(self.target_ghost.rect, speed_mod=1.5)  # 50% faster when hunting
                    
                    # Kill target on contact
                    if self.rect.colliderect(self.target_ghost.rect):
                        self.target_ghost.kill()
                        print(f"💀 Greed assassinated {self.target_ghost.name}!")
                        self.hunter_mode = False
                        self.target_ghost = None
                        self.cooldown_timer = 180  # 3 second cooldown after successful kill
                        return
                else:
                    # Target was killed by something else or doesn't exist
                    print("Target lost! Greed is searching...")
                    self.hunter_mode = False
                    self.target_ghost = None
                    self.move_towards(player.rect)
                return

        # Normal behavior - use AI with status effects
        self.update_with_ai(player, all_ghosts)

    def handle_catch(self):
        # Don't kill player if in passive mode
        if self.passive_timer > 0:
            return "SPARE"
        return "GREED_EVENT"

    def pay_for_mercy(self):
        """Player pays to make Greed leave them alone temporarily"""
        self.cost_spare += 50 
        self.cooldown_timer = 180 
        self.trade_active = False
        self.passive_timer = 600  # 10 seconds of not hunting player
        print(f"Greed will leave you alone for 10 seconds!")
        print(f"Greed's next mercy price: {self.cost_spare} coins")

    def pay_for_service(self, target_ghost):
        """Player pays to make Greed hunt a specific ghost"""
        self.hunter_mode = True
        self.target_ghost = target_ghost
        self.hunter_timer = 600  # 10 seconds to complete the kill
        self.cooldown_timer = 60  # 1 second before can trade again
        self.trade_active = False
        self.passive_timer = 600  # 10 seconds of not hunting player
        print(f"🎯 Greed is now hunting {target_ghost.name}!")
        print(f"Greed will leave you alone for 10 seconds!")

# ==========================================
# 3. LUST (Relentless Pursuer)
# ==========================================
class LustGhost(BaseGhost):
    def __init__(self, x, y):
        super().__init__(x, y, "Lust", (255, 105, 180), "ghost_lust.png")
        self.speed = BASE_SPEED * 0.75 

    def update(self, player, all_ghosts):
        # Use AI with status effects
        self.update_with_ai(player, all_ghosts)

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
                                print(f"Envy killed {ghost.name}!")
                            elif roll < 0.35: 
                                ghost.sleep_timer = 600
                                print(f"Envy put {ghost.name} to sleep!")

        # Use AI with status effects
        self.update_with_ai(player, all_ghosts)

# ==========================================
# 5. GLUTTONY (Hungry)
# ==========================================
class GluttonyGhost(BaseGhost):
    def __init__(self, x, y):
        super().__init__(x, y, "Gluttony", (255, 140, 0), "ghost_gluttony.png")

    def update(self, player, all_ghosts):
        # Use AI with status effects
        self.update_with_ai(player, all_ghosts)

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
                        print(f"Wrath knocked out {ghost.name}!")

        # Random erratic movement
        if random.random() < 0.25: 
            self.pos[0] += random.choice([-5, 5])
            self.pos[1] += random.choice([-5, 5])
            self.rect.x = int(self.pos[0])
            self.rect.y = int(self.pos[1])
            return 

        # Get status modifiers
        mods = self.update_status_effects()
        
        # Move with both wrath speed and status modifiers
        self.move_towards(player.rect, speed_mod * mods["speed"])

# ==========================================
# 7. SLOTH (The Lazy Curse)
# ==========================================
class SlothGhost(BaseGhost):
    def __init__(self, x, y):
        super().__init__(x, y, "Sloth", (0, 255, 255), "ghost_sloth.png")
        self.wake_range = 200 
        self.curse_cooldown = 0

    def update(self, player, all_ghosts):
        if not self.check_status(): return

        dist = self.get_distance(player)
        
        # Sleep if out of range
        if dist > self.wake_range:
            return 
            
        # Curse Logic
        if self.curse_cooldown > 0:
            self.curse_cooldown -= 1
        else:
            self.curse_cooldown = 400
            
            # Curse Player
            player.sloth_penalty_timer = 300 
            print("Sloth Cursed the Player! (0.25x Speed)")
            
            # Curse 2 Random Ghosts
            valid_targets = [g for g in all_ghosts if g != self and g.name != "Pride"]
            
            if len(valid_targets) >= 2:
                victims = random.sample(valid_targets, 2)
                for v in victims:
                    v.speed_penalty_timer = 300
                    print(f"Sloth Cursed {v.name}! (0.25x Speed)")
            elif len(valid_targets) == 1:
                valid_targets[0].speed_penalty_timer = 300
                print(f"Sloth Cursed {valid_targets[0].name}!")

        # Use AI with status effects
        self.update_with_ai(player, all_ghosts)

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