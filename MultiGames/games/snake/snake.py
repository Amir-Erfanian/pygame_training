import sys
import random
import pygame
from core.scene import Scene
BACKGROUND_COLOR = (164, 216, 1)
SNAKE_COLOR = (46, 56, 40)
GRID_DOT_COLOR = (163, 176, 132) 
FRAME_COLOR = (60, 66, 50)
PANEL_SHADOW_COLOR = (120, 130, 100)

CELL_SIZE = 18
COLUMNS = 22
ROWS = 12

TOP_BAR_HEIGHT = CELL_SIZE * 2
BEZEL_THICKNESS = 14

PLAY_AREA_WIDTH = COLUMNS * CELL_SIZE
PLAY_AREA_HEIGHT = ROWS * CELL_SIZE

SCREEN_WIDTH = PLAY_AREA_WIDTH + BEZEL_THICKNESS * 2
SCREEN_HEIGHT = PLAY_AREA_HEIGHT + TOP_BAR_HEIGHT + BEZEL_THICKNESS * 2

FPS = 60

START_SPEED_INTERVAL = 160
MIN_SPEED_INTERVAL = 70
SPEED_INCREMENT = 4

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

MOVE_EVENT = pygame.USEREVENT + 1


def make_beep(freq=880, ms=60, volume=0.25):
    try:
        import numpy as np
        sample_rate = 44100
        n_samples = int(sample_rate * ms / 1000)
        t = np.linspace(0, ms / 1000, n_samples, endpoint=False)
        wave = np.sign(np.sin(2 * np.pi * freq * t))
        audio = (wave * volume * 32767).astype(np.int16)
        stereo = np.column_stack([audio, audio])
        return pygame.sndarray.make_sound(stereo)
    except Exception:
        return None


class SnakeScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)


        self.screen = self.engine.screen
        self.font_big = pygame.font.SysFont("couriernew,monospace", 22, bold=True)
        self.font_small = pygame.font.SysFont("couriernew,monospace", 14, bold=True)
        self.font_score = pygame.font.SysFont("couriernew,monospace", 18, bold=True)

        self.beep_eat = make_beep(1000, 50)
        self.beep_die = make_beep(160, 300)
        self.beep_start = make_beep(660, 80)

        self.high_score = 0
        self.reset()

    def reset(self):
        cx, cy = COLUMNS // 2, ROWS // 2
        self.snake = [(cx - 1, cy), (cx - 2, cy), (cx - 3, cy)]
        self.direction = RIGHT
        self.pending_direction = RIGHT
        self.grow_pending = 0
        self.score = 0
        self.interval = START_SPEED_INTERVAL
        self.state = "START"
        self.food = self.spawn_food()
        pygame.time.set_timer(MOVE_EVENT, self.interval)

    def spawn_food(self):
        occupied = set(self.snake)
        while True:
            pos = (random.randrange(COLUMNS), random.randrange(ROWS))
            if pos not in occupied:
                return pos

    def handle_input(self, event):

        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            from menus.library import Library
            self.manager.change_scene(Library(self.manager))
            return

        if self.state == "START":
            if event.key == pygame.K_RETURN:
                self.state = "PLAYING"
                if self.beep_start:
                    self.beep_start.play()
            return

        if self.state == "GAMEOVER":
            if event.key == pygame.K_RETURN:
                self.reset()
            return

        if event.key == pygame.K_p:
            if self.state == "PLAYING":
                self.state = "PAUSED"
            elif self.state == "PAUSED":
                self.state = "PLAYING"
            return

        if self.state != "PLAYING":
            return

        if event.key in (pygame.K_UP, pygame.K_w) and self.direction != DOWN:
            self.pending_direction = UP

        elif event.key in (pygame.K_DOWN, pygame.K_s) and self.direction != UP:
            self.pending_direction = DOWN

        elif event.key in (pygame.K_LEFT, pygame.K_a) and self.direction != RIGHT:
            self.pending_direction = LEFT

        elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.direction != LEFT:
            self.pending_direction = RIGHT


    def step(self):
        if self.state != "PLAYING":
            return

        self.direction = self.pending_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if not (0 <= new_head[0] < COLUMNS and 0 <= new_head[1] < ROWS):
            self.game_over()
            return

        body_to_check = self.snake if self.grow_pending > 0 else self.snake[:-1]
        if new_head in body_to_check:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.high_score = max(self.high_score, self.score)
            self.grow_pending += 1
            self.food = self.spawn_food()
            if self.beep_eat:
                self.beep_eat.play()
            self.interval = max(MIN_SPEED_INTERVAL, self.interval - SPEED_INCREMENT)
            pygame.time.set_timer(MOVE_EVENT, self.interval)

        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.snake.pop()

    def game_over(self):
        self.state = "GAMEOVER"
        if self.beep_die:
            self.beep_die.play()

    def draw_cell(self, gx, gy, color=SNAKE_COLOR, inset=2):
        x = BEZEL_THICKNESS + gx * CELL_SIZE
        y = BEZEL_THICKNESS + TOP_BAR_HEIGHT + gy * CELL_SIZE
        rect = pygame.Rect(x + inset, y + inset, CELL_SIZE - inset * 2, CELL_SIZE - inset * 2)
        pygame.draw.rect(self.screen, color, rect)

    def draw_lcd_background(self):
        for gx in range(COLUMNS):
            for gy in range(ROWS):
                x = BEZEL_THICKNESS + gx * CELL_SIZE
                y = BEZEL_THICKNESS + TOP_BAR_HEIGHT + gy * CELL_SIZE
                dot = pygame.Rect(x + CELL_SIZE // 2 - 1, y + CELL_SIZE // 2 - 1, 2, 2)
                pygame.draw.rect(self.screen, GRID_DOT_COLOR, dot)

    def draw_frame(self):
        pygame.draw.rect(self.screen, FRAME_COLOR, self.screen.get_rect())
        panel = pygame.Rect(BEZEL_THICKNESS // 2, BEZEL_THICKNESS // 2,
                             SCREEN_WIDTH - BEZEL_THICKNESS, SCREEN_HEIGHT - BEZEL_THICKNESS)
        pygame.draw.rect(self.screen, PANEL_SHADOW_COLOR, panel, border_radius=6)
        inner = pygame.Rect(BEZEL_THICKNESS, BEZEL_THICKNESS, SCREEN_WIDTH - BEZEL_THICKNESS * 2, SCREEN_HEIGHT - BEZEL_THICKNESS * 2)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, inner, border_radius=4)

    def draw_status_bar(self):
        bar_rect = pygame.Rect(BEZEL_THICKNESS, BEZEL_THICKNESS, PLAY_AREA_WIDTH, TOP_BAR_HEIGHT)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, bar_rect)

        title = self.font_small.render("SNAKE", True, SNAKE_COLOR)
        self.screen.blit(title, (BEZEL_THICKNESS + 4, BEZEL_THICKNESS + 4))

        score_text = self.font_score.render(f"{self.score:03d}", True, SNAKE_COLOR)
        score_rect = score_text.get_rect()
        score_rect.topright = (BEZEL_THICKNESS + PLAY_AREA_WIDTH - 4, BEZEL_THICKNESS + 2)
        self.screen.blit(score_text, score_rect)

        line_y = BEZEL_THICKNESS + TOP_BAR_HEIGHT - 2
        pygame.draw.line(self.screen, SNAKE_COLOR,
                          (BEZEL_THICKNESS + 2, line_y), (BEZEL_THICKNESS + PLAY_AREA_WIDTH - 2, line_y), 2)

    def draw_centered_text_block(self, lines, start_y, big_first=True):
        y = start_y
        for i, line in enumerate(lines):
            font = self.font_big if (i == 0 and big_first) else self.font_small
            surf = font.render(line, True, SNAKE_COLOR)
            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(surf, rect)
            y += font.get_height() + 6
            
            
    def draw(self, screen):

        self.screen = screen

        self.draw_frame()
        self.draw_status_bar()
        self.draw_lcd_background()

        if self.state == "START":
            self.draw_centered_text_block(
                ["SNAKE", "", "PRESS ENTER", "TO PLAY"],
                start_y=BEZEL_THICKNESS + TOP_BAR_HEIGHT + PLAY_AREA_HEIGHT // 2 - 30,
            )
        else:
            self.draw_cell(*self.food, color=SNAKE_COLOR, inset=4)

            for segment in self.snake:
                self.draw_cell(*segment, color=SNAKE_COLOR, inset=2)

            if self.state == "PAUSED":
                self.draw_centered_text_block(
                    ["PAUSED", "", "PRESS P", "TO RESUME"],
                    start_y=BEZEL_THICKNESS + TOP_BAR_HEIGHT + PLAY_AREA_HEIGHT // 2 - 30,
                )

            elif self.state == "GAMEOVER":
                self.draw_centered_text_block(
                    [
                        "GAME OVER",
                        "",
                        f"SCORE {self.score:03d}",
                        f"BEST  {self.high_score:03d}",
                        "",
                        "ENTER=RETRY",
                    ],
                    start_y=BEZEL_THICKNESS + TOP_BAR_HEIGHT + PLAY_AREA_HEIGHT // 2 - 55,
                )

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOVE_EVENT:
                self.step()

            elif event.type == pygame.KEYDOWN:
                self.handle_input(event)
    def update(self, dt):
        pass

