import pygame
import sys
import os
import random
import traceback
from pygame.locals import *
import shop
import manual
from ui_settings import SettingsScreen
from game_data import get_game_data

# --- CONFIGURATION ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# COLORS
BACKGROUND_COLOR = (0, 0, 0)
MENU_TEXT_COLOR = (255, 255, 255)
LOADING_BG_COLOR = (255, 255, 255)
LOADING_TEXT_COLOR = (0, 0, 0)
PROGRESS_BAR_COLOR = (0, 0, 0)
BAR_BORDER_COLOR = (0, 0, 0)
BAR_BG_COLOR = (200, 200, 200)

pygame.init()

# --- FONTS ---
pygame.font.init()
try:
    FONT_PATH = "pixel_font.ttf"
    font_header = pygame.font.Font(FONT_PATH, 48)
    font_sub = pygame.font.Font(FONT_PATH, 24)
    font_label = pygame.font.Font(FONT_PATH, 20)
    font_small = pygame.font.Font(FONT_PATH, 16)
except FileNotFoundError:
    print("Warning: pixel_font.ttf not found. Using system fonts.")
    font_header = pygame.font.SysFont("arial", 48, bold=True)
    font_sub = pygame.font.SysFont("arial", 24, bold=True)
    font_label = pygame.font.SysFont("arial", 20, bold=True)
    font_small = pygame.font.SysFont("arial", 16)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("7 Deadly Sins Pac-Man")

# --- LOAD ASSETS ---
def load_asset(name, size=None):
    path = os.path.join("assets", name)
    try:
        img = pygame.image.load(path)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except FileNotFoundError:
        print(f"Warning: {name} not found in assets folder.")
        surf = pygame.Surface(size if size else (50, 50))
        surf.fill((200, 50, 50))
        return surf

# Load Buttons
btn_start_img = load_asset("btn_start.png", (120, 60))
btn_shop_img = load_asset("btn_shop.png", (120, 60))
btn_load_img = load_asset("btn_load.png", (120, 60))
btn_manual_img = load_asset("btn_manual.png", (120, 60))
btn_settings_img = load_asset("settings_icon.png", (100, 100))
skull_img = load_asset("skull.png", (150, 150))

def draw_image_button(screen, image, x, y):
    rect = image.get_rect(center=(x, y))
    mx, my = pygame.mouse.get_pos()
    is_hover = rect.collidepoint(mx, my)
    
    if is_hover:
        w, h = rect.width, rect.height
        scaled_img = pygame.transform.scale(image, (int(w * 1.1), int(h * 1.1)))
        new_rect = scaled_img.get_rect(center=(x, y))
        screen.blit(scaled_img, new_rect)
        return True 
    else:
        screen.blit(image, rect)
        return False

def loading_screen():
    progress = 0
    font = pygame.font.SysFont("arial", 20)
    blink_timer = 0
    is_visible = True
    next_blink_time = random.randint(30, 80) 
    
    while progress < 100:
        screen.fill(LOADING_BG_COLOR)
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50
        
        blink_timer += 1
        if is_visible and blink_timer > next_blink_time:
            is_visible = False
            blink_timer = 0
        if not is_visible and blink_timer > 10:
            is_visible = True
            blink_timer = 0
            next_blink_time = random.randint(20, 60)

        if is_visible:
            skull_rect = skull_img.get_rect(center=(center_x, center_y))
            screen.blit(skull_img, skull_rect)

        bar_width = 400
        bar_height = 30
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = center_y + 100
        
        pygame.draw.rect(screen, BAR_BG_COLOR, (bar_x, bar_y, bar_width, bar_height), border_radius=15)
        fill_width = (progress / 100) * bar_width
        pygame.draw.rect(screen, PROGRESS_BAR_COLOR, (bar_x, bar_y, fill_width, bar_height), border_radius=15)
        pygame.draw.rect(screen, BAR_BORDER_COLOR, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=15)
        
        txt = font.render(f"Loading... {int(progress)}%", True, LOADING_TEXT_COLOR)
        screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, bar_y + 40))

        pygame.display.flip()
        progress += 0.5 
        pygame.time.delay(20)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def show_error(error_msg, detailed_trace):
    """Show error message on screen"""
    running = True
    font_title = pygame.font.SysFont("arial", 30, bold=True)
    font_text = pygame.font.SysFont("arial", 16)
    
    # Split long error messages
    lines = []
    lines.append("ERROR LOADING GAME:")
    lines.append("")
    lines.append(error_msg)
    lines.append("")
    lines.append("Details:")
    
    # Add traceback lines
    trace_lines = detailed_trace.split('\n')
    for line in trace_lines[-10:]:  # Last 10 lines
        if line.strip():
            lines.append(line[:80])  # Truncate long lines
    
    lines.append("")
    lines.append("Press ESC to return to menu")
    
    while running:
        screen.fill((50, 0, 0))
        
        title = font_title.render("GAME ERROR", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
        
        y = 80
        for line in lines:
            text = font_text.render(line, True, (255, 200, 200))
            screen.blit(text, (20, y))
            y += 25
            if y > SCREEN_HEIGHT - 50:
                break
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return "menu"

def load_game_screen():
    """Show saved game info"""
    game_data = get_game_data()
    
    running = True
    font_title = pygame.font.SysFont("arial", 36, bold=True)
    font_text = pygame.font.SysFont("arial", 20)
    
    while running:
        screen.fill((20, 20, 40))
        
        # Title
        title = font_title.render("SAVED GAME DATA", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        
        # Display stats
        y = 100
        stats = [
            f"Points: {game_data.get_points()}",
            f"Highest Level: {game_data.data['player']['highest_level']}",
            f"Total Deaths: {game_data.data['player']['deaths']}",
            f"Total Wins: {game_data.data['player']['wins']}",
            "",
            f"Coins Collected: {game_data.data['statistics']['coins_collected']}",
            f"Ghosts Killed: {game_data.data['statistics']['ghosts_killed']}",
            f"Items Collected: {game_data.data['statistics']['items_collected']}",
            "",
            f"Inventory: {len(game_data.get_inventory())} items owned",
        ]
        
        for line in stats:
            text = font_text.render(line, True, (255, 255, 255))
            screen.blit(text, (100, y))
            y += 35
        
        # Back button
        back_text = font_text.render("Press ESC to go back", True, (200, 200, 200))
        screen.blit(back_text, (SCREEN_WIDTH//2 - back_text.get_width()//2, 520))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return

def main_menu():
    # --- LOAD GAME DATA ---
    game_data = get_game_data()
    player_points = game_data.get_points()
    player_inventory = game_data.get_inventory()
    game_config = game_data.get_settings()
    
    while True:
        screen.fill(BACKGROUND_COLOR)
        
        # --- TITLE ---
        title_txt = font_header.render("7 DEADLY SINS: PAC-MAN", True, MENU_TEXT_COLOR)
        screen.blit(title_txt, (SCREEN_WIDTH//2 - title_txt.get_width()//2, 80))
        
        # Show current points
        points_txt = font_sub.render(f"Points: {player_points}", True, (255, 215, 0))
        screen.blit(points_txt, (SCREEN_WIDTH//2 - points_txt.get_width()//2, 140))

        # --- DRAW 5 BUTTONS ---
        y_pos = 300
        x_start = 60
        spacing = 145
        
        # Calculate Positions
        x_start_btn    = x_start
        x_shop_btn     = x_start + spacing
        x_settings_btn = x_start + spacing * 2
        x_load_btn     = x_start + spacing * 3
        x_manual_btn   = x_start + spacing * 4
        
        # Draw Buttons & Check Hovers
        start_hover    = draw_image_button(screen, btn_start_img, x_start_btn, y_pos)
        shop_hover     = draw_image_button(screen, btn_shop_img, x_shop_btn, y_pos)
        settings_hover = draw_image_button(screen, btn_settings_img, x_settings_btn, y_pos)
        load_hover     = draw_image_button(screen, btn_load_img, x_load_btn, y_pos)
        manual_hover   = draw_image_button(screen, btn_manual_img, x_manual_btn, y_pos)

        # Labels (White text under icons)
        labels = [
            ("START", x_start_btn), 
            ("SHOP", x_shop_btn), 
            ("SETTINGS", x_settings_btn), 
            ("LOAD", x_load_btn), 
            ("MANUAL", x_manual_btn)
        ]
        for text, x in labels:
            txt_surf = font_sub.render(text, True, MENU_TEXT_COLOR)
            screen.blit(txt_surf, (x - txt_surf.get_width()//2, y_pos + 55))

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT: 
                game_data.save()
                return "quit"
            if event.type == MOUSEBUTTONDOWN:
                if start_hover: 
                    game_data.save()
                    return "start"
                if shop_hover:
                    # Update points and inventory from shop
                    player_points, player_inventory = shop.shop_screen(screen, player_points, player_inventory)
                    # Save purchases
                    for item_id in player_inventory:
                        game_data.buy_item(item_id)
                    # Update points in game data
                    current_points = game_data.get_points()
                    difference = player_points - current_points
                    if difference < 0:  # Spent money
                        game_data.spend_points(abs(difference))
                    
                if settings_hover:
                    # Open settings screen
                    settings_ui = SettingsScreen(screen, game_config)
                    settings_ui.run()
                    # Save updated settings
                    game_data.update_audio(
                        game_config["audio"]["music"],
                        game_config["audio"]["sfx"]
                    )
                    for action, key in game_config["keybinds"].items():
                        game_data.update_keybind(action, key)
                    
                if load_hover: 
                    load_game_screen()
                if manual_hover: 
                    manual.manual_screen(screen)


# --- MAIN LAUNCHER LOOP ---
if __name__ == "__main__":
    print("="*50)
    print("LAUNCHER STARTING...")
    print("="*50)
    
    # Load game data
    game_data = get_game_data()
    print(f"Loaded save: {game_data.get_points()} points")
    
    loading_screen()
    
    while True:
        action = main_menu()
        
        if action == "quit":
            print("User quit from menu")
            game_data.save()
            break
        
        elif action == "start":
            print("\n" + "="*50)
            print("START BUTTON CLICKED!")
            print("Attempting to load game...")
            print("="*50)
            
            # Get fresh data
            player_points = game_data.get_points()
            player_inventory = game_data.get_inventory()
            game_config = game_data.get_settings()
            
            try:
                # Step 1: Try importing main
                print("Step 1: Importing main.py...")
                from main import main as run_game
                print("✓ main.py imported successfully")
                
                # Step 2: Try running it with parameters
                print("Step 2: Running main()...")
                print(f"Passing: points={player_points}, inventory={player_inventory}")
                run_game(player_points, player_inventory, game_config)
                print("✓ Game completed normally")
                
                # Reload data after game ends
                game_data.load()
                
            except ImportError as e:
                print(f"✗ ERROR: Could not import main.py")
                print(f"Error: {e}")
                error_trace = traceback.format_exc()
                print(error_trace)
                
                result = show_error(f"Import Error: {str(e)}", error_trace)
                if result == "quit":
                    break
                    
            except Exception as e:
                print(f"✗ ERROR: Exception in game")
                print(f"Error: {e}")
                error_trace = traceback.format_exc()
                print(error_trace)
                
                result = show_error(f"Game Error: {str(e)}", error_trace)
                if result == "quit":
                    break
            
            print("\nReturning to main menu...")
    
    pygame.quit()
    print("\n" + "="*50)
    print("LAUNCHER CLOSED")
    print("="*50)
    sys.exit()