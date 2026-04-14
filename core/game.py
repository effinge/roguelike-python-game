from core.game_factory import GameFactory
from systems.command_handler import CommandHandler
from systems.enemy_turn_system import EnemyTurnSystem
from ui.terminal_input import TerminalInput


class Game:
    def __init__(self):
        self.state = GameFactory.create_new_game()
        self.terminal = TerminalInput(self.state.tick)
        self.command_handler = CommandHandler(self.terminal)

    def run(self):
        try:
            self.terminal.enable()

            while self.state.is_running:
                self.state.renderer.draw(self.state)
                command = self.terminal.read_command()

                if command is not None:
                    self.command_handler.handle(command, self.state)
                else:
                    EnemyTurnSystem.run(self.state)

        finally:
            self.terminal.restore()
            print("Игра закончена.")