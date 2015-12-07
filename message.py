"""Game message format and functions to convert to/from other message formats."""

# Game message types.  These could just as easily be strings.  Constants make refactoring easier.
MSG_START = 0
MSG_ASK = 1
MSG_GUESS = 2
MSG_QUIT = 3
MSG_STATUS = 4
MSG_ANSWER = 5

class GameMessage(object):
    """Standard message class for all client-server communications.

    Messages are immutable.

    Args:
        mtype : message type or game operation
        game : id of the game this message is for (0 for start-game)
        user : id of the user
        body : message body
    """
    def __init__(self, mtype, game, user, body=None):
        self._type = mtype
        self._game = game
        self._user = user
        self._body = body

    @property
    def game(self):
        return self._game

    @property
    def user(self):
        return self._user

    @property
    def type(self):
        return self._type

    @property
    def body(self):
        return self._body

    def __repr__(self):
        return 'message.GameMessage({}, {}, {}, {})'.format(self._type, self._game, self._user, self._body)
