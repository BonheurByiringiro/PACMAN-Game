import unittest
from src.maze import Maze

class TestMaze(unittest.TestCase):
    def test_maze_loads(self):
        maze = Maze("maze_layout.txt")
        self.assertEqual(maze.rows, 5)
        self.assertEqual(maze.cols, 10)

if __name__ == '__main__':
    unittest.main()
