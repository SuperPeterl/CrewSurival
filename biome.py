import pygame
import random
import colorsys
from constants import biome_item_list
from inventory import Inventory
from item import Item,Food, Equipment

class Biome:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.inventory = Inventory(capacity=10)
        self.biome_items = biome_item_list
        self.possible_items = self.get_possible_items()
        self.initialize_items()

    def get_possible_items(self):
        return self.biome_items.get(self.name, [])  # Return an empty list if biome not found

    def initialize_items(self):
        # Add some random items from the possible items list
        for _ in range(random.randint(3, 6)):  # Add 3 to 6 items
            if self.possible_items:
                item = random.choice(self.possible_items)
                create_item = self.create_item(item)
                self.inventory.add_item(create_item)
    def create_item(self, item):
    # Create a new instance of the item to avoid reference issues
        if isinstance(item, Food):
            new_item = Food(item.name, item.description, item.weight, 
                            item.stamina_restore, item.hunger_restore, item.thirst_restore)
        elif isinstance(item, Equipment):
            new_item = Equipment(item.name, item.description, item.weight)
        else:
            new_item = Item(item.name, item.description, item.weight)
        return new_item
    
    def random_take_item(self):
        if len(self.inventory.items) > 0:
            item = self.inventory.get_item(random.randint(0, len(self.inventory.items) - 1))
            take_item = self.create_item(item)
            self.inventory.remove_item(item)
            return take_item
        return

    def replenish_items(self):
        if len(self.inventory.items) < self.inventory.capacity:
            self.initialize_items()

    def apply_lighting(self, color):
        if random.randint(0,100) > 25:
            return color 
        h, s, v = colorsys.rgb_to_hsv(*[c/255.0 for c in color])
        v *= random.uniform(0.95, 1.0)
        return [int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v)]
    
    def draw(self,screen,screen_x,screen_y,TILE_SIZE):
        pygame.draw.rect(screen, self.apply_lighting(self.color), (screen_x, screen_y, TILE_SIZE, TILE_SIZE))


    def get_name(self):
        return self.name
    
    def get_inventory(self):
        return self.inventory.items