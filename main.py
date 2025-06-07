# Example file showing a circle moving on screen
import pygame
import numpy as np
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1024, 1024))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def getRandomColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return pygame.Color(r, g, b)

class Rectangle:
    def __init__(self, left, top, width, height, color):
        self.rect = pygame.Rect(left, top, width, height)
        self.color = color

    def get_rect(self):
        return self.rect

    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Grid:
    def __init__(self, left, top, width, height, rows, cols, color, line_width=2):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.rows_count = rows
        self.cols_count = cols

        self.rows = []
        self.cols = []
        self.line_width = line_width
        self.color = color

        self.row_cell_pixels = (height - (rows + 1) * self.line_width) / rows
        self.col_cell_pixels = (width - (cols + 1) * self.line_width) / cols

        for y in range(rows):
            row = Rectangle(
                left,
                y * self.row_cell_pixels + y * self.line_width + top,
                width,
                self.line_width,
                self.color
            )
            self.rows.append(row)
        last_row = Rectangle(
            left,
            height - self.line_width + top,
            width,
            self.line_width,
            self.color
        )
        self.rows.append(last_row)

        for x in range(cols):
            col = Rectangle(
                x * self.col_cell_pixels + x * self.line_width + left,
                top,
                self.line_width,
                height,
                self.color
            )
            self.cols.append(col)
        last_col = Rectangle(
            width - self.line_width + left,
            top,
            self.line_width,
            height,
            self.color
        )
        self.cols.append(last_col)

    def get_cell_position(self, x, y):
        cell_left = self.left + self.line_width + x * (self.col_cell_pixels + self.line_width)
        cell_top = self.top + self.line_width + y * (self.row_cell_pixels + self.line_width)

        center_x = cell_left + self.col_cell_pixels / 2
        center_y = cell_top + self.row_cell_pixels / 2

        return (center_x, center_y)

    def render(self, surface):
        if self.line_width <= 0:
            return
        for row in self.rows:
            row.render(surface)
        for col in self.cols:
            col.render(surface)


class ConwaysGame:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # Random grid of 0s and 1s
        self.grid = np.random.randint(2, size=(rows, cols), dtype=np.uint8)

    def get_live_cells(self):
        return np.argwhere(self.grid == 1) 

    def update(self):
        # Count neighbors using slicing (without loops)
        neighbors = sum(np.roll(np.roll(self.grid, i, 0), j, 1)
                        for i in (-1, 0, 1) for j in (-1, 0, 1)
                        if not (i == 0 and j == 0))

        # Apply rules:
        # 1. Cell survives if it has 2 or 3 neighbors and is currently alive
        # 2. Cell is born if it has exactly 3 neighbors and is currently dead
        self.grid = ((self.grid == 1) & ((neighbors == 2) | (neighbors == 3))) | \
                    ((self.grid == 0) & (neighbors == 3))
        self.grid = self.grid.astype(np.uint8)  # Ensure it's still binary


map_rows = 256
map_cols = 256
cell_size = 4
grid = Grid(0, 0, screen.get_width() - 0, screen.get_height() - 0, map_rows, map_cols, getRandomColor(), line_width=0)
game = ConwaysGame(map_rows, map_cols)

paused = False
font = pygame.font.SysFont(None, 24)
blue = (255, 165, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

    if not paused:
        game.update()
        
    screen.fill("black")

    grid.render(screen)

    live_cells = game.get_live_cells()

    for i, j in live_cells:
        x, y = grid.get_cell_position(i, j)
        pygame.draw.rect(screen, "white", (x - cell_size // 2, y - cell_size // 2, cell_size, cell_size))

    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, blue)
    screen.blit(fps_text, (screen.get_width() - fps_text.get_width() - 10, 10))

    pygame.display.flip()

    dt = clock.tick(1000) / 1000

pygame.quit()