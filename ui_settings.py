import pygame

# Configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
ACTIVE_COLOR = (50, 205, 50) # Green
RED = (255, 50, 50)

class SettingsScreen:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config # Reference to the main config dictionary
        self.font_title = pygame.font.SysFont("arial", 40, bold=True)
        self.font_text = pygame.font.SysFont("arial", 24)
        
        self.rebinding_action = None # Which action are we currently rebinding?
        
        # Define clickable areas (Rects)
        self.buttons = {
            "back": pygame.Rect(SCREEN_WIDTH//2 - 100, 520, 200, 50),
            
            # Audio Toggles
            "music_vol": pygame.Rect(450, 150, 200, 30),
            "sfx_vol":   pygame.Rect(450, 200, 200, 30),
            
            # Keybind Buttons
            "ability_1": pygame.Rect(450, 300, 150, 35),
            "ability_2": pygame.Rect(450, 350, 150, 35),
            "shop_1":    pygame.Rect(450, 400, 150, 35),
            "shop_2":    pygame.Rect(450, 450, 150, 35),
        }

    def get_key_name(self, key_code):
        """Converts pygame key integer to string name"""
        return pygame.key.name(key_code).upper()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            
            # 1. KEY REBINDING LOGIC
            if self.rebinding_action:
                if event.type == pygame.KEYDOWN:
                    # Assign new key
                    self.config["keybinds"][self.rebinding_action] = event.key
                    self.rebinding_action = None # Stop listening
                return None

            # 2. STANDARD CLICKS
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mp = pygame.mouse.get_pos()
                
                # Check Back Button
                if self.buttons["back"].collidepoint(mp):
                    return "MENU" # Go back to menu
                
                # Check Volume Clicks (Cycle 0 -> 50 -> 100 -> 0)
                if self.buttons["music_vol"].collidepoint(mp):
                    self.config["audio"]["music"] = (self.config["audio"]["music"] + 0.5) 
                    if self.config["audio"]["music"] > 1.0: self.config["audio"]["music"] = 0.0
                    # Apply real mixer volume here if you had music loaded
                    # pygame.mixer.music.set_volume(self.config["audio"]["music"])

                if self.buttons["sfx_vol"].collidepoint(mp):
                    self.config["audio"]["sfx"] = (self.config["audio"]["sfx"] + 0.5)
                    if self.config["audio"]["sfx"] > 1.0: self.config["audio"]["sfx"] = 0.0

                # Check Keybind Buttons
                for action in ["ability_1", "ability_2", "shop_1", "shop_2"]:
                    if self.buttons[action].collidepoint(mp):
                        self.rebinding_action = action # Start waiting for key
        
        return None

    def draw(self):
        self.screen.fill((40, 40, 40))
        
        # --- TITLE ---
        title = self.font_title.render("SETTINGS", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

        # --- AUDIO SECTION ---
        # Labels
        self.screen.blit(self.font_text.render("Music Volume:", True, WHITE), (200, 150))
        self.screen.blit(self.font_text.render("Game Sound:", True, WHITE), (200, 200))
        
        # Values (Clickable)
        m_vol = int(self.config["audio"]["music"] * 100)
        s_vol = int(self.config["audio"]["sfx"] * 100)
        
        self.draw_button(self.buttons["music_vol"], f"{m_vol}%", GRAY)
        self.draw_button(self.buttons["sfx_vol"], f"{s_vol}%", GRAY)

        # --- CONTROLS SECTION ---
        # Labels
        self.screen.blit(self.font_text.render("Ability 1 Key:", True, WHITE), (200, 300))
        self.screen.blit(self.font_text.render("Ability 2 Key:", True, WHITE), (200, 350))
        self.screen.blit(self.font_text.render("Shop Item 1 Key:", True, WHITE), (200, 400))
        self.screen.blit(self.font_text.render("Shop Item 2 Key:", True, WHITE), (200, 450))

        # Key Buttons
        for action in ["ability_1", "ability_2", "shop_1", "shop_2"]:
            rect = self.buttons[action]
            
            # If we are currently rebinding this specific key, make it Red and say "PRESS KEY"
            if self.rebinding_action == action:
                self.draw_button(rect, "PRESS KEY...", RED)
            else:
                key_name = self.get_key_name(self.config["keybinds"][action])
                self.draw_button(rect, key_name, ACTIVE_COLOR)

        # --- BACK BUTTON ---
        self.draw_button(self.buttons["back"], "BACK TO MENU", WHITE, text_color=(0,0,0))
        
        pygame.display.flip()

    def draw_button(self, rect, text, bg_color, text_color=WHITE):
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=8)
        pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=8) # Border
        txt_surf = self.font_text.render(text, True, text_color)
        self.screen.blit(txt_surf, (rect.centerx - txt_surf.get_width()//2, rect.centery - txt_surf.get_height()//2))

    def run(self):
        """Blocking Loop for settings menu"""
        running = True
        while running:
            result = self.handle_input()
            if result == "QUIT": return "QUIT"
            if result == "MENU": return "MENU"
            
            self.draw()