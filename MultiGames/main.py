import pygame

import settings

from core.engine import Engine
from core.scene_manager import SceneManager

from menus.main_menu import MainMenu


engine = Engine()

manager = SceneManager(engine)

manager.scene = MainMenu(manager)


while engine.running:

    dt = engine.clock.tick(settings.FPS) / 1000

    engine.fps = engine.clock.get_fps()

    events = pygame.event.get()

    for event in events:

        if event.type == pygame.QUIT:
            engine.quit()

    manager.handle_events(events)

    manager.update(dt)

    manager.draw(engine.screen)

    pygame.display.flip()

pygame.quit()