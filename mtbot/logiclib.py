# -*- coding: utf-8 -*-
import logging
import random
from datetime import datetime, timedelta
from mtbot import dal, settings


class UserStatus:
    WAIT = 0  # bot should wait for answer from user
    SEND = 1  # bot should send message according to logic (e.g. next question)
    ERROR = 2  # error during processing


class LogicLib(object):
    """Library, which implements bot's 'brain'.
    It tracks users and makes decision what to ask and how to reply."""
    def __init__(self):
        super(LogicLib, self).__init__()
        self.log = logging.getLogger(__name__)
        self.data = dal.DAL()
        self._send_message = None

    def refresh_contact_list(self, contact_list):
        """
        Sync bot's contact list with server's one.
        If user is in bot's contact list, the bot should start to "teach"
        him/her (add to user's list).
        """
        for jid in contact_list:
            self.data.create_or_update_user(jid)

    def process_income_message(self, jid, msg):
        user = self.data.get_user(jid)
        if not user:  # ignore unknown user
            self.log.info(
                'Income message from unknown user %s: %s' % (jid, msg))
            return None
        self.log.info('Income message from %s: %s' % (jid, msg))
        self.data.update_user(user[0], UserStatus.SEND,
            datetime.now() + timedelta(
                seconds=settings.NEXT_MESSAGE_PERIOD_SECONDS))
        return ('Thanks! Will send you something in %s seconds' %
            settings.NEXT_MESSAGE_PERIOD_SECONDS)

    def set_send_message_handler(self, handler):
        self._send_message = handler

    def process_users(self):
        """
        Read all users and process next action (e.g. send message)
        for each one if required. To be called on regular basis
        (e.g. each 60 seconds).
        """
        if not self._send_message:
            raise ValueError('Send message handler is required')
        users = self.data.get_users_for_check(datetime.now())
        self.log.debug('%s users to process' % len(users))
        for user in users:
            try:
                self._process_user(user)
            except Exception as e:
                self.log.error('Error in processing user jid = %s: %s'
                    % (user[1], e))
                self.data.update_user(user[0], UserStatus.ERROR, None)
                raise

    def _process_user(self, user):
        jid = user[1]
        self.log.debug('Process user %s' % jid)
        if user[2] == UserStatus.SEND:
            self._send_message(jid, self._get_next_message(jid))
            self.data.update_user(user[0], UserStatus.WAIT, None)

    def _get_next_message(self, jid):
        return random.choice(['hi', 'hello', 'test'])
