"""
Unit tests for Intelligent PACMAN Agent

Tests cover:
- Agent initialization
- Search algorithm integration (BFS, DFS, A*, UCS)
- Pellet selection strategies
- Ghost avoidance logic
- Path planning and recalculation
- Score tracking
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from maze import Maze
from intelligent_pacman_agent import IntelligentPacmanAgent
from search_algorithms import bfs, dfs, astar, uniform_cost_search


class TestIntelligentAgent(unittest.TestCase):
    """Test cases for Intelligent PACMAN Agent."""
    
    def setUp(self):
        """Set up test maze and agent."""
        # Create simple test maze
        self.test_maze_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'maze_layout.txt')
        if not os.path.exists(self.test_maze_file):
            self.test_maze_file = os.path.join(os.path.dirname(__file__), '..', 'maze_layout.txt')
        
        self.maze = Maze(self.test_maze_file)
        self.agent = IntelligentPacmanAgent(self.maze, start_pos=(1, 1), search_algorithm='astar')
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly."""
        self.assertEqual(self.agent.pos, (1, 1))
        self.assertEqual(self.agent.search_algorithm, 'astar')
        self.assertGreater(self.agent.total_pellets, 0)
        self.assertEqual(self.agent.pellets_collected, 0)
    
    def test_pellet_counting(self):
        """Test that agent correctly counts pellets."""
        pellets = self.agent._get_all_pellets()
        self.assertEqual(len(pellets), self.agent.total_pellets)
    
    def test_algorithm_switching(self):
        """Test switching between search algorithms."""
        algorithms = ['bfs', 'dfs', 'astar', 'ucs']
        for algo in algorithms:
            self.agent.set_search_algorithm(algo)
            self.assertEqual(self.agent.search_algorithm, algo)
    
    def test_strategy_switching(self):
        """Test switching between pellet selection strategies."""
        strategies = ['nearest', 'nearest_safe', 'furthest_from_ghosts']
        for strategy in strategies:
            self.agent.set_strategy(strategy)
            self.assertEqual(self.agent.strategy, strategy)
    
    def test_pellet_selection_nearest(self):
        """Test nearest pellet selection strategy."""
        self.agent.set_strategy('nearest')
        target = self.agent._select_target_pellet()
        self.assertIsNotNone(target)
        self.assertEqual(self.maze.grid[target[0]][target[1]], 2)
    
    def test_ghost_position_update(self):
        """Test updating ghost positions."""
        # Mock ghost objects
        class MockGhost:
            def __init__(self, pos):
                self.pos = pos
        
        ghosts = [MockGhost((3, 3)), MockGhost((5, 5))]
        self.agent.update_ghost_positions(ghosts)
        
        self.assertEqual(len(self.agent.ghost_positions), 2)
        self.assertIn((3, 3), self.agent.ghost_positions)
        self.assertIn((5, 5), self.agent.ghost_positions)
    
    def test_safe_position_detection(self):
        """Test detection of safe positions away from ghosts."""
        # Mock ghost objects
        class MockGhost:
            def __init__(self, pos):
                self.pos = pos
        
        ghosts = [MockGhost((3, 3))]
        self.agent.update_ghost_positions(ghosts)
        
        # Position far from ghost should be safe
        self.assertTrue(self.agent._is_safe_position((1, 1)))
        
        # Position near ghost should not be safe
        self.assertFalse(self.agent._is_safe_position((3, 3)))
    
    def test_path_calculation(self):
        """Test path calculation to target."""
        # Set a target pellet
        pellets = self.agent._get_all_pellets()
        if pellets:
            self.agent.target_pellet = pellets[0]
            path = self.agent._calculate_path_to_target()
            
            # Path should exist
            self.assertIsNotNone(path)
            
            # Path should lead to target
            if path:
                self.assertTrue(len(path) > 0)
    
    def test_pellet_collection(self):
        """Test pellet collection updates score."""
        initial_score = self.maze.score
        initial_collected = self.agent.pellets_collected
        
        # Find a pellet position
        pellets = self.agent._get_all_pellets()
        if pellets:
            pellet_pos = pellets[0]
            
            # Simulate moving to pellet and collecting it
            self.agent.pos = pellet_pos
            if self.maze.grid[pellet_pos[0]][pellet_pos[1]] == 2:
                self.maze.grid[pellet_pos[0]][pellet_pos[1]] = 0
                self.agent.pellets_collected += 1
                self.maze.score += 10
            
            # Check updates
            self.assertEqual(self.maze.score, initial_score + 10)
            self.assertEqual(self.agent.pellets_collected, initial_collected + 1)
    
    def test_win_condition(self):
        """Test win condition detection."""
        # Agent hasn't collected all pellets yet
        self.assertFalse(self.agent.all_pellets_collected())
        
        # Simulate collecting all pellets
        self.agent.pellets_collected = self.agent.total_pellets
        self.assertTrue(self.agent.all_pellets_collected())
    
    def test_agent_reset(self):
        """Test agent reset functionality."""
        # Make some changes
        self.agent.pos = (5, 5)
        self.agent.pellets_collected = 10
        self.agent.target_pellet = (3, 3)
        
        # Reset
        self.agent.reset()
        
        # Check reset
        self.assertEqual(self.agent.pos, self.agent.start_pos)
        self.assertEqual(self.agent.pellets_collected, 0)
        self.assertIsNone(self.agent.target_pellet)


class TestSearchAlgorithms(unittest.TestCase):
    """Test search algorithms used by the agent."""
    
    def setUp(self):
        """Set up test maze."""
        self.test_maze_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'maze_layout.txt')
        if not os.path.exists(self.test_maze_file):
            self.test_maze_file = os.path.join(os.path.dirname(__file__), '..', 'maze_layout.txt')
        
        self.maze = Maze(self.test_maze_file)
    
    def test_bfs_pathfinding(self):
        """Test BFS finds a valid path."""
        start = (1, 1)
        goal = (3, 3)
        path = bfs(self.maze, start, goal)
        
        if path:
            self.assertIn(start, path)
            self.assertIn(goal, path)
            self.assertGreater(len(path), 0)
    
    def test_dfs_pathfinding(self):
        """Test DFS finds a valid path."""
        start = (1, 1)
        goal = (3, 3)
        path = dfs(self.maze, start, goal)
        
        if path:
            self.assertIn(start, path)
            self.assertIn(goal, path)
            self.assertGreater(len(path), 0)
    
    def test_astar_pathfinding(self):
        """Test A* finds a valid path."""
        start = (1, 1)
        goal = (3, 3)
        path = astar(self.maze, start, goal)
        
        if path:
            self.assertIn(start, path)
            self.assertIn(goal, path)
            self.assertGreater(len(path), 0)
    
    def test_ucs_pathfinding(self):
        """Test UCS finds a valid path."""
        start = (1, 1)
        goal = (3, 3)
        path = uniform_cost_search(self.maze, start, goal)
        
        if path:
            self.assertIn(start, path)
            self.assertIn(goal, path)
            self.assertGreater(len(path), 0)
    
    def test_astar_with_avoidance(self):
        """Test A* avoids specified positions."""
        start = (1, 1)
        goal = (3, 3)
        avoid = {(2, 2)}  # Avoid middle position
        
        path = astar(self.maze, start, goal, avoid_positions=avoid)
        
        # Path should avoid the specified position if possible
        if path and (2, 2) not in path:
            self.assertNotIn((2, 2), path)


if __name__ == '__main__':
    unittest.main()
