"""
Intelligent PACMAN Agent - Rational Agent Using Search Algorithms

This module implements a rational PACMAN agent that uses search algorithms
(BFS, DFS, A*, UCS) to plan optimal paths for pellet collection while avoiding ghosts.

The agent:
- Analyzes the maze environment
- Uses search algorithms to find paths to pellets
- Avoids ghosts by factoring their positions into pathfinding
- Makes intelligent decisions about which pellet to pursue
- Recalculates paths dynamically as the environment changes
"""

import logging
from search_algorithms import bfs, dfs, astar, uniform_cost_search, manhattan_distance

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [INTELLIGENT PACMAN] - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class IntelligentPacmanAgent:
    """
    Intelligent PACMAN agent that uses search algorithms for decision-making.
    
    This agent is a rational agent that:
    - Uses search algorithms (BFS, DFS, A*, UCS) to plan paths
    - Dynamically selects target pellets based on strategy
    - Avoids ghosts by incorporating their positions into pathfinding
    - Recalculates paths when environment changes
    """
    
    def __init__(self, maze, start_pos=(1, 1), search_algorithm='astar', move_delay_frames=15):
        """
        Initialize the intelligent PACMAN agent.
        
        Args:
            maze: Maze object with grid, rows, cols attributes
            start_pos: Starting position (row, col)
            search_algorithm: Algorithm to use ('bfs', 'dfs', 'astar', 'ucs')
            move_delay_frames: Frames between moves (controls speed)
        """
        self.maze = maze
        self.pos = start_pos
        self.start_pos = start_pos
        self.search_algorithm = search_algorithm
        self.move_delay_frames = move_delay_frames
        self.frame_count = 0
        
        # Path planning
        self.current_path = []
        self.target_pellet = None
        self.pellets_collected = 0
        self.total_pellets = self._count_pellets()
        
        # Ghost awareness
        self.ghost_positions = set()
        self.danger_zone_radius = 3  # Avoid ghosts within this distance
        
        # Decision making
        self.strategy = 'nearest_safe'  # 'nearest', 'nearest_safe', 'furthest_from_ghosts'
        self.recalculate_frequency = 30  # Recalculate path every N frames
        
        # Algorithm mapping
        self.algorithm_functions = {
            'bfs': bfs,
            'dfs': dfs,
            'astar': astar,
            'ucs': uniform_cost_search
        }
        
        logger.info(f"Intelligent PACMAN initialized at {self.pos} using {search_algorithm}")
        logger.info(f"Total pellets to collect: {self.total_pellets}")
        logger.info(f"Strategy: {self.strategy}")
    
    def _count_pellets(self):
        """Count total pellets in the maze."""
        count = 0
        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                if self.maze.grid[r][c] == 2:
                    count += 1
        return count
    
    def _get_all_pellets(self):
        """Get positions of all remaining pellets in the maze."""
        pellets = []
        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                if self.maze.grid[r][c] == 2:
                    pellets.append((r, c))
        return pellets
    
    def _is_safe_position(self, pos):
        """Check if a position is safe (not too close to ghosts)."""
        for ghost_pos in self.ghost_positions:
            if manhattan_distance(pos, ghost_pos) <= self.danger_zone_radius:
                return False
        return True
    
    def _get_dangerous_positions(self):
        """Get all positions that are dangerous (near ghosts)."""
        dangerous = set()
        for ghost_pos in self.ghost_positions:
            gr, gc = ghost_pos
            # Add positions within danger zone
            for dr in range(-self.danger_zone_radius, self.danger_zone_radius + 1):
                for dc in range(-self.danger_zone_radius, self.danger_zone_radius + 1):
                    r, c = gr + dr, gc + dc
                    if 0 <= r < self.maze.rows and 0 <= c < self.maze.cols:
                        if manhattan_distance((r, c), ghost_pos) <= self.danger_zone_radius:
                            dangerous.add((r, c))
        return dangerous
    
    def _select_target_pellet(self):
        """
        Select the best pellet to pursue based on strategy.
        
        Strategies:
        - 'nearest': Simply go to nearest pellet
        - 'nearest_safe': Go to nearest pellet that's safe from ghosts
        - 'furthest_from_ghosts': Go to pellet furthest from all ghosts
        
        Returns:
            Tuple (row, col) of target pellet, or None if no pellets
        """
        pellets = self._get_all_pellets()
        
        if not pellets:
            logger.info("No pellets remaining!")
            return None
        
        if self.strategy == 'nearest':
            # Simply find nearest pellet
            pellets_with_dist = [(p, manhattan_distance(self.pos, p)) for p in pellets]
            pellets_with_dist.sort(key=lambda x: x[1])
            target = pellets_with_dist[0][0]
            logger.debug(f"Selected NEAREST pellet: {target}")
            return target
        
        elif self.strategy == 'nearest_safe':
            # Find nearest safe pellet, fallback to nearest if none are safe
            safe_pellets = [p for p in pellets if self._is_safe_position(p)]
            
            if safe_pellets:
                pellets_with_dist = [(p, manhattan_distance(self.pos, p)) for p in safe_pellets]
                pellets_with_dist.sort(key=lambda x: x[1])
                target = pellets_with_dist[0][0]
                logger.debug(f"Selected NEAREST SAFE pellet: {target}")
                return target
            else:
                # No safe pellets, go to nearest anyway
                pellets_with_dist = [(p, manhattan_distance(self.pos, p)) for p in pellets]
                pellets_with_dist.sort(key=lambda x: x[1])
                target = pellets_with_dist[0][0]
                logger.warning(f"No safe pellets! Selected nearest: {target}")
                return target
        
        elif self.strategy == 'furthest_from_ghosts':
            # Find pellet that maximizes minimum distance to all ghosts
            def min_ghost_distance(pellet):
                if not self.ghost_positions:
                    return float('inf')
                return min(manhattan_distance(pellet, ghost) for ghost in self.ghost_positions)
            
            pellets_with_safety = [(p, min_ghost_distance(p)) for p in pellets]
            pellets_with_safety.sort(key=lambda x: x[1], reverse=True)
            target = pellets_with_safety[0][0]
            logger.debug(f"Selected FURTHEST FROM GHOSTS pellet: {target}")
            return target
        
        # Default to nearest
        return pellets[0]
    
    def _calculate_path_to_target(self):
        """
        Calculate path to target pellet using selected search algorithm.
        
        Factors in ghost positions for A* and UCS algorithms.
        """
        if self.target_pellet is None:
            return None
        
        # Get dangerous positions to avoid
        avoid_positions = self._get_dangerous_positions() if self.ghost_positions else set()
        
        # Select search algorithm
        search_func = self.algorithm_functions.get(self.search_algorithm, astar)
        
        # Some algorithms support ghost avoidance
        if self.search_algorithm in ['astar', 'ucs']:
            path = search_func(self.maze, self.pos, self.target_pellet, avoid_positions)
        else:
            path = search_func(self.maze, self.pos, self.target_pellet)
        
        if path:
            logger.debug(f"Calculated path to {self.target_pellet}: {len(path)} steps using {self.search_algorithm}")
            # Remove current position from path
            if len(path) > 1 and path[0] == self.pos:
                return path[1:]
            return path
        else:
            logger.warning(f"Could not find path to {self.target_pellet}")
            return None
    
    def update_ghost_positions(self, ghost_list):
        """
        Update knowledge of ghost positions.
        
        Args:
            ghost_list: List of ghost objects with 'pos' attribute
        """
        self.ghost_positions = set()
        for ghost in ghost_list:
            if hasattr(ghost, 'pos'):
                self.ghost_positions.add(ghost.pos)
        
        logger.debug(f"Updated ghost positions: {self.ghost_positions}")
    
    def plan_next_move(self):
        """
        Plan the next move using search algorithms.
        
        This is the core decision-making function that:
        1. Selects a target pellet
        2. Calculates path using search algorithm
        3. Factors in ghost positions
        """
        # Select target if we don't have one or reached it
        if self.target_pellet is None or self.maze.grid[self.target_pellet[0]][self.target_pellet[1]] != 2:
            self.target_pellet = self._select_target_pellet()
            if self.target_pellet is None:
                logger.info("No more pellets to collect!")
                return
        
        # Calculate or recalculate path
        if not self.current_path or self.frame_count % self.recalculate_frequency == 0:
            self.current_path = self._calculate_path_to_target()
            
            if not self.current_path:
                # Can't reach target, try another
                logger.warning(f"Cannot reach target {self.target_pellet}, selecting new target")
                self.target_pellet = None
                self.current_path = []
    
    def move(self):
        """
        Execute one move step along the planned path.
        
        Called every frame. Movement is rate-limited by move_delay_frames.
        """
        self.frame_count += 1
        
        # Only move every N frames
        if self.frame_count % self.move_delay_frames != 0:
            return
        
        # Plan next move if needed
        self.plan_next_move()
        
        # Execute move if we have a path
        if self.current_path:
            next_pos = self.current_path[0]
            
            # Check if next position is still valid (not a wall, pellet might be collected)
            if self.maze.grid[next_pos[0]][next_pos[1]] != 1:
                old_pos = self.pos
                self.pos = next_pos
                self.current_path.pop(0)
                
                # Collect pellet if present
                if self.maze.grid[self.pos[0]][self.pos[1]] == 2:
                    self.maze.grid[self.pos[0]][self.pos[1]] = 0
                    self.pellets_collected += 1
                    logger.info(f"Pellet collected at {self.pos}! ({self.pellets_collected}/{self.total_pellets})")
                    
                    # Clear target so we select a new one
                    self.target_pellet = None
                    self.current_path = []
                
                logger.debug(f"Moved from {old_pos} to {self.pos}")
            else:
                # Path is blocked, recalculate
                logger.warning(f"Path blocked at {next_pos}, recalculating")
                self.current_path = []
        else:
            logger.debug("No path to follow")
    
    def is_valid_move(self, r, c):
        """Check if a position is valid (not a wall)."""
        if 0 <= r < self.maze.rows and 0 <= c < self.maze.cols:
            return self.maze.grid[r][c] != 1
        return False
    
    def set_strategy(self, strategy):
        """
        Change the pellet selection strategy.
        
        Args:
            strategy: 'nearest', 'nearest_safe', or 'furthest_from_ghosts'
        """
        if strategy in ['nearest', 'nearest_safe', 'furthest_from_ghosts']:
            self.strategy = strategy
            logger.info(f"Strategy changed to: {strategy}")
            # Clear current target to force reselection
            self.target_pellet = None
            self.current_path = []
    
    def set_search_algorithm(self, algorithm):
        """
        Change the search algorithm used for pathfinding.
        
        Args:
            algorithm: 'bfs', 'dfs', 'astar', or 'ucs'
        """
        if algorithm in self.algorithm_functions:
            self.search_algorithm = algorithm
            logger.info(f"Search algorithm changed to: {algorithm}")
            # Recalculate path with new algorithm
            self.current_path = []
    
    def all_pellets_collected(self):
        """Check if all pellets have been collected (win condition)."""
        return self.pellets_collected >= self.total_pellets
    
    def reset(self):
        """Reset agent to starting position."""
        self.pos = self.start_pos
        self.current_path = []
        self.target_pellet = None
        self.pellets_collected = 0
        self.ghost_positions = set()
        logger.info("Agent reset")
    
    def get_decision_info(self):
        """
        Get information about agent's current decision-making.
        
        Useful for visualization and debugging.
        
        Returns:
            Dictionary with decision information
        """
        return {
            'position': self.pos,
            'target': self.target_pellet,
            'path_length': len(self.current_path) if self.current_path else 0,
            'algorithm': self.search_algorithm,
            'strategy': self.strategy,
            'pellets_collected': self.pellets_collected,
            'total_pellets': self.total_pellets,
            'ghosts_tracked': len(self.ghost_positions)
        }
