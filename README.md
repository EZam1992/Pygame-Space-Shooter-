# 🚀 Space Shooter

A 2D top-down arcade-style space shooter game built with **Pygame**. Control a spaceship, dodge falling meteors, and destroy them with your laser cannon to survive as long as possible. The game features smooth controls, sound effects, animated explosions, and a retro-themed starfield background.

## 🎮 Gameplay Overview

You control a spaceship that can move freely across the screen using the arrow keys. Meteors fall from the top of the screen, and you must avoid them or shoot them down. Lasers are fired with the spacebar and have a cooldown to prevent spamming. Each destroyed meteor triggers an explosion animation. Your score is based on how long you survive.

## ✨ Features

- **Player Controls:**
  - Move using the **arrow keys**.
  - Fire lasers with the **spacebar** (with a short cooldown).

- **Core Mechanics:**
  - Randomly spawning meteors that fall toward the bottom of the screen.
  - Destroy meteors with lasers to stay alive.
  - Touching a meteor results in a **game over**.
  - Score is based on **survival time** (displayed on-screen).

- **Graphics & Audio:**
  - Sprites for player, lasers, meteors, stars, and explosions.
  - Smooth explosion animations using sprite frames.
  - Starfield background to create a space atmosphere.
  - Laser and explosion sound effects.
  - Background music loop during gameplay.
 
## 🛠️ Requirements

- Python 3.x
- Pygame-ce

Install Pygame using pip:

```bash
pip install pygame-ce

