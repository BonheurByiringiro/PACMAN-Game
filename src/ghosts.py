import logging
from search_algorithms import (
    bfs, level_order_search, is_passable_cell,
    greedy_search, lazy_greedy_search, optimized_bfs,
    get_search_algorithm_for_difficulty
)

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
    
    def __init__(self, maze, start_pos, move_delay_frames=30, search_algorithm=None, difficulty=None):
        """
        Initialize Haduyi adversary.
        
        Args:
            maze: Maze object with grid, rows, and cols attributes
            start_pos: Tuple (row, col) representing starting position
            move_delay_frames: Number of frames between moves (default: 30)
            search_algorithm: Algorithm name ('bfs', 'greedy', 'lazy_greedy', 'optimized_bfs', 'level_order')
                           If None and difficulty is provided, uses difficulty instead.
            difficulty: Difficulty level ('easy', 'medium', 'hard', 'extreme' or 1-4)
                       Takes precedence over search_algorithm if both provided.
                       If neither provided, defaults to 'hard' (bfs).
        """
        if not hasattr(maze, 'grid') or not hasattr(maze, 'rows') or not hasattr(maze, 'cols'):
            raise ValueError("Maze object must have 'grid', 'rows', and 'cols' attributes")
        
        self.maze = maze
        self.pos = start_pos
        self.target_pos = None  # Will be set when pacman is known
        self.path = []  # Current path to target
        self.move_delay_frames = move_delay_frames
        self.frame_count = 0
        
        # Handle difficulty vs search_algorithm
        # If difficulty is provided, it takes precedence
        if difficulty is not None:
            _, self.search_algorithm = get_search_algorithm_for_difficulty(difficulty)
            self.difficulty = difficulty
        elif search_algorithm is not None:
            # Check if search_algorithm is actually a difficulty level
            try:
                _, self.search_algorithm = get_search_algorithm_for_difficulty(search_algorithm)
                self.difficulty = search_algorithm
                logger.debug(f"Interpreted '{search_algorithm}' as difficulty level")
            except (KeyError, AttributeError):
                # It's an actual algorithm name
                self.search_algorithm = search_algorithm
                self.difficulty = None
        else:
            # Default to hard difficulty (bfs)
            _, self.search_algorithm = get_search_algorithm_for_difficulty('hard')
            self.difficulty = 'hard'
        
        # Validate starting position
        if not is_passable_cell(maze, start_pos[0], start_pos[1]):
            raise ValueError(f"Starting position {start_pos} is not passable (wall or out of bounds)")
        
        diff_info = f"difficulty: {self.difficulty}" if self.difficulty else ""
        logger.info(f"Haduyi initialized at position {self.pos} with search algorithm: {self.search_algorithm} ({diff_info})")
    
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
        elif self.search_algorithm == 'greedy':
            path = greedy_search(self.maze, self.pos, self.target_pos)
        elif self.search_algorithm == 'lazy_greedy':
            path = lazy_greedy_search(self.maze, self.pos, self.target_pos)
        elif self.search_algorithm == 'optimized_bfs':
            path = optimized_bfs(self.maze, self.pos, self.target_pos)
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


def set_haduyi_difficulty(haduyi_list, difficulty):
    """
    Set difficulty for a list of Haduyi adversaries.
    
    This function can be called from main.py when UI team adds difficulty selection.
    It updates all Haduyi in the list to use the appropriate search algorithm based on difficulty.
    
    Args:
        haduyi_list: List of Haduyi objects
        difficulty: String or int difficulty level ('easy', 'medium', 'hard', 'extreme' or 1-4)
    
    Example usage in main.py:
        from ghosts import Haduyi, set_haduyi_difficulty
        
        # Create Haduyi list (they can use difficulty directly or algorithm name)
        haduyi_list = [Haduyi(maze, start_pos=(3, 2), difficulty='medium'), ...]
        
        # When UI changes difficulty (e.g., user selects "Hard")
        set_haduyi_difficulty(haduyi_list, 'hard')
    
    Returns:
        None (modifies Haduyi objects in place)
    """
    _, algo_name = get_search_algorithm_for_difficulty(difficulty)
    
    for haduyi in haduyi_list:
        if hasattr(haduyi, 'search_algorithm'):
            haduyi.search_algorithm = algo_name
            haduyi.difficulty = difficulty  # Store difficulty for reference
            # Recalculate path with new algorithm if target is set
            if hasattr(haduyi, 'target_pos') and haduyi.target_pos:
                haduyi._calculate_path()
    
    logger.info(f"Set difficulty '{difficulty}' for {len(haduyi_list)} Haduyi adversaries (algorithm: {algo_name})")


# Alias for backward compatibility
Ghost = Haduyi
