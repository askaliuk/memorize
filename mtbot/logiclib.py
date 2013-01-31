# -*- coding: utf-8 -*-
import logging
import random
from datetime import datetime, timedelta
from mtbot import settings
from mtdata import BotUser, UserStatus, Deck, Card, DeckCategory


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
        reply = None
        if bot_user.active_card:
            if self._is_correct_answer(msg, bot_user.active_card):
                reply = ("Correct! I will ask next question in %s seconds" %
                    settings.NEXT_MESSAGE_PERIOD_SECONDS)
            else:
                return "I'm afraid, you are wrong. Try again."
        else:
            reply = "Hello. Your next question has been scheduled."
        # schedule next question action
        bot_user.status = UserStatus.SEND
        bot_user.next_check = datetime.now() + timedelta(
                seconds=settings.NEXT_MESSAGE_PERIOD_SECONDS)
        bot_user.save()
        return reply

    def _is_correct_answer(self, msg, card):
        if card.deck.category == DeckCategory.WORD_SET_TRANSLATION:
            words = card.answer.split(',')
            for word in words:
                if word.lower() == msg.lower():
                    return True
            return False
        else:
            raise NotImplemented

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
                    % (user.jid, e))
                user.status = UserStatus.ERROR
                user.next_check = None
                user.active_card = None
                user.save()
                raise

    def _process_user(self, bot_user):
        self.log.debug('Process bot user %s' % bot_user.jid)
        if bot_user.status == UserStatus.SEND:
            self._send_message(bot_user.jid, self._get_next_message(bot_user))
            bot_user.status = UserStatus.WAIT
            bot_user.next_check = None
            bot_user.save()

    def _get_next_message(self, bot_user):
        answers = []
        active_deck = None
        active_card = None
        if Deck.objects.count() == 0:
            active_deck = Deck(bot_user=bot_user, name="First deck")
            active_deck.save()
            answers.append(
                "You don't have any decks. I've created first one for you.")
        else:
            # select random deck
            active_deck = Deck.objects.order_by('?')[0]
        if Card.objects.filter(deck=active_deck).count() == 0:
            active_card = Card(deck=active_deck, question="hello",
                answer="hello")
            active_card.save()
            answers.append(
                "Deck '%s' is empty. I've filled it with test data." %
                active_deck.name)
        else:
            # select random card
            active_card = Card.objects.filter(deck=active_deck).order_by('?')[0]
        bot_user.active_card = active_card
        bot_user.save()
        question = self._build_question(active_card)
        if answers:
            return " ".join(answers + question)
        return question

    def _build_question(self, card):
        if card.deck.category == DeckCategory.WORD_SET_TRANSLATION:
            words = card.question.split(',')
            return "Translate word '%s'" % random.choice(words)
        else:
            raise NotImplemented
