import pygame
import sys
import os

# --- CONFIGURATION ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0) # Black background for shop
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 149, 237)
BUTTON_HOVER_COLOR = (30, 144, 255)
DISABLED_COLOR = (80, 80, 80)
GOLD_COLOR = (255, 215, 0)

# Default Red Background for most icons
DEFAULT_ICON_BG = (200, 0, 0) 

# --- FONTS ---
pygame.font.init()
try:
    font_header = pygame.font.SysFont("arial", 40, bold=True)
    font_sub = pygame.font.SysFont("arial", 24, bold=True)
    font_desc = pygame.font.SysFont("arial", 16)
except:
    font_header = pygame.font.Font(None, 40)
    font_sub = pygame.font.Font(None, 24)
    font_desc = pygame.font.Font(None, 16)

# --- LOAD ASSETS ---
def load_asset(name, size=None):
    path = os.path.join("assets", name)
    try:
        img = pygame.image.load(path)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except FileNotFoundError:
        print(f"ERROR: Could not find {name} at {path}")
        surf = pygame.Surface(size if size else (60, 60))
        surf.fill((200, 50, 50))
        return surf

# --- ITEM IMAGES ---
ITEM_IMAGES = {
    1: load_asset("item_mirror.png", (60, 60)),
    2: load_asset("item_hunger.png", (60, 60)),
    3: load_asset("item_coin.png", (60, 60)),
    4: load_asset("item_censer.png", (60, 60)),   
    5: load_asset("item_gauntlet.png", (60, 60))
}

# --- SHOP DATA ---
# I added a specific 'icon_bg' color for the 4th and 5th items
SHOP_ITEMS = [
    {
        "id": 1, 
        "name": "Mirror of Vanity", 
        "cost": 100, 
        "desc": "Clones Pride to stop ghosts (15s).", 
        "color": (148, 0, 211),
        "icon_bg": DEFAULT_ICON_BG # Red
    },
    {
        "id": 2, 
        "name": "Bottomless Hunger", 
        "cost": 40, 
        "desc": "Coin value +0.25x.", 
        "color": (210, 105, 30),
        "icon_bg": DEFAULT_ICON_BG # Red
    },
    {
        "id": 3, 
        "name": "The Thief's Coin", 
        "cost": 80, 
        "desc": "Steals 25% of Greed's coins.", 
        "color": (255, 223, 0),
        "icon_bg": DEFAULT_ICON_BG # Red
    },
    {
        "id": 4, 
        "name": "Censer of Devil", 
        "cost": 50, 
        "desc": "Stops all ghosts for 2 sec.", 
        "color": (0, 255, 255),
        "icon_bg": (0, 0, 0) # <--- BLACK BACKGROUND (4th Item)
    },
    {
        "id": 5, 
        "name": "Blood Gauntlet", 
        "cost": 100, 
        "desc": "+10% Player Boost for 5 sec.", 
        "color": (220, 20, 60),
        "icon_bg": (255, 255, 255) # <--- WHITE BACKGROUND (5th Item)
    }
]

def draw_button(surface, text, x, y, w, h, active=True):
    mouse_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)
    
    is_hovered = rect.collidepoint(mouse_pos)
    
    if not active:
        color = DISABLED_COLOR
    else:
        color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
        
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, (255,255,255), rect, 2, border_radius=8)
    
    txt_surf = font_sub.render(text, True, TEXT_COLOR)
    surface.blit(txt_surf, (x + (w - txt_surf.get_width())//2, y + (h - txt_surf.get_height())//2))
    
    return active and is_hovered and pygame.mouse.get_pressed()[0]

def shop_screen(screen, player_points, inventory):
    clock = pygame.time.Clock()
    running = True
    
    click_cooldown = 0
    
    while running:
        screen.fill(BACKGROUND_COLOR)
        
        # Header
        title = font_header.render(f"SHOP - Points: {player_points}", True, GOLD_COLOR)
        screen.blit(title, (50, 30))
        
        # Back Button
        if draw_button(screen, "BACK", 600, 30, 150, 50):
            return player_points, inventory
            
        # Draw Items List
        start_y = 100
        for i, item in enumerate(SHOP_ITEMS):
            y_pos = start_y + (i * 90)
            
            # 1. Icon Background (Custom Colors)
            bg_color = item['icon_bg']
            pygame.draw.rect(screen, bg_color, (100, y_pos, 60, 60))
            
            # 2. Icon Image
            icon_img = ITEM_IMAGES.get(item['id'])
            if icon_img:
                screen.blit(icon_img, (100, y_pos))
            
            # Border (using item's theme color)
            pygame.draw.rect(screen, item['color'], (100, y_pos, 60, 60), 2)
            
            # 3. Text Info
            name_surf = font_sub.render(f"{item['name']}", True, item['color'])
            screen.blit(name_surf, (180, y_pos + 5))
            
            desc_surf = font_desc.render(item['desc'], True, (200, 200, 200))
            screen.blit(desc_surf, (180, y_pos + 35))
            
            # 4. Buy Button
            already_owned = item['id'] in inventory
            can_afford = player_points >= item['cost']
            
            btn_x = 600
            btn_w = 150
            btn_h = 50
            
            if already_owned:
                draw_button(screen, "OWNED", btn_x, y_pos + 5, btn_w, btn_h, active=False)
            elif not can_afford:
                draw_button(screen, f"{item['cost']} Pts", btn_x, y_pos + 5, btn_w, btn_h, active=False)
            else:
                if draw_button(screen, f"BUY {item['cost']}", btn_x, y_pos + 5, btn_w, btn_h, active=True):
                    if click_cooldown == 0:
                        player_points -= item['cost']
                        inventory.append(item['id'])
                        click_cooldown = 20 # Prevent double buy
        
        if click_cooldown > 0:
            click_cooldown -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.flip()
        clock.tick(60)