import pygame

class Maze:
    def __init__(self, filename):
        self.grid = []
        with open(filename, "r") as f:
            for line in f:
                self.grid.append([int(c) for c in line.strip().split()])
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def draw(self, screen, pacman):
        tile = 20
        colors = {0: (0, 0, 0), 1: (0, 0, 255), 2: (255, 255, 255)}
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(c*tile, r*tile, tile, tile)
                pygame.draw.rect(screen, colors[self.grid[r][c]], rect)
        # Draw PACMAN
        pygame.draw.circle(screen, (255, 255, 0), (pacman.pos[1]*tile+10, pacman.pos[0]*tile+10), 10)
