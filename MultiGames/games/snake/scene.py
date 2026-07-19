from core.scene import Scene
from games.snake.snake import SnakeGame


class SnakeScene(Scene):

    def __init__(self, manager):
        super().__init__(manager)

        self.game = SnakeGame()

        # Use the launcher's screen
        self.game.screen = self.engine.screen

    def handle_events(self, events):
        self.events = events

    def update(self, dt):
        self.game.run_frame(self.events)

    def draw(self, screen):
        pygame.display.flip()