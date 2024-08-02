from constants import GRID_SIZE, TILE_SIZE

class Camera:
    def __init__(self, width, height, speed):
        self.x = GRID_SIZE // 2
        self.y = GRID_SIZE // 2
        self.width = width
        self.height = height
        self.speed = 5
        self.direction = ""
    def move_to(self,direction):
        self.direction = direction

    def move(self, dx, dy):
            self.x += dx
            self.y += dy

    def stop(self):
        self.direction = ""


    def update(self,):
        self.check()
        if self.direction == "up":
            self.move(0, -self.speed)
        elif self.direction == "down":
            self.move(0, self.speed)
        elif self.direction == "left":
            self.move(-self.speed, 0)
        elif self.direction == "right":
            self.move(self.speed, 0)

    def check(self):
        if self.x < 0 and self.direction == "left":
            self.direction = ""
        if self.x + self.width > GRID_SIZE*TILE_SIZE and self.direction == "right":
            self.direction = ""
        if self.y < 0 and self.direction == "up":  
            self.direction = ""
        if self.y + self.height > GRID_SIZE*TILE_SIZE and self.direction == "down":
            self.direction = ""
    