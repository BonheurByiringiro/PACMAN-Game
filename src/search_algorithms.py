from queue import Queue
import logging

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
