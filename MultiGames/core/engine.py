import pygame

import settings


class Engine:

    def __init__(self):

        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT)
        )

        pygame.display.set_caption(settings.TITLE)

        self.clock = pygame.time.Clock()

        self.running = True

        self.fps = 0

    def quit(self):
        self.running = False