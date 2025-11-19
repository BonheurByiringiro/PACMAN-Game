import pygame
import os
from maze import Maze
from pacman_agent import PacmanAgent

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 700))
    pygame.display.set_caption("Automated PACMAN AI - Use Arrow Keys or WASD to control")
    # Get the correct path to maze_layout.txt (works whether run from root or src/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    maze_file = os.path.join(script_dir, "maze_layout.txt")
    maze = Maze(maze_file)
    # Move every 30 frames (60 FPS / 30 = 2 moves per second, adjustable)
    pacman = PacmanAgent(maze, move_delay_frames=30)
    running = True
    clock = pygame.time.Clock()

    # Key mapping: arrow keys and WASD to direction
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
        # Handle keyboard input for direction changes (event-based for cleaner control)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Change direction when arrow keys or WASD are pressed
                if event.key in key_to_direction:
                    pacman.set_direction(key_to_direction[event.key])
        
        # Agent automatically continues in current direction
        pacman.move()
        maze.draw(screen, pacman)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
