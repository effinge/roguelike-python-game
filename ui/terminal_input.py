import sys
import tty
import termios
import select


class TerminalInput:
    def __init__(self, tick=0.5):
        self.tick = tick
        self._orig_term_settings = None

    def enable(self):
        try:
            if hasattr(sys.stdin, "fileno"):
                self._orig_term_settings = termios.tcgetattr(sys.stdin)
                tty.setcbreak(sys.stdin.fileno())
        except Exception:
            self._orig_term_settings = None

    def restore(self):
        try:
            if self._orig_term_settings:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._orig_term_settings)
                self._orig_term_settings = None
        except Exception:
            pass

    def read_command(self):
        r, _, _ = select.select([sys.stdin], [], [], self.tick)
        if not r:
            return None

        ch = sys.stdin.read(1)
        if not ch:
            return None

        if ch == "\x03":
            return "q"

        if ch == "\x1b":
            if select.select([sys.stdin], [], [], 0.01)[0]:
                _ = sys.stdin.read(1)
            if select.select([sys.stdin], [], [], 0.01)[0]:
                _ = sys.stdin.read(1)
            return None

        return ch