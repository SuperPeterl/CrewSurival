import pygame
from world import World
from camera import Camera
from renderer import Renderer
from player import Player
from constants import *
from time_system import TimeSystem
from agent import PlayerAgent
from uilts import *
import random
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Post-Apocalyptic")
        self.clock = pygame.time.Clock()
        
        self.world = World()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT,CAMERA_SPEED)
        self.renderer = Renderer(self.screen)
        self.time_system = TimeSystem()
        self.players = self.init_players(self.world)
        self.current_player_index = 0
        self.playeragent = None#PlayerAgent()
        self.last_action = ""
        self.actions = []
        self.mouse = (0, 0)

    def init_players(self,world):
        players = []
        for player_number in range(5):
            #do while loop to get a random position that is not water and border
            while True:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                if world.get_tile(x, y).name in can_spawn_biome:
                    break
            create_player = Player(x,y,f"Player {player_number + 1}" )
            players.append(create_player)
        return players
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.world.regenerate()

                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    self.switch_player(event.key - pygame.K_1)

                self.handle_player_action(event.key)
            if event.type == pygame.MOUSEMOTION:
                self.handle_camera_movement(event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    print(self.get_information())
                if event.key == pygame.K_o:
                    self.handle_player_agent()
            if self.handle_player_die() == False:
                return False
            #print(event)
        return True

    def switch_player(self, index):
        if 0 <= index < len(self.players):
            self.current_player_index = index
            print(f"Now controlling {self.players[self.current_player_index].name}")

    def handle_camera_movement(self, mouse):
        x, y = mouse
        edge_size = 20  # Size of the edge area that triggers movemen
        self.mouse = (x, y)
        #get grid position of mouse
        if x < edge_size:
            self.camera.move_to("left")
        elif x > SCREEN_WIDTH - edge_size:
            self.camera.move_to("right")
        elif y < edge_size:
            self.camera.move_to("up")
        elif y > SCREEN_HEIGHT - edge_size:
            self.camera.move_to("down")
        else:
            self.camera.move_to("")
    def handle_player_action(self, key):
        current_player = self.players[self.current_player_index]
        if key == pygame.K_a:
            current_player.start_move(-1, 0, self.world)
        elif key == pygame.K_d:
            current_player.start_move(1, 0, self.world)
        elif key == pygame.K_w:
            current_player.start_move(0, -1, self.world)
        elif key == pygame.K_s:
            current_player.start_move(0, 1, self.world)
        elif key == pygame.K_e:
            current_player.start_search(self.world)
        #select item
        elif key == pygame.K_UP:
            current_player.select_item(current_player.selected_item_index - 1)
        elif key == pygame.K_DOWN:
            current_player.select_item(current_player.selected_item_index + 1)

        elif key == pygame.K_RETURN:
            current_player.use_item()
        
    def handle_player_agent(self):
        current_player = self.players[self.current_player_index]
        actions = self.playeragent.get_dicision(self.get_information(), self.last_action, read_file("memory.txt"))
        try:
            self.actions = eval(actions)
        except:
            self.last_action = actions + "is invalid action"

    def handle_player_die(self):
        for player in self.players:
            if player.health <= 0:
                self.last_action = "You died"
                self.players.remove(player)
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
                print(f"Now controlling {self.players[self.current_player_index].name}")
        if len(self.players) == 0:
            print("Game Over")
            return False
        return True
    #check player is idle and do action when done pop fist action from list
    def player_do_actions(self):
        current_player = self.players[self.current_player_index]
        if current_player.state == "idle":
            if len(self.actions) > 0:
                action = self.actions.pop(0)
                if action == "move_left":
                    current_player.start_move(-1, 0, self.world)
                elif action == "move_right":
                    current_player.start_move(1, 0, self.world)
                elif action == "move_up":
                    current_player.start_move(0, -1, self.world)
                elif action == "move_down":
                    current_player.start_move(0, 1, self.world)
                elif action == "search":
                    current_player.start_search(self.world)
                elif action == "use":
                    current_player.use_item()
                else:
                    self.last_action =  self.last_action + action + "is invalid action"
            else:
                self.handle_player_agent()

    def update(self):
        current_time = self.time_system.get_current_time()
        for player in self.players:
            player.update(current_time, self.world)
        self.camera.update()
        #self.player_do_actions()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.renderer.draw_map(self.world, self.camera)
        self.renderer.draw_minimap(self.world, self.camera)
        self.renderer.draw_text(f"Game Time: {self.time_system.get_formatted_time()}", (10, 20))
        self.renderer.draw_information(self.world, self.players[self.current_player_index])
        self.renderer.draw_text(str(self.mouse), (self.camera.width//2, 10))
        #draw a grid posint of mouse
        x, y = self.mouse
        grid_x = x // TILE_SIZE + self.camera.x // TILE_SIZE
        grid_y = y // TILE_SIZE + self.camera.y // TILE_SIZE
        self.renderer.draw_text(f"Grid Position: {grid_x}, {grid_y}", (self.camera.width//2, 40))
        for i, player in enumerate(self.players):
            self.renderer.draw_player(player, self.camera)
        pygame.display.flip()
    
    #it will get information from game and write to the file to string of json format
    def get_information_json(self):
        information = {
            "player": self.players[self.current_player_index].name,
            "stamina": self.players[self.current_player_index].stamina,
            "health": self.players[self.current_player_index].health,
            "hunger": self.players[self.current_player_index].hunger,
            "thirst": self.players[self.current_player_index].thirst,
            "position": (self.players[self.current_player_index].x, self.players[self.current_player_index].y),
            "state": self.players[self.current_player_index].state,
            "inventory": str(self.players[self.current_player_index].inventory),
            "selected_item": self.players[self.current_player_index].selected_item_index,
            "time": self.time_system.get_formatted_time()
        }
        return json.dumps(information)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()