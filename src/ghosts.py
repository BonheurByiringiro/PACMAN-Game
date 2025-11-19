import logging
from search_algorithms import bfs, level_order_search, is_passable_cell

logger = logging.getLogger(__name__)

class Haduyi:
    """
    Haduyi adversary class that uses search algorithms to find and chase pacman.
    
    The Haduyi (adversary) is aware of the maze environment and uses BFS/level-order
    search to find the shortest path to pacman, then follows that path to attack.
    
    Attributes:
        maze: Maze object representing the game environment
        pos: Current position as (row, col) tuple
        path: Current path to target (list of positions)
        target_pos: Position of target (pacman) to chase
        move_delay_frames: Number of frames to wait between moves
        frame_count: Internal counter for movement timing
        search_algorithm: Which search algorithm to use ('bfs' or 'level_order')
    """
    
    def __init__(self, maze, start_pos, move_delay_frames=30, search_algorithm='bfs'):
        """
        Initialize Haduyi adversary.
        
        Args:
            maze: Maze object with grid, rows, and cols attributes
            start_pos: Tuple (row, col) representing starting position
            move_delay_frames: Number of frames between moves (default: 30)
            search_algorithm: 'bfs' or 'level_order' (default: 'bfs')
        """
        if not hasattr(maze, 'grid') or not hasattr(maze, 'rows') or not hasattr(maze, 'cols'):
            raise ValueError("Maze object must have 'grid', 'rows', and 'cols' attributes")
        
        self.maze = maze
        self.pos = start_pos
        self.target_pos = None  # Will be set when pacman is known
        self.path = []  # Current path to target
        self.move_delay_frames = move_delay_frames
        self.frame_count = 0
        self.search_algorithm = search_algorithm
        
        # Validate starting position
        if not is_passable_cell(maze, start_pos[0], start_pos[1]):
            raise ValueError(f"Starting position {start_pos} is not passable (wall or out of bounds)")
        
        logger.info(f"Haduyi initialized at position {self.pos} with search algorithm: {self.search_algorithm}")
    
    def update_target(self, target_pos):
        """
        Update the target position (pacman's position) to chase.
        
        Args:
            target_pos: Tuple (row, col) representing target position
        """
        if target_pos != self.target_pos:
            self.target_pos = target_pos
            logger.debug(f"Haduyi target updated to {target_pos}")
            # Recalculate path when target changes
            self._calculate_path()
    
    def _calculate_path(self):
        """Calculate path to target using the selected search algorithm."""
        if self.target_pos is None:
            self.path = []
            return
        
        if self.pos == self.target_pos:
            self.path = [self.pos]
            return
        
        # Use the selected search algorithm
        if self.search_algorithm == 'level_order':
            path = level_order_search(self.maze, self.pos, self.target_pos)
        else:  # Default to BFS
            path = bfs(self.maze, self.pos, self.target_pos)
        
        if path:
            # Remove current position from path (we're already there)
            if len(path) > 1:
                self.path = path[1:]  # Path without current position
            else:
                self.path = path
            logger.debug(f"Haduyi calculated path to target: {len(self.path)} steps remaining")
        else:
            self.path = []
            logger.warning(f"Haduyi could not find path from {self.pos} to {self.target_pos}")
    
    def is_valid_move(self, r, c):
        """Check if a position is valid for movement."""
        return is_passable_cell(self.maze, r, c)
    
    def move(self):
        """
        Move Haduyi along the path to target.
        
        This method should be called every frame. Movement is rate-limited
        internally based on move_delay_frames.
        """
        self.frame_count += 1
        
        # Only move every N frames to control speed
        if self.frame_count % self.move_delay_frames != 0:
            return
        
        # If no target, don't move
        if self.target_pos is None:
            return
        
        # If no path or path is empty, recalculate
        if not self.path:
            self._calculate_path()
        
        # If still no path, can't move
        if not self.path:
            logger.warning(f"Haduyi stuck at {self.pos}, no path to target {self.target_pos}")
            return
        
        # Move to next position in path
        next_pos = self.path[0]
        
        # Validate move before executing
        if self.is_valid_move(next_pos[0], next_pos[1]):
            old_pos = self.pos
            self.pos = next_pos
            self.path.pop(0)  # Remove completed step from path
            
            logger.debug(f"Haduyi moved from {old_pos} to {self.pos}")
            
            # If we reached the target, recalculate path in case target moved
            if self.pos == self.target_pos:
                logger.info(f"Haduyi reached target at {self.target_pos}!")
                self._calculate_path()
        else:
            # Path is invalid (target may have moved into a wall), recalculate
            logger.warning(f"Haduyi path blocked at {next_pos}, recalculating")
            self._calculate_path()
    
    def get_distance_to_target(self):
        """Get Manhattan distance to target."""
        if self.target_pos is None:
            return None
        return abs(self.pos[0] - self.target_pos[0]) + abs(self.pos[1] - self.target_pos[1])
    
    def is_at_target(self):
        """Check if Haduyi has reached the target."""
        return self.target_pos is not None and self.pos == self.target_pos


# Alias for backward compatibility
Ghost = Haduyi
