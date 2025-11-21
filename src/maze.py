import pygame

class Maze:
    def __init__(self, filename):
        self.grid = []
        with open(filename, "r") as f:
            for line in f:
                self.grid.append([int(c) for c in line.strip().split()])
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.initial_pellets = self._count_pellets()
        self.score = 0
    
    def _count_pellets(self):
        """Count total pellets in the maze."""
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 2:
                    count += 1
        return count
    
    def get_remaining_pellets(self):
        """Get count of remaining pellets."""
        return self._count_pellets()
    
    def collect_pellet(self, r, c):
        """Collect pellet at position and update score."""
        if self.grid[r][c] == 2:
            self.grid[r][c] = 0
            self.score += 10
            return True
        return False
    
    def reset_maze(self, filename):
        """Reset maze to initial state."""
        self.grid = []
        with open(filename, "r") as f:
            for line in f:
                self.grid.append([int(c) for c in line.strip().split()])
        self.initial_pellets = self._count_pellets()
        self.score = 0

    def draw(self, screen, pacman, haduyi_list=None, show_path=False, ui_offset=50):
        """
        Draw the maze, pacman, Haduyi adversaries, and UI elements.
        
        Args:
            screen: Pygame screen surface
            pacman: PacmanAgent object with pos attribute
            haduyi_list: Optional list of Haduyi objects to draw
            show_path: Whether to visualize pacman's planned path
            ui_offset: Vertical offset for UI elements at top
        """
        tile = 20
        colors = {0: (0, 0, 0), 1: (0, 0, 255), 2: (255, 255, 255)}
        
        # Fill background
        screen.fill((0, 0, 0))
        
        # Draw maze grid (offset by UI)
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(c*tile, r*tile + ui_offset, tile, tile)
                pygame.draw.rect(screen, colors[self.grid[r][c]], rect)
                
                # Draw pellets as small circles instead of filled squares
                if self.grid[r][c] == 2:
                    center = (c*tile + tile//2, r*tile + tile//2 + ui_offset)
                    pygame.draw.circle(screen, (255, 255, 255), center, 3)
        
        # Draw PACMAN's planned path if requested
        if show_path and hasattr(pacman, 'current_path'):
            if pacman.current_path:
                for i, pos in enumerate(pacman.current_path):
                    r, c = pos
                    # Draw path with fading color
                    alpha = max(50, 200 - i * 10)
                    color = (0, 255, 0, min(alpha, 200))
                    center = (c*tile + tile//2, r*tile + tile//2 + ui_offset)
                    pygame.draw.circle(screen, color[:3], center, 4)
        
        # Draw target pellet if agent has one
        if show_path and hasattr(pacman, 'target_pellet') and pacman.target_pellet:
            r, c = pacman.target_pellet
            center = (c*tile + tile//2, r*tile + tile//2 + ui_offset)
            pygame.draw.circle(screen, (255, 0, 255), center, 6, 2)
        
        # Draw PACMAN (yellow circle)
        pac_center = (pacman.pos[1]*tile + tile//2, pacman.pos[0]*tile + tile//2 + ui_offset)
        pygame.draw.circle(screen, (255, 255, 0), pac_center, 8)
        
        # Draw Haduyi adversaries (red circles) if provided
        if haduyi_list:
            for haduyi in haduyi_list:
                if hasattr(haduyi, 'pos'):
                    r, c = haduyi.pos
                    center = (c*tile + tile//2, r*tile + tile//2 + ui_offset)
                    pygame.draw.circle(screen, (255, 0, 0), center, 7)
    
    def draw_ui(self, screen, pacman, font, game_state='playing', ui_offset=50):
        """
        Draw UI elements (score, pellets, algorithm info).
        
        Args:
            screen: Pygame screen surface
            pacman: PACMAN agent object
            font: Pygame font for text rendering
            game_state: Current game state ('playing', 'won', 'game_over')
            ui_offset: Height of UI area
        """
        # Draw UI background
        ui_rect = pygame.Rect(0, 0, screen.get_width(), ui_offset)
        pygame.draw.rect(screen, (20, 20, 40), ui_rect)
        
        # Get agent info
        remaining = self.get_remaining_pellets()
        score_text = f"Score: {self.score}"
        pellets_text = f"Pellets: {remaining}/{self.initial_pellets}"
        
        # Get algorithm info if available
        algo_text = ""
        strategy_text = ""
        if hasattr(pacman, 'search_algorithm'):
            algo_text = f"Algorithm: {pacman.search_algorithm.upper()}"
        if hasattr(pacman, 'strategy'):
            strategy_text = f"Strategy: {pacman.strategy}"
        
        # Render text
        score_surface = font.render(score_text, True, (255, 255, 255))
        pellets_surface = font.render(pellets_text, True, (255, 255, 0))
        
        # Draw text
        screen.blit(score_surface, (10, 10))
        screen.blit(pellets_surface, (200, 10))
        
        if algo_text:
            algo_surface = font.render(algo_text, True, (0, 255, 255))
            screen.blit(algo_surface, (10, 28))
        
        if strategy_text:
            strategy_surface = font.render(strategy_text, True, (0, 255, 0))
            screen.blit(strategy_surface, (250, 28))
        
        # Draw game state messages
        if game_state == 'won':
            win_font = pygame.font.Font(None, 64)
            win_text = win_font.render("YOU WIN!", True, (0, 255, 0))
            win_rect = win_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            
            # Semi-transparent overlay
            overlay = pygame.Surface(screen.get_size())
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            screen.blit(win_text, win_rect)
            
            restart_text = font.render("Press ENTER to restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 50))
            screen.blit(restart_text, restart_rect)
