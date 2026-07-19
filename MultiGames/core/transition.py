import pygame


class FadeTransition:

    def __init__(self, duration=0.5):
        self.duration = duration

        self.timer = 0

        self.phase = "fade_out"

        self.finished = False

        self.alpha = 0

    def update(self, dt):

        self.timer += dt

        progress = min(self.timer / self.duration, 1)

        if self.phase == "fade_out":

            self.alpha = int(progress * 255)

            if progress >= 1:
                self.phase = "fade_in"
                self.timer = 0

                return True

        else:

            self.alpha = int((1 - progress) * 255)

            if progress >= 1:
                self.finished = True

        return False

    def draw(self, screen):

        overlay = pygame.Surface(screen.get_size())

        overlay.fill((0, 0, 0))

        overlay.set_alpha(self.alpha)

        screen.blit(overlay, (0, 0))