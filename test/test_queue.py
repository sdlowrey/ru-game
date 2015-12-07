import gq
import message
import unittest

class SQSMessageTest(unittest.TestCase):
    """Test queue creation and raw message put/get delete.

    This test case purges all messages in the SQS queue when it's done.

    Since unittest orders tests alphabetically, """

    @classmethod
    def setUpClass(cls):
        """Create or retrieve an SQS queue and verify that it has a valid URL.

        If this raises NoRegionError, you need to set a default region in .aws/credentials.
        """
        # TODO: purge the queue and poll it until it's empty; manual deletion via console required for now
        cls.q = gq.SqsQueue('test')

    @classmethod
    def tearDownClass(cls):
        """Purge the queue of messages that might be hanging around after test failures."""
        cls.q.purge()

    def test_a_create(self):
        self.assertRegexpMatches(self.q.url, '^https*')

    def test_b_put_crap(self):
        """Put a plain string message into the queue."""
        with self.assertRaises(gq.GameQueueError):
            self.q.put('hello world!')

    def test_c_put_real(self):
        """Put a game message into the queue."""
        msg = message.GameMessage(message.MSG_START, 0, 'my_queue_name')
        response = self.q.put(msg)
        self.assertIsInstance(response, dict)
        self.assertTrue('MessageId' in response.keys())

    def test_c_get(self):
        """Get a single message from the queue."""
        response = self.q.get()
        self.assertIsInstance(response, message.GameMessage)
