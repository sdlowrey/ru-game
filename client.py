"""The client"""

import cmd

VERSION = '0.1'


class Game(object):
    """The client's game perspective"""

    def __init__(self):
        self._game = 0

    def start(self):
        self._game = 1

    @property
    def version(self):
        return VERSION


class GameShell(cmd.Cmd):
    """Command line game UI"""

    intro = 'Welcome to ru-game!  Enter "help" or "?" for commands.'
    prompt = '[ru-game] '

    def preloop(self):
        """Create a Game before starting the loop."""
        self._game = Game()

    def do_version(self, arg):
        """Print the game client version."""
        print(self._game.version)

    def do_quit(self, arg):
        """Quit the game."""
        return True
