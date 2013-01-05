import unittest
from gtalkbot_test import GtalkBotTest
from mtbot.gtalkbot import GTalkBot


class TestBot(GtalkBotTest):

    def test_session_start(self):
        """session_start handler test."""
        self.memorize_stream_start()
        self.xmpp.event("session_start")
        self.send(self.xmpp.make_presence(pstatus=GTalkBot.PRESENSE_STATUS))

    def tearDown(self):
        self.stream_close()

if __name__ == '__main__':
    unittest.main()
