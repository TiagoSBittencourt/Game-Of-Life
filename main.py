import pygame
import numpy as np

# Display setup
HEIGHT, WIDTH = 750, 750
SQUARE_SIZE = 50
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
SCREEN_COLOR = BLACK_COLOR

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

# Initialize grid with boolean values
rows, cols = HEIGHT // SQUARE_SIZE, WIDTH // SQUARE_SIZE
grid = np.zeros((rows, cols), dtype=bool)  # Create a grid with boolean values

def gameLoop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                grid[row, col] = not grid[row, col]  # Toggle cell state

        screen.fill(SCREEN_COLOR)
        drawCells()
        drawGrid()

        pygame.display.update()
        clock.tick(30)  # Set the frame rate

def drawGrid():
    for x in range(0, WIDTH, SQUARE_SIZE):
        for y in range(0, HEIGHT, SQUARE_SIZE):
            rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, WHITE_COLOR, rect, 1)

def drawCells():
    for x in range(rows):
        for y in range(cols):
            color = WHITE_COLOR if grid[x, y] else BLACK_COLOR
            pygame.draw.rect(screen, color, pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))




gameLoop()