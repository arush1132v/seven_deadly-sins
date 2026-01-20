import pygame
import sys
import time
from ghosts import spawn_ghosts
from abilities import AbilityManager, AbilityEffectTracker
from audio_manager import AudioManager
from ui_selection import AbilitySelectScreen
from ui_hud import EnhancedHUD
from ui_settings import SettingsScreen
from ui_pause import PauseMenu
from ui_shop import ShopMenu
from ui_level_complete import LevelCompleteMenu
from ui_greed_trade import GreedTradeDialog
from levels import Map, Camera, TILE_SIZE
from loading_utils import show_loading_transition
from ui_opening import OpeningSequence
from game_data import get_game_data
from visual_effects import EffectManager, ABILITY_COLORS, ITEM_NAMES

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
        self.stats_multiplier = 1.0  # Affected by John Snow passive
        self.lives = 3 
        self.coins = 0 
        
        self.coin_multiplier = 1.0
        self.coin_mult_timer = 0
        
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_direction = pygame.math.Vector2(0, 0)
        self.speed_buff_timer = 0  # Wolf Vein buff
        self.invincible = False
        self.invincible_timer = 0
        self.sloth_penalty_timer = 0
        
        # Angels Halo dash properties
        self.walls_to_break = None
        self.broken_walls = []
        self.dash_distance = 0

    def take_damage(self, map_start_pos, has_john_snow, ability_manager):
        """Take damage and apply John Snow passive if equipped"""
        self.lives -= 1
        
        # Apply John Snow passive (+3% stats on death)
        if has_john_snow:
            ability_manager.apply_john_snow_passive(self)
        
        if self.lives <= 0: 
            return False
            
        self.rect.center = map_start_pos 
        self.is_dashing = False
        self.sloth_penalty_timer = 0
        self.invincible = True
        self.invincible_timer = 180 
        return True

    def start_dash(self, walls=None):
        """Angels Halo dash ability - dashes 20 blocks and breaks walls"""
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
        self.dash_timer = 30  # Increased for 20 blocks
        self.dash_distance = 600  # 20 blocks * 30 pixels per block
        self.walls_to_break = walls  # Store walls reference
        self.broken_walls = []  # Track walls broken during dash 

    def update(self, walls):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer == 0 and not self.is_dashing: 
                self.invincible = False
            
        if self.coin_mult_timer > 0:
            self.coin_mult_timer -= 1
            if self.coin_mult_timer == 0: 
                self.coin_multiplier = 1.0

        # Handle dash (Angels Halo)
        if self.is_dashing:
            move_speed = 20  # Fast constant speed for dash
            
            # Calculate new position
            new_x = self.rect.x + (self.dash_direction.x * move_speed)
            new_y = self.rect.y + (self.dash_direction.y * move_speed)
            
            # Break walls in path
            if self.walls_to_break:
                dash_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)
                for wall in self.walls_to_break[:]:  # Use slice to avoid modification during iteration
                    if dash_rect.colliderect(wall):
                        self.walls_to_break.remove(wall)
                        self.broken_walls.append(wall)
                        print("💥 Wall destroyed by Angels Halo!")
            
            # Move without collision check during dash
            self.rect.x = int(new_x)
            self.rect.y = int(new_y)
            
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.invincible = False
                self.walls_to_break = None
                print(f"✓ Dash complete! Broke {len(self.broken_walls)} walls")
                self.broken_walls = []
            return

        # Calculate current speed
        current_speed = self.base_speed * self.stats_multiplier
        
        # Wolf Vein speed buff (+10%)
        if self.speed_buff_timer > 0: 
            current_speed *= 1.10
            self.speed_buff_timer -= 1
            
        # Sloth curse (-75%)
        if self.sloth_penalty_timer > 0: 
            current_speed *= 0.25
            self.sloth_penalty_timer -= 1

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


def apply_item_effect(item_id, player, ghosts, game_map, audio):
    """Apply the effect of a shop item"""
    
    if item_id == 1:  # Mirror of Vanity (Pride Clone)
        from ghosts import PrideGhost
        clone = PrideGhost(player.rect.x - 50, player.rect.y)
        ghosts.add(clone)
        clone.lifespan = 900
        print("✓ Pride Clone summoned for 15 seconds!")
        
    elif item_id == 2:  # Bottomless Hunger
        player.coin_multiplier += 0.25
        print(f"✓ Coin multiplier increased to {player.coin_multiplier}x!")
        
    elif item_id == 3:  # Thief's Coin
        stolen = 0
        for ghost in ghosts:
            if ghost.name == "Greed":
                stolen = 50
                player.coins += stolen
                break
        if stolen > 0:
            print(f"✓ Stole {stolen} coins from Greed!")
        else:
            player.coins += 25
            print("✓ Greed not found, but found 25 coins!")
            
    elif item_id == 4:  # Censer of Devil
        for g in ghosts:
            g.sleep_timer = 120
        print("✓ All ghosts stunned for 2 seconds!")
        
    elif item_id == 5:  # Blood Gauntlet
        player.stats_multiplier += 0.10
        player.speed_buff_timer = 300
        print(f"✓ Stats boosted to {player.stats_multiplier * 100}%!")


# --- MAIN LOOP ---
def main(player_points=0, player_inventory=None, game_config=None):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Seven Deadly Sins: Final")
    clock = pygame.time.Clock()
    
    # --- LOAD GAME DATA ---
    game_data = get_game_data()
    
    if game_config is None:
        game_config = game_data.get_settings()
    
    if player_inventory is None:
        player_inventory = game_data.get_inventory()
    
    player_points = game_data.get_points()
    
    print("\n" + "="*50)
    print("💼 POINTS BANK STATUS")
    print("="*50)
    print(f"Current Points Bank: {player_points}")
    
    # GIVE PLAYER 1000 BONUS POINTS IF STARTING FRESH (after restart or first time)
    if player_points == 0:
        player_points = 1000
        game_data.add_points(1000)
        print("🎁 Starting bonus: +1000 points!")
        print("   (This bonus only appears when your points bank is empty)")
        print(f"Points Bank After Bonus: {player_points}")
    
    print("="*50 + "\n")
    
    for key in game_config["keybinds"]:
        game_config["keybinds"][key] = int(game_config["keybinds"][key])

    # Audio Setup
    audio = AudioManager()
    audio.set_music_volume(game_config["audio"]["music"])
    audio.set_sfx_volume(game_config["audio"]["sfx"])
    audio.play_music("gameplay")

    # --- PLAY ANIMATED OPENING ---
    if OpeningSequence(screen, audio).run() == "QUIT":
        audio.cleanup()
        game_data.save()
        pygame.quit()
        return    
    
    # --- MANAGERS ---
    effects = EffectManager()
    greed_dialog = GreedTradeDialog(WIDTH, HEIGHT)
    ability_manager = AbilityManager()
    effect_tracker = AbilityEffectTracker()
    
    # Init Objects
    current_level = 1
    game_map = Map(current_level)
    camera = Camera(game_map.width, game_map.height)
    
    player = Player(game_map.start_pos)
    
    # GIVE PLAYER STARTING COINS IMMEDIATELY
    # Transfer points to coins and add 200 bonus
    starting_coins = player_points + 200
    player.coins = starting_coins
    
    # Deduct points from bank (points become coins for this session)
    game_data.spend_points(player_points)
    
    print(f"💰 Starting with {player.coins} coins")
    print(f"   - {player_points} from your points bank")
    print(f"   - 200 bonus coins")
    print(f"⚠️  Coins spent this session won't return until you restart the game!")
    
    ghosts = spawn_ghosts(300, 300)
    
    def get_shop_item_image(item_id):
        import os
        path = os.path.join("assets", f"item_{item_id}.png")
        try:
            img = pygame.image.load(path)
            return img
        except:
            surf = pygame.Surface((50, 50))
            colors = {1: (148, 0, 211), 2: (210, 105, 30), 3: (255, 223, 0), 
                     4: (0, 255, 255), 5: (220, 20, 60)}
            surf.fill(colors.get(item_id, (100, 100, 100)))
            return surf
    
    hud = EnhancedHUD(get_shop_item_image)
    
    # States
    STATE_SELECT, STATE_LOADING, STATE_GAME = 0, 1, 2
    STATE_SETTINGS, STATE_PAUSE, STATE_GAMEOVER = 3, 4, 5
    STATE_SHOP, STATE_LEVEL_COMPLETE, STATE_GREED_TRADE = 6, 7, 8
    
    current_state = STATE_SELECT
    previous_state = STATE_SELECT
    player_abilities = game_data.get_selected_abilities()
    
    if len(player_abilities) != 2:
        current_state = STATE_SELECT
    else:
        current_state = STATE_LOADING
    
    # Check for John Snow passive
    has_john_snow = "John Snow" in player_abilities
    
    # Greed trade tracking
    greed_ghost = None
    ghost_warning_cooldown = 0
    session_start = time.time()
    game_data.reset_used_items()

    running = True
    while running:
        if current_state == STATE_GAME:
            camera.update(player)
            # Update effect tracker for HUD
            effect_tracker.update(player, ghosts)

        # --- ABILITY SELECTION STATE ---
        if current_state == STATE_SELECT:
            audio.stop_music(fade_ms=500)
            sel = AbilitySelectScreen(screen).run()
            if sel: 
                player_abilities = sel
                game_data.set_selected_abilities(sel)
                has_john_snow = "John Snow" in sel
                current_state = STATE_LOADING
                audio.play_ui_sound("click")
            else: 
                audio.cleanup()
                game_data.save()
                return
        
        # --- LOADING TRANSITION STATE ---
        elif current_state == STATE_LOADING:
            show_loading_transition(screen, player_abilities)
            current_state = STATE_GAME
            audio.play_music("gameplay", fade_ms=1000)

        # --- GAMEPLAY ---
        elif current_state == STATE_GAME:
            screen.fill((20, 20, 30))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    audio.cleanup()
                    session_time = int(time.time() - session_start)
                    game_data.add_playtime(session_time)
                    game_data.save()
                    return
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if hud.is_pause_clicked(event.pos): 
                        current_state = STATE_PAUSE
                        audio.play_ui_sound("click")
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        current_state = STATE_PAUSE
                        audio.play_ui_sound("open")
                    
                    if event.key == pygame.K_F1:
                        print(game_data.get_full_report())
                        print(f"\nCurrent Stats Multiplier: {player.stats_multiplier * 100}%")
                    
                    keys = game_config["keybinds"]
                    
                    # ABILITY 1
                    if event.key == keys["ability_1"] and len(player_abilities) > 0:
                        ability_name = player_abilities[0]
                        now = time.time()
                        last_used = ability_manager.last_used.get(ability_name, 0)
                        cooldown = ability_manager.data[ability_name]["cd"]
                        
                        if now - last_used >= cooldown:
                            ability_manager.activate(ability_name, player, ghosts, game_map.walls)
                            color = ABILITY_COLORS.get(ability_name, (255, 255, 255))
                            effects.add_ability_effect(
                                player.rect.centerx,
                                player.rect.centery,
                                ability_name,
                                color
                            )
                            audio.play_sound("ability_activate")
                            game_data.record_ability_use(ability_name)
                        else:
                            audio.play_sound("cooldown")
                    
                    # ABILITY 2
                    if event.key == keys["ability_2"] and len(player_abilities) > 1:
                        ability_name = player_abilities[1]
                        now = time.time()
                        last_used = ability_manager.last_used.get(ability_name, 0)
                        cooldown = ability_manager.data[ability_name]["cd"]
                        
                        if now - last_used >= cooldown:
                            ability_manager.activate(ability_name, player, ghosts, game_map.walls)
                            color = ABILITY_COLORS.get(ability_name, (255, 255, 255))
                            effects.add_ability_effect(
                                player.rect.centerx,
                                player.rect.centery,
                                ability_name,
                                color
                            )
                            audio.play_sound("ability_activate")
                            game_data.record_ability_use(ability_name)
                        else:
                            audio.play_sound("cooldown")
                    
                    # SHOP ITEM 1 (Q)
                    if event.key == keys["shop_1"]:
                        unused_items = game_data.get_unused_items()
                        if len(unused_items) > 0:
                            item_id = unused_items[0]
                            item_name = ITEM_NAMES.get(item_id, "Unknown Item")
                            effects.add_item_effect(item_id, item_name, WIDTH, HEIGHT)
                            audio.play_sound("item")
                            game_data.use_item(item_id)
                            apply_item_effect(item_id, player, ghosts, game_map, audio)
                    
                    # SHOP ITEM 2 (E)
                    if event.key == keys["shop_2"]:
                        unused_items = game_data.get_unused_items()
                        if len(unused_items) > 1:
                            item_id = unused_items[1]
                            item_name = ITEM_NAMES.get(item_id, "Unknown Item")
                            effects.add_item_effect(item_id, item_name, WIDTH, HEIGHT)
                            audio.play_sound("item")
                            game_data.use_item(item_id)
                            apply_item_effect(item_id, player, ghosts, game_map, audio)

            player.update(game_map.walls)
            ghosts.update(player, ghosts)
            
            # Update ghost lifespans
            for ghost in list(ghosts):
                if hasattr(ghost, 'lifespan'):
                    ghost.lifespan -= 1
                    if ghost.lifespan <= 0:
                        ghost.kill()
                        print("Pride clone vanished!")
            
            # Check for Greed trade opportunity
            greed_ghost = None
            for ghost in ghosts:
                if ghost.name == "Greed" and hasattr(ghost, 'trade_active'):
                    if ghost.trade_active:
                        greed_ghost = ghost
                        current_state = STATE_GREED_TRADE
                        audio.play_ui_sound("hover")
                        break
            
            # Ghost proximity warning
            if ghost_warning_cooldown > 0:
                ghost_warning_cooldown -= 1
            else:
                for ghost in ghosts:
                    if ghost.get_distance(player) < 150:
                        audio.play_sound("ghost_spawn")
                        ghost_warning_cooldown = 120
                        break

            # --- CHECK EXIT ---
            if game_map.exit_rect and player.rect.colliderect(game_map.exit_rect):
                audio.play_sound("level_complete")
                current_state = STATE_LEVEL_COMPLETE

            # Coins & Items
            for coin in game_map.coins[:]:
                if player.rect.colliderect(coin):
                    game_map.coins.remove(coin)
                    coins_gained = int(1 * player.coin_multiplier)
                    player.coins += coins_gained
                    game_data.add_coins_collected(coins_gained)
                    audio.play_player_sound("coin")
                    
            for item in game_map.items[:]:
                if player.rect.colliderect(item["rect"]):
                    game_map.items.remove(item)
                    audio.play_player_sound("item")
                    game_data.add_item_collected()
                    
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
                        audio.play_player_sound("hurt")
                        if not player.take_damage(game_map.start_pos, has_john_snow, ability_manager):
                            audio.play_player_sound("death")
                            game_data.record_death()
                            current_state = STATE_GAMEOVER
                    elif action == "SPARE":
                        player.rect.x -= 50
                    elif action == "GREED_EVENT":
                        pass  # Handled by trade_active flag

            # Draw game world
            game_map.draw(screen, camera)
            screen.blit(player.image, camera.apply(player))
            
            # Draw ghosts with names
            for ghost in ghosts:
                screen.blit(ghost.image, camera.apply(ghost))
                ghost.draw_name(screen, camera)
            
            # Draw HUD
            owned_items = game_data.get_inventory()
            used_items = game_data.data["inventory"]["used_items"]
            
            hud.draw(
                screen,
                abilities=player_abilities,
                owned_items=owned_items,
                used_items=used_items,
                lives=player.lives,
                coins=player.coins,
                ability_manager=ability_manager
            )
            
            # Draw visual effects LAST
            effects.update()
            effects.draw(screen)

        # --- GREED TRADE STATE ---
        elif current_state == STATE_GREED_TRADE:
            # Redraw game scene in background
            screen.fill((20, 20, 30))
            game_map.draw(screen, camera)
            screen.blit(player.image, camera.apply(player))
            for ghost in ghosts:
                screen.blit(ghost.image, camera.apply(ghost))
                ghost.draw_name(screen, camera)
            
            # Draw trade dialog with ghost list
            if greed_ghost:
                hover_info = greed_dialog.draw(
                    screen,
                    player.coins,
                    greed_ghost.cost_spare,
                    greed_ghost.cost_kill_service,
                    ghosts=list(ghosts)  # Pass ghost list for selection
                )
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        audio.cleanup()
                        game_data.save()
                        return
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        result = greed_dialog.handle_click(
                            event.pos,
                            player.coins,
                            greed_ghost.cost_spare,
                            greed_ghost.cost_kill_service
                        )
                        
                        if result == "MERCY":
                            player.coins -= greed_ghost.cost_spare
                            greed_ghost.pay_for_mercy()
                            audio.play_ui_sound("buy")
                            print(f"✓ Paid {greed_ghost.cost_spare} coins for mercy!")
                            current_state = STATE_GAME
                        
                        elif result == "SERVICE_SELECT":
                            # Just entered selection mode, stay in this state
                            audio.play_ui_sound("hover")
                        
                        elif isinstance(result, tuple) and result[0] == "SERVICE":
                            # Player selected a ghost to assassinate
                            target_ghost = result[1]
                            player.coins -= greed_ghost.cost_kill_service
                            greed_ghost.pay_for_service(target_ghost)  # Pass target to Greed
                            audio.play_ui_sound("buy")
                            print(f"✓ Greed is now hunting {target_ghost.name}!")
                            current_state = STATE_GAME
                        
                        elif result == "BACK":
                            # Player went back from selection mode
                            audio.play_ui_sound("click")
                        
                        elif result == "CLOSE":
                            audio.play_ui_sound("click")
                            current_state = STATE_GAME
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        greed_dialog.selection_mode = False
                        current_state = STATE_GAME

        # --- LEVEL COMPLETE STATE ---
        elif current_state == STATE_LEVEL_COMPLETE:
            menu = LevelCompleteMenu(screen, current_level)
            action = menu.run()
            
            game_data.complete_level()
            game_data.update_highest_level(current_level)
            game_data.add_points(player.coins)
            
            if action == "QUIT": 
                audio.cleanup()
                game_data.save()
                return
                
            elif action == "MENU": 
                audio.cleanup()
                game_data.save()
                return
            
            if action == "NEXT" or action == "ABILITY":
                audio.play_ui_sound("click")
                current_level += 1
                game_map = Map(current_level)
                camera = Camera(game_map.width, game_map.height)
                
                player.rect.center = game_map.start_pos
                ghosts = spawn_ghosts(game_map.start_pos[0] + 200, game_map.start_pos[1] + 200)
                
                game_data.reset_used_items()
                effects.clear()
                
                if action == "NEXT":
                    current_state = STATE_LOADING
                elif action == "ABILITY":
                    current_state = STATE_SELECT

        # --- SHOP STATE ---
        elif current_state == STATE_SHOP:
            shop_ui = ShopMenu(screen)
            item_bought = shop_ui.run(player)
            
            if item_bought == "QUIT": 
                audio.cleanup()
                game_data.save()
                return
                
            elif item_bought == "BACK": 
                audio.play_ui_sound("click")
                current_state = STATE_PAUSE
            else:
                audio.play_ui_sound("buy")
                
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
                            player.coins += int(1 * player.coin_multiplier)
                            audio.play_player_sound("coin")
                elif item_bought == "sloth": 
                    for g in ghosts: g.speed_penalty_timer = 900
                elif item_bought == "greed": 
                    player.coin_multiplier = 2
                    player.coin_mult_timer = 1800
                
                current_state = STATE_PAUSE

        # --- PAUSE STATE ---
        elif current_state == STATE_PAUSE:
            result = PauseMenu(screen).run()
            audio.play_ui_sound("click")
            
            if result == "RESUME": 
                current_state = STATE_GAME
            elif result == "SHOP": 
                current_state = STATE_SHOP
            elif result == "SETTINGS": 
                previous_state = STATE_PAUSE
                current_state = STATE_SETTINGS
            elif result == "MENU":
                # Don't add back the starting coins - they're lost until restart
                session_time = int(time.time() - session_start)
                game_data.add_playtime(session_time)
                game_data.save()
                audio.cleanup()
                return
            elif result == "QUIT": 
                game_data.save()
                audio.cleanup()
                pygame.quit()
                sys.exit()

        # --- SETTINGS STATE ---
        elif current_state == STATE_SETTINGS:
            result = SettingsScreen(screen, game_config, audio).run()
            
            if result == "MENU":
                game_data.update_audio(
                    game_config["audio"]["music"],
                    game_config["audio"]["sfx"]
                )
                for action, key in game_config["keybinds"].items():
                    game_data.update_keybind(action, key)
                
                current_state = previous_state
            
            elif result == "RESTART_GAME":
                # Restart the entire game
                game_data.restart_game()
                audio.play_ui_sound("click")
                
                # Reload fresh data
                game_data.load()
                
                # Return to launcher/main menu
                audio.cleanup()
                return
        
        # --- GAME OVER STATE ---
        elif current_state == STATE_GAMEOVER:
            audio.stop_music(fade_ms=500)
                
            screen.fill((50, 0, 0))
            t = pygame.font.SysFont("arial", 50).render("GAME OVER - Press R to Restart", True, (255,255,255))
            screen.blit(t, (WIDTH//2 - t.get_width()//2, 250))
            t2 = pygame.font.SysFont("arial", 30).render("Press ESC for Menu", True, (200,200,200))
            screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 320))
            
            # Show final stats
            stats_text = pygame.font.SysFont("arial", 20).render(
                f"Final Stats Multiplier: {player.stats_multiplier * 100:.1f}%", 
                True, (200, 240, 255)
            )
            screen.blit(stats_text, (WIDTH//2 - stats_text.get_width()//2, 380))
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    game_data.save()
                    audio.cleanup()
                    return
                    
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        audio.play_ui_sound("click")
                        current_level = 1
                        game_map = Map(1)
                        player = Player(game_map.start_pos)
                        player.coins = game_data.get_points() + 200  # Add 200 bonus coins
                        ghosts = spawn_ghosts(300, 300)
                        game_data.reset_used_items()
                        effects.clear()
                        current_state = STATE_SELECT
                        audio.play_music("gameplay")
                    elif e.key == pygame.K_ESCAPE:
                        session_time = int(time.time() - session_start)
                        game_data.add_playtime(session_time)
                        game_data.save()
                        audio.cleanup()
                        return

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()