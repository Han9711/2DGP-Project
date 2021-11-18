from pico2d import *
import random
import game_framework
import game_world

class Heart:
    image = None

    def __init__(self):
        self.x, self.y = random.randint(100, 800 - 25), random.randint(100, 600 - 25)
        if Heart.image is None:
            Heart.image = load_image('Texture/heart.png')



    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def remove(self):
        game_world.remove_object(self)