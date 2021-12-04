from pico2d import *
import game_framework
import game_world

from ball import Ball

import server
import collision

# Character Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Character Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8       # 내 스프라이트에 따라 변동가능

# Attack speed
C_TIME_PER_ACTION = 0.3
C_ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
C_FRAMES_PER_ACTION = 8

# Character Event
RIGHT_DOWN, LEFT_DOWN, UPKEY_DOWN, DOWNKEY_DOWN, UPKEY_UP, DOWNKEY_UP, RIGHT_UP, LEFT_UP, SLEEP_TIMER, SPACE, CTRL_DOWN, CTRL_UP = range(12)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_UP): UPKEY_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWNKEY_DOWN,
    (SDL_KEYUP, SDLK_UP): UPKEY_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWNKEY_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_LCTRL): CTRL_DOWN,
    (SDL_KEYUP, SDLK_LCTRL) : CTRL_UP
}



# Character States
# 캐릭터 프레임 46 x 50

class IdleState:

    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity_x += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity_x -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.velocity_x -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity_x += RUN_SPEED_PPS

        if event == UPKEY_DOWN:
            player.velocity_y += RUN_SPEED_PPS
        elif event == UPKEY_UP:
            player.velocity_y -= RUN_SPEED_PPS
        if event == DOWNKEY_DOWN:
            player.velocity_y -= RUN_SPEED_PPS
        elif event == DOWNKEY_UP:
            player.velocity_y += RUN_SPEED_PPS
        player.timer = 1000

    def exit(player, event):
        if event == SPACE:
            player.fire_ball()
        if event == CTRL_DOWN:
            print('ctrl pressed')
            player.Attack()
        pass

    def do(player):
        pass
        # character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        # character.timer -= 1
        # if character.timer == 0:
        #     character.add_event(SLEEP_TIMER)

    def draw(player):
        if player.dir == 1:
            player.right.draw(player.x, player.y)
        elif player.dir == -1:
            player.left.draw(player.x, player.y)

        if player.dir == 2:
            player.back.draw(player.x, player.y)
        elif player.dir == -2:
            player.front.draw(player.x, player.y)




class RunState:

    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity_x += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity_x -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.velocity_x -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity_x += RUN_SPEED_PPS

        if event == UPKEY_DOWN:
            player.velocity_y += RUN_SPEED_PPS
        elif event == UPKEY_UP:
            player.velocity_y -= RUN_SPEED_PPS
        if event == DOWNKEY_DOWN:
            player.velocity_y -= RUN_SPEED_PPS
        elif event == DOWNKEY_UP:
            player.velocity_y += RUN_SPEED_PPS
        # zelda.dir = clamp(-1, zelda.velocity_x, 1)
        pass

    def exit(player, event):
        if event == SPACE:
            player.fire_ball()

    def do(player):
        player.x += player.velocity_x * game_framework.frame_time
        player.x = clamp(25, player.x, 800-25)
        player.y += player.velocity_y * game_framework.frame_time
        player.y = clamp(25, player.y, 600-25)

        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10


    @staticmethod
    def draw(player):
        if player.velocity_x > 0:
            player.image.clip_draw(int(player.frame) * 100, 500, 100, 100, player.x, player.y)
            player.dir = 1
            # character.image.clip_draw(int(character.frame) * 100, 100, 100, 100, character.x, character.y)
        elif player.velocity_x < 0:
            player.image.clip_draw(int(player.frame) * 100, 400, 100, 100, player.x, player.y)
            player.dir = -1
            # character.image.clip_draw(int(character.frame) * 100, 0, 100, 100, character.x, character.y)

        if player.velocity_y > 0:
            player.image.clip_draw(int(player.frame) * 100, 600, 100, 100, player.x, player.y)
            player.dir = 2
        elif player.velocity_y < 0:
            player.image.clip_draw(int(player.frame) * 100, 700, 100, 100, player.x, player.y)
            player.dir = -2


class AttackState:

    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity_x += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity_x -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.velocity_x -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity_x += RUN_SPEED_PPS

        if event == UPKEY_DOWN:
            player.velocity_y += RUN_SPEED_PPS
        elif event == UPKEY_UP:
            player.velocity_y -= RUN_SPEED_PPS
        if event == DOWNKEY_DOWN:
            player.velocity_y -= RUN_SPEED_PPS
        elif event == DOWNKEY_UP:
            player.velocity_y += RUN_SPEED_PPS
        # zelda.dir = clamp(-1, zelda.velocity_x, 1)
        pass

    def exit(player, event):
        if event == SPACE:
            player.fire_ball()

    def do(player):
        player.x += player.velocity_x * game_framework.frame_time
        player.x = clamp(25, player.x, 800-25)
        player.y += player.velocity_y * game_framework.frame_time
        player.y = clamp(25, player.y, 600-25)

        player.frame = (player.frame + FRAMES_PER_ACTION * C_ACTION_PER_TIME * game_framework.frame_time) % 8


    @staticmethod
    def draw(player):
        if player.velocity_x > 0:
            player.image.clip_draw(int(player.frame) * 100, 100, 100, 100, player.x, player.y)
            player.dir = 1
            player.get_bb()
            # draw_rectangle(*player.get_bb())
            for server.monsters in server.jelly_monsters:
                if collision.collide(player, server.monsters):
                    server.monsters.x, server.monsters.y = 0, 0
                    server.jelly_monsters.remove(server.monsters)
                    server.monsters.remove()
            # character.image.clip_draw(int(character.frame) * 100, 100, 100, 100, character.x, character.y)
        elif player.velocity_x < 0:
            player.image.clip_draw(int(player.frame) * 100, 0, 100, 100, player.x, player.y)
            player.dir = -1
            # character.image.clip_draw(int(character.frame) * 100, 0, 100, 100, character.x, character.y)

        if player.velocity_y > 0:
            player.image.clip_draw(int(player.frame) * 100, 200, 100, 100, player.x, player.y)
            player.dir = 2
        elif player.velocity_y < 0:
            player.image.clip_draw(int(player.frame) * 100, 300, 100, 100, player.x, player.y)
            player.dir = -2


# class SleepState:
#
#     def enter(player, event):
#         player.frame = 0
#
#     def exit(player, event):
#         pass
#
#     def do(player):
#         player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
#
#     def draw(player):
#         if player.dir == 1:
#             player.image.clip_composite_draw(int(player.frame) * 100, 300, 100, 100, 3.141592 / 2, '', player.x - 25, player.y - 25, 100, 100)
#         else:
#             player.image.clip_composite_draw(int(player.frame) * 100, 200, 100, 100, -3.141592 / 2, '', player.x + 25, player.y - 25, 100, 100)



next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, UPKEY_DOWN: RunState, UPKEY_UP:RunState, DOWNKEY_DOWN:RunState, DOWNKEY_UP: RunState, SPACE: IdleState,
                CTRL_DOWN: IdleState, CTRL_UP: IdleState},

    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, UPKEY_UP:IdleState, DOWNKEY_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, UPKEY_DOWN:IdleState, DOWNKEY_DOWN: IdleState, SPACE: RunState, CTRL_DOWN: AttackState,
               CTRL_UP:RunState},

    AttackState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, UPKEY_UP:IdleState, DOWNKEY_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, UPKEY_DOWN:IdleState, DOWNKEY_DOWN: IdleState, CTRL_DOWN: IdleState, CTRL_UP: IdleState,
                  RIGHT_UP: RunState, LEFT_UP: RunState, UPKEY_UP:RunState, DOWNKEY_UP: RunState, LEFT_DOWN: RunState, RIGHT_DOWN: RunState, UPKEY_DOWN:RunState, DOWNKEY_DOWN: RunState, CTRL_DOWN: RunState, CTRL_UP: RunState}
}



class Player:


    def __init__(self):
        self.x, self.y = 800 // 2, 90
        # Character is only once created, so instance image loading is fine
        self.image = load_image('Texture/Player/player_sheet.png')
        self.front = load_image('Texture/Player/front_sword_idle.png')
        self.back = load_image('Texture/Player/back_sword_idle.png')
        self.right = load_image('Texture/Player/right_sword_idle.png')
        self.left = load_image('Texture/Player/left_sword_idle.png')
        # self.font = load_font('ENCR10B.TTF', 16)
        self.dir = -2
        self.velocity_x = 0
        self.velocity_y = 0
        self.frame = 0
        self.heart = 3
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

        # 사운드

    def fire_ball(self):
        ball = Ball(self.x, self.y, self.dir*3)
        game_world.add_object(ball, 1)

        pass


    def get_bb(self):
            return self.x + 30, self.y - 10, self.x + 45, self.y + 45

            # return self.x - 22, self.y - 22, self.x + 22, self.y + 25


    def add_event(self, event):
        self.event_que.insert(0, event)


    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)



    def Attack(self):
        print('공격')
        pass




    def draw(self):
        self.cur_state.draw(self)
        debug_print('Velcotiy : ' + str(self.velocity_x) + str(self.velocity_y) + ' Dir: ' + str(self.dir))
        # draw_rectangle(*self.get_bb())

        # self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))
        # draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)















