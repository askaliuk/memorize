import unittest
from sleekxmpp.test import SleekTest
from mtbot.gtalkbot import GTalkBot


class TestSimple(SleekTest):

    def test_simple(self):
        """Test that we can interact with a mock GTalkBot instance."""
        pass

    def tearDown(self):
        self.stream_close()

if __name__ == '__main__':
    unittest.main()
