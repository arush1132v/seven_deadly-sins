import pygame

# Configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
ACTIVE_COLOR = (50, 205, 50) # Green
RED = (255, 50, 50) # Red for rebinding

class SettingsScreen:
    def __init__(self, screen, config, audio_manager=None): 
        self.screen = screen
        self.config = config 
        self.audio_manager = audio_manager
        
        # Fonts
        self.font_title = pygame.font.SysFont("arial", 40, bold=True)
        self.font_text = pygame.font.SysFont("arial", 24)
        self.font_small = pygame.font.SysFont("arial", 16)
        
        self.rebinding_action = None 
        
        # --- DEFINE BUTTONS ---
        self.buttons = {
            "back": pygame.Rect(SCREEN_WIDTH//2 - 100, 520, 200, 50),
            
            # Audio Sliders
            "music_vol": pygame.Rect(450, 150, 200, 30),
            "sfx_vol":   pygame.Rect(450, 200, 200, 30),
            
            # Keybind Buttons
            "ability_1": pygame.Rect(450, 300, 150, 35),
            "ability_2": pygame.Rect(450, 350, 150, 35),
            "shop_1":    pygame.Rect(450, 400, 150, 35),
            "shop_2":    pygame.Rect(450, 450, 150, 35)
        }

    def get_key_name(self, key_code):
        return pygame.key.name(key_code).upper()

    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1. Back Button
                if self.buttons["back"].collidepoint(mouse_pos):
                    return "MENU"
                
                # 2. Audio Sliders
                if self.buttons["music_vol"].collidepoint(mouse_pos):
                    rel_x = mouse_pos[0] - self.buttons["music_vol"].x
                    new_vol = rel_x / self.buttons["music_vol"].width
                    self.config["audio"]["music"] = max(0, min(1, new_vol))
                    if self.audio_manager:
                        self.audio_manager.set_music_volume(self.config["audio"]["music"])
                    
                if self.buttons["sfx_vol"].collidepoint(mouse_pos):
                    rel_x = mouse_pos[0] - self.buttons["sfx_vol"].x
                    new_vol = rel_x / self.buttons["sfx_vol"].width
                    self.config["audio"]["sfx"] = max(0, min(1, new_vol))
                    if self.audio_manager:
                        self.audio_manager.set_sfx_volume(self.config["audio"]["sfx"])

                # 3. Keybind Rebinding
                for action in ["ability_1", "ability_2", "shop_1", "shop_2"]:
                    if self.buttons[action].collidepoint(mouse_pos):
                        self.rebinding_action = action

# [INSERT THIS NEW BLOCK HERE]
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]: # If holding down click
                    # 1. Dragging Music Slider
                    if self.buttons["music_vol"].collidepoint(mouse_pos):
                        rel_x = mouse_pos[0] - self.buttons["music_vol"].x
                        new_vol = rel_x / self.buttons["music_vol"].width
                        self.config["audio"]["music"] = max(0, min(1, new_vol))
                        if self.audio_manager:
                            self.audio_manager.set_music_volume(self.config["audio"]["music"])
                    
                    # 2. Dragging SFX Slider
                    if self.buttons["sfx_vol"].collidepoint(mouse_pos):
                        rel_x = mouse_pos[0] - self.buttons["sfx_vol"].x
                        new_vol = rel_x / self.buttons["sfx_vol"].width
                        self.config["audio"]["sfx"] = max(0, min(1, new_vol))
                        if self.audio_manager:
                            self.audio_manager.set_sfx_volume(self.config["audio"]["sfx"])

            # 4. Handle Key Press for Rebinding
            if event.type == pygame.KEYDOWN:
                if self.rebinding_action:
                    self.config["keybinds"][self.rebinding_action] = event.key
                    self.rebinding_action = None
        
        return None

    def draw(self):
        self.screen.fill((20, 20, 20)) # Dark background
        
        # Title
        title_surf = self.font_title.render("SETTINGS", True, WHITE)
        self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))

        # --- AUDIO SECTION ---
        # Draw Music Slider
        self.draw_slider(self.screen, self.buttons["music_vol"], 
                         self.config["audio"]["music"], "Music Volume")
        
        # Draw SFX Slider
        self.draw_slider(self.screen, self.buttons["sfx_vol"], 
                         self.config["audio"]["sfx"], "SFX Volume")

        # --- CONTROLS SECTION ---
        y_label = 300
        labels = ["Ability 1 Key:", "Ability 2 Key:", "Shop Item 1 Key:", "Shop Item 2 Key:"]
        actions = ["ability_1", "ability_2", "shop_1", "shop_2"]
        
        for i in range(len(labels)):
            # Draw Label
            label_surf = self.font_text.render(labels[i], True, WHITE)
            self.screen.blit(label_surf, (200, y_label + (i*50)))
            
            # Draw Button
            rect = self.buttons[actions[i]]
            if self.rebinding_action == actions[i]:
                self.draw_button(self.screen, rect, "PRESS KEY...", RED)
            else:
                key_name = self.get_key_name(self.config["keybinds"][actions[i]])
                self.draw_button(self.screen, rect, key_name, GRAY)

        # Back Button
        self.draw_button(self.screen, self.buttons["back"], "BACK TO MENU", WHITE, text_color=(0,0,0))
        
        pygame.display.flip()

    def draw_slider(self, surface, rect, value, label_text):
        # Draw Label
        label = self.font_text.render(label_text, True, WHITE)
        surface.blit(label, (rect.x - 220, rect.y))
        
        # Draw Bar Background
        pygame.draw.rect(surface, GRAY, rect, border_radius=5)
        
        # Draw Fill (Green part)
        fill_width = rect.width * value
        fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
        pygame.draw.rect(surface, ACTIVE_COLOR, fill_rect, border_radius=5)

    def draw_button(self, surface, rect, text, bg_color, text_color=WHITE):
        pygame.draw.rect(surface, bg_color, rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8) # Border
        txt_surf = self.font_text.render(text, True, text_color)
        surface.blit(txt_surf, (rect.centerx - txt_surf.get_width()//2, rect.centery - txt_surf.get_height()//2))

    def run(self):
        """Main loop for the settings screen"""
        clock = pygame.time.Clock()
        while True:
            result = self.handle_input()
            if result == "MENU":
                return "MENU"
            if result == "QUIT":
                pygame.quit()
                import sys
                sys.exit()
                
            self.draw()
            clock.tick(60)