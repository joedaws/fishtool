from cartomancy.engine.animators.animator import Animator


class SlowText(Animator):
    def __init__(self):
        super().__init__()
        # make the fps faster
        self.fps = 30  

    def make_str_list(self, s):
        """Return a list of substrs of s of increasing length.

        Example:
            s = 'hello'
            returns ['h', 'he', 'hel', 'hell', 'hello']
        """
        return [s[:k] for k in range(len(s)+1)]

    def animate_text(self, s):
        """Animate some text by revealing each character one at a time.

        Improvements:
            Should spaces be treated differently?
        """
        str_list = self.make_str_list(s)
        self.animate(strings_to_draw=str_list)

