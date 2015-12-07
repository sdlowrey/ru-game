"""A simple game queue abstraction with generic queue methods that accept/return GameMessage objects."""

import boto3
import message

POLL_WAIT = 20  # seconds

# TODO: if there is time to create a non-AWS test implementation, then create ABCMeta class here and have subs inherit


class GameQueueError(Exception):
    """General error class"""
    pass


class SqsQueue(object):
    """Game queue implmentationAWS SQS queue"""
    def __init__(self, name):
        self._name = name
        self._sqs = boto3.resource('sqs')
        self._q = self._sqs.create_queue(QueueName=name)

    def delete(self):
        """Delete the queue."""
        self._q.delete()

    def get(self):
        """Get a single message from the queue.

        Long polling is used.  If no messages are received within 20 seconds, return None.
        """
        msg = self._q.receive_messages(MaxNumberOfMessages=1, MessageAttributeNames=['All'], WaitTimeSeconds=POLL_WAIT)
        if not self._isvalid(msg):
            return None
        body = msg[0].body
        attrs = msg[0].message_attributes
        mtype = int(attrs['mtype']['StringValue'])
        gameid = int(attrs['gameid']['StringValue'])
        userid = int(attrs['userid']['StringValue'])
        msg[0].delete()
        return message.GameMessage(mtype, gameid, userid, body)

    def put(self, msg):
        """Convert a GameMessage to an SQS message and place it on the queue"""
        if not isinstance(msg, message.GameMessage):
            raise GameQueueError('put() requires a GameMessage')
        attrs = {
            'gameid' : {'DataType': 'Number', 'StringValue': str(msg.game)},
            'userid' : {'DataType': 'Number', 'StringValue': str(msg.user)},
            'mtype' : {'DataType': 'Number', 'StringValue': str(msg.type)}
        }
        return self._q.send_message(MessageBody=msg.body, MessageAttributes=attrs)

    def purge(self):
        """Delete all messages in the queue."""
        self._q.purge()

    @property
    def url(self):
        return self._q.url

    def _isvalid(self, msg):
        """Validate that the message is complete and has attributes.

        Important side effect: if the message doesn't have any attributes but is otherwise intact, it is considered
        bogus and deleted from the queue
        """
        if not isinstance(msg, list):
            print "No message received"
            return False
        if len(msg) == 0:
            # empty list happens on timeout, so stay quiet
            return False
        if msg[0].message_attributes is None:
            print('Invalid message; deleting from queue')
            msg[0].delete()
            return False
        return True
