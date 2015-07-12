"""
-*- test-case-name: PyHouse.src.Modules.communication.test.test_ir_control -*-

@name:      PyHouse/src/Modules/communication/ir_control.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on Jan 26, 2014
@license:   MIT License
@summary:   Provides PyHouse IR service via a Lirc connection.

Allow various IR receivers to collect signals from various IR remotes.
IR Receivers may be on nodes or on sensors.  All funnel thru MQTT to get dispatched.

Connect to the LIRC daemon socket and listen to everything coming down that path.
Connect to the PyHouse node cluster port and pass all the IR codes on.

Use irrecord to use

Remote  |  Raw    |  App    |  App    |  Key    |
Name    |  Code   |  Name   |  Action |  Name   |

"""

# Import system type stuff
from twisted.application.internet import StreamServerEndpointService
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint, clientFromString
from twisted.protocols.amp import AMP

# Import PyMh files and modules.
from Modules.Entertainment import pandora
from Modules.Computer import logging_pyh as Logger


g_debug = 1
LOG = Logger.getLogger('PyHouse.IrControl   ')

g_pandora = None
g_pyhouse_obj = None


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
    """
    Protocol for listening to the lirc socket.

    We get one line of data here (with lots of repeats) for every key pressed on the remote.

    KeyCode_________ Rp KeyName_______ Remote_________
    00000000a55ad02f 00 KEY_VOLUMEDOWN pioneer-AXD7595
    """

    def dataReceived(self, p_data):
        l_data = p_data.rstrip('\r\n')
        (l_keycode, l_repeatcnt, l_keyname, l_remote) = l_data.split()
        if l_repeatcnt == '00':
            IrDispatch(l_keycode, l_keyname, l_remote)


class LircFactory(Factory):
    """Factory to build instances of LircProtocol
    """

    def buildProtocol(self, _addr):
        # "LircFactory - connected"
        return LircProtocol()

    def clientConnectionLost(self, _connector, p_reason):
        LOG.error('LircFactory - lost connection {0:}'.format(p_reason))

    def clientConnectionFailed(self, _connector, p_reason):
        LOG.error('LircFactory - Connection failed {0:}'.format(p_reason))


class LircConnection(object):
    """
    Connect to the LIRC socket.
    """

    def start_lirc_connect(self, p_pyhouse_obj):

        def cb_connect(p_reason):
            LOG.debug("LircConnection good {0:}".format(p_reason))

        def eb_connect(p_reason):
            LOG.error("LircConnection Error {0:}".format(p_reason))

        l_endpoint = clientFromString(p_pyhouse_obj.Twisted.Reactor, LIRC_SOCKET)
        l_factory = LircFactory()
        l_defer = l_endpoint.connect(l_factory)
        l_defer.addCallback(cb_connect)
        l_defer.addErrback(eb_connect)


class IrDispatch(object):
    """
    """

    def __init__(self, p_keycode, p_keyname, p_remote):
        """
        KeyCode_________ KeyName_______ Remote_________
        00000000a55ad02f KEY_VOLUMEDOWN pioneer-AXD7595
        """
        if g_debug >= 1:
            LOG.debug("Received {0:} ({1:}) from {2:}".format(p_keycode, p_keyname, p_remote))
        for l_dispatch in IR_KEYS:
            (l_keyname, l_module, l_command) = l_dispatch
            if p_keyname == l_keyname:
                if l_module == 'pandora':
                    self.pandora_ctl(l_command)
                pass

    def pandora_ctl(self, p_command):
        LOG.debug('Pandora_ctl command - {0:}'.format(p_command))
        if p_command == 'start':
            g_pandora.Start(g_pyhouse_obj)
        elif p_command == 'stop':
            g_pandora.Stop()


class Utility(LircConnection):

    def start_AMP(self, p_pyhouse_obj):
        l_endpoint = TCP4ServerEndpoint
        l_factory = Factory()
        l_factory.protocol = AMP
        p_pyhouse_obj.Services.IrControlService = StreamServerEndpointService(l_endpoint, l_factory)
        p_pyhouse_obj.Services.IrControlService.setName('IrControl')
        p_pyhouse_obj.Services.IrControlService.setServiceParent(p_pyhouse_obj.Twisted.Application)


class API(Utility):

    def __init__(self):
        """Connect to the Lirc procees.
        """
        global g_pandora
        g_pandora = pandora.API()
        LOG.debug('Initialized')

    def Start(self, p_pyhouse_obj):
        global g_pyhouse_obj
        g_pyhouse_obj = p_pyhouse_obj
        self.start_lirc_connect(p_pyhouse_obj)
        self.start_AMP(p_pyhouse_obj)
        LOG.debug('Started')

    def Stop(self):
        LOG.debug('Stopped')

# ## END DBK
