import random
import noise
from constants import *
from biome import Biome
class TerrainGenerator:
    def __init__(self):
        pass

    def generate_terrain(self):
        terrain = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                nx = x / GRID_SIZE - 0.5
                ny = y / GRID_SIZE - 0.5
                elevation = noise.pnoise2(nx * 3, ny * 3, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0)
                terrain[y][x] = self.get_biome(elevation)
                if x == 0 or y == 0 or y == GRID_SIZE - 1 or x == GRID_SIZE - 1:
                    terrain[y][x] = Biome("Border", (255,0,0))
        
        self.generate_buildings_and_rubble(terrain)
        return terrain

    def xget_biome(self, value):
        for biome in self.biomes:
            if value < biome.threshold:
                return biome
        return self.biomes[-1]  # Default to last biome if no threshold met

    def get_biome(self,value):
        for threshold in biome_list_parameter.keys():
            if value < threshold:
                return Biome(biome_list_parameter[threshold][0], biome_list_parameter[threshold][1])
            

    def is_valid_building_location(self, terrain, x, y, size):
        for dx in range(size):
            for dy in range(size):
                new_x, new_y = x + dx, y + dy
                if not (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE):
                    return False
                if terrain[new_y][new_x].name != "Grassland":
                    return False
        return True

    def place_building(self, terrain, x, y, size):
        for dx in range(size):
            for dy in range(size):
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    if random.random() < 0.7:
                        terrain[new_y][new_x] = Biome("Rubble", (80,80,80), 0)
                    else:
                        terrain[new_y][new_x] = Biome("Building", (150,150,250), 0)

    def generate_buildings_and_rubble(self, terrain):
        for _ in range(5):
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                size = random.randint(3, 8)
                if self.is_valid_building_location(terrain, x, y, size):
                    self.place_building(terrain, x, y, size)
                    placed = True
                attempts += 1