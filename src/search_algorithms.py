from queue import Queue
import logging
import random

logger = logging.getLogger(__name__)

def is_passable_cell(maze, r, c):
    """Check if a cell is passable (empty or pellet, not a wall).
    
    Args:
        maze: Maze object with grid attribute
        r: Row index
        c: Column index
    
    Returns:
        True if cell is passable (0 or 2), False if wall (1) or out of bounds
    """
    if 0 <= r < maze.rows and 0 <= c < maze.cols:
        # 0 = empty, 2 = pellet (both passable), 1 = wall (not passable)
        return maze.grid[r][c] != 1
    return False

def bfs(maze, start, goal):
    """Breadth-First Search that explores all nodes at each level before moving down.
    
    This algorithm naturally searches level by level (all nodes at depth N before depth N+1),
    making it perfect for finding shortest paths in unweighted graphs.
    
    Args:
        maze: Maze object with grid, rows, and cols attributes
        start: Tuple (row, col) representing starting position
        goal: Tuple (row, col) representing goal position
    
    Returns:
        List of positions (path from start to goal) if path exists, None otherwise
    """
    visited = set()
    queue = Queue()
    queue.put((start, [start]))  # (current_position, path_so_far)
    
    while not queue.empty():
        curr, path = queue.get()
        
        if curr == goal:
            logger.debug(f"BFS found path from {start} to {goal} with {len(path)} steps")
            return path
        
        visited.add(curr)
        r, c = curr
        
        # Explore all neighbors at current level (all 4 directions)
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is passable and not visited
            if is_passable_cell(maze, nr, nc) and (nr, nc) not in visited:
                queue.put(((nr, nc), path + [(nr, nc)]))
                visited.add((nr, nc))  # Mark as visited immediately to avoid duplicates
    
    logger.warning(f"BFS: No path found from {start} to {goal}")
    return None

def level_order_search(maze, start, goal, max_depth=None):
    """Level-order BFS search that explicitly processes nodes level by level.
    
    This version processes all nodes at each depth level before proceeding to the next level.
    This ensures we explore all nodes at the same distance before moving deeper.
    This is a strict level-order traversal that searches ALL nodes at level N before level N+1.
    
    Args:
        maze: Maze object with grid, rows, and cols attributes
        start: Tuple (row, col) representing starting position
        goal: Tuple (row, col) representing goal position
        max_depth: Optional maximum depth to search (None = no limit)
    
    Returns:
        List of positions (path from start to goal) if path exists, None otherwise
    """
    if start == goal:
        return [start]
    
    visited = {start}
    current_level = [(start, [start])]  # List of (position, path) tuples at current depth
    current_depth = 0
    
    while current_level:
        # Check all nodes at current level before moving to next
        next_level = []
        
        for pos, path in current_level:
            # If goal found at current level, return immediately
            if pos == goal:
                logger.debug(f"Level-order search found path from {start} to {goal} at depth {current_depth}")
                return path
            
            r, c = pos
            neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
            
            # Explore all neighbors
            for dr, dc in neighbors:
                nr, nc = r + dr, c + dc
                
                if is_passable_cell(maze, nr, nc) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    next_path = path + [(nr, nc)]
                    next_level.append(((nr, nc), next_path))
        
        # Move to next depth level
        current_level = next_level
        current_depth += 1
        
        # Check depth limit
        if max_depth and current_depth > max_depth:
            break
    
    logger.warning(f"Level-order search: No path found from {start} to {goal}")
    return None

def greedy_search(maze, start, goal):
    """
    Greedy search that moves toward the goal (Manhattan distance heuristic).
    This is less optimal than BFS but simpler. Used for medium difficulty.
    
    Args:
        maze: Maze object with grid, rows, and cols attributes
        start: Tuple (row, col) representing starting position
        goal: Tuple (row, col) representing goal position
    
    Returns:
        List of positions (path from start to goal) if path exists, None otherwise
    """
    if start == goal:
        return [start]
    
    path = [start]
    current = start
    visited = {start}
    max_steps = maze.rows * maze.cols  # Prevent infinite loops
    
    for _ in range(max_steps):
        if current == goal:
            return path
        
        r, c = current
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        
        # Find neighbors and their distances to goal
        valid_neighbors = []
        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc
            if is_passable_cell(maze, nr, nc) and (nr, nc) not in visited:
                # Manhattan distance to goal
                distance = abs(nr - goal[0]) + abs(nc - goal[1])
                valid_neighbors.append(((nr, nc), distance))
        
        if not valid_neighbors:
            break
        
        # Sort by distance and pick the closest (greedy choice)
        valid_neighbors.sort(key=lambda x: x[1])
        current, _ = valid_neighbors[0]
        visited.add(current)
        path.append(current)
    
    logger.debug(f"Greedy search reached limit or got stuck")
    return path if current == goal else None

def lazy_greedy_search(maze, start, goal, suboptimal_chance=0.3):
    """
    Lazy greedy search that sometimes makes suboptimal moves.
    Used for easy difficulty - makes Haduyi less efficient at catching pacman.
    
    Args:
        maze: Maze object with grid, rows, and cols attributes
        start: Tuple (row, col) representing starting position
        goal: Tuple (row, col) representing goal position
        suboptimal_chance: Probability of choosing a suboptimal move (0.0-1.0)
    
    Returns:
        List of positions (path from start to goal) if path exists, None otherwise
    """
    if start == goal:
        return [start]
    
    path = [start]
    current = start
    visited = {start}
    max_steps = maze.rows * maze.cols  # Prevent infinite loops
    
    for _ in range(max_steps):
        if current == goal:
            return path
        
        r, c = current
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Find valid neighbors and their distances to goal
        valid_neighbors = []
        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc
            if is_passable_cell(maze, nr, nc) and (nr, nc) not in visited:
                distance = abs(nr - goal[0]) + abs(nc - goal[1])
                valid_neighbors.append(((nr, nc), distance))
        
        if not valid_neighbors:
            break
        
        # Sort by distance
        valid_neighbors.sort(key=lambda x: x[1])
        
        # Sometimes choose a suboptimal move (makes it easier)
        if random.random() < suboptimal_chance and len(valid_neighbors) > 1:
            # Choose randomly from top 50% (not always the best)
            top_half = valid_neighbors[:max(2, len(valid_neighbors) // 2)]
            current, _ = random.choice(top_half)
        else:
            # Choose the best move
            current, _ = valid_neighbors[0]
        
        visited.add(current)
        path.append(current)
    
    logger.debug(f"Lazy greedy search reached limit or got stuck")
    return path if current == goal else None

def optimized_bfs(maze, start, goal):
    """
    Optimized BFS with immediate goal checking and better neighbor ordering.
    Used for extreme/hard difficulty - most efficient at catching pacman.
    
    This version checks for goal immediately when neighbors are explored,
    potentially finding paths faster than standard BFS.
    
    Args:
        maze: Maze object with grid, rows, and cols attributes
        start: Tuple (row, col) representing starting position
        goal: Tuple (row, col) representing goal position
    
    Returns:
        List of positions (path from start to goal) if path exists, None otherwise
    """
    if start == goal:
        return [start]
    
    visited = set()
    queue = Queue()
    queue.put((start, [start]))
    
    while not queue.empty():
        curr, path = queue.get()
        
        if curr == goal:
            logger.debug(f"Optimized BFS found path from {start} to {goal} with {len(path)} steps")
            return path
        
        visited.add(curr)
        r, c = curr
        
        # Order neighbors by Manhattan distance to goal (heuristic optimization)
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbor_list = []
        
        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc
            if is_passable_cell(maze, nr, nc) and (nr, nc) not in visited:
                # Check if this is the goal immediately
                if (nr, nc) == goal:
                    logger.debug(f"Optimized BFS found goal immediately")
                    return path + [(nr, nc)]
                
                # Calculate distance to goal for ordering
                distance = abs(nr - goal[0]) + abs(nc - goal[1])
                neighbor_list.append(((nr, nc), distance))
        
        # Sort by distance to goal (explore promising paths first)
        neighbor_list.sort(key=lambda x: x[1])
        
        for (nr, nc), _ in neighbor_list:
            queue.put(((nr, nc), path + [(nr, nc)]))
            visited.add((nr, nc))
    
    logger.warning(f"Optimized BFS: No path found from {start} to {goal}")
    return None

def get_search_algorithm_for_difficulty(difficulty):
    """
    Get the appropriate search algorithm function based on difficulty level.
    
    This function can be called from main.py when UI team adds difficulty selection.
    
    Args:
        difficulty: String difficulty level - 'easy', 'medium', 'hard', 'extreme'
                   or integer 1-4 where 1=easy, 4=extreme
    
    Returns:
        Tuple: (search_function, algorithm_name)
        - search_function: Function to use for pathfinding
        - algorithm_name: String name of the algorithm
    
    Example usage in main.py:
        from search_algorithms import get_search_algorithm_for_difficulty
        
        # When UI sets difficulty
        search_func, algo_name = get_search_algorithm_for_difficulty('hard')
        
        # Create Haduyi with difficulty-based algorithm
        haduyi = Haduyi(maze, start_pos=(3, 2), search_algorithm=algo_name)
    """
    # Normalize difficulty input
    difficulty_map = {
        'easy': 'easy',
        'e': 'easy',
        '1': 'easy',
        1: 'easy',
        'medium': 'medium',
        'med': 'medium',
        'm': 'medium',
        '2': 'medium',
        2: 'medium',
        'hard': 'hard',
        'h': 'hard',
        '3': 'hard',
        3: 'hard',
        'extreme': 'extreme',
        'ext': 'extreme',
        'x': 'extreme',
        '4': 'extreme',
        4: 'extreme',
    }
    
    normalized = difficulty_map.get(difficulty.lower() if isinstance(difficulty, str) else difficulty, 'hard')
    
    # Map to search algorithms
    algorithms = {
        'easy': (lazy_greedy_search, 'lazy_greedy'),
        'medium': (greedy_search, 'greedy'),
        'hard': (bfs, 'bfs'),
        'extreme': (optimized_bfs, 'optimized_bfs'),
    }
    
    search_func, algo_name = algorithms.get(normalized, algorithms['hard'])
    logger.info(f"Difficulty '{difficulty}' mapped to '{normalized}' using algorithm: {algo_name}")
    
    return search_func, algo_name
