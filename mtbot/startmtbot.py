#!/usr/bin python
# -*- coding: utf-8 -*-
import mtbot
import getpass
from optparse import OptionParser

if __name__ == "__main__":
    # Setup the command line arguments.
    optp = OptionParser()

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    opts, args = optp.parse_args()

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")
    mtbot.start(opts.jid, opts.password)
