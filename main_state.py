import random
import json
import os

from pico2d import *
import game_framework
import game_world



import title_state

name = "MainState"

boy = None
grass = None
font = None
keyboard_x = 0

# bgm=load_music('SAMPLE_1.mp3')
# bgm.set_volume(64)
# bgm.repeat_play()

class Grass:
    def __init__(self):
        self.image = load_image('moonlighter_main.jpg')

    def draw(self):
        self.image.draw(400, 300)



class Boy:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.image = load_image('run_animation.png')
        self.dir = 1

    def update(self):
        # self.frame = (self.frame + 1) % 8
        self.x+=keyboard_x

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


def enter():
    global boy, grass
    boy = Boy()
    grass = Grass()


def exit():
    global boy, grass
    del(boy)
    del(grass)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
            keyboard_x = 10

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            keyboard_x = 10

def update():
    boy.update()


def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()
