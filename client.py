"""Client game CLI."""

import cmd
import game

class GameShell(cmd.Cmd):
    """Command line game UI"""

    intro = 'Welcome to ru-game!  Enter "help" or "?" for commands.'
    prompt = '[ru-game] '

    def preloop(self):
        """Create a Game instance before starting the loop."""
        self._game = game.ClientGame()

    def do_start(self, arg):
        """Start a new game."""
        if self._game.state == game.ON:
            print('Game {} is already in progress.'.format(self._game.id))
            return
        self._game.start()

    def do_ask(self, arg):
        """Ask a question. You will be prompted to answer the question. Punctuation not required."""
        self._game.ask(raw_input('Question: '))

    def do_guess(self, arg):
        """Guess the answer. You will be prompted to answer the question. You only get one guess!"""
        self._game.guess(raw_input('Guess: '))

    def do_quit(self, arg):
        """Quit the game and exit. If the game isn't over, the server will be notified."""
        self._game.quit()
        return True

    def do_version(self, arg):
        """Print the game client version."""
        print(self._game.version)

