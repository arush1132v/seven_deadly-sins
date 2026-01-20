import pygame
import os
import math

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GREEN = (50, 205, 50)

class EnhancedHUD:
    """
    Enhanced HUD that displays:
    - Lives
    - Coins
    - Abilities with cooldowns
    - ALL 5 shop items with usage indicators
    - Pause button
    """
    
    def __init__(self, get_image_func):
        self.get_image = get_image_func
        self.font_main = pygame.font.SysFont("arial", 20, bold=True)
        self.font_small = pygame.font.SysFont("arial", 16)
        self.font_tiny = pygame.font.SysFont("arial", 14)
        
        # Pause Button Rect (Top Right)
        self.pause_rect = pygame.Rect(700, 10, 80, 30)
        
        # Load ability icons
        self.ability_icons = {}
        self.load_ability_icons()
        
        # Load all 5 item images
        self.item_images = {}
        self.load_item_images()
        
        # Animation timer
        self.anim_timer = 0
    
    def load_ability_icons(self):
        """Load ability icons from assets folder"""
        ability_files = {
            "Wolf Vein": "wolf_vein.png",
            "Dragon Heart": "dragon_heart.png",
            "Demon Eye": "demon_eye.png",
            "Angels Halo": "angels_halo.png",
            "John Snow": "john_snow.png"
        }
        
        for name, filename in ability_files.items():
            path = os.path.join("assets", filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                self.ability_icons[name] = pygame.transform.scale(img, (30, 30))
            except FileNotFoundError:
                surf = pygame.Surface((30, 30))
                colors = {
                    "Wolf Vein": (192, 192, 192),
                    "Dragon Heart": (255, 50, 50),
                    "Demon Eye": (148, 0, 211),
                    "Angels Halo": (255, 215, 0),
                    "John Snow": (200, 240, 255)
                }
                surf.fill(colors.get(name, (100, 100, 100)))
                self.ability_icons[name] = surf
    
    def load_item_images(self):
        """Load all 5 shop item images using specific filenames"""
        # --- UPDATED FILE MAPPING ---
        files = {
            1: "item_mirror.png",
            2: "item_hunger.png",
            3: "item_coin.png",
            4: "item_censer.png",
            5: "item_gauntlet.png"
        }
        # ----------------------------

        for item_id, filename in files.items():
            path = os.path.join("assets", filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                self.item_images[item_id] = pygame.transform.scale(img, (50, 50))
            except FileNotFoundError:
                # Fallback colors if specific image not found
                print(f"HUD Warning: Could not find {filename}")
                colors = {
                    1: (148, 0, 211),   # Purple
                    2: (210, 105, 30),  # Brown
                    3: (255, 223, 0),   # Gold
                    4: (0, 255, 255),   # Cyan
                    5: (220, 20, 60)    # Red
                }
                surf = pygame.Surface((50, 50))
                surf.fill(colors.get(item_id, (100, 100, 100)))
                self.item_images[item_id] = surf

    def draw(self, screen, abilities, owned_items, used_items, lives=3, coins=0, ability_manager=None):
        """
        Enhanced draw method
        """
        self.anim_timer += 1
        
        # --- TOP LEFT: LIVES & COINS ---
        lives_text = self.font_main.render(f"Lives: {lives}", True, RED)
        screen.blit(lives_text, (10, 10))
        
        coins_text = self.font_main.render(f"Coins: {int(coins)}", True, GOLD)
        screen.blit(coins_text, (10, 40))
        
        # --- TOP RIGHT: PAUSE BUTTON ---
        pygame.draw.rect(screen, GRAY, self.pause_rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, self.pause_rect, 2, border_radius=5)
        pause_txt = self.font_small.render("PAUSE", True, WHITE)
        screen.blit(pause_txt, (self.pause_rect.centerx - pause_txt.get_width()//2, 
                                self.pause_rect.centery - pause_txt.get_height()//2))
        
        # --- BOTTOM LEFT: ABILITIES WITH COOLDOWNS ---
        if abilities:
            y_offset = 480
            
            for i, ability_name in enumerate(abilities):
                box_rect = pygame.Rect(10, y_offset + (i * 55), 280, 50)
                
                # Check if on cooldown
                is_ready = True
                cooldown_pct = 0
                if ability_manager:
                    import time
                    now = time.time()
                    last_used = ability_manager.last_used.get(ability_name, 0)
                    cooldown = ability_manager.data[ability_name]["cd"]
                    time_since = now - last_used
                    
                    if time_since < cooldown:
                        is_ready = False
                        cooldown_pct = time_since / cooldown
                
                # Background (darker if on cooldown)
                bg_color = (40, 40, 40) if is_ready else (60, 30, 30)
                pygame.draw.rect(screen, bg_color, box_rect, border_radius=5)
                
                # Border (pulsing if ready)
                if is_ready:
                    pulse = abs(math.sin(self.anim_timer * 0.1))
                    border_alpha = int(100 + pulse * 155)
                    border_surf = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
                    pygame.draw.rect(border_surf, (*GOLD, border_alpha), border_surf.get_rect(), 3, border_radius=5)
                    screen.blit(border_surf, box_rect)
                else:
                    pygame.draw.rect(screen, GRAY, box_rect, 2, border_radius=5)
                
                # Cooldown bar
                if not is_ready:
                    bar_height = 4
                    bar_width = int(box_rect.width * cooldown_pct)
                    bar_rect = pygame.Rect(box_rect.x, box_rect.bottom - bar_height, bar_width, bar_height)
                    pygame.draw.rect(screen, GREEN, bar_rect)
                
                # Icon
                icon = self.ability_icons.get(ability_name)
                if icon:
                    icon_pos = (box_rect.x + 8, box_rect.centery - 15)
                    screen.blit(icon, icon_pos)
                
                # Text
                key_num = i + 1
                ability_txt = self.font_small.render(f"{key_num}. {ability_name}", True, WHITE)
                screen.blit(ability_txt, (box_rect.x + 45, box_rect.centery - ability_txt.get_height()//2))
                
                # Cooldown time remaining
                if not is_ready:
                    time_left = cooldown - time_since
                    cd_text = self.font_tiny.render(f"{time_left:.1f}s", True, RED)
                    screen.blit(cd_text, (box_rect.right - cd_text.get_width() - 5, box_rect.centery - 6))
        
        # --- BOTTOM RIGHT: ALL 5 SHOP ITEMS ---
        self.draw_shop_items_panel(screen, owned_items, used_items)
    
    def draw_shop_items_panel(self, screen, owned_items, used_items):
        """
        Draws ALL 5 shop items in bottom right.
        Shows which are owned, which are used, and which are available.
        """
        panel_x = 460
        panel_y = 450
        panel_width = 330
        panel_height = 140
        
        # Panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, (30, 30, 50), panel_rect, border_radius=8)
        pygame.draw.rect(screen, GOLD, panel_rect, 2, border_radius=8)
        
        # Title
        title = self.font_small.render("SHOP ITEMS", True, GOLD)
        screen.blit(title, (panel_x + 10, panel_y + 5))
        
        # Item names (short)
        item_names = {
            1: "Mirror",
            2: "Hunger",
            3: "Coin",
            4: "Censer",
            5: "Gauntlet"
        }
        
        # Draw 5 items in a row
        start_x = panel_x + 15
        start_y = panel_y + 35
        gap = 60
        
        for i, item_id in enumerate([1, 2, 3, 4, 5]):
            x = start_x + (i * gap)
            y = start_y
            
            is_owned = item_id in owned_items
            is_used = item_id in used_items
            
            # Item box
            box_rect = pygame.Rect(x, y, 55, 90)
            
            # Background color based on state
            if is_used:
                bg_color = (20, 20, 20)  # Dark - already used
            elif is_owned:
                bg_color = (40, 60, 40)  # Green tint - available
                # Pulsing effect for available items
                pulse = abs(math.sin(self.anim_timer * 0.08))
                glow_alpha = int(50 + pulse * 100)
                glow_surf = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (50, 255, 50, glow_alpha), glow_surf.get_rect(), border_radius=5)
                screen.blit(glow_surf, box_rect)
            else:
                bg_color = (60, 60, 60)  # Gray - not owned
            
            pygame.draw.rect(screen, bg_color, box_rect, border_radius=5)
            
            # Border
            if is_used:
                border_color = RED
            elif is_owned:
                border_color = GREEN
            else:
                border_color = DARK_GRAY
            
            pygame.draw.rect(screen, border_color, box_rect, 2, border_radius=5)
            
            # Item image
            item_img = self.item_images.get(item_id)
            if item_img:
                img_scaled = pygame.transform.scale(item_img, (40, 40))
                # Darken if used
                if is_used:
                    img_scaled = img_scaled.copy()
                    dark_overlay = pygame.Surface((40, 40), pygame.SRCALPHA)
                    dark_overlay.fill((0, 0, 0, 180))
                    img_scaled.blit(dark_overlay, (0, 0))
                
                screen.blit(img_scaled, (x + 7, y + 5))
            
            # Status indicator
            if is_used:
                status_txt = self.font_tiny.render("USED", True, RED)
            elif is_owned:
                # Show key binding (Q for first owned, E for second)
                owned_list = [id for id in owned_items if id not in used_items]
                if item_id in owned_list:
                    idx = owned_list.index(item_id)
                    if idx == 0:
                        status_txt = self.font_tiny.render("Q", True, GOLD)
                    elif idx == 1:
                        status_txt = self.font_tiny.render("E", True, GOLD)
                    else:
                        status_txt = self.font_tiny.render("OK", True, GREEN)
                else:
                    status_txt = self.font_tiny.render("OK", True, GREEN)
            else:
                status_txt = self.font_tiny.render("---", True, GRAY)
            
            screen.blit(status_txt, (x + 27 - status_txt.get_width()//2, y + 48))
            
            # Item name
            name_txt = self.font_tiny.render(item_names[item_id], True, WHITE)
            screen.blit(name_txt, (x + 27 - name_txt.get_width()//2, y + 65))
    
    def is_pause_clicked(self, mouse_pos):
        """Check if the pause button was clicked"""
        return self.pause_rect.collidepoint(mouse_pos)