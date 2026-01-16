import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
HOVER = (70, 70, 70)

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 30, bold=True)
        
        center_x = SCREEN_WIDTH // 2
        start_y = 180 # Moved up slightly
        gap = 60
        
        # ADDED "GAME SHOP" BUTTON
        self.buttons = [
            {"text": "RESUME",    "action": "RESUME",    "rect": pygame.Rect(0, 0, 240, 50)},
            {"text": "GAME SHOP", "action": "SHOP",      "rect": pygame.Rect(0, 0, 240, 50)}, # <--- NEW
            {"text": "SETTINGS",  "action": "SETTINGS",  "rect": pygame.Rect(0, 0, 240, 50)},
            {"text": "MAIN MENU", "action": "MENU",      "rect": pygame.Rect(0, 0, 240, 50)},
            {"text": "QUIT GAME", "action": "QUIT",      "rect": pygame.Rect(0, 0, 240, 50)}
        ]
        
        for i, btn in enumerate(self.buttons):
            btn["rect"].center = (center_x, start_y + i * gap)

    def draw(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150) 
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        title = self.font.render("GAME PAUSED", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            rect = btn["rect"]
            color = HOVER if rect.collidepoint(mouse_pos) else GRAY
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=10)
            txt = self.font.render(btn["text"], True, WHITE)
            self.screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    def run(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "QUIT"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mp = pygame.mouse.get_pos()
                    for btn in self.buttons:
                        if btn["rect"].collidepoint(mp):
                            return btn["action"]
            self.draw()
            pygame.display.flip()
        return "RESUME"