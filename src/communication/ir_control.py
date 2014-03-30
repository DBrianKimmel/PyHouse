"""
ir_control.py

Created on Jan 26, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: Provides PyHouse IR service via a Lirc connection.

Allow various IR receivers to collect signals from various IR remotes.

Connect to the LIRC daemon socket and listen to everything coming down that path.
Connect to the PyHouse node cluster port and pass all the IR codes on.

"""

# Import system type stuff
import logging

from twisted.application.internet import StreamServerEndpointService
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint, clientFromString
from twisted.protocols.amp import AMP

from src.entertain import pandora

g_debug = 1
g_logger = logging.getLogger('PyHouse.IrControl   ')

g_pandora = None


LIRC_SOCKET = 'unix:path=/var/run/lirc/lircd'

# KeyName, ModuleName, Action
IR_KEYS = [
           ('KEY_BD'        , 'pandora', 'stop'),
           ('KEY_DVD'       , 'pandora', 'stop'),
           ('KEY_DVR'       , 'pandora', 'start'),
           ('KEY_HDMI'      , 'pandora', 'stop'),
           ('KEY_TV'        , 'pandora', 'stop'),
           ('KEY_CD'        , 'pandora', 'stop'),

           ('KEY_VOLUMEUP'  , 'pandora', 'volup'),
           ('KEY_VOLUMEDOWN', 'pandora', 'voldown'),
           ('KEY_MUTE'      , 'pandora', 'mute'),
           ]

class LircProtocol(Protocol):
    """Protocol for listening to the lirc socket.

    We get one line of data here (lots of repeats) for every key pressed on the remote.

    KeyCode_________ Rp KeyName_______ Remote_________
    00000000a55ad02f 00 KEY_VOLUMEDOWN pioneer-AXD7595
    """

    def dataReceived(self, p_data):
        l_data = p_data.rstrip('\r\n')
        (l_keycode, l_repeatcnt, l_keyname, l_remote) = l_data.split()
        if l_repeatcnt == '00':
            IrDispatch(l_keycode, l_keyname, l_remote)


class LircFactory(Factory):

    def buildProtocol(self, _addr):
        # "LircFactory - connected"
        return LircProtocol()

    def clientConnectionLost(self, _connector, p_reason):
        g_logger.error('LircFactory - lost connection {0:}'.format(p_reason))

    def clientConnectionFailed(self, _connector, p_reason):
        g_logger.error('LircFactory - Connection failed {0:}'.format(p_reason))


class LircConnection(object):

    def __init__(self, p_pyhouses_obj):
        def cb_connect(self, p_reason):
            g_logger.debug("LircConnection good {0:}".format(p_reason))

        def eb_connect(self, p_reason):
            g_logger.error("LircConnection Error {0:}".format(p_reason))

        l_endpoint = clientFromString(p_pyhouses_obj.Reactor, LIRC_SOCKET)
        l_factory = LircFactory()
        l_defer = l_endpoint.connect(l_factory)
        l_defer.addCallback(self.cb_connect)
        l_defer.addErrback(self.eb_connect)


class IrDispatch(object):
    """
    """

    def __init__(self, p_keycode, p_keyname, p_remote):
        """
        KeyCode_________ KeyName_______ Remote_________
        00000000a55ad02f KEY_VOLUMEDOWN pioneer-AXD7595
        """
        if g_debug >= 1:
            g_logger.debug("Received {0:} ({1:}) from {2:}".format(p_keycode, p_keyname, p_remote))
        for l_dispatch in IR_KEYS:
            (l_keyname, l_module, l_command) = l_dispatch
            if p_keyname == l_keyname:
                if l_module == 'pandora':
                    self.pandora_ctl(l_command)
                pass

    def pandora_ctl(self, p_command):
        if p_command == 'start':
            g_pandora.Start(None)
        elif p_command == 'stop':
            g_pandora.Stop()


class Utility(object):

    def start_AMP(self, p_pyhouses_obj):
        l_endpoint = TCP4ServerEndpoint
        l_factory = Factory()
        l_factory.protocol = AMP
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        l_service.setServiceParent(p_pyhouses_obj.Application)

class API(Utility):

    def __init__(self):
        """Connect to the Lirc procees.
        """
        global g_pandora
        g_pandora = pandora.API()

    def Start(self, p_pyhouses_obj):
        _x = LircConnection(p_pyhouses_obj)
        self.start_AMP(p_pyhouses_obj)

    def Stop(self):
        pass

# ## END DBK
