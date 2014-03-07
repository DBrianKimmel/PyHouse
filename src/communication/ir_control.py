"""
ir_control.py

Created on Jan 26, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: Lirc connection.

Allow various IR receivers to collect signals from various IR remotes.

Connect to the LIRC daemon socket and listen to everything coming down that path.
Connect to the PyHouse node cluster port and pass all the IR codes on.

"""

# Import system type stuff
import logging

from twisted.application.internet import StreamServerEndpointService
from twisted.application.service import Application
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint, clientFromString
from twisted.protocols.amp import AMP

from src.entertain import pandora

g_debug = 1
g_logger = logging.getLogger('PyHouse.IrControl   ')


LIRC_SOCKET = 'unix:path=/var/run/lirc/lircd'

IR_KEYS = [
           ('KEY_BD', 'pandora', 'stop'),
           ('KEY_DVD', 'pandora', 'stop'),
           ('KEY_DVR', 'pandora', 'start'),
           ('KEY_HDMI', 'pandora', 'stop'),
           ('KEY_TV', 'pandora', 'stop'),
           ('KEY_CD', 'pandora', 'stop'),

           ('KEY_VOLUMEUP', 'pandora', 'volup'),
           ('KEY_VOLUMEDOWN', 'pandora', 'voldown'),
           ('KEY_MUTE', 'pandora', 'mute'),
           ]

class LircProtocol(Protocol):
    """
    """

    def dataReceived(self, p_data):
        l_data = p_data.rstrip('\r\n')
        IrDispatch(l_data)


class LircClientFactory(ClientFactory):

    def startedConnecting(self, p_connector):
        print "LircClientFactory - Started to connect."

    def buildProtocol(self, addr):
        # print "LircClientFactory - connected"
        return LircProtocol()


class LircConnection(object):

    def __init__(self):
        l_endpoint = clientFromString(reactor, LIRC_SOCKET)
        l_factory = LircFactory()
        l_endpoint.connect(l_factory)
        if g_debug >= 1:
            g_logger.debug("LircConnection Open")


class LircFactory(Factory):

    def startedConnecting(self, p_connector):
        print "LircFactory - Started to connect."

    def buildProtocol(self, addr):
        print "LircFactory - connected"
        return LircProtocol()

    def clientConnectionLost(self, connector, p_reason):
        print 'LircFactory - lost connection ', p_reason

    def clientConnectionFailed(self, connector, p_reason):
        print 'LircFactory - Connection failed ', p_reason


class IrDispatch(object):
    """
    """
    def __init__(self, p_data):
        (l_keycode, l_repeatcnt, l_keyname, l_remote) = p_data.split()
        # print 'IrDispatch data =', l_keycode, l_repeatcnt, l_keyname, l_remote
        if l_repeatcnt == '00':
            if g_debug >= 1:
                g_logger.debug("Received {0:}".format(p_data))
            for tpl in IR_KEYS:
                if l_keyname == tpl[0]:
                    if tpl[1] == 'pandora':
                        # print "found a pandora key", tpl[0], tpl[2]
                        self.pandor_ctl(p_data, tpl)
                    pass

    def pandor_ctl(self, p_data, p_tpl):
        print "Pandora ctl ", p_data, p_tpl
        (_l_keyname, _l_pandora, l_command) = p_tpl
        if l_command == 'start':
            self.m_pandora = pandora.API()
            self.m_pandora.Start(None)
        elif l_command == 'stop':
            self.m_pandora.Stop()


class API(object):

    def __init__(self):
        """Connect to the Lirc procees.
        """
        _x = LircConnection()
        # print "ir_control.API()"

    def Start(self, _p_pyhouses_obj):
        print 'ir_control.API.Start()'
        l_application = Application('IR Control Server')
        l_endpoint = TCP4ServerEndpoint
        l_factory = Factory()
        l_factory.protocol = AMP
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        l_service.setServiceParent(l_application)

    def Stop(self):
        pass

# ## END DBK
