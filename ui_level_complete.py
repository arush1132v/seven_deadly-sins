import pygame

# Colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
HOVER_COLOR = (70, 70, 70)
BTN_COLOR = (50, 50, 50)

class LevelCompleteMenu:
    def __init__(self, screen, level_num):
        self.screen = screen
        self.font_title = pygame.font.SysFont("arial", 50, bold=True)
        self.font_btn = pygame.font.SysFont("arial", 24, bold=True)
        self.level_num = level_num
        
        # Center coordinates
        cx = SCREEN_WIDTH // 2
        start_y = 250
        gap = 70
        
        # Define 3 Buttons
        self.buttons = [
            {"text": "CHANGE ABILITY", "action": "ABILITY", "rect": pygame.Rect(0, 0, 250, 50)},
            {"text": "NEXT LEVEL",     "action": "NEXT",    "rect": pygame.Rect(0, 0, 250, 50)},
            {"text": "MAIN MENU",      "action": "MENU",    "rect": pygame.Rect(0, 0, 250, 50)}
        ]
        
        # Position buttons
        for i, btn in enumerate(self.buttons):
            btn["rect"].center = (cx, start_y + i * gap)

    def draw(self):
        # 1. Background Overlay (Dark Greenish)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((10, 30, 10))
        self.screen.blit(overlay, (0, 0))
        
        # 2. Title Text
        title = self.font_title.render(f"LEVEL {self.level_num} COMPLETE!", True, GREEN)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        # 3. Draw Buttons
        mouse_pos = pygame.mouse.get_pos()
        
        for btn in self.buttons:
            rect = btn["rect"]
            
            # Hover Effect
            color = HOVER_COLOR if rect.collidepoint(mouse_pos) else BTN_COLOR
            
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=10) # Border
            
            text_surf = self.font_btn.render(btn["text"], True, WHITE)
            self.screen.blit(text_surf, (rect.centerx - text_surf.get_width()//2, 
                                         rect.centery - text_surf.get_height()//2))

    def run(self):
        """Blocking Loop"""
        running = True
        while running:
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for btn in self.buttons:
                        if btn["rect"].collidepoint(mouse_pos):
                            return btn["action"]
            
            # Drawing
            self.draw()
            pygame.display.flip()