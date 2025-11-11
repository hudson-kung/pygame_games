"""
🎮 DODGE THE SQUARES GAME - Main Game File

A game where you control a character and dodge enemies.
"""

import pygame
import sys
import os
import random

# Game settings
FPS = 60
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1080

class DTSGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Game window setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dodge The Squares")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.level = 1
        self.score = 0
        self.spawn_rate = 40
        self.spawn_counter = 0
        
        # Player controls
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        
        # Game directories
        self.game_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load assets
        self.load_assets()
        
        # Initialize game objects
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.player = self.create_player()
        self.create_level(self.level)
    
    def load_assets(self):
        """Load all game assets (images, sounds, etc.)"""
        # Load and play background music
        sound = os.path.join(self.game_dir, "songs", "sound.mp3")
        pygame.mixer_music.load(sound)
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.play(-1)
        
        # Load sound effects
        self.hit_sound = pygame.mixer.Sound(os.path.join(self.game_dir, "songs", "die.mp3"))
        
        # Load fonts
        self.font = pygame.font.SysFont("Arial", 50)
        
        # Load images
        self.enemy_img = self.load_image("zomB.png")
        self.player_img = self.load_image("avatar.png")
        self.background = self.load_background()
    
    def load_image(self, name, scale=0.5):
        """Load and scale an image from the img directory"""
        image_path = os.path.join(self.game_dir, "img", name)
        try:
            image = pygame.image.load(image_path).convert_alpha()
            if scale != 1:
                size = (int(image.get_width() * scale), int(image.get_height() * scale))
                image = pygame.transform.scale(image, size)
            return image
        except pygame.error as e:
            print(f"Error loading image {name}: {e}")
            # Return a placeholder surface if image fails to load
            surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            surf.fill((255, 0, 255))  # Magenta placeholder
            return surf
    
    def load_background(self):
        """Load and return the background image"""
        bg_img = pygame.image.load(os.path.join(self.game_dir, "img", "background.png"))
        return pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def create_player(self):
        """Create and return the player character"""
        return Player(200, 200, 0.5, 15, self.player_img)
    
    def create_enemy(self, x, y):
        """Create and return an enemy at the specified position"""
        speed = random.randint(3, 7) * 5  # Make enemies faster
        return Enemy(x, y, 0.5, speed, self.enemy_img)
    
    def create_level(self, level):
        """Create a level with enemies based on the level number"""
        self.enemies.empty()
        self.all_sprites.empty()
        
        # Add player to sprites
        self.all_sprites.add(self.player)
        
        # Create enemies based on level
        num_enemies = 5 if level == 1 else (level * 3) + 2
        for _ in range(num_enemies):
            x = SCREEN_WIDTH + random.randint(50, 300)  # Spawn off-screen to the right
            y = random.randint(0, SCREEN_HEIGHT)
            enemy = self.create_enemy(x, y)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle keydown events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.moving_left = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.moving_right = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.moving_up = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.moving_down = True
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            
            # Handle keyup events
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.moving_left = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.moving_right = False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.moving_up = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.moving_down = False
    
    def update(self):
        """Update game state"""
        # Update player
        self.player.move(self.moving_left, self.moving_right, 
                        self.moving_up, self.moving_down)
        
        # Update enemies
        self.enemies.update()
        
        # Check for collisions
        if pygame.sprite.spritecollide(self.player, self.enemies, True):
            self.hit_sound.set_volume(0.5)
            self.hit_sound.play()
            # Wait for the sound to finish playing before ending the game
            pygame.time.delay(int(self.hit_sound.get_length() * 1000))
            self.running = False
        
        # Check if level is complete (all enemies cleared)
        if len(self.enemies) == 0:
            self.level += 1
            self.score += 100 * self.level  # Bonus points for completing a level
            self.create_level(self.level)
            print(f"Level {self.level-1} completed! Starting level {self.level}")
        
        # Spawn new enemies occasionally
        self.spawn_counter += 1
        if self.spawn_counter >= self.spawn_rate and len(self.enemies) < 10:  # Limit max enemies
            self.spawn_counter = 0
            x = SCREEN_WIDTH + random.randint(50, 300)  # Spawn off-screen to the right
            y = random.randint(0, SCREEN_HEIGHT)
            enemy = self.create_enemy(x, y)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
        
        # Score is now only increased by completing levels
    
    def draw(self):
        """Draw everything to the screen"""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw all sprites
        for entity in self.all_sprites:
            if hasattr(entity, 'draw'):
                entity.draw(self.screen)
            else:
                self.screen.blit(entity.image, entity.rect)
        
        # Draw UI elements
        self.draw_ui()
        
        # Update the display
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Draw level
        level_text = self.font.render(f'Level: {self.level}', True, (255, 255, 255))
        self.screen.blit(level_text, (10, 60))
        
        # Draw controls hint
        controls_text = self.font.render('WASD to move', True, (200, 200, 200))
        self.screen.blit(controls_text, (10, SCREEN_HEIGHT - 40))
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        
        # Clean up
        pygame.quit()
        sys.exit()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect = self.rect.inflate(-20, -20)
        self.speed = speed
        self.flip = False
    
    def move(self, left, right, up, down):
        """Move the player based on input"""
        dx = 0
        dy = 0
        
        if left:
            dx = -self.speed
            self.flip = True
        if right:
            dx = self.speed
            self.flip = False
        if up:
            dy = -self.speed
        if down:
            dy = self.speed
        
        # Update position
        self.rect.x += dx
        self.rect.y += dy
        
        # Keep player on screen
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
    
    def draw(self, surface):
        """Draw the player on the given surface"""
        # Flip the image if moving left
        if self.flip:
            surface.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else:
            surface.blit(self.image, self.rect)
        
        # Draw hitbox
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect = self.rect.inflate(-20, -20)
        self.speed = speed
    
    def update(self):
        """Update enemy position"""
        self.rect.x -= self.speed
        
        # Remove the enemy if it goes off the left side of the screen
        if self.rect.right < 0:
            self.kill()  # This removes the sprite from all groups
    
    def draw(self, surface):
        """Draw the enemy on the given surface"""
        surface.blit(self.image, self.rect)
        # Draw hitbox
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)


# Start the game
if __name__ == "__main__":
    game = DTSGame()
    game.run()
