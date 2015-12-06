"""Game message format and functions to convert to/from other message formats."""

# Game message types.  These could just as easily be strings.  Constants make refactoring easier.
MSG_START = 0
MSG_ASK = 1
MSG_GUESS = 2
MSG_QUIT = 3
MSG_STATUS = 4

class GameMessage(object):
    """Standard message class for all client-server communications.

    Messages are immutable.

    Args:
        type : message type or game operation
        game : id of the game this message is for (0 for start-game)
        body : message body
    """
    def __init__(self, mtype, game, body=None):
        self._type = mtype
        self._game = game
        self._body = body

    @property
    def game(self):
        return self._game

    @property
    def type(self):
        return self._type

    @property
    def body(self):
        return self._body
