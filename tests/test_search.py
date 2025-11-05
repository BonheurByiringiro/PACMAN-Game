import unittest
from src.search_algorithms import bfs
from src.maze import Maze

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.maze = Maze("maze_layout.txt")

    def test_bfs(self):
        start, goal = (1,1), (1,3)
        path = bfs(self.maze, start, goal)
        self.assertIn(goal, path)

if __name__ == '__main__':
    unittest.main()
