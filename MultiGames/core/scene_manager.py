from core.transition import FadeTransition


class SceneManager:

    def __init__(self, engine):

        self.engine = engine

        self.scene = None

        self.next_scene = None

        self.transition = None

    def change_scene(self, new_scene):

        self.next_scene = new_scene

        self.transition = FadeTransition()

    def handle_events(self, events):

        if self.transition:
            return

        if self.scene:
            self.scene.handle_events(events)

    def update(self, dt):

        if self.transition:

            change = self.transition.update(dt)

            if change:
                self.scene = self.next_scene

            if self.transition.finished:
                self.transition = None

            return

        if self.scene:
            self.scene.update(dt)

    def draw(self, screen):

        if self.scene:
            self.scene.draw(screen)

        if self.transition:
            self.transition.draw(screen)