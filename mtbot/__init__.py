# -*- coding: utf-8 -*-
from mtbot import gtalkbot, logiclib, settings


def start(jid, password):
    # Setup the GtalkBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    logic = logiclib.LogicLib()
    bot = gtalkbot.GTalkBot(jid, password, logic)

    # Process users each 60 seconds using build-in SleekXMPP scheduler
    bot.scheduler.add("mtbot_action", settings.PROCESS_USERS_PERIOD_SECONDS,
        logic.process_users, repeat=True)

    # If you are working with an OpenFire server, you may need
    # to adjust the SSL version used:
    # xmpp.ssl_version = ssl.PROTOCOL_SSLv3

    # If you want to verify the SSL certificates offered by a server:
    # xmpp.ca_certs = "path/to/ca/cert"

    # Connect to the XMPP server and start processing XMPP stanzas.
    if bot.connect(('talk.google.com', 5222)):
        bot.process(block=True)
    else:
        raise IOError("Unable to connect to Gtalk server.")
