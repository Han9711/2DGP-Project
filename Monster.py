from pico2d import *
import random
import game_framework
import game_world
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

import server
import collision

# monster Move Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# monster Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 9

class Jelly_Monster:

    image = None

    def __init__(self, x=0, y=0):
        self.x, self.y = x * PIXEL_PER_METER, y * PIXEL_PER_METER
        # self.velocity_x = random.randint(0, 10)
        # self.velocity_y = random.randint(0, 10)
        self.frame = 0
        self.dir = random.random() * 2 * math.pi  # random moving direction
        self.speed = 0
        self.timer = 1.0  # change direction every 1 sec when wandering
        if Jelly_Monster.image == None:
            Jelly_Monster.image = load_image('Texture/Jellymonster_Sheet.png')

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.random()*2*math.pi

        return BehaviorTree.SUCCESS


    def find_player(self):
        distance = (server.boy.x - self.x)**2 + (server.boy.y - self.y)**2
        if distance < (PIXEL_PER_METER * 10)**2:
            self.dir = math.atan2(server.boy.y - self.y, server.boy.x - self.x)
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        wander_node = LeafNode("Wnader", self.wander)
        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        wander_chase_node = SelectorNode("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)
        self.bt = BehaviorTree(wander_chase_node)


    def get_bb(self):
        return self.x - 22, self.y - 22, self.x + 22, self.y + 25
        pass

    def update(self):
        # self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        # self.bt.run()
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x -= self.speed * math.cos(self.dir)*game_framework.frame_time
        self.y -= self.speed * math.sin(self.dir)*game_framework.frame_time
        self.x = clamp(60, self.x, get_canvas_width() - 60)
        self.y = clamp(60, self.y, get_canvas_height() - 60)


    def draw(self):
        self.image.clip_draw(int(self.frame) * 50, 70, 50, 35, self.x, self.y)    #60 x 70,  55 x 35, 3번째 칸 175
        draw_rectangle(*self.get_bb())
        pass


    def remove(self):
        game_world.remove_object(self)


