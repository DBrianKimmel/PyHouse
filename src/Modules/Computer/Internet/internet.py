"""
-*- test-case-name: PyHouse.src.Modules.Computer.Internet.test.test_internet -*-

@Name:      PyHouse/src/Modules/Computer/Internet/internet.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2012-2015 by D. Brian Kimmel
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

#  Import system type stuff
#  from twisted.application import service

#  Import PyMh files and modules.
from Modules.Computer.Internet.internet_xml import API as internetAPI
from Modules.Computer.Internet import inet_find_external_ip, inet_update_dyn_dns
from Modules.Computer import logging_pyh as Logger


LOG = Logger.getLogger('PyHouse.Internet       ')
INITIAL_DELAY = 5
REPEAT_DELAY = 2 * 60 * 60



class Utility(object):
    """
    """

    m_pyhouse_obj = None
    m_snarAPI = None
    m_freednsAPI = None


    def _start_internet_discovery(self, _p_pyhouse_obj):
        pass


    def _stop_internet_discovery(self, _p_pyhouse_obj):
        pass


    def _create_internet_discovery_service(self, p_pyhouse_obj):
        """
        Create the twisted service for Internet discovery.
        """
        #  try:
        #    p_pyhouse_obj.Services.InternetDiscoveryService = service.Service()
        #    p_pyhouse_obj.Services.InternetDiscoveryService.setName('NodeDiscovery')
        #    p_pyhouse_obj.Services.InternetDiscoveryService.setServiceParent(p_pyhouse_obj.Twisted.Application)
        #  RuntimeError:  # The service is already installed
        #    LOG.warning('Internet Discovery Service already loaded.')
        self.m_service_installed = True


    def _internet_loop(self, p_pyhouse_obj):
        API.FindExternalIp(p_pyhouse_obj)
        API.UpdateDynDnsSites(p_pyhouse_obj)
        self.m_pyhouse_obj.Twisted.Reactor.callLater(REPEAT_DELAY, self._internet_loop, p_pyhouse_obj)


    def _read_xml_configuration(self, p_pyhouse_obj):
        l_config = internetAPI().read_internet_xml(p_pyhouse_obj)
        p_pyhouse_obj.Computer.InternetConnection = l_config
        return l_config

    def _write_xml_config(self, p_pyhouse_obj):
        l_xml = internetAPI().write_internet_xml(p_pyhouse_obj.Computer.InternetConnection)
        return l_xml



class API(Utility):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadXml(self, p_pyhouse_obj):
        self._read_xml_configuration(p_pyhouse_obj)

    def Start(self):
        """
        Start async operation of the Internet module.
        """
        self._create_internet_discovery_service(self.m_pyhouse_obj)
        self._start_internet_discovery(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Twisted.Reactor.callLater(INITIAL_DELAY, self._internet_loop, self.m_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        """
        Stop async operations.
        """
        self._stop_internet_discovery(self.m_pyhouse_obj)
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        l_xml = self._write_xml_config(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info('Saved XML')
        return p_xml

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
        l_defer = inet_find_external_ip.API().FindExternalIP(p_pyhouse_obj)
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
        l_defer = inet_update_dyn_dns.API().UpdateAllDynDns(p_pyhouse_obj)
        l_defer.addCallback(cb_done_updating)
        l_defer.addErrback(eb_error)
        return l_defer

#  ## END DBK
