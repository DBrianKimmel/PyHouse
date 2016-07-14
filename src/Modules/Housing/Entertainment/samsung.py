"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Entertainment/samsung.py -*-

@name:      src.Modules.Entertainment.samsung
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@note:      Created on Jul 11, 2016
@license:   MIT License
@summary:


"""

__updated__ = '2016-07-14'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import error

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.onkyo import API as onkyoApi
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Samsung        ')

PORT = 55000


class OnkyoProtocol(Protocol):
    """
    """

    def dataReceived(self, data):
        Protocol.dataReceived(self, data)

    def connectionMade(self):
        Protocol.connectionMade(self)

    def connectionLost(self, reason=error.ConnectionDone):
        Protocol.connectionLost(self, reason=reason)


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


class API(object):
    def __init__(self, p_pyhouse_obj):
        LOG.info("Initializing.")
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        LOG.info('XML Loading')
        LOG.info('XML Loaded')

    def Start(self):
        LOG.info("Starting.")
        LOG.info("Started.")

    def SaveXml(self, p_xml):
        LOG.info("Saving XML.")
        l_xml = ET.Element('EntertainmentSection')
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopping.")
        LOG.info("Stopped.")

# ## END DBK
