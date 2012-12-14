import unittest
from mtbot.gtalkbot import GTalkBot


class GtalkBotTest(unittest.TestCase):

    def start_bot(self, skip=True, header=None, socket='mock',
                  jid='tester@localhost', password='test', server='localhost',
                  port=5222, sasl_mech=None, plugins=None, plugin_config={}):
        self.xmpp = GTalkBot(jid, password,
                             sasl_mech=sasl_mech,
                             plugin_config=plugin_config)

        # We will use this to wait for the session_start event
        # for live connections.
        skip_queue = Queue()

        if socket == 'mock':
            self.xmpp.set_socket(TestSocket())

            # Simulate connecting for mock sockets.
            self.xmpp.auto_reconnect = False
            self.xmpp.state._set_state('connected')

            # Must have the stream header ready for xmpp.process() to work.
            if not header:
                header = self.xmpp.stream_header
            self.xmpp.socket.recv_data(header)
        elif socket == 'live':
            self.xmpp.socket_class = TestLiveSocket

            def wait_for_session(x):
                self.xmpp.socket.clear()
                skip_queue.put('started')

            self.xmpp.add_event_handler('session_start', wait_for_session)
            if server is not None:
                self.xmpp.connect((server, port))
            else:
                self.xmpp.connect()
        else:
            raise ValueError("Unknown socket type.")

        if plugins is None:
            self.xmpp.register_plugins()
        else:
            for plugin in plugins:
                self.xmpp.register_plugin(plugin)

        # Some plugins require messages to have ID values. Set
        # this to True in tests related to those plugins.
        self.xmpp.use_message_ids = False

        self.xmpp.process(threaded=True)
        if skip:
            if socket != 'live':
                # Mark send queue as usable
                self.xmpp.session_started_event.set()
                # Clear startup stanzas
                self.xmpp.socket.next_sent(timeout=1)
            else:
                skip_queue.get(block=True, timeout=10)

if __name__ == '__main__':
    unittest.main()
