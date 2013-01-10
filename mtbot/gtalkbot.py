# -*- coding: utf-8 -*-
import sys
import logging
import sleekxmpp

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class GTalkBot(sleekxmpp.ClientXMPP):

    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    PRESENSE_STATUS = "I'm memorize bot"

    def __init__(self, jid, password, logiclib, log_level=logging.DEBUG):
        logging.basicConfig(
            level=log_level,
            format=GTalkBot.logging_format)
        self.log = logging.getLogger(__name__)
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        if not logiclib:
            raise ValueError("logiclib instance is required")
        self.logiclib = logiclib
        # TODO(askalyuk): make send message handler independent
        # from XMPP implementation
        self.logiclib.set_send_message_handler(
            lambda jid, body: self._send_message(jid, body))

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.income_message)

    def start(self, event):
        """
        Process the session_start event.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence(pstatus=GTalkBot.PRESENSE_STATUS)
        self.log.info("Retrieve contact list")
        self.get_roster()
        self.log.info("%d contact(s) found." % len(self.client_roster.keys()))
        # TODO(askalyuk): make contact list independent from XMPP
        # implementation
        self.logiclib.refresh_contact_list(self.client_roster)

    def _send_message(self, jid, body):
        self.send_message(jid, body, mtype="chat")

    def income_message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the message's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        # TODO(askalyuk): make income message processor independent
        # from XMPP implementation
        if msg['type'] not in ('chat', 'normal'):
            error_message = 'Error income message: %s' % msg
            self.log.error(error_message)
            raise ValueError(error_message)
        # msg['from'] is JID instance
        bare_jid = msg['from'].bare
        reply = self.logiclib.process_income_message(bare_jid, msg['body'])
        if reply:
            msg.reply(reply).send()
