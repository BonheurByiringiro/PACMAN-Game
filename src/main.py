import pygame
import os
from maze import Maze
from pacman_agent import PacmanAgent
from ghosts import Haduyi

def initialize_game(maze):
    """
    Initialize or reset game objects.
    
    Args:
        maze: Maze object
    
    Returns:
        tuple: (pacman, haduyi_list)
    """
    # Create pacman agent
    pacman = PacmanAgent(maze, move_delay_frames=30)
    
    # Create Haduyi adversaries at different starting positions
    haduyi_list = []
    try:
        # Add Haduyi at different positions in the maze
        haduyi_list.append(Haduyi(maze, start_pos=(3, 2), move_delay_frames=30, search_algorithm='bfs'))
        # haduyi_list.append(Haduyi(maze, start_pos=(3, 6), move_delay_frames=30, search_algorithm='bfs'))
    except Exception as e:
        print(f"Warning: Could not create all Haduyi: {e}")
    
    return pacman, haduyi_list

def check_collision(pacman, haduyi_list):
    """
    Check if pacman has been caught by any Haduyi.
    
    Args:
        pacman: PacmanAgent object
        haduyi_list: List of Haduyi objects
    
    Returns:
        bool: True if pacman collided with any Haduyi, False otherwise
    """
    for haduyi in haduyi_list:
        if hasattr(haduyi, 'pos') and pacman.pos == haduyi.pos:
            return True
    return False

def draw_game_over(screen, font):
    """
    Draw game over message and restart instructions.
    
    Args:
        screen: Pygame screen surface
        font: Pygame font object for text rendering
    """
    # Semi-transparent overlay
    overlay = pygame.Surface(screen.get_size())
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 30))
    screen.blit(game_over_text, game_over_rect)
    
    # Restart instruction
    restart_text = font.render("Press ENTER to Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 30))
    screen.blit(restart_text, restart_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 700))
    pygame.display.set_caption("Automated PACMAN AI - Use Arrow Keys or WASD to control")
    
    # Initialize font for game over message
    pygame.font.init()
    font = pygame.font.Font(None, 48)
    
    # Get the correct path to maze_layout.txt (works whether run from root or src/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    maze_file = os.path.join(script_dir, "maze_layout.txt")
    maze = Maze(maze_file)
    
    # Initialize game objects
    pacman, haduyi_list = initialize_game(maze)
    
    # Game state
    game_state = "playing"  # "playing" or "game_over"
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
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == "playing":
                    # Change direction when arrow keys or WASD are pressed
                    if event.key in key_to_direction:
                        pacman.set_direction(key_to_direction[event.key])
                elif game_state == "game_over":
                    # Press Enter to restart
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        # Reset game
                        pacman, haduyi_list = initialize_game(maze)
                        game_state = "playing"
        
        # Game logic only runs when playing
        if game_state == "playing":
            # Agent automatically continues in current direction
            pacman.move()
            
            # Update Haduyi adversaries - make them chase pacman
            for haduyi in haduyi_list:
                haduyi.update_target(pacman.pos)  # Update target to pacman's current position
                haduyi.move()  # Move along calculated path
            
            # Check for collision with Haduyi
            if check_collision(pacman, haduyi_list):
                game_state = "game_over"
                print("Game Over! Pacman was caught by Haduyi!")
        
        # Draw everything
        maze.draw(screen, pacman, haduyi_list)
        
        # Draw game over screen if game is over
        if game_state == "game_over":
            draw_game_over(screen, font)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
