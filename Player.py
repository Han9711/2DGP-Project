from pico2d import *
import game_framework
import game_world

from ball import Ball

import server

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

# Character Event
RIGHT_DOWN, LEFT_DOWN, UPKEY_DOWN, DOWNKEY_DOWN, UPKEY_UP, DOWNKEY_UP, RIGHT_UP, LEFT_UP, SLEEP_TIMER, SPACE, CTRL = range(11)

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
    (SDL_KEYDOWN, SDLK_LCTRL): CTRL
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
        # if event == CTRL:
        #     server.sword.Attack()
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

        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8


    @staticmethod
    def draw(player):
        if player.velocity_x > 0:
            player.image.clip_draw(int(player.frame) * 100, 100, 100, 100, player.x, player.y)
            player.dir = 1
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
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, UPKEY_DOWN: RunState, UPKEY_UP:RunState, DOWNKEY_DOWN:RunState, DOWNKEY_UP: RunState, SPACE: IdleState, CTRL: IdleState},            #SLEEP_TIMER: SleepState
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, UPKEY_UP:IdleState, DOWNKEY_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, UPKEY_DOWN:IdleState, DOWNKEY_DOWN: IdleState, SPACE: RunState, CTRL: RunState},
}



class Player:


    def __init__(self):
        self.x, self.y = 800 // 2, 90
        # Character is only once created, so instance image loading is fine
        self.image = load_image('Texture/Player/player_sheet.png')
        self.front = load_image('Texture/Player/front.png')
        self.back = load_image('Texture/Player/back.png')
        self.right = load_image('Texture/Player/right_side.png')
        self.left = load_image('Texture/Player/left_side.png')
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

    def get_sword_right(self):
        server.sword.image.draw(self.x + 30, self.y + 5, 45, 45)
        # server.sword.draw()
        pass


    def get_bb(self):
        return self.x - 22, self.y - 22, self.x + 22, self.y + 25


    def add_event(self, event):
        self.event_que.insert(0, event)


    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)







    def draw(self):
        self.cur_state.draw(self)
        debug_print('Velcotiy : ' + str(self.velocity_x) + str(self.velocity_y) + ' Dir: ' + str(self.dir))


        # self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))
        # draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)














