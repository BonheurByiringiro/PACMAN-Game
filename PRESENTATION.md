# AUTOMATED PACMAN AI
## 3-Slide Presentation

---

## SLIDE 1: Problem & Objective

### The Problem
How can an autonomous agent efficiently navigate a complex maze, collect all targets, and avoid obstacles using intelligent search strategies?

### Our Solution
Automated PACMAN AI that uses search algorithms to:
- Navigate maze autonomously
- Collect all 194 pellets
- Avoid ghost adversaries
- Find optimal paths in real-time

### Key Challenge
Making intelligent decisions in a dynamic environment with moving obstacles (ghosts)

---

## SLIDE 2: Technology Stack

### Core Technologies
- **Python 3.12** - Programming language
- **Pygame** - 2D game rendering and UI
- **Grid-based Maze** - 22x20 cell environment

### AI Architecture
- **Intelligent Agent** - Autonomous decision-making entity
- **Search Algorithms** - A*, BFS, DFS, UCS
- **Real-time Pathfinding** - Dynamic route calculation
- **State Management** - Game state tracking and updates

### Key Features
- Algorithm switching during gameplay (keys 1-4)
- Path visualization showing AI decisions
- Score and pellet tracking

---

## SLIDE 3: AI Algorithms Implementation

### 1. A* (A-Star) - Default Algorithm
- **Strategy**: Best-first search with heuristic (Manhattan distance)
- **Use Case**: Optimal path with minimal computation
- **Advantage**: Balances path quality and speed

### 2. BFS (Breadth-First Search)
- **Strategy**: Explores all neighbors level by level
- **Use Case**: Guaranteed shortest path
- **Advantage**: Finds shortest route in unweighted graphs

### 3. DFS (Depth-First Search)
- **Strategy**: Explores as deep as possible before backtracking
- **Use Case**: Quick exploration, memory efficient
- **Advantage**: Low memory usage

### 4. UCS (Uniform Cost Search)
- **Strategy**: Expands lowest-cost nodes first
- **Use Case**: Weighted pathfinding
- **Advantage**: Optimal for varying path costs

### Algorithm Selection Logic
```
Target = Nearest uncollected pellet
Path = Selected_Algorithm(current_position, target)
Execute: Move along path while avoiding ghosts
```

---

## Demo Highlights
✓ 194 pellets collected successfully  
✓ Real-time algorithm comparison  
✓ Autonomous navigation without human input  
✓ Dynamic path recalculation when needed
