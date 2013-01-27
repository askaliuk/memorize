import unittest
from gtalkbot_test import GtalkBotTest


class TestSimple(GtalkBotTest):

    def test_simple(self):
        """Basic simple test which interacts with a mocked GTalkBot instance."""
        def echo(jid, msg):
            return 'Thanks for sending: %s' % msg
        self.mock_logiclib_method('process_income_message', echo)

        self.memorize_stream_start()

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
