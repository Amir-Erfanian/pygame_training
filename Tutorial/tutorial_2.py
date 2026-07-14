import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Square")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SQUARE_COLOR = (250, 250, 150)


square_x = 400
square_y = 300
square_size = 40
square_speed_x = 5
square_speed_y = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move the square
    square_x += square_speed_x
    square_y += square_speed_y
    
    if square_x <= 0 or square_x + square_size >= WIDTH:
        square_speed_x = -square_speed_x #Moves back when speed is negative
    if square_y <= 0 or square_y + square_size >= HEIGHT:
        square_speed_y = -square_speed_y
    
    screen.fill(BLACK)
    pygame.draw.rect(screen, SQUARE_COLOR, (square_x, square_y, square_size, square_size))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()