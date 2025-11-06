"""
🎮 GAME TEMPLATE - Use This to Create Your Own Game!

This is a starter template for making your own Pygame!
Copy this file, fill in the blanks, and create something amazing!

INSTRUCTIONS:
1. Copy this entire file to your new game folder
2. Rename it to 'main.py'
3. Replace all the TODO comments with your own code
4. Read the comments - they explain everything!

Let's make a game! 🚀
"""

import pygame
import sys

# ============================================================================
# CONSTANTS (Your Game Settings)
# ============================================================================

# TODO: Choose your window size!
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# TODO: Choose your background color!
# Colors are in RGB format: (Red, Green, Blue)
# Each value is between 0 and 255
BACKGROUND_COLOR = (0, 0, 0)  # Black

# TODO: Define more colors for your game!
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# TODO: Set your game speed (higher = faster)
FPS = 60  # 60 frames per second is smooth!


# ============================================================================
# GAME CLASS (The Brain of Your Game)
# ============================================================================

class MyGame:
    """
    This is where all your game logic goes!
    
    A class is like a blueprint for your game.
    It keeps all the game data and functions organized.
    """
    
    def __init__(self):
        """
        Initialize your game - this runs once when the game starts!
        
        TODO: Set up your starting game state here:
        - Player position
        - Score
        - Enemy positions
        - Any other starting values
        """
        
        # Initialize Pygame
        pygame.init()
        
        # Create the game window
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # TODO: Change this to your game's name!
        pygame.display.set_caption("🎮 My Awesome Game!")
        
        # Create a clock to control frame rate
        self.clock = pygame.time.Clock()
        
        # TODO: Set up your game variables here!
        # Example:
        # self.player_x = WINDOW_WIDTH // 2
        # self.player_y = WINDOW_HEIGHT // 2
        # self.score = 0
        
        # Game state
        self.running = True
        self.game_over = False
    
    def handle_events(self):
        """
        Handle player input (keyboard, mouse, etc.)
        
        TODO: Add controls for your game!
        - Arrow keys for movement?
        - Space bar to jump?
        - Mouse clicks to shoot?
        """
        
        for event in pygame.event.get():
            
            # Did the player close the window?
            if event.type == pygame.QUIT:
                self.running = False
            
            # TODO: Handle key presses!
            if event.type == pygame.KEYDOWN:
                
                # Example: Press SPACE to restart
                if event.key == pygame.K_SPACE and self.game_over:
                    self.__init__()  # Restart the game
                
                # TODO: Add more controls here!
                # if event.key == pygame.K_UP:
                #     # Move player up
                # if event.key == pygame.K_LEFT:
                #     # Move player left
                # etc...
    
    def update(self):
        """
        Update game logic (move things, check collisions, etc.)
        
        TODO: This is where the game "thinks"!
        - Move the player
        - Move enemies
        - Check if things collide
        - Update the score
        - Check for game over
        """
        
        if self.game_over:
            return  # Don't update if game is over
        
        # TODO: Add your game logic here!
        
        # Example: Move a player
        # self.player_x += self.player_speed
        
        # Example: Check if player hit a wall
        # if self.player_x < 0 or self.player_x > WINDOW_WIDTH:
        #     self.game_over = True
        
        pass  # Remove this when you add your code!
    
    def draw(self):
        """
        Draw everything on the screen!
        
        TODO: Make your game look awesome!
        - Draw the background
        - Draw the player
        - Draw enemies
        - Draw the score
        - Draw game over screen
        """
        
        # Clear the screen with background color
        self.screen.fill(BACKGROUND_COLOR)
        
        # TODO: Draw your game objects here!
        
        # Example: Draw a rectangle (the player?)
        # pygame.draw.rect(self.screen, RED, [x, y, width, height])
        
        # Example: Draw a circle (a coin?)
        # pygame.draw.circle(self.screen, YELLOW, [x, y], radius)
        
        # Example: Draw text (the score?)
        # font = pygame.font.Font(None, 36)
        # text = font.render('Score: 0', True, WHITE)
        # self.screen.blit(text, [10, 10])
        
        # TODO: Draw game over screen if needed
        if self.game_over:
            font = pygame.font.Font(None, 72)
            text = font.render('GAME OVER', True, RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(text, text_rect)
        
        # Update the display (show everything we drew)
        pygame.display.flip()
    
    def run(self):
        """
        The main game loop!
        
        This keeps the game running continuously.
        You don't need to change this!
        """
        
        while self.running:
            self.handle_events()  # 1. Get input
            self.update()         # 2. Update game
            self.draw()           # 3. Draw everything
            self.clock.tick(FPS)  # 4. Wait to maintain FPS
        
        # Clean up when game ends
        pygame.quit()
        sys.exit()


# ============================================================================
# START THE GAME!
# ============================================================================

if __name__ == "__main__":
    """
    This runs when you execute this file directly.
    It creates a game and starts it!
    """
    
    game = MyGame()  # Create your game
    game.run()       # Start the game loop!


# ============================================================================
# 💡 TIPS FOR MAKING YOUR GAME AWESOME! 💡
# ============================================================================
#
# GAME IDEAS:
# - Collect coins before time runs out
# - Dodge falling obstacles
# - Catch items falling from the sky
# - Navigate a maze
# - Simple platformer (jump on platforms)
# - Pong-style game
# - Breakout/brick breaker
# - Space shooter
#
# PYGAME DRAWING FUNCTIONS:
# - pygame.draw.rect(surface, color, [x, y, width, height])
# - pygame.draw.circle(surface, color, [x, y], radius)
# - pygame.draw.line(surface, color, start_pos, end_pos, width)
# - pygame.draw.polygon(surface, color, points)
#
# COLLISION DETECTION:
# - rect1.colliderect(rect2)  # Check if two rectangles touch
# - Check if coordinates overlap
# - Use distance formula for circles: sqrt((x2-x1)² + (y2-y1)²)
#
# MAKING IT FUN:
# - Add sound effects! pygame.mixer.Sound('sound.wav').play()
# - Add increasing difficulty (speed up over time)
# - Add power-ups and bonuses
# - Add particle effects (lots of small colored dots)
# - Add screen shake when hit
# - Add a high score system
#
# DEBUGGING TIPS:
# - Use print() to see what's happening
# - Draw debug info on screen (player position, score, etc.)
# - Start simple and add features one at a time
# - Test after each new feature!
#
# REMEMBER:
# - Games are just loops! Handle input → Update → Draw → Repeat
# - Start simple, add complexity gradually
# - It's okay if your first game is basic!
# - Have FUN! Experiment! Break things! Learn!
#
# ============================================================================
