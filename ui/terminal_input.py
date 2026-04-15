import sys
import time

if sys.platform == "win32":
    import msvcrt
else:
    import select
    import termios
    import tty


class TerminalInput:
    def __init__(self, tick=0.5):
        self.tick = tick
        self._is_windows = sys.platform == "win32"
        self._orig_term_settings = None

    def enable(self):
        if self._is_windows:
            return

        try:
            if hasattr(sys.stdin, "fileno"):
                self._orig_term_settings = termios.tcgetattr(sys.stdin)
                tty.setcbreak(sys.stdin.fileno())
        except Exception:
            self._orig_term_settings = None

    def restore(self):
        if self._is_windows:
            return

        try:
            if self._orig_term_settings:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._orig_term_settings)
                self._orig_term_settings = None
        except Exception:
            pass

    def read_command(self):
        if self._is_windows:
            return self._read_command_windows()

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

    def _read_command_windows(self):
        deadline = time.monotonic() + self.tick
        while time.monotonic() < deadline:
            if msvcrt.kbhit():
                ch = msvcrt.getwch()

                if ch == "\x03":
                    return "q"

                # Arrow/function keys arrive as a two-character sequence.
                if ch in ("\x00", "\xe0"):
                    if msvcrt.kbhit():
                        msvcrt.getwch()
                    return None

                if ch == "\x1b":
                    return None

                return ch

            time.sleep(0.01)

        return None
