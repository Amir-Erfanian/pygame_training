import pygame

import settings

from core.scene import Scene
from core.ui.button import Button
from core.ui.layout import Layout


class MainMenu(Scene):

    def __init__(self, manager):
        super().__init__(manager)
        self.title_font = self.engine.assets.font(
            "Poppins-Bold.ttf",
            60
        )

        self.subtitle_font = self.engine.assets.font(
            "Poppins-Regular.ttf",
            24
        )

        self.button_font = self.engine.assets.font(
            "Poppins-Regular.ttf",
            32
        )

        self.layout = Layout()

        button_width = 260
        button_height = 60

        start_y = 240
        spacing = 80

        labels = [
            ("Play", self.play),
            ("Settings", self.settings),
            ("Exit", self.exit_game)
        ]

        for i, (text, callback) in enumerate(labels):

            x = settings.WIDTH // 2 - button_width // 2
            y = start_y + i * spacing

            button = Button(
                text,
                x,
                y,
                button_width,
                button_height,
                self.button_font,
                callback
            )

            self.layout.add(button)

    def play(self):
        from menus.library import Library

        self.manager.change_scene(
            Library(self.manager)
        )

    def settings(self):
        print("Settings clicked")

    def exit_game(self):
        pygame.quit()
        raise SystemExit

    def handle_events(self, events):

        for event in events:

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                self.exit_game()

        self.layout.handle_events(events)

    def update(self, dt):

        self.layout.update(dt)

    def draw_gradient(self, screen):

        top = (20, 25, 45)
        bottom = (45, 55, 90)

        for y in range(settings.HEIGHT):

            ratio = y / settings.HEIGHT

            color = (
                int(top[0] + (bottom[0] - top[0]) * ratio),
                int(top[1] + (bottom[1] - top[1]) * ratio),
                int(top[2] + (bottom[2] - top[2]) * ratio)
            )

            pygame.draw.line(
                screen,
                color,
                (0, y),
                (settings.WIDTH, y)
            )

    def draw(self, screen):

        self.draw_gradient(screen)

        title = self.title_font.render(
            "PYGAME GAME HUB",
            True,
            settings.WHITE
        )

        title_rect = title.get_rect(
            center=(settings.WIDTH // 2, 100)
        )

        screen.blit(title, title_rect)

        subtitle = self.subtitle_font.render(
            "A collection of classic arcade games",
            True,
            (180, 180, 180)
        )

        subtitle_rect = subtitle.get_rect(
            center=(settings.WIDTH // 2, 155)
        )

        screen.blit(subtitle, subtitle_rect)

        self.layout.draw(screen)