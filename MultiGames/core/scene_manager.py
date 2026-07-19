class SceneManager:

    def __init__(self):
        self.scene = None

    def change_scene(self, scene):
        self.scene = scene

    def handle_events(self, events):
        self.scene.handle_events(events)

    def update(self, dt):
        self.scene.update(dt)

    def draw(self, screen):
        self.scene.draw(screen)