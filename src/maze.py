import pygame

class Maze:
    def __init__(self, filename):
        self.grid = []
        with open(filename, "r") as f:
            for line in f:
                self.grid.append([int(c) for c in line.strip().split()])
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def draw(self, screen, pacman, haduyi_list=None):
        """
        Draw the maze, pacman, and Haduyi adversaries.
        
        Args:
            screen: Pygame screen surface
            pacman: PacmanAgent object with pos attribute
            haduyi_list: Optional list of Haduyi objects to draw
        """
        tile = 20
        colors = {0: (0, 0, 0), 1: (0, 0, 255), 2: (255, 255, 255)}
        
        # Draw maze grid
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(c*tile, r*tile, tile, tile)
                pygame.draw.rect(screen, colors[self.grid[r][c]], rect)
        
        # Draw PACMAN (yellow circle)
        pygame.draw.circle(screen, (255, 255, 0), (pacman.pos[1]*tile+10, pacman.pos[0]*tile+10), 10)
        
        # Draw Haduyi adversaries (red circles) if provided
        if haduyi_list:
            for haduyi in haduyi_list:
                if hasattr(haduyi, 'pos'):
                    r, c = haduyi.pos
                    pygame.draw.circle(screen, (255, 0, 0), (c*tile+10, r*tile+10), 8)
