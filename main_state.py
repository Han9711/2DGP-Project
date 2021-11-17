import random
import json
import os

from pico2d import *
import game_framework
import game_world

from Character import Character
from background import BackGround


import title_state

name = "MainState"

character = None
background = None
font = None
keyboard_x = 0

# bgm=load_music('SAMPLE_1.mp3')
# bgm.set_volume(64)
# bgm.repeat_play()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True



def enter():
    global background, character
    character = Character()
    background = BackGround()
    game_world.add_object(background, 1)
    game_world.add_object(character, 1)

    # global balls
    # balls = [Ball() for i in range(10)]
    # game_world.add_objects(balls, 1)


def exit():
    game_world.clear()

    # global character, grass
    # del(character)
    # del(grass)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            character.handle_event(event)

        # if event.type == SDL_QUIT:
        #     game_framework.quit()
        # elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
        #     keyboard_x = 10
        #
        # elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
        #     keyboard_x = 10

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    # character.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


    # grass.draw()
    # boy.draw()
    # character.draw()

