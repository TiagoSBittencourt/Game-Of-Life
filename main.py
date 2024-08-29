import pygame
import numpy as np

# Display setup
HEIGHT, WIDTH = 750, 750
SQUARE_SIZE = 50
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
SCREEN_COLOR = BLACK_COLOR
COUNTER_COLOR = (139, 0, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 54)
counter_pos = (WIDTH//2, SQUARE_SIZE//2)

# Initialize grid with boolean values
rows, cols = HEIGHT // SQUARE_SIZE, WIDTH // SQUARE_SIZE
grid = np.zeros((rows, cols), dtype=bool)  # Create a grid with boolean values

def gameLoop():
    countGeneratins = 0
    count_text = font.render(str(countGeneratins), True, COUNTER_COLOR)
    text_rect = count_text.get_rect(center=counter_pos)
    holding_left = False
    holding_right = False
    running = True
    fps = 60
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    holding_left = True
                    x, y = pygame.mouse.get_pos()
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    grid[row, col] = not grid[row, col]  # Change cell state
                if event.button == 3:
                    holding_right = True
                    fps = 8 # Slower visualization while holding
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    holding_left = False
                if event.button == 3:
                    holding_right = False
                    fps = 60

        if holding_right:
            count_text = font.render(str(countGeneratins), True, (COUNTER_COLOR))
            text_rect = count_text.get_rect(center=counter_pos)
            countGeneratins += 1
            nextGen()
        if holding_left:
            countGeneratins = 0
            count_text = font.render(str(countGeneratins), True, (COUNTER_COLOR))
            text_rect = count_text.get_rect(center=counter_pos)
            nx, ny = pygame.mouse.get_pos()
            if nx // SQUARE_SIZE != x // SQUARE_SIZE or ny // SQUARE_SIZE != y // SQUARE_SIZE:
                x, y = nx, ny
                row, col = (y // SQUARE_SIZE) % (WIDTH // SQUARE_SIZE), (x // SQUARE_SIZE) % (HEIGHT // SQUARE_SIZE)
                grid[row, col] = not grid[row, col]  # Change cell state

        screen.fill(SCREEN_COLOR)
        drawCells()
        drawGrid()
        screen.blit(count_text, text_rect)

        pygame.display.update()
        clock.tick(fps)  # Set the frame rate

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

def nextGen():
    global grid

    # Neighbors search func
    def findNeighbors(row, col):
        neighbors = []
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if (i != row or j != col) and 0 <= i < rows and 0 <= j < cols:
                    neighbors.append(grid[i, j])
        return neighbors

    # Temporary grid to store updates for the next generation
    tempGrid = np.copy(grid)
    
    for i in range(rows):
        for j in range(cols):
            neighbors = findNeighbors(i, j)
            sumNeighbors = sum(neighbors)
            if grid[i, j]:  
                if sumNeighbors < 2 or sumNeighbors > 3: # Death Rule
                    tempGrid[i, j] = False  
            else:  # Cell is dead
                if sumNeighbors == 3:
                    tempGrid[i, j] = True  # Birth Rule
    
    # Update the grid with the new generation
    grid = tempGrid

gameLoop()