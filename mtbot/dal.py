# -*- coding: utf-8 -*-
import logging
import sqlite3


class DAL(object):
    """
    Temporary data access layer implementation based on direct sqlite access.
    TODO(askalyuk): to be removed/refactored.
    """
    def __init__(self):
        super(DAL, self).__init__()
        self.log = logging.getLogger(__name__)
        self.log.debug("Connect to database")
        self.conn = sqlite3.connect('mtbot.db')

    def create_or_update_user(email):
        pass
