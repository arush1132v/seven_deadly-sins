import pygame
import sys
from abilities import AbilityManager

# --- CONFIGURATION ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 140
CARD_HEIGHT = 180
GAP = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (50, 205, 50)
HOVER_COLOR = (50, 50, 50)

class AbilitySelectScreen:
    def __init__(self, screen):
        self.screen = screen
        self.manager = AbilityManager()
        self.font_title = pygame.font.SysFont("arial", 40, bold=True)
        self.font_card = pygame.font.SysFont("arial", 20, bold=True)
        self.font_desc = pygame.font.SysFont("arial", 16)
        
        # Create Rects for the 5 cards
        self.ability_cards = []
        names = list(self.manager.data.keys())
        
        # Layout: Row of 3, Row of 2
        start_x_row1 = (SCREEN_WIDTH - (3 * CARD_WIDTH + 2 * GAP)) // 2
        start_x_row2 = (SCREEN_WIDTH - (2 * CARD_WIDTH + GAP)) // 2
        
        for i, name in enumerate(names):
            if i < 3: # First row
                x = start_x_row1 + i * (CARD_WIDTH + GAP)
                y = 150
            else: # Second row
                x = start_x_row2 + (i - 3) * (CARD_WIDTH + GAP)
                y = 150 + CARD_HEIGHT + GAP
            
            rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            self.ability_cards.append({"name": name, "rect": rect})

        # Confirm Button
        self.confirm_rect = pygame.Rect(0, 0, 200, 50)
        self.confirm_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        
        self.selected_abilities = []

    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True

        # Check Card Clicks
        if mouse_click:
            # 1. Check Cards
            for card in self.ability_cards:
                if card["rect"].collidepoint(mouse_pos):
                    name = card["name"]
                    if name in self.selected_abilities:
                        self.selected_abilities.remove(name) # Deselect
                    elif len(self.selected_abilities) < 2:
                        self.selected_abilities.append(name) # Select
            
            # 2. Check Confirm Button
            if len(self.selected_abilities) == 2:
                if self.confirm_rect.collidepoint(mouse_pos):
                    return "CONFIRM" # Signal to main loop to proceed
        
        return None

    def draw(self):
        self.screen.fill((30, 30, 30)) # Dark Grey Background

        # Title
        title_surf = self.font_title.render("Choose 2 Abilities", True, WHITE)
        self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))

        # Draw Cards
        for card in self.ability_cards:
            name = card["name"]
            rect = card["rect"]
            data = self.manager.data[name]
            is_selected = name in self.selected_abilities
            
            # Card Background
            color = data["color"]
            # Dim the color if not selected and we already have 2 picked
            if len(self.selected_abilities) == 2 and not is_selected:
                draw_color = (50, 50, 50)
            else:
                draw_color = (40, 40, 40)

            pygame.draw.rect(self.screen, draw_color, rect, border_radius=10)
            
            # Border (Highlight if selected)
            if is_selected:
                pygame.draw.rect(self.screen, color, rect, 4, border_radius=10)
            else:
                pygame.draw.rect(self.screen, GRAY, rect, 2, border_radius=10)

            # Icon Placeholder (Using the color circle from your manager)
            # You can replace this with your actual Icon images later
            center_x = rect.x + rect.width // 2
            pygame.draw.circle(self.screen, data["color"], (center_x, rect.y + 40), 20)

            # Text: Name
            name_surf = self.font_card.render(name, True, WHITE)
            self.screen.blit(name_surf, (center_x - name_surf.get_width()//2, rect.y + 70))

            # Text: Description (Simple wrap logic)
            desc_words = data["desc"].split(" ")
            line = ""
            y_offset = 100
            for word in desc_words:
                test_line = line + word + " "
                if self.font_desc.size(test_line)[0] < rect.width - 10:
                    line = test_line
                else:
                    text_surf = self.font_desc.render(line, True, (200, 200, 200))
                    self.screen.blit(text_surf, (rect.x + 10, rect.y + y_offset))
                    line = word + " "
                    y_offset += 20
            # Draw last line
            text_surf = self.font_desc.render(line, True, (200, 200, 200))
            self.screen.blit(text_surf, (rect.x + 10, rect.y + y_offset))

        # Draw Confirm Button
        if len(self.selected_abilities) == 2:
            btn_color = GREEN
            text_color = BLACK
        else:
            btn_color = (60, 60, 60)
            text_color = GRAY
        
        pygame.draw.rect(self.screen, btn_color, self.confirm_rect, border_radius=20)
        btn_text = self.font_title.render("CONFIRM", True, text_color)
        self.screen.blit(btn_text, (self.confirm_rect.centerx - btn_text.get_width()//2, 
                                    self.confirm_rect.centery - btn_text.get_height()//2))

    def run(self):
        """Blocking loop that waits for selection"""
        waiting = True
        while waiting:
            result = self.handle_input()
            if result == "CONFIRM":
                return self.selected_abilities
            
            self.draw()
            pygame.display.flip()
            pygame.time.Clock().tick(60)