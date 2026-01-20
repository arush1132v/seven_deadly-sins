import os
import wave
import math
import struct
import random

# Configuration matching your Audio Manager
ASSETS_DIR = "assets"
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")

# Sound definitions from your audio_manager.py
# Format: (filename, duration_sec, frequency_hz, type)
sounds_to_generate = [
    # Player
    ("coin.wav", 0.1, 1000, "square"),
    ("item.wav", 0.3, 1200, "sine"),
    ("hurt.wav", 0.3, 200, "saw"),
    ("death.wav", 1.0, 100, "noise"),
    ("dash.wav", 0.2, 600, "slide_down"),
    
    # UI
    ("click.wav", 0.05, 800, "sine"),
    ("hover.wav", 0.02, 1200, "sine"),
    ("menu_open.wav", 0.2, 500, "slide_up"),
    ("purchase.wav", 0.4, 1500, "coin_noise"),
    ("victory.wav", 2.0, 440, "major_chord"),
    
    # Ability/Ghosts
    ("ability.wav", 0.5, 400, "wobble"),
    ("cooldown.wav", 0.1, 200, "sine"),
    ("ghost_spawn.wav", 0.5, 300, "wobble"),
    ("ghost_death.wav", 0.4, 150, "noise"),
    ("sleep.wav", 1.0, 800, "slide_down"),
]

# Music files (just empty placeholders to prevent errors, or simple loops)
music_files = ["music_menu.ogg", "music_game.ogg", "music_boss.ogg"]

def generate_wave(filename, duration, freq, wave_type):
    filepath = os.path.join(SOUNDS_DIR, filename)
    print(f"Generating {filepath}...")
    
    sample_rate = 44100
    n_frames = int(sample_rate * duration)
    
    try:
        with wave.open(filepath, 'w') as obj:
            obj.setnchannels(1) # mono
            obj.setsampwidth(2) # 2 bytes
            obj.setframerate(sample_rate)
            
            for i in range(n_frames):
                t = i / sample_rate
                value = 0
                
                if wave_type == "sine":
                    value = math.sin(2 * math.pi * freq * t)
                elif wave_type == "square":
                    value = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
                elif wave_type == "saw":
                    value = 2.0 * (t * freq - math.floor(t * freq + 0.5))
                elif wave_type == "noise":
                    value = random.uniform(-1, 1)
                elif wave_type == "slide_down":
                    f = freq * (1 - t/duration)
                    value = math.sin(2 * math.pi * f * t)
                elif wave_type == "slide_up":
                    f = freq * (t/duration)
                    value = math.sin(2 * math.pi * f * t)
                elif wave_type == "wobble":
                    f = freq + 50 * math.sin(2 * math.pi * 10 * t)
                    value = math.sin(2 * math.pi * f * t)
                elif wave_type == "major_chord":
                    # Simple arpeggio
                    notes = [1, 1.25, 1.5] # Root, Third, Fifth
                    note_idx = int((t / duration) * 10) % 3
                    f = freq * notes[note_idx]
                    value = math.sin(2 * math.pi * f * t)
                else:
                    value = math.sin(2 * math.pi * freq * t)

                # Volume scaling and conversion to 16-bit integer
                volume = 32767 * 0.5
                data = struct.pack('<h', int(value * volume))
                obj.writeframesraw(data)
                
    except Exception as e:
        print(f"Error generating {filename}: {e}")

def create_dummy_music():
    # We can't easily generate OGG files with standard python lib, 
    # but we can create WAV files and rename them or use WAVs for music temporarily.
    # For now, we'll create empty files so the file checker doesn't crash,
    # OR create silent WAVs.
    
    # Note: pygame.mixer.music supports WAV, so we will generate WAVs 
    # but name them .ogg for the code to find them without editing main.py
    for m in music_files:
        path = os.path.join(MUSIC_DIR, m)
        if not os.path.exists(path):
            print(f"Creating placeholder music: {path}")
            # Generate a 1-second silent wav disguised as ogg
            generate_wave(m, 1.0, 440, "sine") 
            # Move it to music dir (generate_wave defaults to sounds dir)
            src = os.path.join(SOUNDS_DIR, m)
            if os.path.exists(src):
                os.replace(src, path)

def main():
    if not os.path.exists(ASSETS_DIR): os.mkdir(ASSETS_DIR)
    if not os.path.exists(SOUNDS_DIR): os.mkdir(SOUNDS_DIR)
    if not os.path.exists(MUSIC_DIR): os.mkdir(MUSIC_DIR)
    
    for fname, dur, freq, wtype in sounds_to_generate:
        generate_wave(fname, dur, freq, wtype)
        
    create_dummy_music()
    print("Done! Assets generated.")

if __name__ == "__main__":
    main()