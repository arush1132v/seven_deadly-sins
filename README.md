# demo_arush
my first project

# 7 Deadly Sins Pac-Man 💀🍒

**A dark, RPG-infused twist on the classic arcade game.**

In this game, you don't just run from ghosts—you face the **Seven Deadly Sins** themselves. Each sin has unique AI behavior, status effects, and mechanics that challenge the player in different ways. Collect coins, upgrade your character, and try to achieve Absolution.

---

## 🎮 Features

### 👻 Unique AI for Every Sin
Unlike standard ghosts, every enemy has a personality:
* **Pride (💜):** Fast and relentless. Refuses to use shortcuts but chases directly.
* **Greed (💛):** An assassin and merchant. He might kill you, or he might offer you mercy... for a price.
* **Sloth (🩵):** Moves slowly but radiates an aura that slows *you* down.
* **Wrath (❤️):** Gets angry and speeds up drastically when you get too close.
* **Envy (💚):** Sabotages other ghosts to get to you first.
* **Gluttony (🧡):** Slow but effectively blocks paths.
* **Lust (🩷):** Unpredictable movement patterns.

### ⚔️ RPG & Progression Mechanics
* **Character Creation:** Choose your name, age, and gender.
* **Shop System:** Collect coins to buy permanent upgrades (Speed, Lives, etc.).
* **Inventory:** Manage items to help you survive the labyrinth.
* **Status Effects:** Beware of being **Feared**, **Confused**, or **Slowed** by specific Sins.

### 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Engine:** Pygame
* **Features:** Custom Pathfinding AI, Save/Load System, Animated UI.

---

## 🚀 Installation & Setup

### Prerequisites
You need Python installed on your machine.

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YourUsername/SinsPacman.git](https://github.com/YourUsername/SinsPacman.git)
    cd SinsPacman
    ```

2.  **Install Dependencies**
    ```bash
    pip install pygame
    ```

3.  **Run the Game**
    ```bash
    python3 launcher.py
    ```

---

## 🕹️ Controls

| Key | Action |
| :--- | :--- |
| **Arrow Keys / WASD** | Move Player |
| **ESC** | Pause / Back |
| **Space** | Use Active Item |
| **Mouse** | Navigate Menus |

---

## 📂 Project Structure

* `launcher.py` - The entry point (Main Menu, Settings, Profile).
* `main.py` - The core game loop and logic.
* `ghosts.py` - Contains the specific AI behavior for all 7 Sins.
* `game_data.py` - Handles saving/loading player stats and inventory.
* `assets/` - Images and sound files.

---

## 🔮 Future Roadmap
- [ ] Add "Virtue" power-ups (e.g., Patience, Charity).
- [ ] Boss fights for each Sin.
- [ ] Online Leaderboard.

---

**Created by [ARUSH KATIYAR]**
