import pygame
import random

# Configuration
TILE_SIZE = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- CAMERA CLASS ---
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)
        x = min(0, max(x, -(self.width - SCREEN_WIDTH)))
        y = min(0, max(y, -(self.height - SCREEN_HEIGHT)))
        self.camera = pygame.Rect(x, y, self.width, self.height)

# --- MAP CLASS ---
class Map:
    def __init__(self, level_num):
        # Scale Map Size based on level
        self.width = 1600 + (level_num * 200) 
        self.height = 1200 + (level_num * 200)
        self.level_num = level_num
        
        self.walls = []
        self.coins = []
        self.items = [] # <--- THIS IS WHAT WAS MISSING!
        self.exit_rect = None
        self.start_pos = (150, 150)
        
        self.generate_level()

    def generate_level(self):
        # 1. Create Borders
        self.walls.append(pygame.Rect(0, 0, self.width, TILE_SIZE)) 
        self.walls.append(pygame.Rect(0, self.height - TILE_SIZE, self.width, TILE_SIZE)) 
        self.walls.append(pygame.Rect(0, 0, TILE_SIZE, self.height)) 
        self.walls.append(pygame.Rect(self.width - TILE_SIZE, 0, TILE_SIZE, self.height)) 

        # 2. Define Exit Area (Bottom Right)
        self.exit_rect = pygame.Rect(self.width - 150, self.height - 150, 40, 40)

        # 3. Generate Random Walls
        rows = self.height // TILE_SIZE
        cols = self.width // TILE_SIZE
        
        # Difficulty: More walls in higher levels
        density = 0.2 + (self.level_num * 0.02) 
        if density > 0.40: density = 0.40 

        for r in range(2, rows - 2):
            for c in range(2, cols - 2):
                x = c * TILE_SIZE
                y = r * TILE_SIZE
                
                # SAFETY ZONES: Don't spawn walls on Start or Exit
                if x < 400 and y < 400: continue
                if x > self.width - 400 and y > self.height - 400: continue
                
                # WALL SPAWN
                if random.random() < density:
                    self.walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                
                # COIN SPAWN
                elif random.random() < 0.05: 
                    self.coins.append(pygame.Rect(x + 15, y + 15, 10, 10))

        # 4. Spawn Special Items (Critical for main.py)
        # Hourglass (Cyan)
        self.items.append({
            "rect": pygame.Rect(100, 300, 30, 30), 
            "color": (0, 255, 255), 
            "name": "Hourglass"
        })
        # Berserker Core (Red)
        self.items.append({
            "rect": pygame.Rect(self.width//2, self.height//2, 30, 30), 
            "color": (255, 0, 0), 
            "name": "Core"
        })
        # Magnet (Silver)
        self.items.append({
            "rect": pygame.Rect(self.width - 200, self.height//2, 30, 30), 
            "color": (192, 192, 192), 
            "name": "Magnet"
        })

    def draw(self, screen, camera):
        # Draw Walls
        for wall in self.walls:
            if camera.camera.colliderect(wall):
                rect = camera.apply_rect(wall)
                pygame.draw.rect(screen, (50, 50, 150), rect) 
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        # Draw Coins
        for coin in self.coins:
            if camera.camera.colliderect(coin):
                rect = camera.apply_rect(coin)
                pygame.draw.circle(screen, (255, 215, 0), rect.center, 8)

        # Draw Special Items
        for item in self.items:
            if camera.camera.colliderect(item["rect"]):
                rect = camera.apply_rect(item["rect"])
                pygame.draw.rect(screen, item["color"], rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 2) 

        # Draw Exit
        if self.exit_rect and camera.camera.colliderect(self.exit_rect):
            rect = camera.apply_rect(self.exit_rect)
            pygame.draw.rect(screen, (0, 255, 0), rect) 
            font = pygame.font.SysFont("arial", 30)
            txt = font.render("E", True, (0,0,0))
            screen.blit(txt, (rect.x + 10, rect.y + 5))