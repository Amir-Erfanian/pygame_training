import pygame
import sys
import random

pygame.init()

pygame.mixer.init()

# ===== LOAD BACKGROUND MUSIC =====
try:
    pygame.mixer.music.load("breakout_music.ogg")
    pygame.mixer.music.set_volume(0.5)  # 0.0 to 1.0 (50% volume)
    pygame.mixer.music.play(-1)  # -1 means loop forever
    print("Background music loaded!")
except pygame.error:
    print("Could not load background music - continuing without music")

# ============= CONSTANTS =============
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (111, 29, 27)
CREAM = (187, 148, 87)
BROWN = (67, 40, 24)
YELLOW = (255, 230, 167)
ORANGE = (153, 88, 42)
PURPLE = (155, 93, 229)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)



background = pygame.image.load("breakout_background.jpg")  # Your image file
background = pygame.transform.scale(background, (WIDTH, HEIGHT))



# Paddle settings
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 18
PADDLE_SPEED = 10
PADDLE_COLOR = WHITE

# Ball settings
BALL_SIZE = 16
BALL_SPEED = 4
MAX_BALL_SPEED = 8

# Brick settings
BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS - 4
BRICK_HEIGHT = 25
BRICK_SPACING = 3

# ============= SETUP WINDOW =============
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout - Brick Breaker")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)

# ============= GAME OBJECTS =============

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - PADDLE_WIDTH//2, 
                               HEIGHT - 50, 
                               PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
        self.color = PADDLE_COLOR
    
    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        
        # Keep paddle on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    
    def draw(self):
        # Draw paddle with rounded corners effect
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, LIGHT_GRAY, self.rect, 2)
        
        # Glow effect
        glow_rect = self.rect.inflate(10, 6)
        pygame.draw.rect(screen, (200, 200, 200, 50), glow_rect, 2)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - BALL_SIZE//2, 
                               HEIGHT//2, 
                               BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = -BALL_SPEED
        self.max_speed = MAX_BALL_SPEED
        self.stuck_to_paddle = True  # Ball starts on paddle
    
    def move(self):
        if not self.stuck_to_paddle:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            
            # Bounce off walls
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.speed_x = -self.speed_x
            
            if self.rect.top <= 0:
                self.speed_y = -self.speed_y
    
    def bounce_off_paddle(self, paddle):
        # Calculate where ball hits paddle (0 = left, 1 = right)
        hit_pos = (self.rect.centerx - paddle.rect.left) / paddle.rect.width
        hit_pos = max(0, min(1, hit_pos))  # Clamp between 0 and 1
        
        # Convert to angle: -60 to +60 degrees
        angle = (hit_pos - 0.5) * 2 * 0.8  # -0.8 to 0.8 radians (~ -46 to +46 degrees)
        
        # Set new direction
        self.speed_x = self.max_speed * (angle * 1.5)
        self.speed_y = -abs(self.max_speed * 0.9)  # Always go up
        
        # Ensure minimum horizontal speed
        if abs(self.speed_x) < 2:
            self.speed_x = 2 if self.speed_x >= 0 else -2
    
    def reset(self, paddle):
        self.rect.center = (paddle.rect.centerx, paddle.rect.top - BALL_SIZE//2 - 2)
        self.stuck_to_paddle = True
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = -BALL_SPEED
    
    def draw(self):
        # Draw ball with glow
        pygame.draw.ellipse(screen, WHITE, self.rect)
        pygame.draw.ellipse(screen, LIGHT_GRAY, self.rect, 2)
        
        # Glow effect
        glow_rect = self.rect.inflate(8, 8)
        pygame.draw.ellipse(screen, (200, 200, 200, 30), glow_rect, 2)

class Brick:
    COLORS = [RED, ORANGE, YELLOW, CREAM, BROWN, PURPLE]
    POINTS = [50, 40, 30, 20, 10, 5]
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = self.COLORS[row % len(self.COLORS)]
        self.points = self.POINTS[row % len(self.POINTS)]
        self.rect = pygame.Rect(
            col * (BRICK_WIDTH + BRICK_SPACING) + BRICK_SPACING//2 + 2,
            row * (BRICK_HEIGHT + BRICK_SPACING) + 50,
            BRICK_WIDTH,
            BRICK_HEIGHT
        )
        self.alive = True
        self.hit_count = 0
        self.max_hits = 1
    
    def draw(self):
        if self.alive:
            # Main brick
            pygame.draw.rect(screen, self.color, self.rect)
                                   

            if self.points >= 30:
                text_color = WHITE
            else:
                text_color = BLACK

            if self.points >= 40:
                text_size = 22
            elif self.points >= 20:
                text_size = 18
            else:
                text_size = 15
            
            points_font = pygame.font.Font(None, text_size)
            points_text = points_font.render(str(self.points), True, text_color)
            text_rect = points_text.get_rect(center=self.rect.center)
            screen.blit(points_text, text_rect)
    
    def hit(self):
        self.hit_count += 1
        if self.hit_count >= self.max_hits:
            self.alive = False
            return True  # Brick destroyed
        return False  # Brick still alive

# ============= GAME STATE =============

class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.win = False
        self.paused = False
        
        self.create_level()
            # ... existing code ...
        self.music_playing = True
        self.sound_effects = True
    
    def toggle_music(self):
        """Turn music on/off"""
        if self.music_playing:
            pygame.mixer.music.pause()
            self.music_playing = False
        else:
            pygame.mixer.music.unpause()
            self.music_playing = True
    
    def set_music_volume(self, volume):
        """Change volume (0.0 to 1.0)"""
        pygame.mixer.music.set_volume(volume)
        
    def create_level(self):
        self.bricks = []
        # Create grid of bricks
        for row in range(BRICK_ROWS):
            # Some rows are tougher in higher levels
            max_hits = 1
            if self.level >= 2 and row == 0:
                max_hits = 2  # Top row needs 2 hits
            if self.level >= 3 and row in [0, 1]:
                max_hits = 2 if row == 1 else 3
            
            for col in range(BRICK_COLS):
                # Random missing bricks for variety
                if self.level >= 2 and random.random() < 0.1:
                    continue  # Skip some bricks
                
                brick = Brick(row, col)
                brick.max_hits = max_hits
                self.bricks.append(brick)
    
    def reset_ball(self):
        self.ball.reset(self.paddle)
    
    def launch_ball(self):
        self.ball.stuck_to_paddle = False
    
    def update(self, keys):
        if self.game_over or self.win or self.paused:
            return
        
        # Move paddle
        self.paddle.move(keys)
        
        # Launch ball with space
        if self.ball.stuck_to_paddle and keys[pygame.K_SPACE]:
            self.launch_ball()
        
        # If ball is stuck, follow paddle
        if self.ball.stuck_to_paddle:
            self.ball.rect.centerx = self.paddle.rect.centerx
            self.ball.rect.bottom = self.paddle.rect.top - 2
            return
        
        # Move ball
        self.ball.move()
        
        # Ball collision with paddle
        if self.ball.rect.colliderect(self.paddle.rect):
            # Only bounce if ball is moving down
            if self.ball.speed_y > 0:
                self.ball.bounce_off_paddle(self.paddle)
                # Play sound effect (if we had sounds)
        
        # Ball collision with bricks
        for brick in self.bricks:
            if brick.alive and self.ball.rect.colliderect(brick.rect):
                # Determine collision side
                overlap_left = self.ball.rect.right - brick.rect.left
                overlap_right = brick.rect.right - self.ball.rect.left
                overlap_top = self.ball.rect.bottom - brick.rect.top
                overlap_bottom = brick.rect.bottom - self.ball.rect.top
                
                # Find smallest overlap
                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                
                # Bounce in correct direction
                if min_overlap == overlap_left:
                    self.ball.speed_x = -abs(self.ball.speed_x)
                elif min_overlap == overlap_right:
                    self.ball.speed_x = abs(self.ball.speed_x)
                elif min_overlap == overlap_top:
                    self.ball.speed_y = -abs(self.ball.speed_y)
                elif min_overlap == overlap_bottom:
                    self.ball.speed_y = abs(self.ball.speed_y)
                
                # Hit the brick
                if brick.hit():
                    self.score += brick.points
                
                break  # Only hit one brick per frame
        
        # Ball falls off screen
        if self.ball.rect.bottom > HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.reset_ball()
        
        # Check win condition
        if all(not brick.alive for brick in self.bricks):
            self.win = True
            # Automatically go to next level after a delay
            self.level += 1
            # In a real game, you'd show a message and wait for input
    
    def draw(self):
        # ===== DRAW BACKGROUND FIRST =====
        if background:
            screen.blit(background, (0, 0))  # Draw background image
        else:
            screen.fill(BLACK)  # Fallback to black if no image
        
        # Draw bricks
        for brick in self.bricks:
            brick.draw()
        
        # Draw paddle
        self.paddle.draw()
        
        # Draw ball
        self.ball.draw()
        
        # Draw UI
        self.draw_ui()
        
        # Draw game over / win screens
        if self.game_over:
            self.draw_game_over()
        elif self.win:
            self.draw_win()
        elif self.paused:
            self.draw_paused()
    
    def draw_ui(self):
        # Score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Lives (hearts)
        lives_text = font.render("+" * self.lives, True, WHITE)
        screen.blit(lives_text, (700, 10))
        
        # Level
        level_text = font.render(f"Level {self.level}", True, WHITE)
        level_rect = level_text.get_rect(center=(WIDTH//2, 20))
        screen.blit(level_text, level_rect)
        
        # Instructions
        if self.ball.stuck_to_paddle:
            instruct = small_font.render("Press SPACE to launch!", True, YELLOW)
            instruct_rect = instruct.get_rect(center=(WIDTH//2, HEIGHT - 100))
            screen.blit(instruct, instruct_rect)
    
    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        go_text = font.render("GAME OVER!!", True, RED)
        go_rect = go_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
        screen.blit(go_text, go_rect)
        
        # Final score
        score_text = font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(score_text, score_rect)
        
        # Restart instruction
        restart_text = small_font.render("Press R to restart or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
        screen.blit(restart_text, restart_rect)
    
    def draw_win(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Win text
        win_text = font.render("LEVEL COMPLETE!", True, CREAM)
        win_rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
        screen.blit(win_text, win_rect)
        
        # Score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(score_text, score_rect)
        
        # Next level instruction
        next_text = small_font.render("Press N for next level or R to restart", True, WHITE)
        next_rect = next_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
        screen.blit(next_text, next_rect)
    
    def draw_paused(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        pause_text = font.render("⏸ PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(pause_text, pause_rect)
    
    def restart(self):
        self.__init__()  # Reset everything

# ============= MAIN GAME LOOP =============

def main():
    game = Game()
    running = True
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if event.key == pygame.K_p:
                    game.paused = not game.paused
                
                if event.key == pygame.K_r:
                    game.restart()
                
                if event.key == pygame.K_n and game.win:
                    game.win = False
                    game.create_level()
                    game.reset_ball()
                
                # Launch ball with any key when stuck
                if game.ball.stuck_to_paddle and event.key == pygame.K_SPACE:
                    game.launch_ball()
        
        # Update
        keys = pygame.key.get_pressed()
        game.update(keys)

        # Draw
        game.draw()
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()