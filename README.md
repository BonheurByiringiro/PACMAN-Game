# Automated PACMAN AI

## Project Description
This project implements an automated PACMAN game using Python and Pygame, where PACMAN acts as an intelligent agent using search algorithms (A*, BFS, DFS) to navigate a maze, collect pellets, and avoid ghosts.

---

## Features

- Automated PACMAN agent with AI pathfinding (A*, BFS, DFS, UCS)
- Real-time algorithm switching during gameplay
- Intelligent ghost adversaries with chase behavior
- Maze environment using grid representation
- Score tracking and game UI
- Path visualization showing AI decision-making
- Professional dark theme UI

---

## Repository Structure

```
PACMAN-Game/
│
├── src/             # Source code (game logic, agents, algorithms)
├── assets/          # Game assets (sprites, sounds)
├── tests/           # Unit tests
├── maze_layout.txt  # Maze design file
├── requirements.txt # Python dependencies
├── README.md        # Project documentation
├── .gitignore
```

---

## Project Setup & Installation

### 1. Clone the Repository

```
git clone https://github.com/BonheurByiringiro/PACMAN-Game.git
cd PACMAN-Game
```

### 2. (Recommended) Create and Activate a Virtual Environment

**Windows:**
```
python -m venv venv
venv\Scripts\activate
```
**Mac/Linux:**
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Project Dependencies

```
pip install -r requirements.txt
```

---

## How to Run

1. Ensure you're in the project root directory.
2. Launch the game:
   
   **AI Mode (Recommended):**
   ```
   python src/intelligent_main.py
   ```
   
   **Manual Control Mode:**
   ```
   python src/main.py
   ```

### Controls (AI Mode):
- **1**: Switch to BFS algorithm
- **2**: Switch to DFS algorithm
- **3**: Switch to A* algorithm
- **4**: Switch to UCS algorithm
- **SPACE**: Pause/Resume game
- **ESC**: Quit game

---

## How to Contribute

- **Branch Creation:**  
  ```
  git checkout -b feature-your-feature-name
  ```
- **Push Changes:**  
  ```
  git add .
  git commit -m "Describe your changes"
  git push origin feature-your-feature-name
  ```
- **Open a Pull Request for review.**

---

## Requirements

- Python 3.7+
- Pygame

---

## Troubleshooting

- Problems with dependencies?  
  Ensure Python and pip are correctly installed and added to your system PATH.
- Pygame or graphics issues?  
  Upgrade Pygame and check for driver updates.

---

## Authors & Contributors

- Bonheur Byiringiro
- Tessy Pauline Mugisha
- Arsene Manzi
