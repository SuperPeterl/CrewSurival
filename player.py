import pygame
from constants import *
from inventory import Inventory
import random
import datetime as date
from item import Item, Food
class Player:
    def __init__(self, x, y, name="Player"):
        self.x = x
        self.y = y
        self.name = name
        self.font = pygame.font.Font(None, 24)
        self.state = "idle"
        self.stamina = 100.0
        self.health = 100.0
        self.hunger = 100.0
        self.thirst = 100.0
        self.effects = []
        self.inventory = Inventory(capacity=50)
        self.selected_item_index = 0
        self.lasted_time = date.datetime.now()
        self.action_time = date.datetime.now()
        self.action_wait_time = date.timedelta(seconds=0)
        self.current_time = date.datetime.now()

    def update(self, current_time, world):
        self.current_time = current_time
        if (self.current_time - self.lasted_time).total_seconds() >= 1:
            self.lasted_time = self.current_time

            # Decrease rates per real-life second
            self.hunger -= 0.2
            self.thirst -= 0.3
            self.stamina += 0.1
            # ensure stats don't go below 0 and above 100 and by float data type
            self.stamina = max(0.0, min(100.0, self.stamina))
            self.health = max(0.0, min(100.0, self.health))
            self.hunger = max(0.0, min(100.0, self.hunger))
            self.thirst = max(0.0, min(100.0, self.thirst))

            # Health penalties for low stamina, hunger, and thirst
            if self.stamina <= 0:
                self.health -= 1
                self.stamina = 0  # Prevent stamina from going negative

            if self.hunger <= 0:
                self.health -= 1
                self.hunger = 0  # Prevent hunger from going negative

            if self.thirst <= 0:
                self.health -= 1
                self.thirst = 0  # Prevent thirst from going negative

            # Check for death condition
            if self.health <= 0:
                print("You died")
        
        if (self.current_time - self.action_time).total_seconds() > self.action_wait_time.total_seconds():
            self.state = "idle"

    def start_move(self, dx, dy, world):
        if self.state != "idle":
            return
        self.state = "moving"
        self.action_time = date.datetime.now()
        self.action_wait_time = date.timedelta(seconds=3)

        new_x = self.x + dx
        new_y = self.y + dy
        if world.get_tile(new_x, new_y) and world.get_tile(new_x, new_y).name != "Water":
            self.x = new_x
            self.y = new_y
            self.stamina -= 1
            self.hunger -= 0.1
            self.thirst -= 0.1

    #add a random item to the player's inventory by biome
    def start_search(self, world):
        if self.state != "idle":
            return
        self.state = "searching"
        self.action_time = date.datetime.now()
        self.action_wait_time = date.timedelta(seconds=1)
        biome = world.get_tile(self.x, self.y)
        found_rate = random.randint(0, 100)
        if found_rate > 50:
            item = biome.random_take_item()
            self.inventory.add_item(item)
        self.stamina -= 5
        self.hunger -= 0.5
        self.thirst -= 0.5

    def select_item(self, index):
        if 0 <= index < len(self.inventory.items):
            self.selected_item_index = index

    def use_item(self):
        if self.state != "idle":
            return
        self.state = "using"
        self.action_time = date.datetime.now()
        self.action_wait_time = date.timedelta(seconds=1)
        if self.selected_item_index < len(self.inventory.items):
            self.inventory.use_item(self.selected_item_index, self)

    def rest(self):
        if self.state != "idle":
            return
        self.state = "resting"
        self.action_time = date.datetime.now()
        self.action_wait_time = date.timedelta(seconds=5)

        
    def draw(self, screen, camera):
        center_x = self.x * TILE_SIZE - camera.x + TILE_SIZE // 2
        center_y = self.y * TILE_SIZE - camera.y + TILE_SIZE // 2
        radius = TILE_SIZE // 2

        # Draw hollow circle
        pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), radius, 2)

        # Draw player name below
        name_surface = self.font.render(self.name, True, (255, 255, 255))
        name_rect = name_surface.get_rect()
        name_rect.centerx = center_x
        name_rect.top = center_y + radius + 2
        screen.blit(name_surface, name_rect)

        # Draw player stats show int format the screen
        stats = f"Stamina: {int(self.stamina)} Health: {int(self.health)} Hunger: {int(self.hunger)} Thirst: {int(self.thirst)}"
        stats_surface = self.font.render(stats, True, (255, 255, 255))
        stats_rect = stats_surface.get_rect()
        stats_rect.centerx = center_x
        stats_rect.top = name_rect.bottom + 2
        screen.blit(stats_surface, stats_rect)

        # Draw list of item in inventory below stats
        for i,item in enumerate(self.inventory.items):
            item_stats = f"{item.name} amount : {item.amount}"
            if i == self.selected_item_index:
                item_stats_surface = self.font.render(item_stats, True, (255, 0, 0))
            else:
                item_stats_surface = self.font.render(item_stats, True, (255, 255, 255))
            item_stats_rect = item_stats_surface.get_rect()
            item_stats_rect.centerx = center_x
            item_stats_rect.top = stats_rect.bottom + 2
            screen.blit(item_stats_surface, item_stats_rect)
            stats_rect = item_stats_rect
    

