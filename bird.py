# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import get_time, load_image, load_font
import game_world
import game_framework
from math import *

# Bird Run Speed
# fill here
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Bird Action Speed
# fill here
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Run:

    @staticmethod
    def enter(bird, e):
        pass

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        print('Bird do')
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if bird.x >= 0 or bird.x <= 1600:
            bird.x += bird.face_dir * RUN_SPEED_PPS * game_framework.frame_time
            bird.face_dir = 1
        elif bird.x <= 1600 or bird.x >= 0:
            bird.x -= bird.face_dir * RUN_SPEED_PPS * game_framework.frame_time
            bird.face_dir = -1

    @staticmethod
    def draw(bird):
        if bird.face_dir == 1:
            bird.image.clip_draw(int(bird.frame) * 180, 330, 185, 170, bird.x, bird.y)
        if bird.face_dir == -1:
            bird.image.clip_composite_draw(int(bird.frame) * 170, 330, 185, 170, radians(360), 'h', bird.x, bird.y)


class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Run

    def start(self):
        self.cur_state.enter(self.bird, ('Run', 0))

    def update(self):
        self.cur_state.do(self.bird)

    def handle_event(self, e):
        pass

    def draw(self):
        self.cur_state.draw(self.bird)


class Bird:
    def __init__(self):
        self.x, self.y = random.randint(50, 800), 400
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 60, self.y + 50, f'(Time: {get_time():.2f})', (255, 255, 0))
