"""The server's game perspective."""

import botocore.exceptions
# from configparser import ConfigParser
import message
import gq
import game
import signal


class Server(object):
    """Core service functions for the game, including message receipt, dispatch, and response.

    A server queue for incoming requests is created (or acquired, if it exists) during instantiation.
    """
    # TODO server games that lost their client will need to time out
    def __init__(self):
        # self._getcfg()
        # TODO the inability to restart quickly should either be handled by a built-in wait (or handling in __new__?)
        self._next_game = 0
        self._games = {}
        self._running = False
        try:
            self._in = gq.SqsQueue('server')
        except botocore.exceptions.ClientError:
            print('Error creating/opening queue.  If you just restarted the server, wait 60s and try again.')
            return
        self._running = True

    def loop(self):
        """Main loop for getting and processing requests from the queue.

        When a message is received, the message type is used as the key call the associated handler.  The handler does
        its thing and puts a response into the client queue.

        Prototype runs interactively, so loop can end on Ctrl-C.  Queue is deleted on cleanup.
        """
        signal.signal(signal.SIGINT, self._sighandler)
        if not self._running:
            return
        print('Ready')
        while self._running:
            msg = self._in.get()
            if msg is None:
                print('Polling...')
                continue
            print('received: {}'.format(msg))
            self._dispatch(msg)
        self._cleanup()
        return

    def _dispatch(self, msg):
        """Dispatch the message to a game.

        Side effect: game instances are created (start) and deleted (quit) here.
        """
        if msg.user not in self._games.keys() and msg.type != message.MSG_START:
            print('dropping message from unknown user {}'.format(str(msg)))
            return
        if msg.type == message.MSG_START:
            self._next_game += 1
            self._games[msg.user] = game.ServerGame(self._next_game, msg)
            return
        self._games[msg.user].handle(msg)
        if self._games[msg.user].state == game.OVER:
            # TODO update scoreboard with game result
            del self._games[msg.user]

    def _cleanup(self):
        print('Cleaning up...')
        self._in.delete()

    def _sighandler(self, sig, f):
        """Ctrl-C handler that changes state and lets the main loop cleanup."""
        print('\nInterrupted -- shutting down')
        self._running = False

    def _is_valid(self, msg):
        """Check message against context."""

#    def _getcfg(self):
#        """Get configuration from file."""
#        cfg = ConfigParser()
#        cfg.read('ru-game.cfg')
#        self._mode = cfg.get('server', 'mode')
