from pico2d import *
import game_framework
import game_world


# 무기 클래스 생성 / 마우스 움직임에 따라 이동 / 클릭 누르면 공격


class Sword:

    def __init__(self):
        self.image = load_image('Texture/sword.png')
        self.x
        self.y
        self.velocity = 0


    def draw(self):
        self.image.draw(self.x, self.y, 50, 50)
        pass

    def update_mouseposition(self):
        events = get_events()
        for event in events:
            if event.type == SDL_MOUSEMOTION:
                self.x, self.y = event.x, event.y



