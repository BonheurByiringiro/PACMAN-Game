import pygame
from maze import Maze
from pacman_agent import PacmanAgent

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 700))
    pygame.display.set_caption("Automated PACMAN AI")
    maze = Maze("maze_layout.txt")
    pacman = PacmanAgent(maze)
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pacman.move()
        maze.draw(screen, pacman)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
