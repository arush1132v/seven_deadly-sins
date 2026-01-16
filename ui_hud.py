import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
GRAY = (100, 100, 100)

class HUD:
    def __init__(self, get_image_func):
        """
        get_image_func: A function that takes an item_id and returns a pygame Surface
        """
        self.get_image = get_image_func
        self.font_main = pygame.font.SysFont("arial", 20, bold=True)
        self.font_small = pygame.font.SysFont("arial", 16)
        
        # Pause Button Rect (Top Right)
        self.pause_rect = pygame.Rect(700, 10, 80, 30)

    def draw(self, screen, abilities, inventory, lives=3):
        """
        Draws the HUD overlay on the screen
        
        abilities: List of ability names (e.g. ["Wolf Vein", "Dragon Heart"])
        inventory: List of shop item IDs (e.g. [1, 4])
        lives: Player's remaining lives
        """
        
        # --- LIVES DISPLAY (Top Left) ---
        lives_text = self.font_main.render(f"Lives: {lives}", True, RED)
        screen.blit(lives_text, (10, 10))
        
        # --- PAUSE BUTTON (Top Right) ---
        pygame.draw.rect(screen, GRAY, self.pause_rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, self.pause_rect, 2, border_radius=5)
        pause_txt = self.font_small.render("PAUSE", True, WHITE)
        screen.blit(pause_txt, (self.pause_rect.centerx - pause_txt.get_width()//2, 
                                self.pause_rect.centery - pause_txt.get_height()//2))
        
        # --- ABILITIES DISPLAY (Bottom Left) ---
        if abilities:
            y_offset = 520
            
            for i, ability_name in enumerate(abilities):
                # Background box
                box_rect = pygame.Rect(10, y_offset + (i * 40), 200, 35)
                pygame.draw.rect(screen, (40, 40, 40), box_rect, border_radius=5)
                pygame.draw.rect(screen, GOLD, box_rect, 2, border_radius=5)
                
                # Ability name
                key_num = i + 1
                ability_txt = self.font_small.render(f"{key_num}. {ability_name}", True, WHITE)
                screen.blit(ability_txt, (box_rect.x + 10, box_rect.centery - ability_txt.get_height()//2))
        
        # --- SHOP ITEMS DISPLAY (Bottom Right) ---
        if inventory:
            x_start = 600
            y_pos = 520
            
            for i, item_id in enumerate(inventory):
                # Get the item image
                item_img = self.get_image(item_id)
                
                # Background box
                box_rect = pygame.Rect(x_start + (i * 90), y_pos, 80, 70)
                pygame.draw.rect(screen, (40, 40, 40), box_rect, border_radius=5)
                pygame.draw.rect(screen, GOLD, box_rect, 2, border_radius=5)
                
                # Draw item image (scaled to fit)
                img_scaled = pygame.transform.scale(item_img, (50, 50))
                img_x = box_rect.centerx - 25
                img_y = box_rect.y + 5
                screen.blit(img_scaled, (img_x, img_y))
                
                # Key hint (Q or E)
                key_label = "Q" if i == 0 else "E"
                key_txt = self.font_small.render(key_label, True, WHITE)
                screen.blit(key_txt, (box_rect.centerx - key_txt.get_width()//2, box_rect.bottom - 18))

    def is_pause_clicked(self, mouse_pos):
        """Check if the pause button was clicked"""
        return self.pause_rect.collidepoint(mouse_pos)

    def use_shop_item(self, item_id):
        """Handle when a shop item is used (for future implementation)"""
        print(f"Used shop item: {item_id}")