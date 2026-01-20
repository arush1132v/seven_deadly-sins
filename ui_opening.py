import pygame
import random
import math

class GlowingParticle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()
        # Randomize start y so they don't all spawn at bottom initially
        self.y = random.randint(0, height) 

    def reset(self):
        self.x = random.randint(0, self.width)
        self.y = self.height + 10
        self.speed = random.uniform(0.5, 2.5)
        self.radius = random.uniform(2, 4)
        self.drift = random.uniform(-1, 1) # Sideways movement
        self.pulse_speed = random.uniform(0.05, 0.1)
        self.pulse_offset = random.uniform(0, 6.28)
        
        # Color palette: Red/Orange/Purple for "Sins" theme
        colors = [
            (200, 50, 50),   # Red
            (255, 100, 50),  # Orange-ish
            (150, 20, 150),  # Dark Purple
            (100, 100, 100)  # Grey Ash
        ]
        self.color = random.choice(colors)

    def update(self):
        self.y -= self.speed
        self.x += math.sin(self.y * 0.01) * self.drift # Wavy movement
        
        # Reset if off screen
        if self.y < -50:
            self.reset()

    def draw(self, surface, timer):
        # Pulsing size
        current_radius = self.radius + math.sin(timer * self.pulse_speed + self.pulse_offset) * 1.5
        
        # Draw Glow (Outer Layer - very transparent)
        glow_surf = pygame.Surface((int(current_radius * 6), int(current_radius * 6)), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*self.color, 30), (int(current_radius * 3), int(current_radius * 3)), int(current_radius * 3))
        surface.blit(glow_surf, (self.x - current_radius * 3, self.y - current_radius * 3))
        
        # Draw Core (Solid)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(current_radius))

class OpeningSequence:
    def __init__(self, screen, audio_manager):
        self.screen = screen
        self.audio = audio_manager
        self.width, self.height = screen.get_size()
        
        # Fonts
        self.title_font = pygame.font.SysFont("times new roman", 90, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 26, italic=True)
        self.press_key_font = pygame.font.SysFont("arial", 22)
        
        # Colors
        self.TEXT_COLOR = (220, 50, 50) # Crimson
        self.WHITE = (255, 255, 255)
        
        # Pre-render static text
        self.title_surf = self.title_font.render("SEVEN DEADLY SINS", True, self.TEXT_COLOR)
        self.sub_surf = self.subtitle_font.render("Prepare for Judgment...", True, (180, 180, 180))
        
        # Create center rects
        self.title_rect = self.title_surf.get_rect(center=(self.width//2, self.height//2 - 30))
        self.sub_rect = self.sub_surf.get_rect(center=(self.width//2, self.height//2 + 50))
        
        # Initialize Particles
        self.particles = [GlowingParticle(self.width, self.height) for _ in range(70)]
        
        # Create a vignette (dark corners) for atmosphere
        self.vignette = self.create_vignette()

    def create_vignette(self):
        """Creates a dark gradient overlay"""
        vignette = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Simple radial gradient approximation
        for r in range(self.height, 0, -5):
            alpha = int(255 * (1 - (r / self.height))) # Darker at edges
            if alpha > 0:
                # We draw a transparent rectangle to simulate darkness/shadow
                # A proper radial gradient is complex in Pygame without images, 
                # so we will use a simple darkening overlay approach in the loop instead
                pass
        return vignette

    def draw_background(self):
        # Dark blue/black background
        self.screen.fill((10, 5, 15))
        
        # Draw a faint radial glow in the center (simulating a light source)
        center_glow = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(center_glow, (30, 10, 40, 50), (self.width//2, self.height//2), 300)
        self.screen.blit(center_glow, (0,0))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        timer = 0
        waiting_for_key = False
        
        self.audio.play_ui_sound("menu_open") 
        
        while running:
            timer += 1
            
            # 1. Background
            self.draw_background()
            
            # 2. Update & Draw Particles
            for p in self.particles:
                p.update()
                p.draw(self.screen, timer)
            
            # --- TEXT ANIMATION ---
            
            # Floating effect (Sine wave)
            float_offset = math.sin(timer * 0.05) * 8
            
            # Draw Title Shadow (for depth)
            shadow_rect = self.title_rect.copy()
            shadow_rect.x += 4
            shadow_rect.y += 4 + float_offset
            
            shadow_surf = self.title_font.render("SEVEN DEADLY SINS", True, (0, 0, 0))
            shadow_surf.set_alpha(150)
            
            draw_rect = self.title_rect.copy()
            draw_rect.y += float_offset

            # FADING LOGIC
            if timer < 60:
                # Fade in title (simulated by not drawing shadows yet)
                self.screen.blit(self.title_surf, draw_rect)
                
            elif timer < 120:
                self.screen.blit(shadow_surf, shadow_rect)
                self.screen.blit(self.title_surf, draw_rect)
                
                if timer > 80:
                    self.screen.blit(self.sub_surf, self.sub_rect)
            
            else:
                waiting_for_key = True
                self.screen.blit(shadow_surf, shadow_rect)
                self.screen.blit(self.title_surf, draw_rect)
                self.screen.blit(self.sub_surf, self.sub_rect)
                
                # Smooth pulsing "Press Key"
                pulse_val = (math.sin(timer * 0.08) + 1) / 2 # 0.0 to 1.0
                alpha = int(pulse_val * 255)
                
                press_surf = self.press_key_font.render("- PRESS ANY KEY TO CONTINUE -", True, self.WHITE)
                press_surf.set_alpha(alpha)
                press_rect = press_surf.get_rect(center=(self.width//2, self.height - 100))
                self.screen.blit(press_surf, press_rect)

            # --- INPUT ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                if waiting_for_key:
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        self.audio.play_ui_sound("click")
                        return "DONE"
                
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                     timer = 120 # Skip animation

            pygame.display.flip()
            clock.tick(60)