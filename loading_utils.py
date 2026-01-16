import pygame
import random

def show_loading_transition(screen, selected_abilities):
    """
    Shows a loading screen after ability selection
    
    screen: pygame display surface
    selected_abilities: List of 2 ability names
    """
    SCREEN_WIDTH = screen.get_width()
    SCREEN_HEIGHT = screen.get_height()
    
    # Colors
    BG_COLOR = (20, 20, 40)
    TEXT_COLOR = (255, 255, 255)
    BAR_BG = (50, 50, 70)
    BAR_FILL = (50, 205, 50)  # Green
    GOLD = (255, 215, 0)
    
    # Fonts
    font_title = pygame.font.SysFont("arial", 40, bold=True)
    font_subtitle = pygame.font.SysFont("arial", 24)
    font_small = pygame.font.SysFont("arial", 18)
    
    # Loading messages
    messages = [
        "Awakening the deadly sins...",
        "Preparing the maze...",
        "Summoning ghosts...",
        "Charging your abilities...",
        "Almost ready..."
    ]
    
    progress = 0
    message_index = 0
    clock = pygame.time.Clock()
    
    # Animation variables
    dot_count = 0
    dot_timer = 0
    
    while progress < 100:
        screen.fill(BG_COLOR)
        
        # Title
        title = font_title.render("LOADING GAME", True, GOLD)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        # Show selected abilities
        abilities_y = 180
        ability_text = font_subtitle.render("Your Abilities:", True, TEXT_COLOR)
        screen.blit(ability_text, (SCREEN_WIDTH//2 - ability_text.get_width()//2, abilities_y))
        
        for i, ability in enumerate(selected_abilities):
            key_num = i + 1
            ability_display = font_small.render(f"{key_num}. {ability}", True, (100, 255, 255))
            screen.blit(ability_display, (SCREEN_WIDTH//2 - ability_display.get_width()//2, abilities_y + 40 + (i * 30)))
        
        # Loading bar
        bar_width = 500
        bar_height = 30
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = SCREEN_HEIGHT // 2 + 50
        
        # Background
        pygame.draw.rect(screen, BAR_BG, (bar_x, bar_y, bar_width, bar_height), border_radius=15)
        
        # Fill (progress)
        fill_width = int((progress / 100) * bar_width)
        if fill_width > 0:
            pygame.draw.rect(screen, BAR_FILL, (bar_x, bar_y, fill_width, bar_height), border_radius=15)
        
        # Border
        pygame.draw.rect(screen, TEXT_COLOR, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=15)
        
        # Percentage text
        percent_text = font_subtitle.render(f"{int(progress)}%", True, TEXT_COLOR)
        screen.blit(percent_text, (SCREEN_WIDTH//2 - percent_text.get_width()//2, bar_y + 40))
        
        # Loading message with animated dots
        dot_timer += 1
        if dot_timer > 15:  # Change dots every 15 frames
            dot_timer = 0
            dot_count = (dot_count + 1) % 4
        
        dots = "." * dot_count
        current_message = messages[message_index] + dots
        msg_text = font_small.render(current_message, True, (200, 200, 200))
        screen.blit(msg_text, (SCREEN_WIDTH//2 - msg_text.get_width()//2, bar_y + 80))
        
        # Update progress
        progress += random.uniform(0.5, 2.0)  # Random speed for more natural feel
        
        # Change message at certain progress points
        if progress > 20 and message_index == 0:
            message_index = 1
        elif progress > 40 and message_index == 1:
            message_index = 2
        elif progress > 60 and message_index == 2:
            message_index = 3
        elif progress > 80 and message_index == 3:
            message_index = 4
        
        # Handle events (allow closing during loading)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
        
        pygame.display.flip()
        clock.tick(60)
    
    # Final "Ready!" message
    screen.fill(BG_COLOR)
    ready_text = font_title.render("READY!", True, (50, 255, 50))
    screen.blit(ready_text, (SCREEN_WIDTH//2 - ready_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
    
    hint_text = font_small.render("Get ready to survive the deadly sins...", True, TEXT_COLOR)
    screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
    
    pygame.display.flip()
    pygame.time.delay(1000)  # Show "READY!" for 1 second