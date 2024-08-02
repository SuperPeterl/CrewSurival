import pygame
from constants import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def draw_map(self, world, camera):
        world.draw(self.screen, camera)

    def draw_player(self, player, camera):
        player.draw(self.screen, camera)

    def draw_minimap(self, world, camera):
        minimap_surface = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))
        tile_size = MINIMAP_SIZE / GRID_SIZE
        
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                biome =  world.terrain[y][x]
                #print(biome)
                color = biome.color
                pygame.draw.rect(minimap_surface, color, (x * tile_size, y * tile_size, tile_size, tile_size))
        
        viewport_x = camera.x / (GRID_SIZE * TILE_SIZE) * MINIMAP_SIZE
        viewport_y = camera.y / (GRID_SIZE * TILE_SIZE) * MINIMAP_SIZE
        viewport_width = (camera.width / (GRID_SIZE * TILE_SIZE)) * MINIMAP_SIZE
        viewport_height = (camera.height / (GRID_SIZE * TILE_SIZE)) * MINIMAP_SIZE
        pygame.draw.rect(minimap_surface, VIEWPORT_INDICATOR, (viewport_x, viewport_y, viewport_width, viewport_height), 2)
        
        self.screen.blit(minimap_surface, (SCREEN_WIDTH - MINIMAP_SIZE - 10, 10))
        pygame.draw.rect(self.screen, MINIMAP_BORDER, (SCREEN_WIDTH - MINIMAP_SIZE - 10, 10, MINIMAP_SIZE, MINIMAP_SIZE), 2)

    #Draw the biome name and list of itrm in biome inventory where the player is standing
    def draw_information(self, world, player):
        biome = world.get_tile(player.x, player.y)
        self.draw_text(biome.get_name(), (10, 40))
        self.draw_text("Items:", (10, 60))
        for i, item in enumerate(biome.get_inventory()):
            self.draw_text(f"{i + 1}. {item}", (10, 80 + (i * 20)))

    def draw_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, position)