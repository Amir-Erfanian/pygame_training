import pygame

import settings

from core.scene import Scene
from games.registry import GAMES


class Library(Scene):

    def __init__(self, manager):
        super().__init__(manager)

        self.font = self.engine.assets.font(
            "Poppins-Bold.ttf",
            42
        )

        self.small = self.engine.assets.font(
            "Poppins-Regular.ttf",
            26
        )

        self.selected = 0

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    from menus.main_menu import MainMenu

                    self.manager.change_scene(
                        MainMenu(self.manager)
                    )

                elif event.key == pygame.K_DOWN:

                    self.selected = min(
                        self.selected + 1,
                        len(GAMES) - 1
                    )

                elif event.key == pygame.K_UP:

                    self.selected = max(
                        self.selected - 1,
                        0
                    )

                elif event.key == pygame.K_RETURN:
                    print("ENTER PRESSED")

                    scene = GAMES[self.selected].scene
                    print("Scene:", scene)

                    try:
                        instance = scene(self.manager)
                        print("Scene created successfully")
                        self.manager.change_scene(instance)
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
    def update(self, dt):
        pass

    def draw(self, screen):

        screen.fill((35, 45, 70))

        title = self.font.render(
            "Library",
            True,
            settings.WHITE
        )

        screen.blit(title, (40, 40))

        y = 140

        for i, game in enumerate(GAMES):

            color = (
                (255, 255, 0)
                if i == self.selected
                else settings.WHITE
            )

            text = self.small.render(
                game.title,
                True,
                color
            )

            screen.blit(text, (80, y))

            y += 60