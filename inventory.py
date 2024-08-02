from typing import Any
import pygame
from constants import *

class Inventory:
    def __init__(self, capacity):
        self.items = []
        self.capacity = capacity
        self.font = pygame.font.Font(None, 24)

    def add_item(self, adding_item):
        #print(f"Adding item {adding_item}")
        if self.get_total_weight() + adding_item.total_weight <= self.capacity:
            if adding_item.stackable:
                for item in self.items:
                    if item.name == adding_item.name:
                        item.total_weight += adding_item.weight
                        item.amount += adding_item.amount
                        return True
            self.items.append(adding_item)
    #remove by amount

    def remove_item(self, remove_item):
        #print(f"Removing item {remove_item}")
        for item in self.items:
            if item.name == remove_item.name:
                item.amount -= 1
                item.total_weight -= remove_item.weight
                if item.amount <= 0:
                    self.items.remove(item)
                return True
        return False

    def get_item(self,index):
        return self.items[index]
    
    def have_item(self, item):
        return item in self.items

    def get_total_weight(self):
        return sum(item.total_weight for item in self.items)

    def use_item(self, idex, player):
        item = self.get_item(idex)
        if item.usable:
            item.use(player)
            item.amount -= 1
            if item.amount <= 0:
                self.items.remove(item)

    def __str__(self) -> str:
        str = "\n"
        for i in self.items:
            str += f"{i}\n"
        return str