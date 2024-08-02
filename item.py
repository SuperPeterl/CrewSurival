import pygame
from constants import *

class Item:
    def __init__(self, name, description, weight, stackable=True, usable=True):
        self.name = name
        self.description = description
        self.stackable = stackable
        self.amount = 1
        self.weight = weight
        self.total_weight = self.weight * self.amount
        self.usable = usable
    def draw(self, screen, x, y, font):
        text_surface = font.render(self.name, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))

    def use(self, player):
        pass  # To be overridden by subclasses

    def apply_stat(self, player):
        pass
    
    #all int is float
    def __str__(self):
        return f"{self.name} amount: {self.amount} weight: {self.weight:,.2f}"

class Food(Item):
    def __init__(self, name, description, weight, stamina_restore, hunger_restore, thirst_restore):
        super().__init__(name, description,weight)
        self.stamina_restore = stamina_restore
        self.hunger_restore = hunger_restore
        self.thirst_restore = thirst_restore
    def use(self, player):
        player.stamina = min(player.stamina + self.stamina_restore, 100)
        player.hunger = min(player.hunger + self.hunger_restore, 100)
        player.thirst = min(player.thirst + self.thirst_restore, 100)
    
    def __str__(self):
        return super().__str__() + f"stamina: {self.stamina_restore} hunger: {self.hunger_restore} thirst: {self.thirst_restore}"

#equiment item class can apply status effect to player
class Equipment(Item):
    def __init__(self, name, description, weight, stackable = True,usable = False):
        super().__init__(name, description, weight, stackable, usable)

class Material(Item):
    def __init__(self, name, description, weight, stackable = True,usable = False):
        super().__init__(name, description, weight, stackable, usable)