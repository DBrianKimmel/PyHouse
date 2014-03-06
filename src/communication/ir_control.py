"""
Created on Jan 26, 2014

Name: ir_control.py
@author: briank

Lirc connection.

Allow various IR receivers to collect signals from various IR remotes.

"""

# Import system type stuff
import logging

from twisted.application.internet import StreamServerEndpointService
from twisted.application.service import Application
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint, UNIXClientEndpoint
from twisted.protocols.amp import AMP


g_debug = 0
g_logger = logging.getLogger('PyHouse.CoreSetup   ')


LIRC_SOCKET = 'unix:path=/var/run/lirc/lircd'

class LircProtocol(Protocol):
    """
    """

    def dataReceived(self, p_data):
        print p_data


class LircFactory(Factory):
    def buildProtocol(self, addr):
        return LircProtocol()


class IrDispatch(object):
    """
    """

class API(object):

    def __init__(self):
        l_endpoint = UNIXClientEndpoint(LIRC_SOCKET, reactor)

    def Start(self, _p_pyhouses_obj):
        l_application = Application('IR Control Server')
        l_endpoint = TCP4ServerEndpoint
        l_factory = Factory()
        l_factory.protocol = AMP
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        l_service.setServiceParent(l_application)

    def Stop(self):
        pass

# ## END DBK
