"""Client game CLI."""

import cmd
import game

class GameShell(cmd.Cmd):
    """Command line game UI"""

    intro = """Welcome to ru-game!

Enter "start" to start a new game.  The server will pick an answer from a list of Olympic sports.
Your job is to ask questions about the kinds of actions players take or things that are used in
the game.

Enter "things" to see a list of things you can ask about.

When you think you have the answer, just say "guess".  You only get one chance!

You can start a new game after each guess.

Use arrow keys to recall previous commands.  Pressing Enter executes the last command.

Enter "help" or "?" for command info."""

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

    def do_things(self, arg):
        """List the things that you should ask about."""
        print(self._game.get_props())

    def do_ask(self, arg):
        """Ask a question. You will be prompted to answer the question. Punctuation not required."""
        if not self._got_game():
            return
        self._game.ask(raw_input('Question: '))

    def do_guess(self, arg):
        """Guess the answer. You will be prompted to answer the question. You only get one guess!"""
        if not self._got_game():
            return
        self._game.guess(raw_input('Guess: '))

    def do_quit(self, arg):
        """Quit the game and exit. If the game isn't over, the server will be notified."""
        self._game.quit()
        return True

    def do_version(self, arg):
        """Print the game client version."""
        print(self._game.version)

    def _got_game(self):
        if self._game.state == game.ON:
            return True
        print('No game in progress.  Enter "start" to start a new game.')
        return False
