from django.db import models
import logging

log = logging.getLogger(__name__)


class UserStatus:
    WAIT = 0  # bot should wait for answer from user
    SEND = 1  # bot should send message according to logic (e.g. next question)
    ERROR = 2  # error during processing


class BotUserManager(models.Manager):
    def create_or_update(self, jid):
        log.debug('Create or update BotUser jid = %s' % jid)
        bot_user, created = self.get_or_create(jid=jid)
        # TODO(askalyuk): update what?
        return bot_user

    def get_unprocessed(self, now):
        return self.exclude(status=UserStatus.WAIT).filter(
            next_check__lte=now, next_check__isnull=False)


class BotUser(models.Model):
    STATUS_CHOICES = (
        (UserStatus.WAIT, 'Wait'),
        (UserStatus.SEND, 'Send'),
        (UserStatus.ERROR, 'Error'),
    )
    jid = models.CharField(unique=True, max_length=50)
    status = models.IntegerField(choices=STATUS_CHOICES,
        default=UserStatus.WAIT)
    next_check = models.DateTimeField(null=True)

    objects = BotUserManager()

    class Meta:
        db_table = 'mtdata_botuser'

    def __unicode__(self):
        return u'%s' % (self.jid)

    def __str__(self):
        return '%s' % (self.jid)

