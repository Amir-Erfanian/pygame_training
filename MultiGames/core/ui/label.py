import pygame

from .widget import Widget


class Label(Widget):
    def __init__(self, text, x, y, font, color=(255, 255, 255)):
        surface = font.render(text, True, color)

        super().__init__(x, y, surface.get_width(), surface.get_height())

        self.text = text
        self.font = font
        self.color = color

    def draw(self, screen):
        surface = self.font.render(
            self.text,
            True,
            self.color
        )

        screen.blit(surface, (self.x, self.y))