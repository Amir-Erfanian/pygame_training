class Scene:

    def __init__(self, manager):
        self.manager = manager

    @property
    def engine(self):
        return self.manager.engine

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass