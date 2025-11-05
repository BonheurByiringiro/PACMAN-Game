class Ghost:
    def __init__(self, maze, start_pos):
        self.maze = maze
        self.pos = start_pos

    def move(self):
        # Placeholder: Ghost moves left if possible, otherwise up
        r, c = self.pos
        if c - 1 >= 0 and self.maze.grid[r][c-1] == 0:
            self.pos = (r, c-1)
        elif r - 1 >= 0 and self.maze.grid[r-1][c] == 0:
            self.pos = (r-1, c)
