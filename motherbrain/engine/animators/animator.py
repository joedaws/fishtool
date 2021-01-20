import itertools
import threading
import time
import sys
import os
from os import name, system


DEFAULT_FPS = 3


class Animator:
    """Base animator classes"""
    def __init__(self):
        self.fps = DEFAULT_FPS  # the default frames per second
        self.done = False
        try:
            self.columns, self.lines = os.get_terminal_size()
        except Exception as e:
            self.columns = 80
            self.lines = 30

    @property
    def wait_between_frames(self):
        return 1/self.fps

    def clear(self):
        # for windows
        if name == 'nt':
            _ = system('cls')

            # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    def carriage_return(self):
        sys.stdout.write('\r')

    def write(self, *args):
        sys.stdout.write(*args)

    def flush(self):
        sys.stdout.flush()

    def sleep(self, secs):
        time.sleep(secs)

    def clear_line(self):
        self.carriage_return()
        self.write(' '*(self.columns-3))
        self.flush()
        self.carriage_return()

    def clear_line_decorator(self, func):
        """Decorator for animation functions

        DOES NOT WORK YET!
        """
        def wrapper():
            self.clear_line()
            func()
            self.clear_line()
        return wrapper

    def animate(self, strings_to_draw, animate_fn=None):
        if animate_fn is None:
            animate_fn = self.animate_fn

        animate_fn(strings_to_draw=strings_to_draw)

    def animate_fn(self, strings_to_draw: list):
        """Animates the string objects in the strings to draw list.

        Args:
            strings_to_draw: List of strings that should be drawin in order

        Returns:
            nothing, but prints
        """
        for string in strings_to_draw:
            self.carriage_return()
            self.write(string)
            self.flush()
            self.sleep(self.wait_between_frames)
        self.write('\n')

    def loop_animate(self, duration, strings_to_draw, animate_fn=None):
        if animate_fn is None:
            animate_fn = self.loop_animate_fn

        t = threading.Thread(target=animate_fn,
                             kwargs={'strings_to_draw': strings_to_draw})
        t.start()

        # sleep while the animation is drawing
        self.sleep(duration)
        self.done = True

    def loop_animate_fn(self, strings_to_draw: list):
        """Looping animation the string objects in the strings to draw list.

        Args:
            strings_to_draw: List of strings that should be drawin in order

        Returns:
            nothing, but prints
        """
        # reset done just in case this function has already been called.
        self.done = False
        for c in itertools.cycle(strings_to_draw):
            if self.done:
                break
            self.carriage_return()
            self.write(c)
            self.flush()
            self.sleep(self.wait_between_frames)
        self.carriage_return()
        self.write('\n')
