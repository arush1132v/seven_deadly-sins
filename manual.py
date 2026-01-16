import pygame
import sys

# --- CONFIGURATION ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (20, 20, 40)
TEXT_COLOR = (255, 255, 255)
HEADER_COLOR = (255, 215, 0) # Gold
TAB_COLOR = (100, 149, 237)
TAB_ACTIVE_COLOR = (50, 205, 50)
SCROLL_SPEED = 20

pygame.font.init()
try:
    FONT_PATH = "pixel_font.ttf"
    font_title = pygame.font.Font(FONT_PATH, 40)
    font_tab = pygame.font.Font(FONT_PATH, 24)
    font_text = pygame.font.Font(FONT_PATH, 16)
except FileNotFoundError:
    font_title = pygame.font.SysFont("arial", 40, bold=True)
    font_tab = pygame.font.SysFont("arial", 24, bold=True)
    font_text = pygame.font.SysFont("arial", 18)

# --- DATA ---
GHOST_DATA = [
    {"name": "PRIDE", "desc": "The Strongest. 1.5x Speed. Cannot be harmed by items. Gives you 3 chances (4 total lives). Drop: Unkillable."},
    {"name": "GREED", "desc": "Normal Speed. Can be bribed with coins to leave you alone or kill other ghosts. Drop: Steals 5% stats of any ghost."},
    {"name": "LUST", "desc": "0.75x Speed. Relentless pursuit. Drop: Hypnotizes ghost to protect you for 45s."},
    {"name": "ENVY", "desc": "Betrays other ghosts (25% chance to sleep them, 10% to kill). Drop: Makes 2 nearest ghosts fight."},
    {"name": "WRATH", "desc": "1.1x Speed in straight lines. Erratic turns. Drop: Curses ghost to fight others for 45s."},
    {"name": "SLOTH", "desc": "Lazy until close. Curses player speed (0.25x). Drop: Puts 1 ghost to permanent sleep (wakes on touch)."},
    {"name": "GLUTTONY", "desc": "Standard behavior. Drop: (Standard points)."}
]

ABILITY_DATA = [
    {"name": "1. WOLF VEIN", "desc": "10% speed boost for 5 sec. (Recharge: 15s)"},
    {"name": "2. DRAGON HEART", "desc": "Curse of fear on nearest ghost for 3 sec. (Recharge: 15s)"},
    {"name": "3. DEMON EYE", "desc": "Confuses nearest ghost to target others for 5 sec. (Recharge: 20s)"},
    {"name": "4. ANGEL'S HALO", "desc": "Dash in 1 direction. Invincible during dash."},
    {"name": "5. JOHN SNOW", "desc": "Passive: +3% stats increase after every death."}
]

ITEM_DATA = [
    "-- SHOP ITEMS (One use per game) --",
    {"name": "Mirror of Vanity (Pride)", "desc": "Clones Pride to stop ghosts for 15s. (100 Pts)"},
    {"name": "Bottomless Hunger (Gluttony)", "desc": "Coin value +0.25x. (40 Pts)"},
    {"name": "Thief's Coin (Greed)", "desc": "Steals 25% of Greed's coins. (80 Pts)"},
    {"name": "Censer of Devil (Sloth)", "desc": "Stops all ghosts for 2 sec. (50 Pts)"},
    {"name": "Blood Gauntlet (Wrath)", "desc": "+10% Player Boost for 5 sec. (100 Pts)"},
    "",
    "-- MAP ITEMS --",
    {"name": "Prideful Crown", "desc": "Invincibility for 10s. Cannot eat ghosts."},
    {"name": "Boots of the Envious", "desc": "Permanent +10% Speed."},
    {"name": "Glutton's Belly", "desc": "Magnetizes all coins in row/column."},
    {"name": "Sloth's Tranquilizer", "desc": "Global Slowdown (50%) for 15s."},
    {"name": "Greed's Double-Down", "desc": "2x Coins for 30s."}
]

def draw_text_wrapped(surface, text, font, color, rect):
    y = rect.top
    line_spacing = 2
    font_height = font.size("Tg")[1]
    words = text.split(' ')
    space_width = font.size(' ')[0]
    
    current_line = []
    current_width = 0
    
    for word in words:
        word_surface = font.render(word, True, color)
        word_width = word_surface.get_width()
        if current_width + word_width >= rect.width:
            x = rect.left
            for w_surf in current_line:
                surface.blit(w_surf, (x, y))
                x += w_surf.get_width() + space_width
            y += font_height + line_spacing
            current_line = []
            current_width = 0
        current_line.append(word_surface)
        current_width += word_width

    x = rect.left
    for w_surf in current_line:
        surface.blit(w_surf, (x, y))
        x += w_surf.get_width() + space_width
    return y + font_height

def generate_content_surface(category, width=700):
    """
    Creates a tall Surface containing all the text for the category.
    This allows us to scroll just by moving this surface up and down.
    """
    # 1. Estimate Height (Large buffer)
    temp_height = 2000 
    surf = pygame.Surface((width, temp_height), pygame.SRCALPHA)
    
    current_y = 0
    
    # 2. Draw Content
    if category == "Ghosts":
        for ghost in GHOST_DATA:
            name_surf = font_tab.render(ghost["name"], True, (255, 100, 100))
            surf.blit(name_surf, (0, current_y))
            current_y += 30
            rect = pygame.Rect(0, current_y, width, 500)
            current_y = draw_text_wrapped(surf, ghost["desc"], font_text, TEXT_COLOR, rect)
            current_y += 20

    elif category == "Abilities":
        for ability in ABILITY_DATA:
            name_surf = font_tab.render(ability["name"], True, (100, 255, 255))
            surf.blit(name_surf, (0, current_y))
            current_y += 30
            rect = pygame.Rect(0, current_y, width, 500)
            current_y = draw_text_wrapped(surf, ability["desc"], font_text, TEXT_COLOR, rect)
            current_y += 20

    elif category == "Items":
        for item in ITEM_DATA:
            if isinstance(item, str): 
                if item == "": 
                    current_y += 10
                    continue
                head_surf = font_tab.render(item, True, (255, 215, 0))
                surf.blit(head_surf, (0, current_y))
                current_y += 35
            else:
                name_surf = font_text.render(item["name"], True, (100, 255, 100))
                surf.blit(name_surf, (20, current_y))
                current_y += 20
                rect = pygame.Rect(40, current_y, width - 40, 500)
                current_y = draw_text_wrapped(surf, item["desc"], font_text, (200, 200, 200), rect)
                current_y += 15

    # 3. Crop to exact height used
    final_surf = surf.subsurface((0, 0, width, current_y + 50))
    return final_surf

def manual_screen(screen):
    clock = pygame.time.Clock()
    running = True
    active_tab = "Ghosts"
    
    # Generate initial content
    content_surf = generate_content_surface(active_tab)
    scroll_y = 0
    
    # Define the visible window for text
    VIEW_RECT = pygame.Rect(50, 180, 720, 380) # x, y, w, h
    
    while running:
        screen.fill(BACKGROUND_COLOR)
        mx, my = pygame.mouse.get_pos()
        
        # --- HEADER ---
        title = font_title.render("GAME MANUAL", True, HEADER_COLOR)
        screen.blit(title, (50, 30))
        
        exit_hint = font_text.render("Use Scroll Wheel / Arrows to Read. ESC to Back.", True, (150, 150, 150))
        screen.blit(exit_hint, (50, 80))

        # --- TABS ---
        tabs = ["Ghosts", "Abilities", "Items"]
        tab_rects = []
        start_x = 50
        
        for tab in tabs:
            rect = pygame.Rect(start_x, 120, 150, 40)
            color = TAB_ACTIVE_COLOR if tab == active_tab else TAB_COLOR
            if rect.collidepoint(mx, my):
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            
            pygame.draw.rect(screen, color, rect, border_radius=5)
            text = font_tab.render(tab, True, (255, 255, 255))
            screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))
            tab_rects.append((rect, tab))
            start_x += 160
            
        # --- DRAW CONTENT WITH CLIPPING ---
        # 1. Calculate max scroll
        max_scroll = max(0, content_surf.get_height() - VIEW_RECT.height)
        scroll_y = max(0, min(scroll_y, max_scroll)) # Clamp scroll
        
        # 2. Set Clip (Only draw inside the view box)
        screen.set_clip(VIEW_RECT)
        
        # 3. Draw the content shifted by scroll_y
        screen.blit(content_surf, (VIEW_RECT.x, VIEW_RECT.y - scroll_y))
        
        # 4. Remove Clip
        screen.set_clip(None)
        
        # --- DRAW SCROLLBAR ---
        if max_scroll > 0:
            bar_height = VIEW_RECT.height * (VIEW_RECT.height / content_surf.get_height())
            bar_pos = VIEW_RECT.y + (scroll_y / max_scroll) * (VIEW_RECT.height - bar_height)
            pygame.draw.rect(screen, (100, 100, 100), (VIEW_RECT.right - 5, VIEW_RECT.y, 5, VIEW_RECT.height)) # Track
            pygame.draw.rect(screen, (200, 200, 200), (VIEW_RECT.right - 5, bar_pos, 5, bar_height)) # Handle

        # --- BACK BUTTON ---
        back_btn = pygame.Rect(650, 530, 100, 40)
        pygame.draw.rect(screen, (200, 50, 50), back_btn, border_radius=5)
        b_txt = font_tab.render("BACK", True, TEXT_COLOR)
        screen.blit(b_txt, (back_btn.centerx - b_txt.get_width()//2, back_btn.centery - b_txt.get_height()//2))

        pygame.display.flip()
        
        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False
                if event.key == pygame.K_UP: scroll_y -= SCROLL_SPEED
                if event.key == pygame.K_DOWN: scroll_y += SCROLL_SPEED
            
            if event.type == pygame.MOUSEWHEEL:
                scroll_y -= event.y * SCROLL_SPEED
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(mx, my):
                    running = False
                
                # Tab Switching
                for rect, name in tab_rects:
                    if rect.collidepoint(mx, my):
                        if active_tab != name:
                            active_tab = name
                            content_surf = generate_content_surface(active_tab)
                            scroll_y = 0 # Reset scroll on tab change

        clock.tick(60)

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Manual Test")
    manual_screen(screen)