# -*- coding: utf-8 -*-
import logging
from mtbot.dal import DAL


class LogicLib(object):
    """Library, which implements bot's 'brain'.
    It tracks users and makes decision what to ask and how to reply."""
    def __init__(self):
        super(LogicLib, self).__init__()
        self.log = logging.getLogger(__name__)
        self.dal = DAL()

    def refresh_contact_list(self, contact_list):
        # TODO(askalyuk): if user adds bot to friends,
        # it should start to teach him/her
        pass

    def process_income_message(self, msg):
        pass

    def set_send_message_handler(self, handler):
        pass

    def process_users(self):
        """
        Read all users and process next action (e.g. send message)
        for each one if required. To be called on regular basis
        (e.g. each 60 seconds).
        """
        self.log.debug("Process users")
