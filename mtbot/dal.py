# -*- coding: utf-8 -*-
import logging
import sqlite3


class Cursor(object):
    def __init__(self, log):
        super(Cursor, self).__init__()
        self.log = log

    def __enter__(self):
        self.conn = sqlite3.connect('mtbot.db')
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        if value:
            self.log.error(value)
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


class DAL(object):
    """
    Temporary prototype of data access layer implementation based on direct
    sqlite access. TODO(askalyuk): to be removed/refactored.
    """
    def __init__(self):
        super(DAL, self).__init__()
        self.log = logging.getLogger(__name__)

    def create_or_update_user(self, jid):
        self.log.debug('Create or update user jid = %s' % jid)
        with Cursor(self.log) as cursor:
            cursor.execute('INSERT OR IGNORE INTO user (jid) VALUES (?)',
                [jid])

    def get_users_for_check(self):
        self.log.debug('Get users for check')
        with Cursor(self.log) as cursor:
            cursor.execute(
                "SELECT * FROM user WHERE status <> 0 and " +
                "next_check <= date('now') and next_check is not null")
            return cursor.fetchall()

    def update_user(self, user_id, status, next_check):
        self.log.debug('Update user id = %s, status = %s, next_check = %s' %
            (user_id, status, next_check))
        with Cursor(self.log) as cursor:
            cursor.execute(
                "UPDATE user SET status = ?, next_check = ? "
                "WHERE id = ? ", [status, next_check, user_id])

    def get_user(self, jid):
        self.log.debug('Get user by jid = %s' % jid)
        with Cursor(self.log) as cursor:
            cursor.execute(
                "SELECT * FROM user WHERE jid = ?", [jid])
            return cursor.fetchone()
