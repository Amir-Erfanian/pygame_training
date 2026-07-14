import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paddle game for tutorial")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

ball_x, ball_y = 400, 15
ball_radius = 15
ball_speed_x = 4
ball_speed_y = 4

paddle_width = 120
paddle_height = 20
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 50
paddle_speed = 10

score = 0
font = pygame.font.Font(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT]:
        paddle_x += paddle_speed

    if paddle_x < 0:
        paddle_x = 0
    if paddle_x + paddle_width > WIDTH:
        paddle_x = WIDTH - paddle_width
    
    # Move ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # Wall bounce
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_speed_x = -ball_speed_x
    if ball_y - ball_radius <= 0:
        ball_speed_y = -ball_speed_y
    
    # Game OVER
    if ball_y + ball_radius > HEIGHT:
        print(f"Game Over! Score: {score}")
        running = False
    
    if (ball_y + ball_radius >= paddle_y and 
        ball_y + ball_radius <= paddle_y + paddle_height + 10 and
        paddle_x <= ball_x <= paddle_x + paddle_width):
        ball_speed_y = -ball_speed_y
        score += 1
        # Add a little randomness to speed
        ball_speed_x += 0.2 if ball_speed_x > 0 else -0.2
    

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()