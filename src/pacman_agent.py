class PacmanAgent:
    def __init__(self, maze):
        self.maze = maze
        self.pos = (1, 1)
        self.path = []

    def move(self):
        # Placeholder: Pacman moves right if possible, otherwise down.
        r, c = self.pos
        if c + 1 < self.maze.cols and self.maze.grid[r][c+1] == 0:
            self.pos = (r, c+1)
        elif r + 1 < self.maze.rows and self.maze.grid[r+1][c] == 0:
            self.pos = (r+1, c)
