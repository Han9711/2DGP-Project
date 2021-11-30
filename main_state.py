import random
import json
import os

from pico2d import *
import game_framework
import game_world

from Character import Character
from background import BackGround
from Monster import Jelly_Monster
from item import Heart
from HUD_heart import Hp
from weapon import Sword

import server

import title_state

name = "MainState"


background = None
heart = []
hearts = []


font = None
keyboard_x = 0

hud_hp = None

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
    global background
    background = BackGround()
    game_world.add_object(background, 0)


    server.character = Character()
    game_world.add_object(server.character, 1)


    server.jelly_monsters = [Jelly_Monster() for i in range(1)]
    game_world.add_objects(server.jelly_monsters, 1)

    global hearts
    hearts = [Heart() for i in range(1)]
    game_world.add_objects(hearts, 1)

    global hud_hp
    hud_hp = Hp()
    game_world.add_object(hud_hp, 1)


    server.sword = Sword()
    # game_world.add_object(server.sword, 1)


    # global balls
    # balls = [Ball() for i in range(10)]
    # game_world.add_objects(balls, 1)


def exit():
    game_world.clear()


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
            server.character.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


    for server.monsters in server.jelly_monsters:
        if collide(server.monsters, server.character):
            print('monster collide character')

        if collide(server.monsters, server.sword):
            print('monster sword collide')
            game_world.remove_object(server.monsters)


    for heart in hearts:
        if collide(server.character, heart):
            heart.x, heart.y = 0, 0
            hearts.remove(heart)
            heart.remove()
            hud_hp.heart += 1



        # hearts.remove(heart)
        # game_world.remove_object(heart)
        # hud_hp.heart += 1


    # character.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


    # grass.draw()
    # boy.draw()
    # character.draw()



