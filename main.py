import pygame
import sys
# --- IMPORTS ---
from ghosts import spawn_ghosts
from abilities import AbilityManager
from ui_selection import AbilitySelectScreen
from ui_hud import HUD
from ui_settings import SettingsScreen
from ui_pause import PauseMenu
from ui_shop import ShopMenu
from ui_level_complete import LevelCompleteMenu
from levels import Map, Camera, TILE_SIZE
from loading_utils import show_loading_transition  # <--- NEW IMPORT

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 600
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect(center=start_pos)
        
        self.base_speed = 4.0 
        self.stats_multiplier = 1.0 
        self.lives = 3 
        self.coins = 0 
        
        self.coin_multiplier = 1
        self.coin_mult_timer = 0
        
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_direction = pygame.math.Vector2(0, 0)
        self.speed_buff_timer = 0
        self.invincible = False
        self.invincible_timer = 0
        self.sloth_penalty_timer = 0 

    def take_damage(self, map_start_pos):
        self.lives -= 1
        if self.lives <= 0: return False
        self.rect.center = map_start_pos 
        self.is_dashing = False
        self.sloth_penalty_timer = 0
        self.invincible = True
        self.invincible_timer = 180 
        return True

    def start_dash(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -1
        if keys[pygame.K_RIGHT]: dx = 1
        if keys[pygame.K_UP]: dy = -1
        if keys[pygame.K_DOWN]: dy = 1
        if dx == 0 and dy == 0: dx = 1
        self.dash_direction = pygame.math.Vector2(dx, dy).normalize()
        self.is_dashing = True
        self.invincible = True
        self.dash_timer = 15 

    def apply_buff(self, buff_type, duration):
        if buff_type == "speed_boost":
            self.speed_buff_timer = duration

    def update(self, walls):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer == 0 and not self.is_dashing: self.invincible = False
            
        if self.coin_mult_timer > 0:
            self.coin_mult_timer -= 1
            if self.coin_mult_timer == 0: self.coin_multiplier = 1

        if self.is_dashing:
            move_speed = (self.base_speed * self.stats_multiplier) * 4
            self.move_and_collide(self.dash_direction.x * move_speed, self.dash_direction.y * move_speed, walls)
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.invincible = False
            return

        current_speed = self.base_speed * self.stats_multiplier
        if self.speed_buff_timer > 0: current_speed *= 1.10
        if self.sloth_penalty_timer > 0: current_speed *= 0.25

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -current_speed
        if keys[pygame.K_RIGHT]: dx = current_speed
        if keys[pygame.K_UP]: dy = -current_speed
        if keys[pygame.K_DOWN]: dy = current_speed

        self.move_and_collide(dx, dy, walls)

    def move_and_collide(self, dx, dy, walls):
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0: self.rect.right = wall.left
                if dx < 0: self.rect.left = wall.right
        
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0: self.rect.bottom = wall.top
                if dy < 0: self.rect.top = wall.bottom

# --- MAIN LOOP ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Seven Deadly Sins: Final")
    clock = pygame.time.Clock()
    
    game_config = {
        "audio": {"music": 0.5, "sfx": 1.0},
        "keybinds": {
            "ability_1": pygame.K_1, "ability_2": pygame.K_2,
            "shop_1": pygame.K_q, "shop_2": pygame.K_e
        }
    }
    
    # Init Objects
    current_level = 1
    game_map = Map(current_level)
    camera = Camera(game_map.width, game_map.height)
    
    player = Player(game_map.start_pos)
    ghosts = spawn_ghosts(300, 300)
    ability_manager = AbilityManager()
    hud = HUD(lambda x: pygame.Surface((50,50)))
    
    # States
    STATE_SELECT, STATE_LOADING, STATE_GAME = 0, 1, 2  # <--- ADDED STATE_LOADING
    STATE_SETTINGS, STATE_PAUSE, STATE_GAMEOVER = 3, 4, 5
    STATE_SHOP, STATE_LEVEL_COMPLETE = 6, 7
    
    current_state = STATE_SELECT
    previous_state = STATE_SELECT
    player_abilities = []
    inventory = [1, 4]

    running = True
    while running:
        if current_state == STATE_GAME:
            camera.update(player)

        # --- ABILITY SELECTION STATE ---
        if current_state == STATE_SELECT:
            sel = AbilitySelectScreen(screen).run()
            if sel: 
                player_abilities = sel
                current_state = STATE_LOADING  # <--- Go to loading screen first
            else: 
                running = False
        
        # --- LOADING TRANSITION STATE (NEW) ---
        elif current_state == STATE_LOADING:
            show_loading_transition(screen, player_abilities)
            current_state = STATE_GAME  # <--- Then start game

        # --- GAMEPLAY ---
        elif current_state == STATE_GAME:
            screen.fill((20, 20, 30))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if hud.is_pause_clicked(event.pos): 
                        current_state = STATE_PAUSE
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        current_state = STATE_PAUSE
                    
                    keys = game_config["keybinds"]
                    if event.key == keys["ability_1"] and player_abilities: 
                        ability_manager.activate(player_abilities[0], player, ghosts)
                    if event.key == keys["ability_2"] and len(player_abilities)>1: 
                        ability_manager.activate(player_abilities[1], player, ghosts)

            player.update(game_map.walls)
            ghosts.update(player, ghosts)

            # --- CHECK EXIT (Go to Level Complete) ---
            if game_map.exit_rect and player.rect.colliderect(game_map.exit_rect):
                print("Level Complete!")
                current_state = STATE_LEVEL_COMPLETE

            # Coins & Items
            for coin in game_map.coins[:]:
                if player.rect.colliderect(coin):
                    game_map.coins.remove(coin)
                    player.coins += (1 * player.coin_multiplier)
            for item in game_map.items[:]:
                if player.rect.colliderect(item["rect"]):
                    game_map.items.remove(item)
                    if item["name"] == "Hourglass":
                         for g in ghosts: g.speed_penalty_timer = 300 
                    elif item["name"] == "Core":
                         player.invincible = True
                         player.invincible_timer = 300

            # Collisions
            if not player.invincible:
                hits = pygame.sprite.spritecollide(player, ghosts, False)
                for ghost in hits:
                    action = ghost.handle_catch()
                    if action == "KILL":
                        if not player.take_damage(game_map.start_pos):
                            current_state = STATE_GAMEOVER
                    elif action == "SPARE":
                         player.rect.x -= 50

            # Draw
            game_map.draw(screen, camera)
            screen.blit(player.image, camera.apply(player))
            for ghost in ghosts:
                screen.blit(ghost.image, camera.apply(ghost))
            hud.draw(screen, player_abilities, inventory, player.lives)

        # --- LEVEL COMPLETE STATE ---
        elif current_state == STATE_LEVEL_COMPLETE:
            menu = LevelCompleteMenu(screen, current_level)
            action = menu.run()
            
            if action == "QUIT": 
                running = False
            elif action == "MENU": 
                running = False
            
            if action == "NEXT" or action == "ABILITY":
                current_level += 1
                game_map = Map(current_level)
                camera = Camera(game_map.width, game_map.height)
                
                player.rect.center = game_map.start_pos
                ghosts = spawn_ghosts(game_map.start_pos[0] + 200, game_map.start_pos[1] + 200)
                
                if action == "NEXT":
                    current_state = STATE_LOADING  # <--- Show loading before next level
                elif action == "ABILITY":
                    current_state = STATE_SELECT

        # --- SHOP STATE ---
        elif current_state == STATE_SHOP:
            shop_ui = ShopMenu(screen)
            item_bought = shop_ui.run(player)
            if item_bought == "QUIT": 
                running = False
            elif item_bought == "BACK": 
                current_state = STATE_PAUSE
            else:
                if item_bought == "crown": 
                    player.invincible = True
                    player.invincible_timer = 600
                elif item_bought == "boots": 
                    player.base_speed *= 1.10
                elif item_bought == "glutton":
                    px, py = player.rect.centerx, player.rect.centery
                    for c in game_map.coins[:]:
                        if abs(c.centerx - px) < TILE_SIZE or abs(c.centery - py) < TILE_SIZE:
                            game_map.coins.remove(c)
                            player.coins += (1 * player.coin_multiplier)
                elif item_bought == "sloth": 
                    for g in ghosts: g.speed_penalty_timer = 900
                elif item_bought == "greed": 
                    player.coin_multiplier = 2
                    player.coin_mult_timer = 1800
                
                current_state = STATE_PAUSE

        # --- PAUSE STATE ---
        elif current_state == STATE_PAUSE:
            result = PauseMenu(screen).run()
            if result == "RESUME": 
                current_state = STATE_GAME
            elif result == "SHOP": 
                current_state = STATE_SHOP
            elif result == "SETTINGS": 
                previous_state = STATE_PAUSE
                current_state = STATE_SETTINGS
            elif result == "MENU": 
                running = False
            elif result == "QUIT": 
                running = False

        # --- SETTINGS STATE ---
        elif current_state == STATE_SETTINGS:
            if SettingsScreen(screen, game_config).run() == "MENU": 
                current_state = previous_state
        
        # --- GAME OVER STATE ---
        elif current_state == STATE_GAMEOVER:
            screen.fill((50, 0, 0))
            t = pygame.font.SysFont("arial", 50).render("GAME OVER - Press R to Restart", True, (255,255,255))
            screen.blit(t, (WIDTH//2 - t.get_width()//2, 250))
            t2 = pygame.font.SysFont("arial", 30).render("Press ESC for Menu", True, (200,200,200))
            screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 320))
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT: 
                    running = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        current_level = 1
                        game_map = Map(1)
                        player = Player(game_map.start_pos)
                        ghosts = spawn_ghosts(300, 300)
                        current_state = STATE_SELECT
                    elif e.key == pygame.K_ESCAPE:
                        running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()