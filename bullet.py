import random
from pico2d import *
import game_world
import game_framework

import collision
import server

class Bullet:
    image = None

    def __init__(self, x = -1000, y = -1000, velocity = 1):
        # if Ball.image == None:
        #     Ball.image = load_image('Texture/ball21x21.png')
        self.x, self.y, self.fall_speed = x, y, velocity

    def get_bb(self):
        # fill here
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw(self):
        self.image.draw(self.x, self.y)
        # fill here for draw
        draw_rectangle(*self.get_bb())

    def update(self):
        # self.y -= self.fall_speed * game_framework.frame_time
        self.x += self.fall_speed

        for server.monsters in server.jelly_monsters:
            if collision.collide(self, server.monsters):
                server.monsters.x, server.monsters.y = 0, 0
                server.jelly_monsters.remove(server.monsters)
                server.monsters.remove()

                self.x, self.y = 0, 0
                game_world.remove_object(self)

    #fill here for def stop
    def stop(self):
        self.fall_speed = 0

