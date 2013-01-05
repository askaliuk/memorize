import unittest
from gtalkbot_test import GtalkBotTest


class TestSimple(GtalkBotTest):

    def test_simple(self):
        """Basic simple test which interacts with a mocked GTalkBot instance."""
        self.memorize_stream_start()

        def echo(msg):
            msg.reply('Thanks for sending: %(body)s' % msg).send()

        self.xmpp.add_event_handler('message', echo)
        self.recv("""
            <message to="tester@localhost" from="user@localhost">
                <body>Hi!</body>
            </message>
        """)

        self.send("""
            <message to="user@localhost">
                <body>Thanks for sending: Hi!</body>
            </message>
        """)

    def tearDown(self):
        self.stream_close()

if __name__ == '__main__':
    unittest.main()
