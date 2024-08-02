import pygame

class Effect:
    def __init__(self, name, description, duration):
        self.name = name
        self.description = description
        self.duration = duration
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen, x, y):
        text_surface = self.font.render(self.name, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))

    def apply(self, player):
        pass  # To be overridden by subclasses
    