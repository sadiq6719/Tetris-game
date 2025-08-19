import pygame
import random

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
SIDE_PANEL = 150
win = pygame.display.set_mode((WIDTH + SIDE_PANEL, HEIGHT))
pygame.display.set_caption("Tetris")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],                # I
    [[1, 1], [1, 1]],              # O
    [[0, 1, 0], [1, 1, 1]],        # T
    [[1, 0, 0], [1, 1, 1]],        # L
    [[0, 0, 1], [1, 1, 1]],        # J
    [[1, 1, 0], [0, 1, 1]],        # S
    [[0, 1, 1], [1, 1, 0]]         # Z
]
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, GREEN, BLUE, RED, WHITE]

# Fonts
font = pygame.font.SysFont("comicsans", 28, bold=True)

# Create grid
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(WIDTH // BLOCK_SIZE)] for _ in range(HEIGHT // BLOCK_SIZE)]
    for (x, y), color in locked_positions.items():
        grid[y][x] = color
    return grid

# Draw grid
def draw_grid(surface, grid):
    surface.fill(BLACK)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x],
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    for i in range(WIDTH // BLOCK_SIZE):
        pygame.draw.line(surface, WHITE, (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, HEIGHT))
    for j in range(HEIGHT // BLOCK_SIZE):
        pygame.draw.line(surface, WHITE, (0, j * BLOCK_SIZE), (WIDTH, j * BLOCK_SIZE))

# Piece class
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Check if valid move
def valid_position(piece, grid):
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                if (j + piece.x < 0 or j + piece.x >= WIDTH // BLOCK_SIZE or
                    i + piece.y >= HEIGHT // BLOCK_SIZE or
                    grid[i + piece.y][j + piece.x] != BLACK):
                    return False
    return True

# Place piece
def place_piece(piece, locked_positions):
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                locked_positions[(j + piece.x, i + piece.y)] = piece.color

# Clear rows
def clear_rows(locked_positions):
    full_rows = 0
    for y in range(HEIGHT // BLOCK_SIZE):
        if all((x, y) in locked_positions for x in range(WIDTH // BLOCK_SIZE)):
            full_rows += 1
            for x in range(WIDTH // BLOCK_SIZE):
                del locked_positions[(x, y)]
            # Shift rows down
            for key in sorted(list(locked_positions), key=lambda k: k[1])[::-1]:
                x, yy = key
                if yy < y:
                    locked_positions[(x, yy + 1)] = locked_positions.pop((x, yy))
    return full_rows

# Draw side panel
def draw_side_panel(surface, next_piece, score):
    # Background
    pygame.draw.rect(surface, (30, 30, 30), (WIDTH, 0, SIDE_PANEL, HEIGHT))

    # Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (WIDTH + 20, 20))

    # Next piece
    next_text = font.render("Next:", True, WHITE)
    surface.blit(next_text, (WIDTH + 20, 80))

    for i, row in enumerate(next_piece.shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, next_piece.color,
                                 (WIDTH + 20 + j * BLOCK_SIZE,
                                  120 + i * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE), 0)

# Game over screen
def draw_game_over(surface, score):
    surface.fill(BLACK)
    over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    surface.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 40))
    surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(3000)

# Main
def main():
    clock = pygame.time.Clock()
    locked_positions = {}
    grid = create_grid(locked_positions)

    current_piece = Piece(3, 0, random.choice(SHAPES))
    next_piece = Piece(3, 0, random.choice(SHAPES))
    fall_time = 0
    fall_speed = 0.5
    score = 0

    running = True
    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # Fall
        if fall_time / 1000 >= fall_speed:
            current_piece.y += 1
            if not valid_position(current_piece, grid):
                current_piece.y -= 1
                place_piece(current_piece, locked_positions)
                score += clear_rows(locked_positions) * 100
                current_piece = next_piece
                next_piece = Piece(3, 0, random.choice(SHAPES))
                if not valid_position(current_piece, grid):
                    draw_game_over(win, score)
                    running = False
            fall_time = 0

        # Controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_position(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_position(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_position(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_position(current_piece, grid):
                        # undo 3 rotations
                        for _ in range(3):
                            current_piece.rotate()

        # Draw current piece
        for i, row in enumerate(current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    grid[i + current_piece.y][j + current_piece.x] = current_piece.color

        draw_grid(win, grid)
        draw_side_panel(win, next_piece, score)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
