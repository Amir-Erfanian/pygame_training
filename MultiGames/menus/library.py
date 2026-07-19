import pygame

import settings

from core.scene import Scene


class Library(Scene):

    def __init__(self, manager):
        super().__init__(manager)

        self.title_font = pygame.font.SysFont(
            settings.FONT_NAME,
            52
        )

        self.small_font = pygame.font.SysFont(
            settings.FONT_NAME,
            28
        )

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    from menus.main_menu import MainMenu
                    self.manager.change_scene(
                        MainMenu(self.manager)
                    )

    def update(self, dt):
        pass

    def draw(self, screen):

        screen.fill((35, 45, 70))

        title = self.title_font.render(
            "Game Library",
            True,
            settings.WHITE
        )

        screen.blit(title, (60, 50))

        text = self.small_font.render(
            "Games will appear here.",
            True,
            settings.WHITE
        )

        screen.blit(text, (60, 130))
        
        pygame.draw.rect(
        screen,
        (20, 25, 40),
        (0, 0, settings.WIDTH, 80))