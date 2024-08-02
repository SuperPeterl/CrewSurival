from terrain import TerrainGenerator
from biome import Biome
from constants import *

class World:
    def __init__(self):
        self.terrain_generator = TerrainGenerator()
        self.terrain = self.generate_world()
    def generate_world(self):
        return self.terrain_generator.generate_terrain()

    def regenerate(self):
        self.terrain = self.generate_world()

    def get_tile(self, x, y):
        if 0 <= x < len(self.terrain) and 0 <= y < len(self.terrain[0]):
            return self.terrain[y][x]
        return None

    def draw(self, screen, camera):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                screen_x = x * TILE_SIZE - camera.x
                screen_y = y * TILE_SIZE - camera.y
                
                if -TILE_SIZE <= screen_x < SCREEN_WIDTH and -TILE_SIZE <= screen_y < SCREEN_HEIGHT:
                    biome = self.terrain[y][x]
                    biome.draw(screen, screen_x, screen_y, TILE_SIZE)