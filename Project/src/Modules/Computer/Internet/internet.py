"""
@Name:      Modules/Computer/Internet/internet.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2012-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 20, 2012
@summary:   This module determines the IP address of the ISP connection.


All nodes currently run this.  This is overkill!
We need a way to have only one of the nodes run this and if successful, block the other nodes from running.

Get the Internet address and make reports available for web interface.

Since PyHouse is always running (as a daemon) this module will get the IP-v4 address that is
assigned to our router by the ISP.
It will then take that IP address and update our Dynamic DNS provider(s) so we may browse to that
address from some external device and check on the status of the house.
"""

__updated__ = '2019-10-08'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Computer.Internet.internet_xml import Api as internetApi
from Modules.Computer.Internet.inet_find_external_ip import Api as findApi
from Modules.Computer.Internet.inet_update_dyn_dns import Api as updateApi
from Modules.Core import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Internet       ')
INITIAL_DELAY = 5
REPEAT_DELAY = 2 * 60 * 60


class lightingUtility(object):
    """
    """

    @staticmethod
    def _internet_loop(p_pyhouse_obj):
        # Api.FindExternalIp(p_pyhouse_obj)
        # Api.UpdateDynDnsSites(p_pyhouse_obj)
        p_pyhouse_obj._Twisted.Reactor.callLater(REPEAT_DELAY, lightingUtility._internet_loop, p_pyhouse_obj)

    @staticmethod
    def _read_xml_configuration(p_pyhouse_obj):
        l_config = internetApi().read_internet_xml(p_pyhouse_obj)
        p_pyhouse_obj.Computer.InternetConnection = l_config
        return l_config


class Api:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadConfig(self):
        lightingUtility._read_xml_configuration(self.m_pyhouse_obj)
        LOG.info('Loaded Internet Config')

    def Start(self):
        """
        Start async operation of the Internet module.
        """
        self.m_pyhouse_obj._Twisted.Reactor.callLater(INITIAL_DELAY, lightingUtility._internet_loop, self.m_pyhouse_obj)
        LOG.info("Started Internet.")

    def SaveConfig(self):
        internetApi().write_internet_xml(self.m_pyhouse_obj)
        LOG.info('Saved Internet Config')

    def Stop(self):
        """
        Stop async operations.
        """
        LOG.info("Stopped.")

    @staticmethod
    def FindExternalIp(p_pyhouse_obj):
        """
        Async find our external IP address
        """

        def cb_find_external_ip(p_ip):
            LOG.info('Found External IP - {}'.format(p_ip))

        def eb_find_external_ip(p_reason):
            LOG.error('ERROR - No IP found - Reason: {}'.format(p_reason))

        LOG.info('Start')
        l_defer = findApi().FindExternalIP(p_pyhouse_obj)
        l_defer.addCallback(cb_find_external_ip)
        l_defer.addErrback(eb_find_external_ip)
        return l_defer

    @staticmethod
    def UpdateDynDnsSites(p_pyhouse_obj):
        """
        """

        def cb_done_updating(p_ip):
            LOG.info('Updated all to IP: {}'.format(p_ip))

        def eb_error(p_reason):
            LOG.error('ERROR - No DynDns sites found - Reason: {}'.format(p_reason))

        LOG.info('Start')
        l_defer = updateApi().UpdateAllDynDns(p_pyhouse_obj)
        l_defer.addCallback(cb_done_updating)
        l_defer.addErrback(eb_error)
        return l_defer

#  ## END DBK
