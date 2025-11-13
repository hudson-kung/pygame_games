"""
🐍 SNAKE GAME - Educational Example

This is a simple Snake game to help you learn:
- Game loops (how games run continuously)
- User input (keyboard controls)
- Collision detection (when things bump into each other)
- Lists and coordinates (tracking the snake's body)

READ TIME: 15-20 minutes
DIFFICULTY: Easy 🟢

Let's learn by coding a classic game!
"""

import pygame
import random
import sys

# ============================================================================
# CONSTANTS (Settings that never change)
# ============================================================================
# Using ALL_CAPS for constants is a Python convention!

# Window settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20          # Size of each square
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE   # // means divide and round down
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors (RGB format: Red, Green, Blue)
# Each color value is 0-255
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 200, 0)

# Game speed
FPS = 10  # Frames per second (higher = faster)


# ============================================================================
# GAME CLASS (The Brain of Our Game)
# ============================================================================

class SnakeGame:
    """
    This class holds all the game logic!
    
    WHAT'S A CLASS?
    A class is like a blueprint for creating objects.
    Think of it like a cookie cutter - it defines the shape,
    and we can make many cookies from it!
    """
    
    def __init__(self):
        """
        The __init__ method runs when we create a new game.
        It sets up all the starting values!
        
        This is called a CONSTRUCTOR - it constructs (builds) our game!
        """
        
        # Initialize Pygame
        pygame.init()
        
        # Create the game window
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 Snake Game - Use Arrow Keys!")
        
        # Create a clock to control game speed
        self.clock = pygame.time.Clock()
        
        # Snake starting position (middle of screen)
        # The snake is a LIST of positions!
        # Each position is a list [x, y]
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        
        self.snake = [[start_x, start_y]]  # List with one segment
        
        # Snake direction (starts moving right)
        self.direction = [1, 0]  # [1, 0] means right, [0, 1] means down
        
        # Create the first food
        self.food = self.create_food()
        
        # Score starts at 0
        self.score = 0
        
        # Game state
        self.game_over = False
    
    def create_food(self):  
        """
        Creates food at a random position!
        
        RANDOM NUMBERS:
        random.randint(a, b) gives a random number between a and b
        This makes the food appear in different places!
        """
        while True:
            # Pick random x and y coordinates
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            # Make sure food doesn't appear on the snake!
            if [x, y] not in self.snake:
                return [x, y]
    
    def handle_input(self):
        """
        Checks what keys the player presses!
        
        EVENT HANDLING:
        pygame.event.get() gives us all the things that happened
        (key presses, mouse clicks, etc.)
        """
        for event in pygame.event.get():
            
            # Did the player close the window?
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Did the player press a key?
            if event.type == pygame.KEYDOWN:
                
                # Arrow key controls!
                # We check that they're not trying to go backwards
                
                if event.key == pygame.K_UP and self.direction != [0, 1]:
                    self.direction = [0, -1]  # Up
                
                elif event.key == pygame.K_DOWN and self.direction != [0, -1]:
                    self.direction = [0, 1]   # Down
                
                elif event.key == pygame.K_LEFT and self.direction != [1, 0]:
                    self.direction = [-1, 0]  # Left
                
                elif event.key == pygame.K_RIGHT and self.direction != [-1, 0]:
                    self.direction = [1, 0]   # Right
                
                # Press SPACE to restart after game over
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.__init__()  # Restart the game!
    
    def update(self):
        """
        Updates the game state (moves the snake, checks collisions)
        
        GAME LOOP CONCEPT:
        Games run in a loop - update position, check collisions, repeat!
        """
        
        if self.game_over:
            return  # Don't update if game is over
        
        # Calculate new head position
        # The head is the first item in the snake list
        old_head = self.snake[0]
        new_head = [
            old_head[0] + self.direction[0],
            old_head[1] + self.direction[1]
        ]
        
        # Check if snake hit the wall
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return
        
        # Check if snake hit itself
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head to snake
        # insert(0, item) adds item at the beginning of the list
        self.snake.insert(0, new_head)
        
        # Did the snake eat the food?
        if new_head == self.food:
            # Yay! Grow the snake and make new food!
            self.score += 1
            self.food = self.create_food()
        else:
            # Remove the tail (snake doesn't grow)
            # pop() removes the last item from a list
            self.snake.pop()
    
    def draw(self):
        """
        Draws everything on the screen!
        
        DRAWING ORDER MATTERS:
        We draw from back to front (background first, then objects)
        """
        
        # Fill background with black
        self.screen.fill(BLACK)
        
        # Draw the snake
        for segment in self.snake:
            # Convert grid position to pixel position
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            
            # Draw the segment
            # pygame.draw.rect(surface, color, [x, y, width, height])
            pygame.draw.rect(self.screen, GREEN, [x, y, GRID_SIZE, GRID_SIZE])
            
            # Draw a border to make it look nicer
            pygame.draw.rect(self.screen, DARK_GREEN, [x, y, GRID_SIZE, GRID_SIZE], 2)
        
        # Draw the food
        food_x = self.food[0] * GRID_SIZE
        food_y = self.food[1] * GRID_SIZE
        pygame.draw.rect(self.screen, RED, [food_x, food_y, GRID_SIZE, GRID_SIZE])
        
        # Draw the score
        font = pygame.font.Font(None, 36)  # Create a font
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))  # blit means "draw text"
        
        # Draw game over message
        if self.game_over:
            # Create semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)  # 128 = half transparent
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Game over text
            big_font = pygame.font.Font(None, 72)
            game_over_text = big_font.render('GAME OVER', True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
            
            # Restart instruction
            small_font = pygame.font.Font(None, 36)
            restart_text = small_font.render('Press SPACE to restart', True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 60))
            self.screen.blit(restart_text, restart_rect)
        
        # Update the display
        pygame.display.flip()  # flip() shows everything we drew
    
    def run(self):
        """
        The main game loop!
        
        GAME LOOP PATTERN:
        1. Handle Input (what did the player do?)
        2. Update (move things, check collisions)
        3. Draw (show everything on screen)
        4. Repeat!
        """
        
        while True:
            self.handle_input()    # 1. Check for player input
            self.update()          # 2. Update game state
            self.draw()            # 3. Draw everything
            self.clock.tick(FPS)   # 4. Wait to maintain FPS


# ============================================================================
# START THE GAME!
# ============================================================================

if __name__ == "__main__":
    # This only runs if we run THIS file directly
    # (not if another file imports it)
    
    game = SnakeGame()  # Create a new game
    game.run()          # Start the game loop!


# ============================================================================
# 🎉 WHAT YOU LEARNED! 🎉
# ============================================================================
#
# PROGRAMMING CONCEPTS:
# ✅ Classes and objects (organizing code)
# ✅ Lists (storing multiple items)
# ✅ Game loops (the heart of every game)
# ✅ Event handling (responding to input)
# ✅ Collision detection (checking if things touch)
#
# PYGAME CONCEPTS:
# ✅ Creating a window
# ✅ Drawing shapes
# ✅ Handling keyboard input
# ✅ Controlling frame rate
# ✅ Displaying text
#
# MATH CONCEPTS:
# ✅ Coordinates (x, y positions)
# ✅ Grid systems (dividing space into squares)
# ✅ Random numbers
#
# TRY THESE CHALLENGES:
# 🎯 Make the snake move faster as the score increases
# 🎯 Add different colored food worth different points
# 🎯 Add obstacles to the game
# 🎯 Add a high score system
# 🎯 Make the snake rainbow colored!
#
# ============================================================================
