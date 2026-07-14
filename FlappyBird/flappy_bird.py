import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_SPEED = 4
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (135, 206, 235)
DARK_GREEN = (0, 100, 0)
ORANGE = (255, 165, 0)

class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 20
        
    def jump(self):
        self.velocity = JUMP_STRENGTH
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Keep bird on screen
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
            self.velocity = 0
            
    def draw(self, screen):
        # Draw bird body
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        # Draw eye
        pygame.draw.circle(screen, BLACK, (int(self.x + 8), int(self.y - 5)), 5)
        # Draw beak
        pygame.draw.polygon(screen, ORANGE, [
            (self.x + 15, self.y),
            (self.x + 25, self.y - 5),
            (self.x + 15, self.y - 10)
        ])
        # Draw wing
        pygame.draw.ellipse(screen, (200, 200, 0), 
                           (self.x - 15, self.y - 5, 20, 10))
        
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, screen):
        # Draw top pipe
        pygame.draw.rect(screen, DARK_GREEN, 
                        (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, 
                        (self.x - 5, self.height - 30, PIPE_WIDTH + 10, 30))
        
        # Draw bottom pipe
        bottom_pipe_top = self.height + PIPE_GAP
        pygame.draw.rect(screen, DARK_GREEN, 
                        (self.x, bottom_pipe_top, PIPE_WIDTH, 
                         SCREEN_HEIGHT - bottom_pipe_top))
        pygame.draw.rect(screen, GREEN, 
                        (self.x - 5, bottom_pipe_top, PIPE_WIDTH + 10, 30))
        
    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, 
                                 PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)
        return top_rect, bottom_rect
    
    def is_offscreen(self):
        return self.x < -PIPE_WIDTH

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.reset_game()
        
    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.pipe_timer = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_started:
                        self.game_started = True
                    if not self.game_over:
                        self.bird.jump()
                    else:
                        self.reset_game()
                        self.game_started = True
                        self.bird.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_started:
                    self.game_started = True
                if not self.game_over:
                    self.bird.jump()
                else:
                    self.reset_game()
                    self.game_started = True
                    self.bird.jump()
        return True
        
    def update(self):
        if not self.game_started or self.game_over:
            return
            
        # Update bird
        self.bird.update()
        
        # Check if bird hits ground or ceiling
        if self.bird.y >= SCREEN_HEIGHT or self.bird.y <= 0:
            self.game_over = True
            
        # Update pipes
        for pipe in self.pipes:
            pipe.update()
            
        # Remove offscreen pipes
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_offscreen()]
        
        # Generate new pipes
        self.pipe_timer += 1
        if self.pipe_timer > 90:  # New pipe every 1.5 seconds at 60 FPS
            self.pipes.append(Pipe(SCREEN_WIDTH))
            self.pipe_timer = 0
            
        # Check collisions
        bird_rect = self.bird.get_rect()
        for pipe in self.pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                self.game_over = True
                
            # Update score
            if not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                pipe.passed = True
                self.score += 1
                
    def draw(self):
        # Draw background
        self.screen.fill(BLUE)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)
            
        # Draw bird
        self.bird.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw start screen
        if not self.game_started:
            start_text = self.big_font.render("FLAPPY BIRD", True, WHITE)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(start_text, start_rect)
            
            instruction_text = self.font.render("Press SPACE or Click to Start", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(instruction_text, instruction_rect)
            
        # Draw game over screen
        if self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, WHITE)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(game_over_text, game_over_rect)
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(final_score_text, final_score_rect)
            
            restart_text = self.font.render("Press SPACE or Click to Restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(restart_text, restart_rect)
            
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()