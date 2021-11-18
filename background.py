from pico2d import *
import random
import game_framework

class BackGround:

    def __init__(self):
        self.image = load_image('Texture/Map.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 300)