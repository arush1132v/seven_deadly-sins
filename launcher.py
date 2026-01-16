import pygame
import sys
import os
import random
import traceback
from pygame.locals import *
import shop
import manual

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("7 Deadly Sins Pac-Man")

# --- GLOBAL STATE ---
player_points = 500
player_inventory = []

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
    pass

def main_menu():
    global player_points, player_inventory
    running = True
    
    font_title = pygame.font.SysFont("arial", 50, bold=True)
    font_label = pygame.font.SysFont("arial", 18, bold=True) 

    while running:
        screen.fill(BACKGROUND_COLOR)
        
        title_surf = font_title.render("7 DEADLY SINS PAC-MAN", False, (255, 215, 0))
        screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 80))
        
        y_pos = SCREEN_HEIGHT // 2 + 50
        spacing = 150
        x_start = SCREEN_WIDTH // 2 - (spacing * 1.5)
        x_shop  = x_start + spacing
        x_load  = x_start + spacing * 2
        x_manual = x_start + spacing * 3
        
        start_hover = draw_image_button(screen, btn_start_img, x_start, y_pos)
        
        shop_hover = draw_image_button(screen, btn_shop_img, x_shop, y_pos)
        shop_txt = font_label.render("SHOP", True, MENU_TEXT_COLOR)
        screen.blit(shop_txt, (x_shop - shop_txt.get_width()//2, y_pos + 45))
        
        load_hover = draw_image_button(screen, btn_load_img, x_load, y_pos)
        load_txt = font_label.render("LOAD", True, MENU_TEXT_COLOR)
        screen.blit(load_txt, (x_load - load_txt.get_width()//2, y_pos + 45))
        
        manual_hover = draw_image_button(screen, btn_manual_img, x_manual, y_pos)
        manual_txt = font_label.render("MANUAL", True, MENU_TEXT_COLOR)
        screen.blit(manual_txt, (x_manual - manual_txt.get_width()//2, y_pos + 45))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT: 
                return "quit"
            if event.type == MOUSEBUTTONDOWN:
                if start_hover: 
                    return "start"
                if shop_hover: 
                    player_points, player_inventory = shop.shop_screen(screen, player_points, player_inventory)
                if load_hover: 
                    load_game_screen()
                if manual_hover: 
                    manual.manual_screen(screen)

# --- MAIN LAUNCHER LOOP ---
if __name__ == "__main__":
    print("="*50)
    print("LAUNCHER STARTING...")
    print("="*50)
    
    loading_screen()
    
    while True:
        action = main_menu()
        
        if action == "quit":
            print("User quit from menu")
            break
        
        elif action == "start":
            print("\n" + "="*50)
            print("START BUTTON CLICKED!")
            print("Attempting to load game...")
            print("="*50)
            
            try:
                # Step 1: Try importing main
                print("Step 1: Importing main.py...")
                from main import main as run_game
                print("✓ main.py imported successfully")
                
                # Step 2: Try running it
                print("Step 2: Running main()...")
                run_game()
                print("✓ Game completed normally")
                
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