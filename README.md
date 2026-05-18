# Seven Deadly Sins: Pac-Man Reborn

### A Roguelike Arcade Experience with Strategic Depth

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-00A67E.svg?style=flat&logo=pygame&logoColor=white)](https://www.pygame.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=flat)](https://github.com/YourUsername/SevenDeadlySinsPacman)

<p align="center">
  <img src="https://via.placeholder.com/800x300/1a1a2e/ffffff?text=Seven+Deadly+Sins+Pac-Man" alt="Game Banner"/>
</p>

<p align="center">
  <strong>A sophisticated reimagining of the arcade classic, featuring advanced AI, dynamic environments, and strategic gameplay mechanics.</strong>
</p>

---

## 📖 Table of Contents
- [About](#-about)
- [Features](#-features)
- [The Seven Sins](#-the-seven-sins)
- [Abilities](#-player-abilities)
- [Items](#-items)
- [Installation](#-installation)
- [Controls](#-controls)
- [Gameplay Tips](#-gameplay-tips)
- [Project Structure](#-project-structure)
- [Credits](#-credits)

---

## Overview

Seven Deadly Sins: Pac-Man Reborn is a modern take on the classic arcade formula, incorporating roguelike elements, advanced artificial intelligence, and RPG-inspired progression systems. Each adversary represents one of the seven deadly sins, featuring unique behavioral patterns and strategic challenges that require careful planning and execution.

### Key Highlights

- **Adaptive AI System**: Seven distinct enemy archetypes, each with sophisticated pathfinding and behavioral patterns
- **Dynamic Difficulty Scaling**: Progressive level design across 10 carefully crafted stages
- **Environmental Systems**: Real-time day/night cycle affecting gameplay mechanics and visual presentation
- **Persistent Progression**: RPG-style character advancement and resource management
- **Strategic Depth**: Multi-layered combat system with abilities, items, and environmental interactions

---

## Technical Features

### Architecture & Systems

#### Core Gameplay
- **Procedural Map Generation**: Algorithm-driven maze creation with configurable parameters
- **Advanced Camera System**: Smooth interpolation with viewport culling for performance optimization
- **Real-time Physics**: Collision detection, momentum-based movement, and environmental interactions
- **State Machine Architecture**: Clean separation of game states (menu, gameplay, pause, shop)

#### AI Implementation
- **Pathfinding**: A* algorithm with dynamic obstacle avoidance
- **Behavioral Trees**: Individual decision-making systems for each enemy archetype
- **Status Effect System**: Temporal debuffs affecting movement, targeting, and decision-making
- **Inter-enemy Interactions**: Complex relationship systems between different sin types

#### Visual Systems
- **Particle Engine**: Real-time particle effects for abilities, environmental interactions, and feedback
- **Animation Framework**: Sprite-based animation with interpolation and state blending
- **Dynamic Lighting**: Day/night cycle with ambient lighting adjustments
- **Post-processing Effects**: Screen shake, color grading, and overlay systems

#### Progression & Economy
- **Dual Currency System**: Points (meta) and coins (in-game) with balanced exchange rates
- **Upgrade Trees**: Permanent and temporary enhancement systems
- **Inventory Management**: Item acquisition, storage, and activation mechanics
- **Save System**: JSON-based serialization with data validation

---

## Enemy Archetypes: The Seven Deadly Sins

Each adversary represents a unique challenge, requiring distinct strategies and counterplay.

### Pride | The Apex Predator
```
Classification: Elite Enemy
Movement Speed: 150% base
Unique Mechanic: Damage immunity, grants player additional lives
```
**Behavioral Pattern**: Exhibits unwavering pursuit with optimal pathfinding. Cannot be eliminated through conventional means. Paradoxically grants three additional life chances due to its prideful nature, considering the player unworthy of immediate defeat.

**Strategic Counter**: Evasion and defensive abilities. Utilize terrain advantages and speed enhancements.

---

### Greed | The Negotiator
```
Classification: Merchant Enemy
Movement Speed: 100% base
Unique Mechanic: Transaction system, mercenary services
```
**Behavioral Pattern**: Upon capture, initiates a negotiation sequence. Offers two transaction options:
- Personal clemency: 100 coins (escalating cost)
- Assassination contract: 200 coins (targets other enemies)

**Strategic Counter**: Maintain sufficient coin reserves. Utilize for strategic enemy elimination.

**Reward on Elimination**: 5% stat acquisition from any defeated enemy (applicable to all archetypes)

---

### Lust | The Relentless
```
Classification: Pursuit Enemy  
Movement Speed: 75% base
Unique Mechanic: Unwavering focus, no pause states
```
**Behavioral Pattern**: Continuous pursuit without interruption. Lower base speed compensated by predictable movement patterns.

**Strategic Counter**: Maintain distance. Low-priority threat compared to faster enemies.

**Reward on Elimination**: Hypnosis ability—converts any enemy into a temporary ally for 45 seconds

---

### Envy | The Saboteur
```
Classification: Chaos Enemy
Movement Speed: 100% base
Unique Mechanic: Friendly fire, betrayal mechanics
```
**Behavioral Pattern**: 
- 25% probability to incapacitate allied enemies (10-second stun)
- 10% probability to eliminate allied enemies
- Exception: Pride will eliminate Envy if betrayed

**Strategic Counter**: Allow Envy to create favorable situations. Minimal direct engagement required.

**Reward on Elimination**: Forced combat between two nearest enemies (elimination outcome based on hierarchy)

---

### Gluttony | The Standard
```
Classification: Basic Enemy
Movement Speed: 100% base
Unique Mechanic: None
```
**Behavioral Pattern**: Standard chase behavior with predictable pathfinding.

**Strategic Counter**: Classic evasion tactics. Baseline difficulty.

**Reward on Elimination**: Standard point value

---

### Wrath | The Berserker
```
Classification: Speed-Variable Enemy
Movement Speed: 110% (linear paths) / 100% (corners)
Unique Mechanic: Directional speed variance, error-prone navigation
```
**Behavioral Pattern**: Accelerated movement in straight corridors. 25% error rate in pathfinding decisions. Inflicts incidental damage to other enemies in pursuit path.

**Strategic Counter**: Force corner-intensive navigation. Exploit pathfinding errors.

**Reward on Elimination**: Berserk curse—target fights all enemies for 45 seconds before self-termination

---

### Sloth | The Ambusher  
```
Classification: Area-Denial Enemy
Movement Speed: 0% (dormant) / 100% (active)
Unique Mechanic: Proximity activation, area debuffs
```
**Behavioral Pattern**: Remains stationary until player enters activation radius. Applies movement speed debuff (-75%) for 5 seconds to player and two random enemies.

**Strategic Counter**: Avoid activation radius. Maintain awareness of positioning.

**Reward on Elimination**: Permanent incapacitation ability for any single enemy (reactivates after 10 seconds if contacted)

---

## Player Ability System

Players select two abilities from five available options at game initialization. Abilities operate on cooldown-based systems with distinct tactical applications.

### Wolf Vein
```yaml
Type: Self-Enhancement
Effect: +10% movement speed
Duration: 5 seconds
Cooldown: 15 seconds
```
**Tactical Application**: Rapid repositioning, coin collection efficiency, emergency evasion

---

### Dragon Heart
```yaml
Type: Crowd Control (Single Target)
Effect: Fear status (50% speed reduction)
Target: Nearest enemy
Duration: 3 seconds
Cooldown: 15 seconds
```
**Tactical Application**: Pursuit interruption, creates engagement opportunities, defensive utility

---

### Demon Eye
```yaml
Type: Manipulation
Effect: Confusion status (attacks other enemies)
Target: Nearest enemy
Duration: 5 seconds
Cooldown: 20 seconds
```
**Tactical Application**: Enemy elimination through proxy, crowd management, strategic chaos

---

### Angel's Halo
```yaml
Type: Mobility/Invulnerability
Effect: Invulnerable dash, obstacle destruction
Direction: Movement input-based
Duration: Instantaneous
Cooldown: 15 seconds
```
**Tactical Application**: Emergency escape, wall-breaking, aggressive positioning

---

### John Snow (Passive)
```yaml
Type: Scaling Passive
Effect: +3% all stats per death
Trigger: Player elimination
Stacks: Unlimited
```
**Tactical Application**: Long-term progression, compensates for learning curve, endgame scaling

---

## Economy & Item Systems

### Dual Currency Model

**Points (Meta-Currency)**
- Persistent across sessions
- Acquired through level completion
- Used for pre-game permanent upgrades

**Coins (Session Currency)**
- Collected during gameplay
- Used for mid-game tactical purchases
- Resets between levels

### Pre-Game Shop (Points)

| Item | Cost | Effect |
|------|------|--------|
| Mirror of Vanity | 100 | Summons Pride clone for area denial (15s) |
| Bottomless Hunger | 40 | +25% coin value multiplier (permanent) |
| Thief's Coin | 80 | Acquire 25% of Greed's coin reserves |
| Censer of Devil | 50 | Global enemy stun (2s) |
| Blood Gauntlet | 100 | +10% all stats (5s) |

### Mid-Game Shop (Coins)

| Item | Cost | Effect |
|------|------|--------|
| Prideful Crown | 50 | Invulnerability state (10s, cannot eliminate enemies) |
| Boots of Envious | 100 | +10% movement speed (level duration) |
| Glutton's Belly | 20 | Collect all coins in perpendicular axes |
| Sloth's Tranquilizer | 40 | 50% global enemy speed reduction (15s) |
| Greed's Double-Down | 15 | 2x coin acquisition rate (30s) |

### Dynamic Spawn Items

These items appear procedurally during gameplay:

**Golden Hourglass**
- Effect: Global enemy freeze (5s)
- Spawn: Random corner locations

**Berserker's Core**
- Effect: +50% speed, damage reflection (8s)
- Spawn: Ghost spawn zone entrance

**Magnet Stone**
- Effect: Automatic coin collection (3-tile radius, 10s)
- Spawn: Map perimeter

**Phantom Cloak**
- Effect: Phase through enemies (6s, cannot eliminate)
- Spawn: Last player elimination location

**Feast Cake**
- Effect: +25% coin value increase (level duration)
- Spawn: Map center

---

## Installation & Configuration

### System Requirements

**Minimum Specifications**
- Python 3.9 or higher
- 512MB RAM
- 100MB available storage
- OpenGL 2.0 compatible graphics

**Recommended Specifications**
- Python 3.11+
- 1GB RAM
- Dedicated graphics card
- 1920x1080 display resolution

### Installation Process

#### Method 1: Standard Installation

```bash
# Clone repository
git clone https://github.com/YourUsername/SevenDeadlySinsPacman.git
cd SevenDeadlySinsPacman

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch application
python launcher.py
```

#### Method 2: Development Installation

```bash
# Clone with development branch
git clone -b develop https://github.com/YourUsername/SevenDeadlySinsPacman.git
cd SevenDeadlySinsPacman

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Launch with debugging
python launcher.py --debug
```

### Configuration

Create a `config.ini` file in the root directory for custom settings:

```ini
[Display]
width = 800
height = 600
fullscreen = false
vsync = true

[Audio]
master_volume = 0.8
music_volume = 0.7
sfx_volume = 0.9

[Gameplay]
difficulty = normal
show_fps = false
particle_density = high
```

### Troubleshooting

**Common Issues**

| Issue | Solution |
|-------|----------|
| Audio not playing | Install `python-mpg123` package |
| Low frame rate | Reduce particle density in settings |
| Save file corruption | Delete `saves/game_data.json`, restart |
| Import errors | Verify all dependencies installed via `pip list` |

**Debug Mode**

Launch with debug flags for diagnostic information:
```bash
python launcher.py --debug --verbose --log-level DEBUG
```

---

## Input Configuration

### Default Keybindings

#### Movement Controls
| Input | Action |
|-------|--------|
| `↑` `↓` `←` `→` | Directional movement (Arrow keys) |
| `W` `A` `S` `D` | Alternative directional movement |

#### Ability Activation
| Input | Action |
|-------|--------|
| `1` | Primary ability activation |
| `2` | Secondary ability activation |
| `Q` | Consumable item slot 1 |
| `E` | Consumable item slot 2 |

#### System Controls
| Input | Action |
|-------|--------|
| `ESC` | Pause menu / Cancel |
| `F1` | Display game statistics |
| `F11` | Toggle fullscreen |
| `Tab` | Map overview (if unlocked) |

#### Debug Commands (Development Build)
| Input | Action |
|-------|--------|
| `F3` | Display debug overlay |
| `F4` | Toggle hitbox visualization |
| `F5` | Quick save state |
| `F9` | Quick load state |

### Customization

Keybindings can be reconfigured through:
1. In-game settings menu
2. Manual `config.ini` editing
3. Command-line arguments: `python launcher.py --keybind-preset=wasd`

---

## Strategic Guidelines

### Beginner Optimization

**Ability Selection**
- Recommended pairing: Wolf Vein + Dragon Heart
- Prioritizes survivability and mobility
- Low skill floor for learning core mechanics

**Early Game Strategy**
1. Master basic movement and collision mechanics
2. Identify enemy spawn patterns
3. Maintain coin acquisition efficiency
4. Avoid Pride encounters until comfortable with evasion

**Resource Management**
- Prioritize point spending on Bottomless Hunger (40pts) for economy scaling
- Reserve coins for Greed's Double-Down (15 coins) early-game multiplier
- Use abilities proactively rather than reactively

### Advanced Tactics

**Ability Synergies**
- John Snow + Demon Eye: Scales into late-game dominance
- Angel's Halo + Wolf Vein: Aggressive positioning and map control
- Dragon Heart + Demon Eye: Enemy manipulation and crowd control

**Greed Manipulation**
- Maintain 200+ coin reserve for strategic assassinations
- Target elimination priority: Wrath → Sloth → Lust
- Negotiate for self-preservation only when cornered

**Environmental Exploitation**
- Utilize Envy's betrayal mechanics for passive enemy reduction
- Position near Sloth during day cycle for debuff avoidance
- Leverage Pride's predictable pathfinding for coin collection routes

**Day/Night Optimization**
- **Day Phase** (Player +10%): Aggressive coin collection, Pride evasion
- **Night Phase** (Enemies +10%): Defensive positioning, ability conservation
- Plan major movements during favorable cycle phases

### Level-Specific Strategies

**Levels 1-3: Foundation Phase**
- Focus: Mechanical mastery and economy establishment
- Objective: Collect 80%+ coins, minimize deaths
- Ability usage: Conservative, emergency-only

**Levels 4-6: Scaling Phase**
- Focus: Permanent upgrade acquisition, enemy prioritization
- Objective: Eliminate non-Pride enemies when advantageous
- Ability usage: Proactive enemy manipulation

**Levels 7-9: Optimization Phase**
- Focus: Efficiency maximization, risk/reward evaluation
- Objective: Complete secondary objectives, stack John Snow passive
- Ability usage: Aggressive positioning and map control

**Level 10: Culmination**
- Focus: All systems active, maximum difficulty
- Objective: Survival and objective completion
- Ability usage: Reactive adaptation to dynamic threat assessment

---

## 📂 Project Structure

```
SevenDeadlySinsPacman/
│
├── launcher.py              # Main menu, profile, settings
├── main.py                  # Core game loop
├── player.py                # Player class and mechanics
├── ghosts.py                # AI for all 7 deadly sins
├── abilities.py             # Ability system and effects
├── levels.py                # Map generation and objectives
├── shop.py                  # Shop UI and transactions
├── game_data.py             # Save/load system
├── audio_manager.py         # Sound and music
├── day_night_system.py      # Day/night cycle logic
│
├── ui_*.py                  # Various UI screens
│   ├── ui_hud.py           # In-game HUD
│   ├── ui_pause.py         # Pause menu
│   ├── ui_settings.py      # Settings screen
│   ├── ui_shop.py          # Shop interface
│   └── ...
│
├── assets/                  # Game assets
│   ├── audio/              # Sound effects and music
│   ├── *.png               # Sprites and icons
│   └── fonts/              # Custom fonts
│
├── saves/                   # Player save files
│   └── game_data.json      # Persistent game data
│
├── README.md               # You are here!
└── requirements.txt        # Python dependencies
```

---

## 🗺️ Roadmap

### Completed ✅
- [x] Core gameplay loop
- [x] All 7 sins with unique AI
- [x] Day/night cycle system
- [x] Shop and inventory system
- [x] Save/load functionality
- [x] 5 unique abilities
- [x] Dynamic camera system
- [x] 10 progressive levels

### In Progress 🚧
- [ ] Interactive tutorial with particle effects
- [ ] Level objective system refinements
- [ ] Boss battle mechanics
- [ ] Achievement system

### Planned 📋
- [ ] Endless mode
- [ ] Custom skins and cosmetics
- [ ] Online leaderboards
- [ ] Virtue power-ups (counter to sins)
- [ ] New game+ mode with harder challenges
- [ ] Mobile port

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas We Need Help
- Sound effects and music composition
- Sprite art for items and ghosts
- Balance testing
- Bug reporting
- Documentation improvements

---

## 🐛 Known Issues

- Camera can occasionally stutter on very large maps
- Audio may not play on some Linux distributions
- Ghost pathfinding can get stuck in rare maze configurations

Report issues at: [GitHub Issues](# Seven Deadly Sins: Pac-Man Reborn

### A Roguelike Arcade Experience with Strategic Depth

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-00A67E.svg?style=flat&logo=pygame&logoColor=white)](https://www.pygame.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=flat)](https://github.com/YourUsername/SevenDeadlySinsPacman)

<p align="center">
  <img src="https://via.placeholder.com/800x300/1a1a2e/ffffff?text=Seven+Deadly+Sins+Pac-Man" alt="Game Banner"/>
</p>

<p align="center">
  <strong>A sophisticated reimagining of the arcade classic, featuring advanced AI, dynamic environments, and strategic gameplay mechanics.</strong>
</p>

---

## 📖 Table of Contents
- [About](#-about)
- [Features](#-features)
- [The Seven Sins](#-the-seven-sins)
- [Abilities](#-player-abilities)
- [Items](#-items)
- [Installation](#-installation)
- [Controls](#-controls)
- [Gameplay Tips](#-gameplay-tips)
- [Project Structure](#-project-structure)
- [Credits](#-credits)

---

## Overview

Seven Deadly Sins: Pac-Man Reborn is a modern take on the classic arcade formula, incorporating roguelike elements, advanced artificial intelligence, and RPG-inspired progression systems. Each adversary represents one of the seven deadly sins, featuring unique behavioral patterns and strategic challenges that require careful planning and execution.

### Key Highlights

- **Adaptive AI System**: Seven distinct enemy archetypes, each with sophisticated pathfinding and behavioral patterns
- **Dynamic Difficulty Scaling**: Progressive level design across 10 carefully crafted stages
- **Environmental Systems**: Real-time day/night cycle affecting gameplay mechanics and visual presentation
- **Persistent Progression**: RPG-style character advancement and resource management
- **Strategic Depth**: Multi-layered combat system with abilities, items, and environmental interactions

---

## Technical Features

### Architecture & Systems

#### Core Gameplay
- **Procedural Map Generation**: Algorithm-driven maze creation with configurable parameters
- **Advanced Camera System**: Smooth interpolation with viewport culling for performance optimization
- **Real-time Physics**: Collision detection, momentum-based movement, and environmental interactions
- **State Machine Architecture**: Clean separation of game states (menu, gameplay, pause, shop)

#### AI Implementation
- **Pathfinding**: A* algorithm with dynamic obstacle avoidance
- **Behavioral Trees**: Individual decision-making systems for each enemy archetype
- **Status Effect System**: Temporal debuffs affecting movement, targeting, and decision-making
- **Inter-enemy Interactions**: Complex relationship systems between different sin types

#### Visual Systems
- **Particle Engine**: Real-time particle effects for abilities, environmental interactions, and feedback
- **Animation Framework**: Sprite-based animation with interpolation and state blending
- **Dynamic Lighting**: Day/night cycle with ambient lighting adjustments
- **Post-processing Effects**: Screen shake, color grading, and overlay systems

#### Progression & Economy
- **Dual Currency System**: Points (meta) and coins (in-game) with balanced exchange rates
- **Upgrade Trees**: Permanent and temporary enhancement systems
- **Inventory Management**: Item acquisition, storage, and activation mechanics
- **Save System**: JSON-based serialization with data validation

---

## Enemy Archetypes: The Seven Deadly Sins

Each adversary represents a unique challenge, requiring distinct strategies and counterplay.

### Pride | The Apex Predator
```
Classification: Elite Enemy
Movement Speed: 150% base
Unique Mechanic: Damage immunity, grants player additional lives
```
**Behavioral Pattern**: Exhibits unwavering pursuit with optimal pathfinding. Cannot be eliminated through conventional means. Paradoxically grants three additional life chances due to its prideful nature, considering the player unworthy of immediate defeat.

**Strategic Counter**: Evasion and defensive abilities. Utilize terrain advantages and speed enhancements.

---

### Greed | The Negotiator
```
Classification: Merchant Enemy
Movement Speed: 100% base
Unique Mechanic: Transaction system, mercenary services
```
**Behavioral Pattern**: Upon capture, initiates a negotiation sequence. Offers two transaction options:
- Personal clemency: 100 coins (escalating cost)
- Assassination contract: 200 coins (targets other enemies)

**Strategic Counter**: Maintain sufficient coin reserves. Utilize for strategic enemy elimination.

**Reward on Elimination**: 5% stat acquisition from any defeated enemy (applicable to all archetypes)

---

### Lust | The Relentless
```
Classification: Pursuit Enemy  
Movement Speed: 75% base
Unique Mechanic: Unwavering focus, no pause states
```
**Behavioral Pattern**: Continuous pursuit without interruption. Lower base speed compensated by predictable movement patterns.

**Strategic Counter**: Maintain distance. Low-priority threat compared to faster enemies.

**Reward on Elimination**: Hypnosis ability—converts any enemy into a temporary ally for 45 seconds

---

### Envy | The Saboteur
```
Classification: Chaos Enemy
Movement Speed: 100% base
Unique Mechanic: Friendly fire, betrayal mechanics
```
**Behavioral Pattern**: 
- 25% probability to incapacitate allied enemies (10-second stun)
- 10% probability to eliminate allied enemies
- Exception: Pride will eliminate Envy if betrayed

**Strategic Counter**: Allow Envy to create favorable situations. Minimal direct engagement required.

**Reward on Elimination**: Forced combat between two nearest enemies (elimination outcome based on hierarchy)

---

### Gluttony | The Standard
```
Classification: Basic Enemy
Movement Speed: 100% base
Unique Mechanic: None
```
**Behavioral Pattern**: Standard chase behavior with predictable pathfinding.

**Strategic Counter**: Classic evasion tactics. Baseline difficulty.

**Reward on Elimination**: Standard point value

---

### Wrath | The Berserker
```
Classification: Speed-Variable Enemy
Movement Speed: 110% (linear paths) / 100% (corners)
Unique Mechanic: Directional speed variance, error-prone navigation
```
**Behavioral Pattern**: Accelerated movement in straight corridors. 25% error rate in pathfinding decisions. Inflicts incidental damage to other enemies in pursuit path.

**Strategic Counter**: Force corner-intensive navigation. Exploit pathfinding errors.

**Reward on Elimination**: Berserk curse—target fights all enemies for 45 seconds before self-termination

---

### Sloth | The Ambusher  
```
Classification: Area-Denial Enemy
Movement Speed: 0% (dormant) / 100% (active)
Unique Mechanic: Proximity activation, area debuffs
```
**Behavioral Pattern**: Remains stationary until player enters activation radius. Applies movement speed debuff (-75%) for 5 seconds to player and two random enemies.

**Strategic Counter**: Avoid activation radius. Maintain awareness of positioning.

**Reward on Elimination**: Permanent incapacitation ability for any single enemy (reactivates after 10 seconds if contacted)

---

## Player Ability System

Players select two abilities from five available options at game initialization. Abilities operate on cooldown-based systems with distinct tactical applications.

### Wolf Vein
```yaml
Type: Self-Enhancement
Effect: +10% movement speed
Duration: 5 seconds
Cooldown: 15 seconds
```
**Tactical Application**: Rapid repositioning, coin collection efficiency, emergency evasion

---

### Dragon Heart
```yaml
Type: Crowd Control (Single Target)
Effect: Fear status (50% speed reduction)
Target: Nearest enemy
Duration: 3 seconds
Cooldown: 15 seconds
```
**Tactical Application**: Pursuit interruption, creates engagement opportunities, defensive utility

---

### Demon Eye
```yaml
Type: Manipulation
Effect: Confusion status (attacks other enemies)
Target: Nearest enemy
Duration: 5 seconds
Cooldown: 20 seconds
```
**Tactical Application**: Enemy elimination through proxy, crowd management, strategic chaos

---

### Angel's Halo
```yaml
Type: Mobility/Invulnerability
Effect: Invulnerable dash, obstacle destruction
Direction: Movement input-based
Duration: Instantaneous
Cooldown: 15 seconds
```
**Tactical Application**: Emergency escape, wall-breaking, aggressive positioning

---

### John Snow (Passive)
```yaml
Type: Scaling Passive
Effect: +3% all stats per death
Trigger: Player elimination
Stacks: Unlimited
```
**Tactical Application**: Long-term progression, compensates for learning curve, endgame scaling

---

## Economy & Item Systems

### Dual Currency Model

**Points (Meta-Currency)**
- Persistent across sessions
- Acquired through level completion
- Used for pre-game permanent upgrades

**Coins (Session Currency)**
- Collected during gameplay
- Used for mid-game tactical purchases
- Resets between levels

### Pre-Game Shop (Points)

| Item | Cost | Effect |
|------|------|--------|
| Mirror of Vanity | 100 | Summons Pride clone for area denial (15s) |
| Bottomless Hunger | 40 | +25% coin value multiplier (permanent) |
| Thief's Coin | 80 | Acquire 25% of Greed's coin reserves |
| Censer of Devil | 50 | Global enemy stun (2s) |
| Blood Gauntlet | 100 | +10% all stats (5s) |

### Mid-Game Shop (Coins)

| Item | Cost | Effect |
|------|------|--------|
| Prideful Crown | 50 | Invulnerability state (10s, cannot eliminate enemies) |
| Boots of Envious | 100 | +10% movement speed (level duration) |
| Glutton's Belly | 20 | Collect all coins in perpendicular axes |
| Sloth's Tranquilizer | 40 | 50% global enemy speed reduction (15s) |
| Greed's Double-Down | 15 | 2x coin acquisition rate (30s) |

### Dynamic Spawn Items

These items appear procedurally during gameplay:

**Golden Hourglass**
- Effect: Global enemy freeze (5s)
- Spawn: Random corner locations

**Berserker's Core**
- Effect: +50% speed, damage reflection (8s)
- Spawn: Ghost spawn zone entrance

**Magnet Stone**
- Effect: Automatic coin collection (3-tile radius, 10s)
- Spawn: Map perimeter

**Phantom Cloak**
- Effect: Phase through enemies (6s, cannot eliminate)
- Spawn: Last player elimination location

**Feast Cake**
- Effect: +25% coin value increase (level duration)
- Spawn: Map center

---

## Installation & Configuration

### System Requirements

**Minimum Specifications**
- Python 3.9 or higher
- 512MB RAM
- 100MB available storage
- OpenGL 2.0 compatible graphics

**Recommended Specifications**
- Python 3.11+
- 1GB RAM
- Dedicated graphics card
- 1920x1080 display resolution

### Installation Process

#### Method 1: Standard Installation

```bash
# Clone repository
git clone https://github.com/YourUsername/SevenDeadlySinsPacman.git
cd SevenDeadlySinsPacman

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch application
python launcher.py
```

#### Method 2: Development Installation

```bash
# Clone with development branch
git clone -b develop https://github.com/YourUsername/SevenDeadlySinsPacman.git
cd SevenDeadlySinsPacman

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Launch with debugging
python launcher.py --debug
```

### Configuration

Create a `config.ini` file in the root directory for custom settings:

```ini
[Display]
width = 800
height = 600
fullscreen = false
vsync = true

[Audio]
master_volume = 0.8
music_volume = 0.7
sfx_volume = 0.9

[Gameplay]
difficulty = normal
show_fps = false
particle_density = high
```

### Troubleshooting

**Common Issues**

| Issue | Solution |
|-------|----------|
| Audio not playing | Install `python-mpg123` package |
| Low frame rate | Reduce particle density in settings |
| Save file corruption | Delete `saves/game_data.json`, restart |
| Import errors | Verify all dependencies installed via `pip list` |

**Debug Mode**

Launch with debug flags for diagnostic information:
```bash
python launcher.py --debug --verbose --log-level DEBUG
```

---

## Input Configuration

### Default Keybindings

#### Movement Controls
| Input | Action |
|-------|--------|
| `↑` `↓` `←` `→` | Directional movement (Arrow keys) |
| `W` `A` `S` `D` | Alternative directional movement |

#### Ability Activation
| Input | Action |
|-------|--------|
| `1` | Primary ability activation |
| `2` | Secondary ability activation |
| `Q` | Consumable item slot 1 |
| `E` | Consumable item slot 2 |

#### System Controls
| Input | Action |
|-------|--------|
| `ESC` | Pause menu / Cancel |
| `F1` | Display game statistics |
| `F11` | Toggle fullscreen |
| `Tab` | Map overview (if unlocked) |

#### Debug Commands (Development Build)
| Input | Action |
|-------|--------|
| `F3` | Display debug overlay |
| `F4` | Toggle hitbox visualization |
| `F5` | Quick save state |
| `F9` | Quick load state |

### Customization

Keybindings can be reconfigured through:
1. In-game settings menu
2. Manual `config.ini` editing
3. Command-line arguments: `python launcher.py --keybind-preset=wasd`

---

## Strategic Guidelines

### Beginner Optimization

**Ability Selection**
- Recommended pairing: Wolf Vein + Dragon Heart
- Prioritizes survivability and mobility
- Low skill floor for learning core mechanics

**Early Game Strategy**
1. Master basic movement and collision mechanics
2. Identify enemy spawn patterns
3. Maintain coin acquisition efficiency
4. Avoid Pride encounters until comfortable with evasion

**Resource Management**
- Prioritize point spending on Bottomless Hunger (40pts) for economy scaling
- Reserve coins for Greed's Double-Down (15 coins) early-game multiplier
- Use abilities proactively rather than reactively

### Advanced Tactics

**Ability Synergies**
- John Snow + Demon Eye: Scales into late-game dominance
- Angel's Halo + Wolf Vein: Aggressive positioning and map control
- Dragon Heart + Demon Eye: Enemy manipulation and crowd control

**Greed Manipulation**
- Maintain 200+ coin reserve for strategic assassinations
- Target elimination priority: Wrath → Sloth → Lust
- Negotiate for self-preservation only when cornered

**Environmental Exploitation**
- Utilize Envy's betrayal mechanics for passive enemy reduction
- Position near Sloth during day cycle for debuff avoidance
- Leverage Pride's predictable pathfinding for coin collection routes

**Day/Night Optimization**
- **Day Phase** (Player +10%): Aggressive coin collection, Pride evasion
- **Night Phase** (Enemies +10%): Defensive positioning, ability conservation
- Plan major movements during favorable cycle phases

### Level-Specific Strategies

**Levels 1-3: Foundation Phase**
- Focus: Mechanical mastery and economy establishment
- Objective: Collect 80%+ coins, minimize deaths
- Ability usage: Conservative, emergency-only

**Levels 4-6: Scaling Phase**
- Focus: Permanent upgrade acquisition, enemy prioritization
- Objective: Eliminate non-Pride enemies when advantageous
- Ability usage: Proactive enemy manipulation

**Levels 7-9: Optimization Phase**
- Focus: Efficiency maximization, risk/reward evaluation
- Objective: Complete secondary objectives, stack John Snow passive
- Ability usage: Aggressive positioning and map control

**Level 10: Culmination**
- Focus: All systems active, maximum difficulty
- Objective: Survival and objective completion
- Ability usage: Reactive adaptation to dynamic threat assessment

---

## 📂 Project Structure

```
SevenDeadlySinsPacman/
│
├── launcher.py              # Main menu, profile, settings
├── main.py                  # Core game loop
├── player.py                # Player class and mechanics
├── ghosts.py                # AI for all 7 deadly sins
├── abilities.py             # Ability system and effects
├── levels.py                # Map generation and objectives
├── shop.py                  # Shop UI and transactions
├── game_data.py             # Save/load system
├── audio_manager.py         # Sound and music
├── day_night_system.py      # Day/night cycle logic
│
├── ui_*.py                  # Various UI screens
│   ├── ui_hud.py           # In-game HUD
│   ├── ui_pause.py         # Pause menu
│   ├── ui_settings.py      # Settings screen
│   ├── ui_shop.py          # Shop interface
│   └── ...
│
├── assets/                  # Game assets
│   ├── audio/              # Sound effects and music
│   ├── *.png               # Sprites and icons
│   └── fonts/              # Custom fonts
│
├── saves/                   # Player save files
│   └── game_data.json      # Persistent game data
│
├── README.md               # You are here!
└── requirements.txt        # Python dependencies
```

---

## 🗺️ Roadmap

### Completed ✅
- [x] Core gameplay loop
- [x] All 7 sins with unique AI
- [x] Day/night cycle system
- [x] Shop and inventory system
- [x] Save/load functionality
- [x] 5 unique abilities
- [x] Dynamic camera system
- [x] 10 progressive levels

### In Progress 🚧
- [ ] Interactive tutorial with particle effects
- [ ] Level objective system refinements
- [ ] Boss battle mechanics
- [ ] Achievement system

### Planned 📋
- [ ] Endless mode
- [ ] Custom skins and cosmetics
- [ ] Online leaderboards
- [ ] Virtue power-ups (counter to sins)
- [ ] New game+ mode with harder challenges
- [ ] Mobile port

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas We Need Help
- Sound effects and music composition
- Sprite art for items and ghosts
- Balance testing
- Bug reporting
- Documentation improvements

---

## 🐛 Known Issues

- Camera can occasionally stutter on very large maps
- Audio may not play on some Linux distributions
- Ghost pathfinding can get stuck in rare maze configurations

Report issues at: (https://github.com/arush1132v/seven_deadly-sins)

### Created By
**Arush Katiyar**
- Email: 25mc3014@rgipt.ac.in

### Special Thanks
- Original Pac-Man by Namco
- Pygame community for excellent documentation
- Seven Deadly Sins mythology for inspiration
- Beta testers and contributors
---

## 📊 Statistics

- **Lines of Code:** ~5,000+
- **Development Time:** [130+hours]
- **Python Version:** 3.9+
- **Pygame Version:** 2.0+

---

## 🎮 Similar Projects

If you enjoyed this game, check out:
- [Pac-Man Championship Edition](https://en.wikipedia.org/wiki/Pac-Man_Championship_Edition)
- [The Binding of Isaac](https://store.steampowered.com/app/113200/The_Binding_of_Isaac/)
- [Enter the Gungeon](https://store.steampowered.com/app/311690/Enter_the_Gungeon/)

---


<div align="center">

**[⬆ Back to Top](#-seven-deadly-sins-pac-man-reborn-)**

Made with ❤️ and ☕ by Arush Katiyar

*"Face your sins, or be consumed by them."*

</div>)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Credits

### Created By
**Arush Katiyar**
- Email: 25mc3014@rgipt.ac.in

### Special Thanks
- Original Pac-Man by Namco
- Pygame community for excellent documentation
- Seven Deadly Sins mythology for inspiration
- Beta testers and contributors
---

## 📊 Statistics

- **Lines of Code:** ~5,000+
- **Development Time:** [130+hours]
- **Python Version:** 3.9+
- **Pygame Version:** 2.0+

---

## 🎮 Similar Projects

If you enjoyed this game, check out:
- [Pac-Man Championship Edition](https://en.wikipedia.org/wiki/Pac-Man_Championship_Edition)
- [The Binding of Isaac](https://store.steampowered.com/app/113200/The_Binding_of_Isaac/)
- [Enter the Gungeon](https://store.steampowered.com/app/311690/Enter_the_Gungeon/)

---

<div align="center">

**[⬆ Back to Top](#-seven-deadly-sins-pac-man-reborn-)**

Made with ❤️ and ☕ by Arush Katiyar

*"Face your sins, or be consumed by them."*

</div>
