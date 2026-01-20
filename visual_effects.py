import pygame
import math
import os

class VisualEffect:
    """Base class for visual effects"""
    def __init__(self, x, y, duration):
        self.x = x
        self.y = y
        self.duration = duration
        self.timer = 0
        self.active = True
    
    def update(self):
        self.timer += 1
        if self.timer >= self.duration:
            self.active = False
    
    def draw(self, screen):
        pass


class AbilityActivationEffect(VisualEffect):
    """
    Animated effect when an ability is activated.
    Shows expanding rings and particles centered on screen.
    """
    def __init__(self, x, y, ability_name, color):
        super().__init__(x, y, 60)
        self.ability_name = ability_name
        self.color = color
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.particles = []
        
        # Create particles
        for _ in range(20):
            angle = (360 / 20) * _
            speed = 3
            self.particles.append({
                "angle": angle,
                "speed": speed,
                "distance": 0,
                "size": 5
            })
    
    def update(self):
        super().update()
        for p in self.particles:
            p["distance"] += p["speed"]
            p["size"] = max(1, 5 - (self.timer / 10))
    
    def draw(self, screen):
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2
        progress = self.timer / self.duration
        
        # 1. Rings
        for i in range(3):
            offset = i * 20
            radius = int(30 + (progress * 100) + offset)
            alpha = int(255 * (1 - progress))
            ring_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            pygame.draw.circle(ring_surf, color_with_alpha, (radius, radius), radius, 3)
            screen.blit(ring_surf, (center_x - radius, center_y - radius))
        
        # 2. Particles
        for p in self.particles:
            angle_rad = math.radians(p["angle"])
            px = center_x + math.cos(angle_rad) * p["distance"]
            py = center_y + math.sin(angle_rad) * p["distance"]
            alpha = int(255 * (1 - progress))
            
            part_surf = pygame.Surface((int(p["size"] * 2), int(p["size"] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(part_surf, (*self.color, alpha), (int(p["size"]), int(p["size"])), int(p["size"]))
            screen.blit(part_surf, (px - p["size"], py - p["size"]))
        
        # 3. Text
        if progress < 0.8:
            text_alpha = int(255 * (1 - progress))
            text_surf = self.font.render(self.ability_name, True, self.color)
            text_surf.set_alpha(text_alpha)
            text_rect = text_surf.get_rect(center=(center_x, center_y - 100))
            screen.blit(text_surf, text_rect)


class ItemUseEffect(VisualEffect):
    """
    Shows item image glowing and floating up when used.
    NO ROTATION included to prevent errors.
    """
    def __init__(self, item_id, item_name, screen_width, screen_height):
        super().__init__(screen_width // 2, screen_height // 2, 90)
        self.item_id = item_id
        self.item_name = item_name
        self.screen_w = screen_width
        self.screen_h = screen_height
        
        # Load item image
        self.image = self.load_item_image()
        self.font_title = pygame.font.SysFont("arial", 36, bold=True)
        self.font_sub = pygame.font.SysFont("arial", 20)
        
        # Animation vars
        self.scale = 1.0
        self.glow_intensity = 0
    
    def load_item_image(self):
        """
        Loads the specific item images matching your filenames.
        """
        file_map = {
            1: "item_mirror.png",
            2: "item_hunger.png",
            3: "item_coin.png",
            4: "item_censer.png",
            5: "item_gauntlet.png"
        }
        
        filename = file_map.get(self.item_id, f"item_{self.item_id}.png")
        path = os.path.join("assets", filename)
        
        try:
            if os.path.exists(path):
                img = pygame.image.load(path)
                return pygame.transform.scale(img, (100, 100))
            else:
                raise FileNotFoundError
        except:
            # Fallback
            colors = {
                1: (148, 0, 211), 
                2: (210, 105, 30), 
                3: (255, 223, 0), 
                4: (0, 255, 255), 
                5: (220, 20, 60)
            }
            surf = pygame.Surface((100, 100))
            surf.fill(colors.get(self.item_id, (100, 100, 100)))
            return surf
    
    def update(self):
        super().update()
        progress = self.timer / self.duration
        
        # Pulsing scale (Grow and shrink slightly)
        self.scale = 1.0 + math.sin(progress * math.pi * 4) * 0.2
        
        # Glow pulsing
        self.glow_intensity = abs(math.sin(progress * math.pi * 6)) * 255
        
        # Float upward
        self.y -= 2
    
    def draw(self, screen):
        progress = self.timer / self.duration
        
        # Dark overlay
        overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(150 * (1 - abs(progress - 0.5) * 2))))
        screen.blit(overlay, (0, 0))
        
        # Glow
        for i in range(5):
            glow_size = int(150 + i * 20)
            glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            glow_alpha = int(self.glow_intensity * (1 - i * 0.15))
            pygame.draw.circle(glow_surf, (255, 255, 100, glow_alpha), 
                             (glow_size // 2, glow_size // 2), glow_size // 2)
            screen.blit(glow_surf, (self.x - glow_size // 2, self.y - glow_size // 2))
        
        # Image (Scaled ONLY, NO ROTATION)
        scaled_size = int(100 * self.scale)
        scaled_img = pygame.transform.scale(self.image, (scaled_size, scaled_size))
        
        # Draw directly without pygame.transform.rotate
        img_rect = scaled_img.get_rect(center=(self.x, self.y))
        screen.blit(scaled_img, img_rect)
        
        # Text
        if progress < 0.7:
            text_alpha = int(255 * (1 - progress / 0.7))
            
            title_surf = self.font_title.render("ITEM ACTIVATED", True, (255, 255, 100))
            title_surf.set_alpha(text_alpha)
            title_rect = title_surf.get_rect(center=(self.x, self.y - 120))
            screen.blit(title_surf, title_rect)
            
            name_surf = self.font_sub.render(self.item_name, True, (200, 200, 200))
            name_surf.set_alpha(text_alpha)
            name_rect = name_surf.get_rect(center=(self.x, self.y + 100))
            screen.blit(name_surf, name_rect)


class EffectManager:
    def __init__(self):
        self.effects = []
    
    def add_ability_effect(self, x, y, ability_name, color):
        effect = AbilityActivationEffect(x, y, ability_name, color)
        self.effects.append(effect)
    
    def add_item_effect(self, item_id, item_name, screen_width, screen_height):
        effect = ItemUseEffect(item_id, item_name, screen_width, screen_height)
        self.effects.append(effect)
    
    def update(self):
        self.effects = [e for e in self.effects if e.active]
        for effect in self.effects:
            effect.update()
    
    def draw(self, screen):
        for effect in self.effects:
            effect.draw(screen)
    
    def clear(self):
        self.effects.clear()


# These names must match your asset filenames
ABILITY_COLORS = {
    "Wolf Vein": (192, 192, 192),
    "Dragon Heart": (255, 50, 50),
    "Demon Eye": (148, 0, 211),
    "Angels Halo": (255, 215, 0),
    "John Snow": (200, 240, 255)
}

ITEM_NAMES = {
    1: "Mirror of Vanity",
    2: "Bottomless Hunger",
    3: "The Thief's Coin",
    4: "Censer of Devil",
    5: "Blood Gauntlet"
}