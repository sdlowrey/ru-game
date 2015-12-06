"""A simple game queue abstraction with generic queue methods that accept/return GameMessage objects."""

import boto3

import message

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

    def get(self):
        """Get a single message from the queue.

        If no messages are received within the polling period, return None.
        """
        msg = self._q.receive_messages(MaxNumberOfMessages=1, MessageAttributeNames=['All'])
        if not isinstance(msg, list): return None
        body = msg[0].body
        attrs = msg[0].message_attributes
        mtype = int(attrs['mtype']['StringValue'])
        gameid = int(attrs['gameid']['StringValue'])
        return message.GameMessage(mtype, gameid, body)

    def put(self, msg):
        """Convert a GameMessage to an SQS message and place it on the queue"""
        if not isinstance(msg, message.GameMessage):
            raise GameQueueError('put() requires a GameMessage')
        attrs = {
            'gameid' : {'DataType': 'Number', 'StringValue': str(msg.game)},
            'mtype' : {'DataType': 'Number', 'StringValue': str(msg.type)}
        }
        return self._q.send_message(MessageBody=msg.body, MessageAttributes=attrs)

    def purge(self):
        """Delete all messages in the queue."""
        self._q.purge()

    @property
    def url(self):
        return self._q.url