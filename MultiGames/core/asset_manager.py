from pathlib import Path
import pygame


class AssetManager:
    def __init__(self):
        self.base_path = Path("MultiGames/assets")

        self.font_cache = {}
        self.image_cache = {}
        self.sound_cache = {}

    def font(self, filename, size):
        key = (filename, size)

        if key not in self.font_cache:
            path = self.base_path / "fonts" / filename
            self.font_cache[key] = pygame.font.Font(path, size)

        return self.font_cache[key]

    def image(self, filename):
        if filename not in self.image_cache:
            path = self.base_path / "images" / filename
            self.image_cache[filename] = (
                pygame.image.load(path).convert_alpha()
            )

        return self.image_cache[filename]

    def sound(self, filename):
        if filename not in self.sound_cache:
            path = self.base_path / "sounds" / filename
            self.sound_cache[filename] = pygame.mixer.Sound(path)

        return self.sound_cache[filename]