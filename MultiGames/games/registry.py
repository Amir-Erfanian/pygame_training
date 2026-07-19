from dataclasses import dataclass

from games.snake.snake import SnakeScene


@dataclass
class GameInfo:
    title: str
    description: str
    scene: type


GAMES = [

    GameInfo(
        title="Snake",
        description="Classic Snake",
        scene=SnakeScene
    )

]