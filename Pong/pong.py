import pygame
import sys

# Initialize Pygame
pygame.init()

# ============= CONSTANTS =============
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Paddle settings
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8

# Ball settings
BALL_SIZE = 20
BALL_SPEED_X = 7
BALL_SPEED_Y = 7

# Score settings
WIN_SCORE = 5

# ============= SETUP WINDOW =============
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏓 Pong - First to 5 Wins!")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# ============= GAME OBJECTS =============
class Paddle:
    def __init__(self, x, y, color, controls):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.speed = PADDLE_SPEED
        self.controls = controls  # {'up': key, 'down': key}
        self.score = 0
    
    def move(self, keys):
        if keys[self.controls['up']]:
            self.rect.y -= self.speed
        if keys[self.controls['down']]:
            self.rect.y += self.speed
        
        # Keep paddle on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def reset_position(self):
        self.rect.centery = HEIGHT // 2

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - BALL_SIZE//2, 
                               HEIGHT//2 - BALL_SIZE//2, 
                               BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X * (1 if pygame.time.get_ticks() % 2 == 0 else -1)
        self.speed_y = BALL_SPEED_Y * (1 if pygame.time.get_ticks() % 3 == 0 else -1)
        self.max_speed = 12
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    
    def bounce_wall(self):
        # Bounce off top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y
    
    def reset(self):
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.speed_x = BALL_SPEED_X * (1 if pygame.time.get_ticks() % 2 == 0 else -1)
        self.speed_y = BALL_SPEED_Y * (1 if pygame.time.get_ticks() % 3 == 0 else -1)
    
    def draw(self):
        pygame.draw.rect(screen, YELLOW, self.rect)
        # Add a glow effect
        pygame.draw.rect(screen, (255, 255, 150), self.rect.inflate(4, 4), 2)

# ============= CREATE OBJECTS =============
player1 = Paddle(30, HEIGHT//2 - PADDLE_HEIGHT//2, BLUE, 
                 {'up': pygame.K_w, 'down': pygame.K_s})
player2 = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, RED, 
                 {'up': pygame.K_UP, 'down': pygame.K_DOWN})
ball = Ball()

# ============= HELPER FUNCTIONS =============
def draw_midfield():
    # Center line
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 2, y, 4, 20))
    
    # Center circle
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 60, 2)

def display_score():
    # Player 1 score
    p1_text = font.render(str(player1.score), True, BLUE)
    screen.blit(p1_text, (WIDTH//4 - 30, 20))
    
    # Player 2 score
    p2_text = font.render(str(player2.score), True, RED)
    screen.blit(p2_text, (3*WIDTH//4 - 30, 20))

def display_winner(winner):
    if winner == 1:
        text = font.render("🏆 Player 1 Wins! 🏆", True, BLUE)
    else:
        text = font.render("🏆 Player 2 Wins! 🏆", True, RED)
    
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(text, text_rect)
    
    # Restart instruction
    restart_text = small_font.render("Press R to restart or ESC to quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(restart_text, restart_rect)

def reset_game():
    player1.score = 0
    player2.score = 0
    player1.reset_position()
    player2.reset_position()
    ball.reset()

# ============= MAIN GAME LOOP =============
running = True
game_over = False
winner = None

while running:
    # ---------- EVENT HANDLING ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
                    game_over = False
                    winner = None
                elif event.key == pygame.K_ESCAPE:
                    running = False
    
    # ---------- UPDATE ----------
    if not game_over:
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Move paddles
        player1.move(keys)
        player2.move(keys)
        
        # Move ball
        ball.move()
        
        # Bounce off walls
        ball.bounce_wall()
        
        # ---------- COLLISION DETECTION ----------
        # Ball hits player 1 paddle
        if ball.rect.colliderect(player1.rect):
            ball.speed_x = abs(ball.speed_x)  # Force to right
            # Add angle based on where ball hits paddle
            offset = (ball.rect.centery - player1.rect.centery) / (PADDLE_HEIGHT // 2)
            ball.speed_y = BALL_SPEED_Y * offset
            # Increase speed slightly
            if abs(ball.speed_x) < ball.max_speed:
                ball.speed_x *= 1.05
        
        # Ball hits player 2 paddle
        elif ball.rect.colliderect(player2.rect):
            ball.speed_x = -abs(ball.speed_x)  # Force to left
            offset = (ball.rect.centery - player2.rect.centery) / (PADDLE_HEIGHT // 2)
            ball.speed_y = BALL_SPEED_Y * offset
            if abs(ball.speed_x) < ball.max_speed:
                ball.speed_x *= 1.05
        
        # ---------- SCORING ----------
        # Player 1 scores (ball goes past right)
        if ball.rect.right >= WIDTH:
            player1.score += 1
            ball.reset()
            # Reset paddle positions
            player1.reset_position()
            player2.reset_position()
        
        # Player 2 scores (ball goes past left)
        elif ball.rect.left <= 0:
            player2.score += 1
            ball.reset()
            player1.reset_position()
            player2.reset_position()
        
        # Check for winner
        if player1.score >= WIN_SCORE:
            game_over = True
            winner = 1
        elif player2.score >= WIN_SCORE:
            game_over = True
            winner = 2
    
    # ---------- DRAW ----------
    screen.fill(BLACK)
    
    # Draw midfield
    draw_midfield()
    
    # Draw paddles
    player1.draw()
    player2.draw()
    
    # Draw ball
    ball.draw()
    
    # Draw scores
    display_score()
    
    # Draw game over screen if needed
    if game_over:
        display_winner(winner)
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()