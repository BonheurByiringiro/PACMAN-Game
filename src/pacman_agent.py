import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [PACMAN] - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class PacmanAgent:
    def __init__(self, maze, move_delay_frames=30):
        self.maze = maze
        self.pos = (1, 1)
        self.prev_pos = None  # Track previous position to avoid 2-cell loops
        self.path = []
        self.move_delay_frames = move_delay_frames  # Move every N frames (slower movement)
        self.frame_count = 0
        
        # Direction: 'UP', 'DOWN', 'LEFT', 'RIGHT' - stored as (dr, dc) tuples
        # Start moving forward (right) by default
        self.direction = 'RIGHT'
        self.direction_map = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }
        
        logger.info(f"PacmanAgent initialized at position {self.pos}, starting direction: {self.direction}")
        self.log_status()

    def is_valid_move(self, r, c):
        """Check if a position is valid (within bounds and not a wall)."""
        if 0 <= r < self.maze.rows and 0 <= c < self.maze.cols:
            # 0 = empty, 2 = pellet (both passable), 1 = wall (not passable)
            return self.maze.grid[r][c] != 1
        return False

    def get_valid_neighbors(self, r, c):
        """Get all valid neighboring positions (up, down, left, right)."""
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.is_valid_move(nr, nc):
                neighbors.append((nr, nc))
        return neighbors

    def get_distance_to_obstacle(self, r, c, direction):
        """Calculate distance to nearest obstacle in a given direction (up, down, left, right)."""
        dr, dc = direction
        distance = 0
        nr, nc = r, c
        
        while True:
            nr += dr
            nc += dc
            if not (0 <= nr < self.maze.rows and 0 <= nc < self.maze.cols):
                return distance
            if self.maze.grid[nr][nc] == 1:  # Hit a wall
                return distance
            distance += 1

    def get_obstacle_distances(self, r, c):
        """Get distances to obstacles in all four directions."""
        directions = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }
        distances = {}
        for name, direction in directions.items():
            distances[name] = self.get_distance_to_obstacle(r, c, direction)
        return distances

    def log_status(self):
        """Log current agent status: location, obstacle distances, and possible moves."""
        r, c = self.pos
        logger.info(f"=== Agent Status ===")
        logger.info(f"Current Location: Row={r}, Col={c} (Grid Position: ({r}, {c}))")
        
        # Get obstacle distances
        obstacle_distances = self.get_obstacle_distances(r, c)
        logger.info(f"Distance to Obstacles:")
        for direction, distance in obstacle_distances.items():
            logger.info(f"  {direction.upper()}: {distance} cells")
        
        # Get possible moves
        valid_neighbors = self.get_valid_neighbors(r, c)
        logger.info(f"Possible Moves: {len(valid_neighbors)}")
        direction_names = {(-1, 0): 'UP', (1, 0): 'DOWN', (0, -1): 'LEFT', (0, 1): 'RIGHT'}
        for neighbor in valid_neighbors:
            nr, nc = neighbor
            dr, dc = nr - r, nc - c
            direction = direction_names.get((dr, dc), 'UNKNOWN')
            cell_type = 'pellet' if self.maze.grid[nr][nc] == 2 else 'empty'
            logger.info(f"  → {direction} to ({nr}, {nc}) [{cell_type}]")
        
        if self.prev_pos:
            logger.info(f"Previous Position: {self.prev_pos}")

    def set_direction(self, direction):
        """Change the direction the agent is moving.
        
        Args:
            direction: One of 'UP', 'DOWN', 'LEFT', 'RIGHT'
        """
        if direction in self.direction_map:
            # Only change direction if the new direction is valid
            r, c = self.pos
            dr, dc = self.direction_map[direction]
            new_pos = (r + dr, c + dc)
            
            if self.is_valid_move(new_pos[0], new_pos[1]):
                self.direction = direction
                logger.info(f"Direction changed to: {direction}")
            else:
                logger.info(f"Cannot change to {direction}: wall ahead. Keeping direction: {self.direction}")
    
    def move(self):
        """Move Pacman in the current direction."""
        self.frame_count += 1
        if self.frame_count < self.move_delay_frames:
            return

        self.frame_count = 0
        dr, dc = self.direction_map[self.direction]
        nr, nc = self.pos[0] + dr, self.pos[1] + dc

        if self.is_valid_move(nr, nc):
            self.prev_pos = self.pos
            self.pos = (nr, nc)
            self.maze.collect_pellet(nr, nc)
            self.log_status()
        else:
            # Can't move in current direction (hit a wall)
            logger.warning(f"Cannot move {self.direction}: obstacle ahead at {self.pos}")
            # Try to find alternative valid moves
            valid_neighbors = self.get_valid_neighbors(self.pos[0], self.pos[1])
            if valid_neighbors:
                logger.info(f"Available alternative moves: {valid_neighbors}")
            else:
                logger.warning(f"Stuck! No valid moves available at position {self.pos}")
