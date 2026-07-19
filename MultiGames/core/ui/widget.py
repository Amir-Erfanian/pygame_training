class Widget:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.visible = True
        self.enabled = True

    @property
    def rect(self):
        import pygame
        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass