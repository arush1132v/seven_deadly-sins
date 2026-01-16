import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
GRAY = (50, 50, 50)
GREEN = (50, 205, 50)
RED = (200, 50, 50)

class ShopMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("arial", 40, bold=True)
        self.font_item = pygame.font.SysFont("arial", 24, bold=True)
        self.font_desc = pygame.font.SysFont("arial", 18)
        
        # Define Items
        self.items = [
            {"id": "crown",   "name": "Prideful Crown",      "cost": 50,  "desc": "Invincibility (10s)"},
            {"id": "boots",   "name": "Boots of Envious",    "cost": 100, "desc": "+10% Speed (Level)"},
            {"id": "glutton", "name": "Glutton's Belly",     "cost": 20,  "desc": "Eat Row/Col Coins"},
            {"id": "sloth",   "name": "Sloth's Tranquilizer","cost": 40,  "desc": "Slow Ghosts (15s)"},
            {"id": "greed",   "name": "Greed's Double-Down", "cost": 15,  "desc": "2x Coins (30s)"}
        ]
        
        # Create Rects for layout
        start_y = 120
        self.item_rects = []
        for i in range(len(self.items)):
            rect = pygame.Rect(100, start_y + (i * 80), 600, 70)
            self.item_rects.append(rect)
            
        self.back_rect = pygame.Rect(300, 530, 200, 50)

    def draw(self, player_coins):
        self.screen.fill((20, 20, 40)) # Dark Blue background
        
        # Title
        title = self.font_title.render(f"GAME SHOP - Coins: {player_coins}", True, GOLD)
        self.screen.blit(title, (400 - title.get_width()//2, 30))
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw Items
        for i, item in enumerate(self.items):
            rect = self.item_rects[i]
            can_afford = player_coins >= item["cost"]
            
            # Background
            if rect.collidepoint(mouse_pos):
                color = (60, 60, 80)
            else:
                color = (40, 40, 60)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            
            # Border (Green if affordable, Red if not)
            border_col = GREEN if can_afford else RED
            pygame.draw.rect(self.screen, border_col, rect, 2, border_radius=10)
            
            # Text: Name
            name_txt = self.font_item.render(item["name"], True, WHITE)
            self.screen.blit(name_txt, (rect.x + 20, rect.y + 10))
            
            # Text: Cost
            cost_col = GOLD if can_afford else RED
            cost_txt = self.font_item.render(f"{item['cost']} G", True, cost_col)
            self.screen.blit(cost_txt, (rect.right - cost_txt.get_width() - 20, rect.centery - 10))
            
            # Text: Desc
            desc_txt = self.font_desc.render(item["desc"], True, (200, 200, 200))
            self.screen.blit(desc_txt, (rect.x + 20, rect.y + 40))

        # Back Button
        color = (100, 100, 100)
        if self.back_rect.collidepoint(mouse_pos): color = (150, 150, 150)
        pygame.draw.rect(self.screen, color, self.back_rect, border_radius=10)
        back_txt = self.font_item.render("BACK", True, WHITE)
        self.screen.blit(back_txt, (self.back_rect.centerx - back_txt.get_width()//2, self.back_rect.centery - back_txt.get_height()//2))

    def run(self, player):
        """Blocking Loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mp = pygame.mouse.get_pos()
                    
                    # Check Item Clicks
                    for i, rect in enumerate(self.item_rects):
                        if rect.collidepoint(mp):
                            item = self.items[i]
                            if player.coins >= item["cost"]:
                                player.coins -= item["cost"]
                                return item["id"] # Return the ID of item bought
                    
                    # Check Back
                    if self.back_rect.collidepoint(mp):
                        return "BACK"

            self.draw(player.coins)
            pygame.display.flip()