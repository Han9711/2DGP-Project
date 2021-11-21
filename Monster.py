from pico2d import *
import random
import game_framework
import game_world

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7

class Jelly_Monster:

    image = None

    def __init__(self):
        self.x, self.y = random.randint(400, 700), random.randint(300, 400)
        self.velocity_x = random.randint(0, 10)
        self.velocity_y = random.randint(0, 10)
        self.frame = 0
        if Jelly_Monster.image == None:
            Jelly_Monster.image = load_image('Texture/Jellymonster_Sheet.png')

    def get_bb(self):
        return self.x - 22, self.y - 22, self.x + 22, self.y + 25
        pass

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        self.x -= self.velocity_x * game_framework.frame_time
        self.y -= self.velocity_y * game_framework.frame_time
        self.x = clamp(60, self.x, 800-60)
        self.y = clamp(60, self.y, 600-60)


    def draw(self):
        self.image.clip_draw(int(self.frame) * 50, 70, 50, 35, self.x, self.y)    #60 x 70,  55 x 35, 3번째 칸 175
        # draw_rectangle(*self.get_bb())
        pass


    def remove(self):
        game_world.remove_object(self)


