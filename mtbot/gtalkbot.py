# -*- coding: utf-8 -*-
import sys
import logging
import sleekxmpp
import logiclib

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

    def __init__(self, jid, password, log_level=logging.DEBUG):
        logging.basicConfig(
            level=log_level,
            format=GTalkBot.logging_format)
        self.log = logging.getLogger(__name__)
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.logiclib = logiclib.LogicLib()
        # TODO(askalyuk): make send message handler independent
        # from XMPP implementation
        self.logiclib.set_send_message_handler(self.send_message)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)

    def start(self, event):
        """
        Process the session_start event.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence(pstatus=GTalkBot.PRESENSE_STATUS)
        # TODO(askalyuk): temporary for testing
        return
        self.log.info("Retrieve contact list")
        self.get_roster()
        self.log.info("%d contact(s) found." % len(self.client_roster.keys()))
        # TODO(askalyuk): make contact list independent from XMPP
        # implementation
        self.logiclib.refresh_contact_list(self.client_roster)

    # def send_messages(self):
    #     """
    #     Ask logic library about new messages for each contact and
    #     send them.
    #     """
    #     for contact in self.client_roster.keys():
    #         self.send_message(contact,
    #             "Hello, i'm bot. Will ask you questions.", mtype="chat")

    # def _send_new_question(self):
    #     new_q = eng.get_new_question()
    #     new_msg = self.make_message(self.first_contact, new_q, mtype="chat")
    #     new_msg.send()
    #     self.timer_on = False

    def message(self, msg):
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
        self.logiclib.process_income_message(msg)
        # if msg['type'] not in ('chat', 'normal'):
        #     return
        # (status, rpl) = eng.reply(msg['body'])
        # if status:
        #     if not self.timer_on:
        #         minutes = 10
        #         msg.reply(rpl + ' I will ask next question in %s minutes' % minutes).send()
        #         k = lambda: self._send_new_question()
        #         t = threading.Timer(60 * minutes, k)
        #         self.timer_on = True
        #         t.start()
        #     else:
        #         msg.reply(rpl + ' Wait for next question.').send()
        # else:
        #     if self.timer_on:
        #         msg.reply('Wait for next question.').send()
        #     else:
        #         msg.reply(rpl).send()
