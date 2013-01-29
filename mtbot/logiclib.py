# -*- coding: utf-8 -*-
import logging
import random
from datetime import datetime, timedelta
from mtbot import settings
from mtdata import BotUser, UserStatus


class LogicLib(object):
    """Library, which implements bot's 'brain'.
    It tracks users and makes decision what to ask and how to reply."""
    def __init__(self):
        super(LogicLib, self).__init__()
        self.log = logging.getLogger(__name__)
        self._send_message = None

    def refresh_contact_list(self, contact_list):
        """
        Sync bot's contact list with server's one.
        If user is in bot's contact list, the bot should start to "teach"
        him/her (add to user's list).
        """
        for jid in contact_list:
            BotUser.objects.create_or_update(jid)

    def process_income_message(self, jid, msg):
        bot_user = None
        try:
            bot_user = BotUser.objects.get(jid=jid)
        except BotUser.DoesNotExist:
            self.log.info(
                'Income message from unknown user %s: %s' % (jid, msg))
            return None
        self.log.info('Income message from %s: %s' % (jid, msg))
        bot_user.status = UserStatus.SEND
        bot_user.next_check = datetime.now() + timedelta(
                seconds=settings.NEXT_MESSAGE_PERIOD_SECONDS)
        bot_user.save()
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
        users = BotUser.objects.get_unprocessed(datetime.now())
        self.log.debug('%s users to process' % len(users))
        for user in users:
            try:
                self._process_user(user)
            except Exception as e:
                self.log.error('Error in processing user jid = %s: %s'
                    % (user[1], e))
                user.status = UserStatus.ERROR
                user.next_check = None
                user.save()
                raise

    def _process_user(self, user):
        self.log.debug('Process user %s' % user.jid)
        if user.status == UserStatus.SEND:
            self._send_message(user.jid, self._get_next_message(user.jid))
            user.status = UserStatus.WAIT
            user.next_check = None
            user.save()

    def _get_next_message(self, jid):
        return random.choice(['hi', 'hello', 'test'])
