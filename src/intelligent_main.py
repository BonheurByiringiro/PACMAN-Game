"""
Intelligent PACMAN Game - Main Entry Point

This is the main game loop for the intelligent PACMAN agent that uses
search algorithms (BFS, DFS, A*, UCS) to make rational decisions.

Features:
- Intelligent agent with multiple search algorithms
- Real-time pathfinding with ghost avoidance
- Score tracking and win/lose conditions
- Visualization of agent's decision-making
- Algorithm and strategy selection via keyboard
"""

import pygame
import os
import sys
from maze import Maze
from intelligent_pacman_agent import IntelligentPacmanAgent
from ghosts import Haduyi

def initialize_game(maze, algorithm='astar', difficulty='hard', maze_file=None):
    """
    Initialize or reset game objects.
    
    Args:
        maze: Maze object
        algorithm: Search algorithm for PACMAN ('bfs', 'dfs', 'astar', 'ucs')
        difficulty: Difficulty level for ghosts ('easy', 'medium', 'hard', 'extreme')
        maze_file: Path to maze file (for reset)
    
    Returns:
        tuple: (pacman, haduyi_list)
    """
    # Reset maze if file provided
    if maze_file:
        maze.reset_maze(maze_file)
    
    # Create intelligent PACMAN agent
    pacman = IntelligentPacmanAgent(
        maze, 
        start_pos=(1, 1), 
        search_algorithm=algorithm,
        move_delay_frames=15
    )
    
    # Create Haduyi adversaries at different starting positions
    haduyi_list = []
    try:
        # Add Haduyi at strategic positions
        haduyi_list.append(Haduyi(maze, start_pos=(3, 3), move_delay_frames=20, difficulty=difficulty))
        haduyi_list.append(Haduyi(maze, start_pos=(maze.rows-4, maze.cols-4), move_delay_frames=22, difficulty=difficulty))
        # haduyi_list.append(Haduyi(maze, start_pos=(maze.rows//2, maze.cols//2), move_delay_frames=25, difficulty=difficulty))
    except Exception as e:
        print(f"Warning: Could not create all Haduyi: {e}")
    
    return pacman, haduyi_list

def check_collision(pacman, haduyi_list):
    """
    Check if pacman has been caught by any Haduyi.
    
    Args:
        pacman: IntelligentPacmanAgent object
        haduyi_list: List of Haduyi objects
    
    Returns:
        bool: True if pacman collided with any Haduyi, False otherwise
    """
    for haduyi in haduyi_list:
        if hasattr(haduyi, 'pos') and pacman.pos == haduyi.pos:
            return True
    return False

def draw_game_over(screen, font, maze):
    """
    Draw game over message and restart instructions.
    
    Args:
        screen: Pygame screen surface
        font: Pygame font object for text rendering
        maze: Maze object (for score display)
    """
    # Semi-transparent overlay
    overlay = pygame.Surface(screen.get_size())
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_font = pygame.font.Font(None, 64)
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50))
    screen.blit(game_over_text, game_over_rect)
    
    # Score text
    score_text = font.render(f"Final Score: {maze.score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
    screen.blit(score_text, score_rect)
    
    # Restart instruction
    restart_text = font.render("Press ENTER to Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 50))
    screen.blit(restart_text, restart_rect)

def draw_help_panel(screen, font, show_help):
    """
    Draw help panel with controls and algorithm info.
    
    Args:
        screen: Pygame screen surface
        font: Pygame font for rendering
        show_help: Whether to show the help panel
    """
    if not show_help:
        # Just show hint
        hint_text = font.render("Press H for Help", True, (150, 150, 150))
        screen.blit(hint_text, (10, screen.get_height() - 25))
        return
    
    # Draw semi-transparent panel
    panel_height = 220
    panel = pygame.Surface((screen.get_width(), panel_height))
    panel.set_alpha(230)
    panel.fill((20, 20, 50))
    screen.blit(panel, (0, screen.get_height() - panel_height))
    
    # Help text
    help_lines = [
        "=== CONTROLS ===",
        "1-4: Switch Algorithm (1=BFS, 2=DFS, 3=A*, 4=UCS)",
        "Q/W/E: Strategy (Q=Nearest, W=Nearest Safe, E=Furthest from Ghosts)",
        "P: Toggle Path Visualization",
        "H: Toggle Help",
        "SPACE: Pause/Resume",
        "ENTER: Restart Game"
    ]
    
    y_pos = screen.get_height() - panel_height + 10
    for line in help_lines:
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (10, y_pos))
        y_pos += 25

def main():
    """Main game loop with intelligent PACMAN agent."""
    pygame.init()
    screen = pygame.display.set_mode((800, 550))
    pygame.display.set_caption("Intelligent PACMAN - Rational Agent with Search Algorithms")
    
    # Initialize fonts
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    
    # Load maze
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try to use the larger maze, fallback to smaller one
    maze_file = os.path.join(script_dir, "..", "maze_layouts", "classic_maze.txt")
    if not os.path.exists(maze_file):
        # Try alternative path
        maze_file = os.path.join(script_dir, "maze_layout.txt")
    
    if not os.path.exists(maze_file):
        print(f"Error: Could not find maze file at {maze_file}")
        sys.exit(1)
    
    maze = Maze(maze_file)
    
    # Initialize game with A* algorithm (default)
    current_algorithm = 'astar'
    current_difficulty = 'hard'
    pacman, haduyi_list = initialize_game(maze, current_algorithm, current_difficulty, maze_file)
    
    # Game state
    game_state = "playing"  # "playing", "won", "game_over"
    paused = False
    show_path = True  # Visualize agent's decision-making
    show_help = False
    
    running = True
    clock = pygame.time.Clock()
    
    print("\n" + "="*60)
    print("INTELLIGENT PACMAN GAME STARTED")
    print("="*60)
    print(f"Algorithm: {current_algorithm.upper()}")
    print(f"Strategy: {pacman.strategy}")
    print(f"Total Pellets: {pacman.total_pellets}")
    print(f"Ghost Difficulty: {current_difficulty}")
    print("\nControls:")
    print("  1-4: Change Algorithm (1=BFS, 2=DFS, 3=A*, 4=UCS)")
    print("  Q/W/E: Change Strategy")
    print("  P: Toggle Path Visualization")
    print("  H: Toggle Help")
    print("  SPACE: Pause/Resume")
    print("="*60 + "\n")
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if game_state == "playing":
                    # Algorithm selection (1-4)
                    if event.key == pygame.K_1:
                        current_algorithm = 'bfs'
                        pacman.set_search_algorithm('bfs')
                        print(f"Switched to BFS algorithm")
                    elif event.key == pygame.K_2:
                        current_algorithm = 'dfs'
                        pacman.set_search_algorithm('dfs')
                        print(f"Switched to DFS algorithm")
                    elif event.key == pygame.K_3:
                        current_algorithm = 'astar'
                        pacman.set_search_algorithm('astar')
                        print(f"Switched to A* algorithm")
                    elif event.key == pygame.K_4:
                        current_algorithm = 'ucs'
                        pacman.set_search_algorithm('ucs')
                        print(f"Switched to UCS algorithm")
                    
                    # Strategy selection (Q/W/E)
                    elif event.key == pygame.K_q:
                        pacman.set_strategy('nearest')
                        print(f"Strategy: Nearest pellet")
                    elif event.key == pygame.K_w:
                        pacman.set_strategy('nearest_safe')
                        print(f"Strategy: Nearest safe pellet")
                    elif event.key == pygame.K_e:
                        pacman.set_strategy('furthest_from_ghosts')
                        print(f"Strategy: Furthest from ghosts")
                    
                    # Toggle path visualization
                    elif event.key == pygame.K_p:
                        show_path = not show_path
                        print(f"Path visualization: {'ON' if show_path else 'OFF'}")
                    
                    # Toggle help
                    elif event.key == pygame.K_h:
                        show_help = not show_help
                    
                    # Pause
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                        print(f"Game {'PAUSED' if paused else 'RESUMED'}")
                
                # Restart game (works in any state)
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    pacman, haduyi_list = initialize_game(maze, current_algorithm, current_difficulty, maze_file)
                    game_state = "playing"
                    paused = False
                    print("\n=== GAME RESTARTED ===\n")
        
        # Game logic (only runs when playing and not paused)
        if game_state == "playing" and not paused:
            # Update PACMAN agent's knowledge of ghost positions
            pacman.update_ghost_positions(haduyi_list)
            
            # Move PACMAN (agent plans and executes moves autonomously)
            pacman.move()
            
            # Update Haduyi adversaries - make them chase pacman
            for haduyi in haduyi_list:
                haduyi.update_target(pacman.pos)
                haduyi.move()
            
            # Check for collision with Haduyi
            if check_collision(pacman, haduyi_list):
                game_state = "game_over"
                print(f"\n=== GAME OVER ===")
                print(f"Caught by ghost at position {pacman.pos}")
                print(f"Final Score: {maze.score}")
                print(f"Pellets Collected: {pacman.pellets_collected}/{pacman.total_pellets}")
            
            # Check for win condition (all pellets collected)
            elif pacman.all_pellets_collected():
                game_state = "won"
                print(f"\n=== VICTORY! ===")
                print(f"All pellets collected!")
                print(f"Final Score: {maze.score}")
                print(f"Algorithm used: {current_algorithm.upper()}")
        
        # Draw everything
        maze.draw(screen, pacman, haduyi_list, show_path=show_path, ui_offset=50)
        maze.draw_ui(screen, pacman, font, game_state=game_state, ui_offset=50)
        
        # Draw game over or won screen
        if game_state == "game_over":
            draw_game_over(screen, font, maze)
        
        # Draw help panel
        draw_help_panel(screen, font, show_help)
        
        # Draw pause indicator
        if paused and game_state == "playing":
            pause_font = pygame.font.Font(None, 48)
            pause_text = pause_font.render("PAUSED", True, (255, 255, 0))
            pause_rect = pause_text.get_rect(center=(screen.get_width()//2, 25))
            screen.blit(pause_text, pause_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("\nGame closed. Thanks for playing!")

if __name__ == "__main__":
    main()
