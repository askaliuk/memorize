import time
import unittest
from gtalkbot_test import GtalkBotTest
from mtbot.gtalkbot import GTalkBot


class TestSessionStart(GtalkBotTest):

    def _get_roster_request_mock(self):
        return """
            <iq type="get" id="1">
            <query xmlns="jabber:iq:roster" />
            </iq>
            """

    def _get_roster_response_mock(self):
        return """
            <iq to='tester@localhost' type="result" id="1">
            <query xmlns="jabber:iq:roster">
                <item jid="contact@localhost"
                name="Contact"
                subscription="from"
                ask="subscribe">
                </item>
            </query>
            </iq>
            """

    def test_session_start(self):
        """The session_start event handler test."""
        import logging
        self.memorize_stream_start(log_level=logging.ERROR)
        # trigger session start handler
        self.xmpp.event("session_start")
        # bot should send corrent presense status
        self.send(self.xmpp.make_presence(pstatus=GTalkBot.PRESENSE_STATUS))
        # bot should query roster (contact list)
        self.send(self._get_roster_request_mock())
        # emulate roster response from server
        self.recv(self._get_roster_response_mock())
        # Give the event queue time to process.
        time.sleep(.1)
        # roster should contain 1 contact
        self.assertEqual(1, len(self.xmpp.client_roster.keys()))
        # logiclib should be called to refresh roster
        self.logiclib.refresh_contact_list.assert_called_once_with(
            self.xmpp.client_roster)

    def tearDown(self):
        self.stream_close()

if __name__ == '__main__':
    unittest.main()
