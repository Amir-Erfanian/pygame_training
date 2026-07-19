import pygame

import settings

from core.scene import Scene


class MainMenu(Scene):

    def __init__(self, manager):
        super().__init__(manager)

        self.font = pygame.font.SysFont(
            settings.FONT_NAME,
            60
        )

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit

    def update(self, dt):
        pass

    def draw(self, screen):

        screen.fill(settings.BG_COLOR)

        title = self.font.render(
            "PYGAME GAME HUB",
            True,
            settings.WHITE
        )

        rect = title.get_rect(
            center=(settings.WIDTH//2,120)
        )

        screen.blit(title, rect)