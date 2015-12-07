"""Classes and definitions for managing games from the client and server perspectives."""

import gq
import message
import random
import string

VERSION = '0.1'
INITIALIZED = 0
ON = 1
OVER = 2

solutions = ['soap', 'toaster', 'refrigerator', 'flour', 'fork', 'sink', 'pot', 'oven', 'foil', ]


class ClientGame(object):
    """The client's game perspective.  Multiple games may be played during the life of the instance.

    The name of the server queue is hardcoded.  OK for testing purposes but, in the case of AWS, the name would have to
    come from some kind of service locator.

    The client (response) queue is created on initialization and destroyed when the client game ends.  The queue name
    consists of a base string and a random 3-character suffix.

    A random user ID is chosen for all games played in this instance.

    The initial game ID is zero and will change when the server responds to the start message.
    """
    # TODO refactor common client/server game methods and attributes into an ABC
    def __init__(self):
        self._gameid = 0
        self._userid = random.randint(0,10000)
        self._server_qname = 'server'
        self._client_qname = 'client' + self._random_id(3)
        self._out = gq.SqsQueue(self._server_qname)
        self._in = gq.SqsQueue(self._client_qname)
        self._state = INITIALIZED

    def start(self):
        """Start a new game by sending a START message to the server.

        The client queue name is in the body so that the server can respond.
        """
        self._out.put(self._message(message.MSG_START, self._client_qname))
        response = self._getresponse()
        self._gameid = response.game
        self._state = ON

    def ask(self, question):
        self._out.put(self._message(message.MSG_ASK, question))
        self._getresponse()

    def guess(self, guess):
        self._out.put(self._message(message.MSG_GUESS, guess))
        self._getresponse()
        self._state = OVER

    def quit(self):
        """End the game if one is in progress."""
        if not self._state == OVER:
            self._out.put(self._message(message.MSG_QUIT))
            self._getresponse()
        self._state = OVER

    @property
    def id(self):
        return self._gameid

    @property
    def version(self):
        return VERSION

    @property
    def state(self):
        return self._state

    def _getresponse(self):
        response = self._in.get()
        print(response.body)
        return response

    def _random_id(self, length):
        """Generate a random string of the specified length.

        See http://stackoverflow.com/questions/2257441 for details.

        Refactor: move this function to a utility module for general use.
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    def _message(self, mtype, body='null'):
        """Create a GameMessage."""
        return message.GameMessage(mtype, self._gameid, self._userid, body)

class ServerGame(object):
    """Game state and functions from the server's perspective.

    The ServerGame is started implicitly upon instantiation.

    Args:
        game : unique game identifier
        msg : client start message
    """
    # TODO replace all print calls with logger calls
    def __init__(self, game, msg):
        self._game = game
        self._user = msg.user
        self._result = None
        self._clientq = msg.body
        self._out = gq.SqsQueue(self._clientq)
        self._solution = solutions[random.randint(0, len(solutions)-1)]
        self._state = INITIALIZED
        self._handler = {
            message.MSG_ASK: self._ask,
            message.MSG_GUESS: self._guess,
            message.MSG_QUIT: self._quit
        }
        self._out.put(self._message(message.MSG_START, 'Game on!'))  # TODO needs excecption handling and response check
        print('Game {} started with client queue {}'.format(self._game, self._clientq))
        print('The solution is "{}"'.format(self._solution))

    def handle(self, msg):
        self._handler[msg.type](msg)

    @property
    def state(self):
        return self._state

    @property
    def result(self):
        return self._result

    def _ask(self, msg):
        """User question handler: parse the raw (string) input and evaluate the resulting expresssion."""
        print('Question: {}'.format(msg.body))
        result = self._eval_question(msg.body)
        reply = 'Yes' if result else 'No'
        self._out.put(self._message(message.MSG_ANSWER, reply))
        print('Answer: {}'.format(reply))

    def _guess(self, msg):
        """Parse the input and see if it matches the solution."""
        self._result = self._eval_guess(msg.body)
        reply = 'Correct!' if self._result else 'Sorry. The answer is {}'.format(self._solution)
        self._out.put(self._message(message.MSG_ANSWER, reply))
        print('Guess: {}\nResult: {}'.format(msg.body, reply))
        self._state = OVER

    def _quit(self, msg):
        """Set game state and acknowledge the client request."""
        self._state = OVER
        self._out.put(self._message(message.MSG_QUIT, 'Game over'))

    def _eval_question(self, question):
        """Parse the question, derive a predicate, apply it to the solution, return the result."""
        return True  # TODO not implemented

    def _eval_guess(self, guess):
        """Parse the guess.  If more than one word, extract the noun.  Compare and return the result."""
        return True  # TODO not implemented

    def _message(self, mtype, body='null'):
        """Create a GameMessage."""
        return message.GameMessage(mtype, self._game, self._user, body)
