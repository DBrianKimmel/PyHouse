"""
-*- test-case-name: PyHouse/src/Modules/Entertainment/test_onkyo.py -*-

@name:      PyHouse/src/Modules/Entertainment/onkyo.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c)2016-2016 by D. Brian Kimmel
@note:      Created on Jul 9, 2016
@license:   MIT License
@summary:

"""
from twisted.internet.error import ConnectionDone

__updated__ = '2016-07-14'

#  Import system type stuff
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import error
# import eiscp

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Onkyo          ')



DEFAULT_EISCP_PORT = 60128


class OnkyoData(object):
    def __init__(self):
        self.DeviceCount = 0
        self.Factory = None


class OnkyoProtocol(Protocol):
    """
    """

    def dataReceived(self, data):
        Protocol.dataReceived(self, data)

    def connectionMade(self):
        Protocol.connectionMade(self)

    def connectionLost(self, reason=ConnectionDone):
        Protocol.connectionLost(self, reason=reason)


class OnkyoClient(OnkyoProtocol):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj


class OnkyoFactory(ReconnectingClientFactory):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def startedConnecting(self, p_connector):
        # ReconnectingClientFactory.startedConnecting(self, p_connector)
        LOG.info('Started to connect. {}'.format(p_connector))

    def buildProtocol(self, p_addr):
        LOG.info('BuildProtocol')
        return ReconnectingClientFactory.buildProtocol(self, p_addr)

    def clientConnectionLost(self, p_connector, p_reason):
        LOG.warn('Lost connection.\n\tReason:{}'.format(p_reason))
        ReconnectingClientFactory.clientConnectionLost(self, p_connector, p_reason)

    def clientConnectionFailed(self, p_connector, p_reason):
        LOG.error('Connection failed.\n\tReason:{}'.format(p_reason))
        ReconnectingClientFactory.clientConnectionFailed(self, p_connector, p_reason)

    def connectionLost(self, p_reason):
        """ This is required. """
        LOG.error('ConnectionLost.\n\tReason: {}'.format(p_reason))

    def makeConnection(self, p_transport):
        """ This is required. """
        LOG.warn('makeConnection - Transport: {}'.format(p_transport))


class Util(object):
    """
    """

    def start_factory(self):
        pass


class API(object):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized")

    def LoadXml(self, p_pyhouse_obj):
        """ Start the onkyo factory See if we have any Onkyo devices.
        """
        LOG.info("Loading XML")
        l_onkyo_obj = OnkyoData()
        l_onkyo_obj.Factory = OnkyoFactory(p_pyhouse_obj)
        LOG.info("Loaded XML")
        return l_onkyo_obj

    def Start(self):
        """
        if self.m_pyhouse_obj.Computer.Mqtt.Brokers != {}:
            LOG.info('Connecting to all MQTT Brokers.')
            l_count = self.connect_to_all_brokers(self.m_pyhouse_obj)
            LOG.info("Mqtt {} broker(s) Started.".format(l_count))
        else:
            LOG.info('No Mqtt brokers are configured.')
        """
        pass

    def SaveXml(self, p_xml):
        l_xml = ''
        # p_xml.append(l_xml)
        LOG.info("Saved Mqtt XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
