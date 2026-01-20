import pygame
import math
import os

class GreedTradeDialog:
    """
    Trade dialog that appears when Greed is close to the player.
    Offers two options: Pay for Mercy or Hire as Assassin (with ghost selection)
    """
    
    def __init__(self, screen_width, screen_height):
        self.width = 500
        self.height = 500  # Increased height for ghost selection with images
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        
        # Fonts
        self.font_title = pygame.font.SysFont("arial", 28, bold=True)
        self.font_desc = pygame.font.SysFont("arial", 18)
        self.font_button = pygame.font.SysFont("arial", 20, bold=True)
        self.font_small = pygame.font.SysFont("arial", 14)
        
        # Colors
        self.bg_color = (20, 20, 30)
        self.border_color = (255, 215, 0)  # Gold
        self.text_color = (255, 255, 255)
        self.gold_color = (255, 215, 0)
        self.red_color = (220, 20, 60)
        self.green_color = (50, 205, 50)
        self.button_color = (60, 60, 80)
        self.button_hover = (80, 80, 100)
        self.button_disabled = (40, 40, 50)
        
        # Animation
        self.anim_timer = 0
        
        # Button areas
        self.mercy_button = pygame.Rect(0, 0, 200, 60)
        self.service_button = pygame.Rect(0, 0, 200, 60)
        self.close_button = pygame.Rect(0, 0, 80, 30)
        
        # Ghost selection state
        self.selection_mode = False
        self.ghost_buttons = []  # Will store rects for each ghost
        self.selected_ghost = None
        
        # Load ghost images
        self.ghost_images = {}
        self.load_ghost_images()
        
    def load_ghost_images(self):
        """Load ghost images for the selection menu"""
        ghost_files = {
            "Pride": ("ghost_pride.png", (148, 0, 211)),
            "Lust": ("ghost_lust.png", (255, 105, 180)),
            "Envy": ("ghost_envy.png", (0, 255, 0)),
            "Gluttony": ("ghost_gluttony.png", (255, 140, 0)),
            "Wrath": ("ghost_wrath.png", (220, 20, 60)),
            "Sloth": ("ghost_sloth.png", (0, 255, 255))
        }
        
        for name, (filename, color) in ghost_files.items():
            path = os.path.join("assets", filename)
            try:
                img = pygame.image.load(path)
                self.ghost_images[name] = pygame.transform.scale(img, (40, 40))
            except FileNotFoundError:
                # Fallback: create colored square
                surf = pygame.Surface((40, 40))
                surf.fill(color)
                self.ghost_images[name] = surf
        
    def draw(self, surface, player_coins, mercy_cost, service_cost, ghosts=None):
        """
        Draw the trade dialog
        
        player_coins: Current player coin count
        mercy_cost: Cost to bribe Greed to leave
        service_cost: Cost to hire Greed as assassin
        ghosts: List of ghost objects (for selection mode)
        """
        self.anim_timer += 1
        
        # Create semi-transparent overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        
        # Main dialog box
        dialog_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Pulsing border effect
        pulse = abs(math.sin(self.anim_timer * 0.05))
        border_width = int(3 + pulse * 2)
        
        pygame.draw.rect(surface, self.bg_color, dialog_rect, border_radius=15)
        pygame.draw.rect(surface, self.border_color, dialog_rect, border_width, border_radius=15)
        
        # If in selection mode, show ghost selection UI
        if self.selection_mode:
            self.draw_ghost_selection(surface, ghosts, service_cost, player_coins)
        else:
            self.draw_main_menu(surface, player_coins, mercy_cost, service_cost)
        
        return {
            "selection_mode": self.selection_mode
        }
    
    def draw_main_menu(self, surface, player_coins, mercy_cost, service_cost):
        """Draw the main trade menu"""
        # --- TITLE ---
        title = self.font_title.render("GREED'S TRADE OFFER", True, self.gold_color)
        title_rect = title.get_rect(center=(self.x + self.width//2, self.y + 30))
        surface.blit(title, title_rect)
        
        # --- GREED'S MESSAGE ---
        message = self.font_desc.render("Choose your deal, mortal...", True, self.text_color)
        msg_rect = message.get_rect(center=(self.x + self.width//2, self.y + 65))
        surface.blit(message, msg_rect)
        
        # --- YOUR COINS ---
        coins_text = self.font_small.render(f"Your Coins: {player_coins}", True, self.gold_color)
        surface.blit(coins_text, (self.x + 20, self.y + 90))
        
        # --- BUTTONS ---
        button_y = self.y + 140
        
        # Calculate button positions
        gap = 40
        button_start_x = self.x + (self.width - (200 * 2 + gap)) // 2
        
        self.mercy_button.x = button_start_x
        self.mercy_button.y = button_y
        
        self.service_button.x = button_start_x + 200 + gap
        self.service_button.y = button_y
        
        mouse_pos = pygame.mouse.get_pos()
        
        # --- MERCY BUTTON ---
        can_afford_mercy = player_coins >= mercy_cost
        mercy_hover = self.mercy_button.collidepoint(mouse_pos) and can_afford_mercy
        
        mercy_color = self.button_hover if mercy_hover else (self.button_color if can_afford_mercy else self.button_disabled)
        pygame.draw.rect(surface, mercy_color, self.mercy_button, border_radius=10)
        pygame.draw.rect(surface, self.green_color if can_afford_mercy else self.red_color, 
                        self.mercy_button, 3, border_radius=10)
        
        # Mercy button text
        mercy_title = self.font_button.render("MERCY", True, self.text_color)
        mercy_title_rect = mercy_title.get_rect(center=(self.mercy_button.centerx, self.mercy_button.centery - 15))
        surface.blit(mercy_title, mercy_title_rect)
        
        mercy_cost_text = self.font_small.render(f"{mercy_cost} Coins", True, self.gold_color)
        mercy_cost_rect = mercy_cost_text.get_rect(center=(self.mercy_button.centerx, self.mercy_button.centery + 10))
        surface.blit(mercy_cost_text, mercy_cost_rect)
        
        # Description below
        mercy_desc = self.font_small.render("Leave me alone", True, (200, 200, 200))
        mercy_desc_rect = mercy_desc.get_rect(center=(self.mercy_button.centerx, self.mercy_button.bottom + 15))
        surface.blit(mercy_desc, mercy_desc_rect)
        
        # --- SERVICE BUTTON ---
        can_afford_service = player_coins >= service_cost
        service_hover = self.service_button.collidepoint(mouse_pos) and can_afford_service
        
        service_color = self.button_hover if service_hover else (self.button_color if can_afford_service else self.button_disabled)
        pygame.draw.rect(surface, service_color, self.service_button, border_radius=10)
        pygame.draw.rect(surface, self.green_color if can_afford_service else self.red_color,
                        self.service_button, 3, border_radius=10)
        
        # Service button text
        service_title = self.font_button.render("ASSASSIN", True, self.text_color)
        service_title_rect = service_title.get_rect(center=(self.service_button.centerx, self.service_button.centery - 15))
        surface.blit(service_title, service_title_rect)
        
        service_cost_text = self.font_small.render(f"{service_cost} Coins", True, self.gold_color)
        service_cost_rect = service_cost_text.get_rect(center=(self.service_button.centerx, self.service_button.centery + 10))
        surface.blit(service_cost_text, service_cost_rect)
        
        # Description below
        service_desc = self.font_small.render("Hunt a ghost", True, (200, 200, 200))
        service_desc_rect = service_desc.get_rect(center=(self.service_button.centerx, self.service_button.bottom + 15))
        surface.blit(service_desc, service_desc_rect)
        
        # --- CLOSE BUTTON ---
        self.close_button.centerx = self.x + self.width // 2
        self.close_button.y = self.y + self.height - 45
        
        close_hover = self.close_button.collidepoint(mouse_pos)
        close_color = self.button_hover if close_hover else self.button_color
        
        pygame.draw.rect(surface, close_color, self.close_button, border_radius=5)
        pygame.draw.rect(surface, self.red_color, self.close_button, 2, border_radius=5)
        
        close_text = self.font_small.render("DECLINE", True, self.text_color)
        close_text_rect = close_text.get_rect(center=self.close_button.center)
        surface.blit(close_text, close_text_rect)
    
    def draw_ghost_selection(self, surface, ghosts, service_cost, player_coins):
        """Draw the ghost selection screen with images"""
        # --- TITLE ---
        title = self.font_title.render("SELECT TARGET GHOST", True, self.red_color)
        title_rect = title.get_rect(center=(self.x + self.width//2, self.y + 30))
        surface.blit(title, title_rect)
        
        # --- INSTRUCTION ---
        instruction = self.font_desc.render(f"Choose which ghost to assassinate ({service_cost} coins)", True, self.text_color)
        inst_rect = instruction.get_rect(center=(self.x + self.width//2, self.y + 65))
        surface.blit(instruction, inst_rect)
        
        # --- GHOST LIST ---
        self.ghost_buttons = []
        mouse_pos = pygame.mouse.get_pos()
        
        y_offset = self.y + 110
        available_ghosts = [g for g in ghosts if g.name != "Greed" and g.name != "Pride"]
        
        if not available_ghosts:
            # No targets available
            no_targets = self.font_desc.render("No valid targets available!", True, self.red_color)
            surface.blit(no_targets, (self.x + self.width//2 - no_targets.get_width()//2, y_offset + 50))
        else:
            for i, ghost in enumerate(available_ghosts):
                ghost_rect = pygame.Rect(self.x + 20, y_offset + (i * 60), self.width - 40, 55)
                self.ghost_buttons.append((ghost_rect, ghost))
                
                is_hover = ghost_rect.collidepoint(mouse_pos)
                
                # Background
                bg_color = self.button_hover if is_hover else self.button_color
                pygame.draw.rect(surface, bg_color, ghost_rect, border_radius=8)
                
                # Border with ghost's color (pulsing if hovered)
                if is_hover:
                    pulse = abs(math.sin(self.anim_timer * 0.15))
                    border_width = int(3 + pulse * 2)
                    pygame.draw.rect(surface, ghost.color, ghost_rect, border_width, border_radius=8)
                else:
                    pygame.draw.rect(surface, ghost.color, ghost_rect, 3, border_radius=8)
                
                # Ghost Image
                ghost_img = self.ghost_images.get(ghost.name)
                if ghost_img:
                    img_x = ghost_rect.x + 10
                    img_y = ghost_rect.centery - 20
                    
                    # Add glow effect if hovered
                    if is_hover:
                        glow_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
                        glow_alpha = int(100 + pulse * 100)
                        pygame.draw.circle(glow_surf, (*ghost.color, glow_alpha), (25, 25), 25)
                        surface.blit(glow_surf, (img_x - 5, img_y - 5))
                    
                    surface.blit(ghost_img, (img_x, img_y))
                
                # Ghost name
                name_text = self.font_button.render(ghost.name, True, self.text_color)
                surface.blit(name_text, (ghost_rect.x + 65, ghost_rect.centery - 20))
                
                # Status effects indicator
                status_parts = []
                if hasattr(ghost, 'sleep_timer') and ghost.sleep_timer > 0:
                    status_parts.append("😴 Asleep")
                if hasattr(ghost, 'speed_penalty_timer') and ghost.speed_penalty_timer > 0:
                    status_parts.append("❄️ Slowed")
                if hasattr(ghost, 'fear_timer') and ghost.fear_timer > 0:
                    status_parts.append("😱 Feared")
                if hasattr(ghost, 'confusion_timer') and ghost.confusion_timer > 0:
                    status_parts.append("😵 Confused")
                
                if status_parts:
                    status_str = " | ".join(status_parts)
                    status_text = self.font_small.render(status_str, True, (150, 200, 255))
                    surface.blit(status_text, (ghost_rect.x + 65, ghost_rect.centery + 5))
                else:
                    # Show "Healthy" if no status effects
                    healthy_text = self.font_small.render("✓ Healthy", True, (100, 255, 100))
                    surface.blit(healthy_text, (ghost_rect.x + 65, ghost_rect.centery + 5))
                
                # Click hint on hover
                if is_hover:
                    hint_text = self.font_small.render("► Click to select", True, self.gold_color)
                    surface.blit(hint_text, (ghost_rect.right - hint_text.get_width() - 10, ghost_rect.centery - 6))
        
        # --- BACK BUTTON ---
        back_button = pygame.Rect(self.x + 30, self.y + self.height - 50, 100, 35)
        back_hover = back_button.collidepoint(mouse_pos)
        
        back_color = self.button_hover if back_hover else self.button_color
        pygame.draw.rect(surface, back_color, back_button, border_radius=5)
        pygame.draw.rect(surface, self.gold_color, back_button, 2, border_radius=5)
        
        back_text = self.font_small.render("BACK", True, self.text_color)
        back_text_rect = back_text.get_rect(center=back_button.center)
        surface.blit(back_text, back_text_rect)
        
        # ESC hint
        esc_hint = self.font_small.render("Press ESC to cancel", True, (150, 150, 150))
        surface.blit(esc_hint, (self.x + self.width - esc_hint.get_width() - 30, self.y + self.height - 35))
        
        self.close_button = back_button  # Reuse close button for back
    
    def handle_click(self, mouse_pos, player_coins, mercy_cost, service_cost):
        """
        Handle click events on the dialog
        
        Returns: "MERCY", "SERVICE_SELECT", ("SERVICE", ghost), "CLOSE", or None
        """
        if self.selection_mode:
            # In ghost selection mode
            for rect, ghost in self.ghost_buttons:
                if rect.collidepoint(mouse_pos):
                    self.selected_ghost = ghost
                    self.selection_mode = False
                    return ("SERVICE", ghost)
            
            # Check back button
            if self.close_button.collidepoint(mouse_pos):
                self.selection_mode = False
                return "BACK"
        else:
            # In main menu mode
            if self.mercy_button.collidepoint(mouse_pos):
                if player_coins >= mercy_cost:
                    return "MERCY"
            
            if self.service_button.collidepoint(mouse_pos):
                if player_coins >= service_cost:
                    # Enter selection mode
                    self.selection_mode = True
                    return "SERVICE_SELECT"
            
            if self.close_button.collidepoint(mouse_pos):
                return "CLOSE"
        
        return None