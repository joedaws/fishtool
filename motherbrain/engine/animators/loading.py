from motherbrain.engine.animators.animator import Animator
import threading


class Loading(Animator):
    NAME = 'LOADING SCREEN'

    def __init__(self):
        super().__init__()
        self.count = 0
        self.load_str = ['l       |',
                         'lo      /',
                         'loa     -',
                         'loa     \\',
                         'load    |',
                         'loadi   /',
                         'loadin  -',
                         'loading \\']

        self.done_str = 'Done!        '

    def draw_loading(self):
        self.loop_animate(duration=10, strings_to_draw=self.load_str)
        self.write(self.done_str)
        self.flush()
        self.count += 1
