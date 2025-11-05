from queue import Queue

def bfs(maze, start, goal):
    visited = set()
    queue = Queue()
    queue.put((start, [start]))
    while not queue.empty():
        curr, path = queue.get()
        if curr == goal:
            return path
        visited.add(curr)
        r, c = curr
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < maze.rows and 0 <= nc < maze.cols and maze.grid[nr][nc] == 0:
                if (nr, nc) not in visited:
                    queue.put(((nr, nc), path + [(nr, nc)]))
    return None
