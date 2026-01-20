import pygame
import math
import random

class TitleMenu:
    def __init__(self, screen, audio_manager):
        self.screen = screen
        self.audio = audio_manager
        self.width, self.height = screen.get_size()
        
        # Colors
        self.BG_COLOR = (15, 10, 20)
        self.TEXT_COLOR = (200, 200, 200)
        self.ACCENT_COLOR = (180, 20, 50) # Red
        self.HOVER_COLOR = (255, 50, 50)
        
        # Fonts
        self.font_title = pygame.font.SysFont("times new roman", 70, bold=True)
        self.font_sub = pygame.font.SysFont("arial", 20, italic=True)
        self.font_menu = pygame.font.SysFont("arial", 30)
        
        # Particles for background animation
        self.particles = []
        for _ in range(50):
            self.particles.append(self.create_particle())
            
        # Menu Options
        self.options = ["START GAME", "SETTINGS", "SHOP", "MANUAL", "LOAD GAME", "QUIT"]
        self.buttons = []
        
        # Calculate button positions
        start_y = 300
        for i, opt in enumerate(self.options):
            rect = pygame.Rect(self.width//2 - 100, start_y + (i * 50), 200, 40)
            self.buttons.append({"text": opt, "rect": rect})

        # State: "PRESS_KEY" or "MAIN_MENU"
        self.state = "PRESS_KEY"
        self.timer = 0

    def create_particle(self):
        return {
            "x": random.randint(0, self.width),
            "y": random.randint(0, self.height),
            "speed": random.uniform(0.5, 2.0),
            "size": random.randint(1, 3),
            "alpha": random.randint(50, 200)
        }

    def update_particles(self):
        for p in self.particles:
            p["y"] -= p["speed"] # Float up
            if p["y"] < 0:
                p["y"] = self.height
                p["x"] = random.randint(0, self.width)

    def draw_particles(self):
        for p in self.particles:
            s = pygame.Surface((p["size"], p["size"]))
            s.fill((100, 100, 150))
            s.set_alpha(p["alpha"])
            self.screen.blit(s, (p["x"], int(p["y"])))

    def draw_press_key(self):
        # Pulsing effect using Sine wave
        alpha = abs(math.sin(self.timer * 0.05)) * 255
        
        text = self.font_sub.render("- PRESS ANY KEY TO CONTINUE -", True, self.TEXT_COLOR)
        text.set_alpha(int(alpha))
        
        rect = text.get_rect(center=(self.width//2, 500))
        self.screen.blit(text, rect)

    def draw_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for btn in self.buttons:
            # Check Hover
            is_hovered = btn["rect"].collidepoint(mouse_pos)
            color = self.HOVER_COLOR if is_hovered else self.TEXT_COLOR
            
            # Draw Text
            txt_surf = self.font_menu.render(btn["text"], True, color)
            rect = txt_surf.get_rect(center=btn["rect"].center)
            
            # Draw simple decorative lines if hovered
            if is_hovered:
                pygame.draw.line(self.screen, self.ACCENT_COLOR, (rect.left - 10, rect.centery), (rect.left - 5, rect.centery), 2)
                pygame.draw.line(self.screen, self.ACCENT_COLOR, (rect.right + 5, rect.centery), (rect.right + 10, rect.centery), 2)
                
            self.screen.blit(txt_surf, rect)

    def run(self):
        clock = pygame.time.Clock()
        self.audio.play_music("menu") # Ensure music is playing
        
        while True:
            self.timer += 1
            self.screen.fill(self.BG_COLOR)
            self.update_particles()
            self.draw_particles()
            
            # Draw Main Title (Always visible)
            title = self.font_title.render("SEVEN DEADLY SINS", True, self.ACCENT_COLOR)
            title_rect = title.get_rect(center=(self.width//2, 150))
            self.screen.blit(title, title_rect)
            
            # Event Handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                if self.state == "PRESS_KEY":
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        self.state = "MAIN_MENU"
                        self.audio.play_ui_sound("open")
                        
                elif self.state == "MAIN_MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for btn in self.buttons:
                                if btn["rect"].collidepoint(event.pos):
                                    self.audio.play_ui_sound("click")
                                    action = btn["text"]
                                    if action == "START GAME": return "START"
                                    if action == "SETTINGS": return "SETTINGS"
                                    if action == "SHOP": return "SHOP"
                                    if action == "QUIT": return "QUIT"
                                    # Placeholders for now
                                    if action == "MANUAL": print("Manual not implemented yet")
                                    if action == "LOAD GAME": print("Load not implemented yet")

            # Drawing based on state
            if self.state == "PRESS_KEY":
                self.draw_press_key()
            else:
                self.draw_menu()

            pygame.display.flip()
            clock.tick(60)