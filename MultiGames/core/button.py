import pygame


class Button:
    def __init__(
        self,
        text,
        x,
        y,
        width,
        height,
        font,
        callback,
        bg_color=(60, 75, 95),
        hover_color=(95, 130, 180),
        text_color=(255, 255, 255)
    ):
        self.text = text

        self.rect = pygame.Rect(x, y, width, height)

        self.font = font

        self.callback = callback

        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color

        self.hovered = False

        self.scale = 1.0
        self.target_scale = 1.0

        self.current_color = list(bg_color)

        self.shadow_offset = 5

    def handle_event(self, event):

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1 and self.hovered:
                self.callback()

    def update(self, dt):

        if self.hovered:
            self.target_scale = 1.05
        else:
            self.target_scale = 1.0

        speed = 10

        self.scale += (
            self.target_scale - self.scale
        ) * speed * dt

        target = self.hover_color if self.hovered else self.bg_color

        for i in range(3):
            self.current_color[i] += (
                target[i] - self.current_color[i]
            ) * speed * dt

    def draw(self, screen):

        width = int(self.rect.width * self.scale)
        height = int(self.rect.height * self.scale)

        rect = pygame.Rect(0, 0, width, height)
        rect.center = self.rect.center

        shadow = rect.copy()
        shadow.y += self.shadow_offset

        pygame.draw.rect(
            screen,
            (20, 20, 20),
            shadow,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            self.current_color,
            rect,
            border_radius=12
        )

        text = self.font.render(
            self.text,
            True,
            self.text_color
        )

        text_rect = text.get_rect(center=rect.center)

        screen.blit(text, text_rect)