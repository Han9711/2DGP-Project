from pico2d import *
import game_framework
import game_world


# Character Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Character Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8       # 내 스프라이트에 따라 변동가능

# Character Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, SPACE = range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


# Character States
# 캐릭터 프레임 46 x 50

class IdleState:

    def enter(character, event):
        if event == RIGHT_DOWN:
            character.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            character.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            character.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            character.velocity += RUN_SPEED_PPS
        character.timer = 1000

    def exit(character, event):
        if event == SPACE:
            character.fire_ball()
        pass

    def do(character):
        pass
        # character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        # character.timer -= 1
        # if character.timer == 0:
        #     character.add_event(SLEEP_TIMER)

    def draw(character):
        if character.dir == 1:
            character.image.clip_draw(int(character.frame) * 46, 150, 46, 50, character.x, character.y)
            # character.image.clip_draw(int(character.frame) * 100, 300, 100, 100, character.x, character.y)
        else:
            character.image.clip_draw(int(character.frame) * 46, 150, 46, 50, character.x, character.y)
            # character.image.clip_draw(int(character.frame) * 100, 200, 100, 100, character.x, character.y)


class RunState:

    def enter(character, event):
        if event == RIGHT_DOWN:
            character.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            character.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            character.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            character.velocity += RUN_SPEED_PPS
        character.dir = clamp(-1, character.velocity, 1)
        pass

    def exit(character, event):
        if event == SPACE:
            character.fire_ball()

    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        character.x += character.velocity * game_framework.frame_time
        character.x = clamp(25, character.x, 1600 - 25)

    @staticmethod
    def draw(character):
        if character.dir == 1:
            character.image.clip_draw(int(character.frame) * 46, 0, 46, 50, character.x, character.y)
            # character.image.clip_draw(int(character.frame) * 100, 100, 100, 100, character.x, character.y)
        else:
            character.image.clip_draw(int(character.frame) * 47, 104, 47, 50, character.x, character.y)
            # character.image.clip_draw(int(character.frame) * 100, 0, 100, 100, character.x, character.y)


# class SleepState:
#
#     def enter(character, event):
#         character.frame = 0
#
#     def exit(character, event):
#         pass
#
#     def do(character):
#         character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
#
#     def draw(character):
#         if character.dir == 1:
#             character.image.clip_composite_draw(int(character.frame) * 100, 300, 100, 100, 3.141592 / 2, '', character.x - 25, character.y - 25, 100, 100)
#         else:
#             character.image.clip_composite_draw(int(character.frame) * 100, 200, 100, 100, -3.141592 / 2, '', character.x + 25, character.y - 25, 100, 100)



next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SPACE: IdleState},            #SLEEP_TIMER: SleepState
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, SPACE: RunState},
    # SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState, LEFT_UP: RunState, RIGHT_UP: RunState, SPACE: IdleState}
}



class Character:

    def __init__(self):
        self.x, self.y = 1600 // 2, 90
        # Character is only once created, so instance image loading is fine
        self.image = load_image('Character_Sheet.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)


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


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)














