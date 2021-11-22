from pico2d import *
import game_framework
import game_world


# 무기 클래스 생성 / 마우스 움직임에 따라 이동 / 클릭 누르면 공격


class Sword:

    def __init__(self):
        self.x, self.y = 500, 500
        self.image = load_image('Texture/sword.png')
        self.velocity = 0


    def draw(self):
        self.image.draw(self.x, self.y, 40, 40)
        draw_rectangle(*self.get_bb())
        pass

    def update(self):
        events = get_events()
        for event in events:
            if event.type == SDL_MOUSEMOTION:
                self.x, self.y = event.x, 600 - 1 - event.y

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20



