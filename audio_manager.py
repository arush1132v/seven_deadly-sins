import pygame
import os
import random

class AudioManager:
    """
    Manages all game audio including music and sound effects.
    Handles missing files gracefully and provides volume controls.
    """
    
    def __init__(self):
        pygame.mixer.init()
        
        # Volume Settings (0.0 to 1.0)
        self.music_volume = 0.5
        self.sfx_volume = 1.0
        
        # Sound Effect Storage
        self.sounds = {}
        
        # Define all sound effects needed
        self.sound_files = {
            # Player Sounds
            "coin": "coin.wav",
            "item": "item.wav",
            "hurt": "hurt.wav",
            "death": "death.wav",
            "dash": "dash.wav",
            
            # Ability Sounds
            "ability_activate": "ability.wav",
            "cooldown": "cooldown.wav",
            
            # Ghost Sounds
            "ghost_spawn": "ghost_spawn.wav",
            "ghost_death": "ghost_death.wav",
            "ghost_sleep": "sleep.wav",
            
            # UI Sounds
            "click": "click.wav",
            "hover": "hover.wav",
            "open": "menu_open.wav",
            "buy": "purchase.wav",
            "level_complete": "victory.wav",
        }
        
        # Music Tracks
        self.music_files = {
            "menu": "music_menu.ogg",
            "gameplay": "music_game.ogg",
            "boss": "music_boss.ogg"
        }
        
        self.current_music = None
        
        # Load sounds immediately
        self.load_assets()

    def load_assets(self):
        """Loads all sound effects from the assets directory"""
        base_path = "assets/sounds"
        music_path = "assets/music"
        
        # Create directories if they don't exist (prevents crashes)
        if not os.path.exists(base_path):
            os.makedirs(base_path, exist_ok=True)
        if not os.path.exists(music_path):
            os.makedirs(music_path, exist_ok=True)
            
        # Load Sound Effects
        for name, filename in self.sound_files.items():
            path = os.path.join(base_path, filename)
            try:
                if os.path.exists(path):
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(self.sfx_volume)
                    self.sounds[name] = sound
                else:
                    print(f"Warning: Sound file missing: {path}")
            except Exception as e:
                print(f"Error loading sound {filename}: {e}")

    def play_sound(self, name):
        """Plays a sound effect by name"""
        if name in self.sounds:
            try:
                self.sounds[name].set_volume(self.sfx_volume)
                self.sounds[name].play()
            except:
                pass

    def play_player_sound(self, action):
        """Convenience method for player sounds"""
        # Map simple actions to internal sound names if needed, 
        # or just pass through if names match keys in self.sounds
        if action in self.sounds:
            self.play_sound(action)

    def play_ui_sound(self, action):
        """Convenience method for UI sounds"""
        if action in self.sounds:
            self.play_sound(action)

    def play_music(self, track_name, loops=-1, fade_ms=0):
        """Plays background music"""
        if track_name == self.current_music and pygame.mixer.music.get_busy():
            return

        filename = self.music_files.get(track_name)
        if not filename:
            return

        path = os.path.join("assets/music", filename)
        if not os.path.exists(path):
            print(f"Warning: Music file missing: {path}")
            return

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            self.current_music = track_name
        except Exception as e:
            print(f"Error playing music {track_name}: {e}")

    def stop_music(self, fade_ms=0):
        pygame.mixer.music.fadeout(fade_ms)
        self.current_music = None

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
            
    def cleanup(self):
        pygame.mixer.quit()