from pico2d import *
from Character import *


class Hp:

    def __init__(self):
        self.x , self.y = 680, 580
        self.heart_image = load_image('Texture/heart.png')
        self.heart = 3
        self.font = load_font('ENCR10B.TTF', 32)

    def update(self):
        pass

    def draw(self):
        self.heart_image.draw(self.x + 7, self.y - 20, 50, 50)
        self.font.draw(self.x + 23, self.y - 20, 'X %1.f' % self.heart, (255, 0, 0))