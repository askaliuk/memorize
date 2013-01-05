# -*- coding: utf-8 -*-
import logging


class LogicLib(object):
    """Library, which implements bot's 'brain'.
    It tracks users and makes decision what to ask and how to reply."""
    def __init__(self):
        super(LogicLib, self).__init__()
        self.log = logging.getLogger(__name__)

    def refresh_contact_list(self, contact_list):
        pass

    def process_income_message(self, msg):
        pass

    def set_send_message_handler(self, handler):
        pass
