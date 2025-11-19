"""
Example Integration File - How to use Haduyi Adversaries with other game files

This file demonstrates how to integrate Haduyi adversaries with:
- Maze environment
- PacmanAgent
- Game loop
- UI rendering

The Haduyi adversaries are designed to be easily adaptable and integrate
seamlessly with other team members' code.
"""

import pygame
import os
from maze import Maze
from pacman_agent import PacmanAgent
from ghosts import Haduyi

def example_game_with_adversaries():
    """
    Example showing how to integrate Haduyi adversaries into a game loop.
    
    This demonstrates:
    1. Creating Haduyi adversaries
    2. Updating their target (pacman position)
    3. Moving them in the game loop
    4. Integrating with maze and pacman
    """
    pygame.init()
    screen = pygame.display.set_mode((600, 700))
    pygame.display.set_caption("PACMAN with Haduyi Adversaries")
    
    # Load maze (adaptable to any maze file)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    maze_file = os.path.join(script_dir, "maze_layout.txt")
    maze = Maze(maze_file)
    
    # Create pacman agent (other team member's code)
    pacman = PacmanAgent(maze, move_delay_frames=30)
    
    # Create Haduyi adversaries at different starting positions
    # Each Haduyi needs: maze, start_pos, move_delay_frames (optional), search_algorithm (optional)
    haduyi_list = [
        Haduyi(maze, start_pos=(3, 2), move_delay_frames=30, search_algorithm='bfs'),
        Haduyi(maze, start_pos=(3, 6), move_delay_frames=35, search_algorithm='level_order'),
        # Add more adversaries as needed
    ]
    
    running = True
    clock = pygame.time.Clock()
    
    # Key mapping for pacman control
    key_to_direction = {
        pygame.K_UP: 'UP',
        pygame.K_DOWN: 'DOWN',
        pygame.K_LEFT: 'LEFT',
        pygame.K_RIGHT: 'RIGHT',
        pygame.K_w: 'UP',
        pygame.K_s: 'DOWN',
        pygame.K_a: 'LEFT',
        pygame.K_d: 'RIGHT'
    }
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in key_to_direction:
                    pacman.set_direction(key_to_direction[event.key])
        
        # Update pacman (other team member's code)
        pacman.move()
        
        # Update all Haduyi adversaries
        # Important: Update their target to pacman's current position
        for haduyi in haduyi_list:
            haduyi.update_target(pacman.pos)  # Make them chase pacman
            haduyi.move()  # Move them along their calculated path
        
        # Draw everything (UI team member's code)
        # Note: This would need to be adapted to draw Haduyi as well
        maze.draw(screen, pacman)
        
        # Example: Draw Haduyi adversaries (red circles)
        # This would typically be in maze.py or a separate renderer
        tile = 20
        for haduyi in haduyi_list:
            r, c = haduyi.pos
            pygame.draw.circle(screen, (255, 0, 0), (c*tile+10, r*tile+10), 8)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


def example_adaptable_interface():
    """
    Example showing how Haduyi adapts to different interfaces.
    
    The Haduyi class is designed to work with any object that has:
    - grid: 2D list of integers (0=passable, 1=wall, 2=pellet)
    - rows: Number of rows in the grid
    - cols: Number of columns in the grid
    """
    
    # Example: Custom maze-like object
    class CustomMaze:
        def __init__(self, grid):
            self.grid = grid
            self.rows = len(grid)
            self.cols = len(grid[0]) if grid else 0
    
    # Create custom maze
    custom_grid = [
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 2, 1],
        [1, 1, 1, 1]
    ]
    custom_maze = CustomMaze(custom_grid)
    
    # Haduyi works with any maze-like object!
    haduyi = Haduyi(custom_maze, start_pos=(1, 1))
    haduyi.update_target((2, 2))  # Set target
    
    # Haduyi will find path automatically
    for _ in range(3):
        haduyi.move()
        print(f"Haduyi position: {haduyi.pos}, Distance to target: {haduyi.get_distance_to_target()}")


if __name__ == "__main__":
    print("Example Integration Guide for Haduyi Adversaries")
    print("=" * 50)
    print("\n1. Basic Usage:")
    print("   from ghosts import Haduyi")
    print("   haduyi = Haduyi(maze, start_pos=(r, c))")
    print("   haduyi.update_target(pacman.pos)")
    print("   haduyi.move()")
    print("\n2. Integration with Game Loop:")
    print("   - Call haduyi.update_target(pacman.pos) each frame")
    print("   - Call haduyi.move() each frame")
    print("   - Haduyi will automatically calculate path and move")
    print("\n3. Search Algorithms:")
    print("   - 'bfs': Standard breadth-first search (default)")
    print("   - 'level_order': Explicit level-order search")
    print("\n4. Adaptable Interface:")
    print("   - Works with any object having grid, rows, cols attributes")
    print("   - Automatically validates maze structure")
    print("\nRun example_game_with_adversaries() to see full integration.")

