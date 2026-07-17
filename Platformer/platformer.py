import math
import random
import sys

import pygame

# ============= CONFIG =============
WIDTH, HEIGHT = 960, 540
FPS = 60

GRAVITY = 0.8
MAX_FALL_SPEED = 18
PLAYER_SPEED = 5
JUMP_STRENGTH = -15

# Colors
SKY_BLUE = (107, 179, 234)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 214, 10)
GOLD = (255, 200, 0)
RED = (220, 60, 60)
DARK_RED = (150, 30, 30)
GREEN = (60, 180, 75)
DARK_GREEN = (30, 120, 45)
BROWN = (120, 80, 45)
DARK_BROWN = (85, 55, 30)
GRAY = (140, 140, 150)
DARK_GRAY = (70, 70, 80)
SKIN = (240, 200, 160)
BLUE = (60, 110, 220)
HILL_GREEN = (90, 160, 110)

pygame.init()
pygame.display.set_caption("Platform Adventure")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 48, bold=True)
mid_font = pygame.font.SysFont("arial", 30, bold=True)
small_font = pygame.font.SysFont("arial", 22)
hud_font = pygame.font.SysFont("arial", 22, bold=True)


# ============= ENTITIES =============
class Platform:
    def __init__(self, x, y, w, h, kind="ground"):
        self.rect = pygame.Rect(x, y, w, h)
        self.kind = kind  # "ground" or "float"

    def draw(self, surface, camera_x):
        r = self.rect.move(-camera_x, 0)
        if r.right < 0 or r.left > WIDTH:
            return
        if self.kind == "ground":
            pygame.draw.rect(surface, DARK_BROWN, r)
            pygame.draw.rect(surface, GREEN, (r.x, r.y, r.width, 10))
        else:
            pygame.draw.rect(surface, GRAY, r, border_radius=4)
            pygame.draw.rect(surface, DARK_GRAY, r, 2, border_radius=4)


class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False
        self.bob_offset = random.uniform(0, math.tau)
        self.timer = 0.0

    def update(self):
        self.timer += 0.12

    def draw(self, surface, camera_x):
        if self.collected:
            return
        bob = math.sin(self.timer + self.bob_offset) * 4
        r = self.rect.move(-camera_x, int(bob))
        if r.right < 0 or r.left > WIDTH:
            return
        pygame.draw.circle(surface, GOLD, r.center, 10)
        pygame.draw.circle(surface, YELLOW, r.center, 7)
        pygame.draw.circle(surface, GOLD, r.center, 10, 2)


class Flag:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 8, 120)
        self.reached = False

    def draw(self, surface, camera_x):
        r = self.rect.move(-camera_x, 0)
        pygame.draw.rect(surface, DARK_GRAY, r)
        cloth = RED if not self.reached else GOLD
        points = [(r.right, r.top), (r.right + 34, r.top + 15), (r.right, r.top + 30)]
        pygame.draw.polygon(surface, cloth, points)
        pygame.draw.circle(surface, GOLD, (r.centerx, r.top), 6)


class Enemy:
    def __init__(self, x, y, left_bound, right_bound, speed=2.0):
        self.rect = pygame.Rect(x, y, 32, 28)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.vel_x = speed
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.rect.x += self.vel_x
        if self.rect.left <= self.left_bound:
            self.rect.left = self.left_bound
            self.vel_x = abs(self.vel_x)
        elif self.rect.right >= self.right_bound:
            self.rect.right = self.right_bound
            self.vel_x = -abs(self.vel_x)

    def draw(self, surface, camera_x):
        if not self.alive:
            return
        r = self.rect.move(-camera_x, 0)
        if r.right < 0 or r.left > WIDTH:
            return
        pygame.draw.ellipse(surface, DARK_RED, r)
        pygame.draw.ellipse(surface, RED, r.inflate(-6, -6))
        eye_shift = 3 if self.vel_x >= 0 else -3
        for dx in (-6, 6):
            ex = r.centerx + dx + eye_shift
            ey = r.top + 10
            pygame.draw.circle(surface, WHITE, (ex, ey), 4)
            pygame.draw.circle(surface, BLACK, (ex, ey), 2)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 34, 46)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.score = 0
        self.lives = 3
        self.invincible_timer = 0

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
            self.facing_right = True
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)

    def move_and_collide(self, platforms):
        # Horizontal pass
        self.rect.x += self.vel_x
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                elif self.vel_x < 0:
                    self.rect.left = p.rect.right

        # Vertical pass
        self.rect.y += round(self.vel_y)
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0

    def update(self, keys, platforms):
        self.handle_input(keys)
        self.apply_gravity()
        self.move_and_collide(platforms)
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def take_damage(self):
        if self.invincible_timer <= 0:
            self.lives -= 1
            self.invincible_timer = 90
            self.vel_y = -10
            self.vel_x = -6 if self.facing_right else 6

    def draw(self, surface, camera_x):
        if self.invincible_timer > 0 and (self.invincible_timer // 4) % 2 == 0:
            return  # flicker while invincible
        r = self.rect.move(-camera_x, 0)
        pygame.draw.rect(surface, BLUE, (r.x, r.y + 16, r.width, r.height - 16), border_radius=6)
        pygame.draw.circle(surface, SKIN, (r.centerx, r.y + 12), 14)
        eye_x = r.centerx + (4 if self.facing_right else -4)
        pygame.draw.circle(surface, BLACK, (eye_x, r.y + 10), 2)
        pygame.draw.rect(surface, DARK_BROWN, (r.x + 2, r.bottom - 8, 10, 8))
        pygame.draw.rect(surface, DARK_BROWN, (r.right - 12, r.bottom - 8, 10, 8))


# ============= LEVEL GENERATION =============
def create_level(level):
    platforms = []
    enemies = []
    coins = []

    level_width = 2400 + level * 400
    ground_y = HEIGHT - 40

    # Ground with occasional gaps to jump over
    x = 0
    gap_chance = 0.12 + level * 0.015
    while x < level_width:
        seg_width = random.randint(160, 320)
        if x > 300 and random.random() < gap_chance:
            x += 90  # leave a gap
            continue
        platforms.append(Platform(x, ground_y, seg_width, HEIGHT - ground_y, "ground"))
        x += seg_width

    # Floating platforms, some with a coin reward above them
    for _ in range(6 + level * 2):
        px = random.randint(300, max(301, level_width - 200))
        py = random.randint(HEIGHT - 260, HEIGHT - 130)
        pw = random.randint(90, 170)
        platforms.append(Platform(px, py, pw, 20, "float"))
        if random.random() < 0.7:
            coins.append(Coin(px + pw // 2 - 10, py - 32))

    # Extra scattered coins
    for _ in range(8 + level * 2):
        cx = random.randint(200, max(201, level_width - 100))
        cy = random.randint(HEIGHT - 300, HEIGHT - 80)
        coins.append(Coin(cx, cy))

    # Patrolling enemies
    for _ in range(3 + level):
        ex = random.randint(400, max(401, level_width - 300))
        patrol_range = random.randint(80, 200)
        enemies.append(
            Enemy(ex, ground_y - 28, ex - patrol_range, ex + patrol_range, speed=2 + level * 0.25)
        )

    flag = Flag(level_width - 80, ground_y - 120)

    return platforms, enemies, coins, flag, level_width


# ============= GAME =============
class Game:
    def __init__(self):
        self.init()

    def init(self):
        self.level = 1
        self.player = Player(100, 400)
        self.platforms, self.enemies, self.coins, self.flag, self.level_width = create_level(
            self.level
        )
        self.camera_x = 0.0
        self.paused = False
        self.win = False
        self.game_over = False

    # ---------- update ----------
    def update(self, keys):
        if self.paused or self.win or self.game_over:
            return

        self.player.update(keys, self.platforms)
        for enemy in self.enemies:
            enemy.update()
        for coin in self.coins:
            coin.update()

        self.check_enemy_collisions()
        self.check_coin_collisions()
        self.check_flag()

        if self.player.rect.top > HEIGHT + 300 or self.player.lives <= 0:
            self.game_over = True

        target_camera = self.player.rect.centerx - WIDTH // 2
        self.camera_x += (target_camera - self.camera_x) * 0.1
        self.camera_x = max(0, min(self.camera_x, self.level_width - WIDTH))

    def check_enemy_collisions(self):
        for enemy in self.enemies:
            if not enemy.alive or not self.player.rect.colliderect(enemy.rect):
                continue
            stomped = self.player.vel_y > 0 and self.player.rect.bottom - enemy.rect.top < 18
            if stomped:
                enemy.alive = False
                self.player.rect.bottom = enemy.rect.top
                self.player.vel_y = JUMP_STRENGTH * 0.6
                self.player.score += 50
            else:
                self.player.take_damage()

    def check_coin_collisions(self):
        for coin in self.coins:
            if not coin.collected and self.player.rect.colliderect(coin.rect):
                coin.collected = True
                self.player.score += 10

    def check_flag(self):
        if not self.win and self.player.rect.colliderect(self.flag.rect):
            self.win = True
            self.flag.reached = True

    # ---------- draw ----------
    def draw_background(self):
        screen.fill(SKY_BLUE)
        for i in range(7):
            hx = (i * 300 - int(self.camera_x * 0.3)) % (WIDTH + 400) - 200
            pygame.draw.circle(screen, HILL_GREEN, (hx, HEIGHT - 50), 90)
        for i in range(5):
            cx = (i * 260 - int(self.camera_x * 0.15)) % (WIDTH + 200) - 100
            cy = 60 + (i % 3) * 40
            pygame.draw.ellipse(screen, WHITE, (cx, cy, 70, 30))
            pygame.draw.ellipse(screen, WHITE, (cx + 20, cy - 12, 60, 30))

    def draw_hud(self):
        screen.blit(hud_font.render(f"Score: {self.player.score}", True, WHITE), (16, 14))
        screen.blit(hud_font.render(f"Lives: {self.player.lives}", True, WHITE), (16, 42))
        level_surf = hud_font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(level_surf, level_surf.get_rect(topright=(WIDTH - 16, 14)))

    def draw(self):
        self.draw_background()
        for p in self.platforms:
            p.draw(screen, self.camera_x)
        for c in self.coins:
            c.draw(screen, self.camera_x)
        for e in self.enemies:
            e.draw(screen, self.camera_x)
        self.flag.draw(screen, self.camera_x)
        self.player.draw(screen, self.camera_x)
        self.draw_hud()

        if self.paused:
            self.draw_paused()
        if self.win:
            self.draw_win()
        if self.game_over:
            self.draw_game_over()

    def draw_win(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(160)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        win_text = font.render("LEVEL COMPLETE!", True, YELLOW)
        screen.blit(win_text, win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))

        score_text = mid_font.render(f"Score: {self.player.score}", True, WHITE)
        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        next_text = small_font.render("Press N for next level or R to restart", True, WHITE)
        screen.blit(next_text, next_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60)))

    def draw_paused(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        pause_text = font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10)))

        bar_w, bar_h, gap = 10, 34, 14
        top = HEIGHT // 2 - 60
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - gap - bar_w, top, bar_w, bar_h), border_radius=2)
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 + gap, top, bar_w, bar_h), border_radius=2)

        hint = small_font.render("Press P to resume", True, WHITE)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        over_text = font.render("GAME OVER", True, RED)
        screen.blit(over_text, over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))

        score_text = mid_font.render(f"Final Score: {self.player.score}", True, WHITE)
        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

        hint = small_font.render("Press R to restart", True, WHITE)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70)))

    # ---------- transitions ----------
    def restart(self):
        self.init()

    def next_level(self):
        self.level += 1
        self.platforms, self.enemies, self.coins, self.flag, self.level_width = create_level(
            self.level
        )
        self.player.rect.x = 100
        self.player.rect.y = 400
        self.player.vel_x = 0
        self.player.vel_y = 0
        self.win = False
        self.camera_x = 0.0


# ============= MAIN GAME LOOP =============
def main():
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_p and not game.win and not game.game_over:
                    game.paused = not game.paused

                if event.key == pygame.K_r:
                    game.restart()

                if event.key == pygame.K_n and game.win:
                    game.next_level()

        keys = pygame.key.get_pressed()
        game.update(keys)
        game.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
