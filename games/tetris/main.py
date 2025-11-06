"""
🎮 TETRIS GAME - Educational Example

This is a simplified Tetris game to help you learn:
- 2D arrays (grids for the game board)
- Rotation logic (spinning pieces)
- Line clearing (removing full rows)
- Timing and gravity (pieces falling)

READ TIME: 20-25 minutes
DIFFICULTY: Medium 🟠

A more advanced example - lots to learn!
"""

import pygame
import random
import sys

# ============================================================================
# CONSTANTS
# ============================================================================

# Window settings
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
GRID_SIZE = 30

# Grid dimensions (in cells)
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Tetromino colors (the falling pieces)
COLORS = [
    (0, 255, 255),    # Cyan - I piece
    (255, 255, 0),    # Yellow - O piece
    (128, 0, 128),    # Purple - T piece
    (0, 255, 0),      # Green - S piece
    (255, 0, 0),      # Red - Z piece
    (0, 0, 255),      # Blue - J piece
    (255, 165, 0),    # Orange - L piece
]

# Tetromino shapes
# These are 2D ARRAYS (lists of lists)!
# 1 = filled block, 0 = empty space
SHAPES = [
    # I piece
    [[1, 1, 1, 1]],
    
    # O piece
    [[1, 1],
     [1, 1]],
    
    # T piece
    [[0, 1, 0],
     [1, 1, 1]],
    
    # S piece
    [[0, 1, 1],
     [1, 1, 0]],
    
    # Z piece
    [[1, 1, 0],
     [0, 1, 1]],
    
    # J piece
    [[1, 0, 0],
     [1, 1, 1]],
    
    # L piece
    [[0, 0, 1],
     [1, 1, 1]],
]

FPS = 60
FALL_SPEED = 500  # Milliseconds between drops


# ============================================================================
# TETROMINO CLASS
# ============================================================================

class Tetromino:
    """
    Represents a falling Tetris piece!
    
    DATA STRUCTURES:
    - self.shape is a 2D array (list of lists)
    - Each number in the array is either 0 or 1
    """
    
    def __init__(self):
        """Create a random tetromino at the top of the screen"""
        
        # Pick a random shape
        shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[shape_index]
        self.color = COLORS[shape_index]
        
        # Starting position (top-middle of grid)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
    
    def rotate(self):
        """
        Rotate the piece 90 degrees clockwise!
        
        ROTATION ALGORITHM:
        To rotate a 2D array, we:
        1. Transpose it (swap rows and columns)
        2. Reverse each row
        
        Example: [[1, 0],    becomes    [[0, 1],
                  [1, 1]]                 [1, 1]]
        """
        # Transpose: convert rows to columns
        rotated = list(zip(*self.shape))
        
        # Reverse each row
        rotated = [list(row[::-1]) for row in rotated]
        
        return rotated


# ============================================================================
# TETRIS GAME CLASS
# ============================================================================

class TetrisGame:
    """The main game logic!"""
    
    def __init__(self):
        """Initialize the game"""
        
        pygame.init()
        
        # Create window
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🎮 Tetris - Arrow Keys to Move, UP to Rotate!")
        
        self.clock = pygame.time.Clock()
        
        # Create the game grid
        # 2D ARRAY: A list of lists representing the board
        # 0 = empty, a color tuple = filled with that color
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Create first piece
        self.current_piece = Tetromino()
        
        # Timing for automatic falling
        self.last_fall_time = pygame.time.get_ticks()
        
        # Score and game state
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
    
    def check_collision(self, piece, offset_x=0, offset_y=0):
        """
        Check if a piece collides with the grid or walls
        
        COLLISION DETECTION:
        We check every filled block in the piece's shape
        against the game grid and boundaries
        """
        
        for row_idx, row in enumerate(piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:  # If this cell is filled
                    
                    # Calculate position in the grid
                    x = piece.x + col_idx + offset_x
                    y = piece.y + row_idx + offset_y
                    
                    # Check boundaries
                    if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                        return True
                    
                    # Check if below the top (prevents collision on spawn)
                    if y < 0:
                        continue
                    
                    # Check collision with existing blocks
                    if self.grid[y][x] != 0:
                        return True
        
        return False
    
    def lock_piece(self):
        """
        Lock the current piece into the grid
        
        GRID MANIPULATION:
        We copy the piece's shape into the main grid
        """
        
        for row_idx, row in enumerate(self.current_piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    x = self.current_piece.x + col_idx
                    y = self.current_piece.y + row_idx
                    
                    # Check for game over (piece at top)
                    if y < 0:
                        self.game_over = True
                        return
                    
                    # Place the color in the grid
                    self.grid[y][x] = self.current_piece.color
        
        # Check for completed lines
        self.clear_lines()
        
        # Create new piece
        self.current_piece = Tetromino()
    
    def clear_lines(self):
        """
        Remove completed lines and shift everything down
        
        LINE CLEARING ALGORITHM:
        1. Find all full rows
        2. Remove them
        3. Add empty rows at the top
        """
        
        lines_to_clear = []
        
        # Find full rows
        for row_idx, row in enumerate(self.grid):
            # all() checks if ALL items in a list are True (non-zero)
            if all(cell != 0 for cell in row):
                lines_to_clear.append(row_idx)
        
        # Remove full rows and add empty rows at top
        for row_idx in lines_to_clear:
            del self.grid[row_idx]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        # Update score
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            # More lines at once = more points!
            self.score += (len(lines_to_clear) ** 2) * 100
    
    def handle_input(self):
        """Handle keyboard input"""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.__init__()  # Restart
                continue
            
            if event.type == pygame.KEYDOWN:
                # Move left
                if event.key == pygame.K_LEFT:
                    if not self.check_collision(self.current_piece, offset_x=-1):
                        self.current_piece.x -= 1
                
                # Move right
                elif event.key == pygame.K_RIGHT:
                    if not self.check_collision(self.current_piece, offset_x=1):
                        self.current_piece.x += 1
                
                # Move down faster
                elif event.key == pygame.K_DOWN:
                    if not self.check_collision(self.current_piece, offset_y=1):
                        self.current_piece.y += 1
                        self.score += 1  # Bonus points for manual drop
                
                # Rotate
                elif event.key == pygame.K_UP:
                    rotated_shape = self.current_piece.rotate()
                    old_shape = self.current_piece.shape
                    self.current_piece.shape = rotated_shape
                    
                    # Check if rotation is valid
                    if self.check_collision(self.current_piece):
                        self.current_piece.shape = old_shape  # Undo rotation
    
    def update(self):
        """Update game state"""
        
        if self.game_over:
            return
        
        # Automatic falling
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time > FALL_SPEED:
            
            # Try to move piece down
            if not self.check_collision(self.current_piece, offset_y=1):
                self.current_piece.y += 1
            else:
                # Can't move down - lock it in place
                self.lock_piece()
            
            self.last_fall_time = current_time
    
    def draw(self):
        """Draw everything"""
        
        self.screen.fill(BLACK)
        
        # Draw the grid (locked pieces)
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                if cell != 0:  # If not empty
                    x = col_idx * GRID_SIZE
                    y = row_idx * GRID_SIZE
                    
                    pygame.draw.rect(self.screen, cell, [x, y, GRID_SIZE, GRID_SIZE])
                    pygame.draw.rect(self.screen, BLACK, [x, y, GRID_SIZE, GRID_SIZE], 2)
        
        # Draw the current piece
        if not self.game_over:
            for row_idx, row in enumerate(self.current_piece.shape):
                for col_idx, cell in enumerate(row):
                    if cell:
                        x = (self.current_piece.x + col_idx) * GRID_SIZE
                        y = (self.current_piece.y + row_idx) * GRID_SIZE
                        
                        pygame.draw.rect(self.screen, self.current_piece.color,
                                       [x, y, GRID_SIZE, GRID_SIZE])
                        pygame.draw.rect(self.screen, BLACK,
                                       [x, y, GRID_SIZE, GRID_SIZE], 2)
        
        # Draw grid lines
        for i in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, GRAY, (i * GRID_SIZE, 0),
                           (i * GRID_SIZE, WINDOW_HEIGHT), 1)
        for i in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, GRAY, (0, i * GRID_SIZE),
                           (WINDOW_WIDTH, i * GRID_SIZE), 1)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        lines_text = font.render(f'Lines: {self.lines_cleared}', True, WHITE)
        self.screen.blit(lines_text, (10, 50))
        
        # Draw game over
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            big_font = pygame.font.Font(None, 48)
            game_over_text = big_font.render('GAME OVER', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
            
            small_font = pygame.font.Font(None, 24)
            restart_text = small_font.render('Press SPACE to restart', True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)


# ============================================================================
# START THE GAME!
# ============================================================================

if __name__ == "__main__":
    game = TetrisGame()
    game.run()


# ============================================================================
# 🎉 ADVANCED CONCEPTS YOU LEARNED! 🎉
# ============================================================================
#
# DATA STRUCTURES:
# ✅ 2D arrays (grids)
# ✅ List comprehensions (quick list creation)
# ✅ Nested loops (loops inside loops)
#
# ALGORITHMS:
# ✅ Collision detection
# ✅ Matrix rotation
# ✅ Line clearing
# ✅ Gravity simulation
#
# CHALLENGES:
# 🎯 Add a "next piece" preview
# 🎯 Increase speed as score goes up
# 🎯 Add a "hold piece" feature
# 🎯 Create a high score system
# 🎯 Add visual effects when clearing lines
#
# ============================================================================
