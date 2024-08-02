from item import *
# Constants
TILE_SIZE = 16
GRID_SIZE = 128
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 960
CAMERA_SPEED = 10
MINIMAP_SIZE = 200

#dict of parameter for item in biome
#dice of parameter for create biome
biome_list_parameter = {
    -0.25 : ("Deep Water", (50, 100, 200)),
    -0.20 : ("Water", (80, 150, 220)),
    -0.15 : ("Sand", (240, 220, 180)),
    -0.05 : ("Walking Path", (150, 150, 150),),
    0.15 : ("Grass", (100, 220, 100),),
    0.3 : ("Forest", (34, 139, 34),),
    0.5 : ("Rubble", (140, 140, 140)),
}

biome_item_list = {
        "Forest": [
            Food("Apple", "A fresh apple", 0.2, 10, 15, 5),
            Food("Berry", "A wild berry", 0.1, 5, 10, 3),
            Equipment("Stick", "A sturdy stick", 0.5),
            Food("Mushroom", "A forest mushroom", 0.1, 8, 5, 0),
        ],
        "Sand": [
            Food("Cactus Fruit", "A juicy cactus fruit", 0.3, 5, 10, 15),
            Equipment("Sand", "A handful of sand", 0.2),
            Food("Scorpion", "A crispy scorpion", 0.1, 15, 20, -5),
        ],
        "Mountain": [
            Food("Mountain Herb", "A rare mountain herb", 0.1, 20, 5, 0),
            Equipment("Rock", "A solid rock", 1.0),
            Food("Mountain Goat Cheese", "Cheese from mountain goats", 0.5, 15, 25, -5),
        ],
        "Grass": [
            Food("Wheat", "Golden wheat", 0.2, 5, 15, 0),
            Food("Grass Seeds", "Nutritious grass seeds", 0.1, 3, 8, 0),
            Equipment("Tall Grass", "A bundle of tall grass", 0.3),
        ],
}

can_spawn_biome = ["Grass","Forest","Sand"]

# Colors
MINIMAP_BORDER = (255, 255, 255)
VIEWPORT_INDICATOR = (255, 0, 0)


#items 
