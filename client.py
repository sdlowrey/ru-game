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
        """Start a new game.

        If a game is already in progress, then no need to send a message.
        """
        if self._game.state == game.ON:
            print('Game {} is already in progress.'.format(self._game.id))
            return
        self._game.start()

    def do_ask(self, arg):
        self._game.ask(raw_input('Question: '))

    def do_guess(self, arg):
        self._game.guess(raw_input('Guess: '))

    def do_quit(self, arg):
        """Quit the game. If the game isn't over, end it with the server.  Exit the UI."""
        self._game.quit()
        return True

    def do_version(self, arg):
        """Print the game client version."""
        print(self._game.version)

