import unittest
import os
from src.maze import Maze

class TestMaze(unittest.TestCase):
    def test_maze_loads(self):
        # Use test-specific maze file with known dimensions
        test_dir = os.path.dirname(os.path.abspath(__file__))
        test_maze_file = os.path.join(test_dir, "test_maze.txt")
        maze = Maze(test_maze_file)
        self.assertEqual(maze.rows, 5)
        self.assertEqual(maze.cols, 10)

if __name__ == '__main__':
    unittest.main()
