import sys

from core.game import Game


def configure_console_encoding():
    for stream_name in ("stdin", "stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def main():
    configure_console_encoding()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
