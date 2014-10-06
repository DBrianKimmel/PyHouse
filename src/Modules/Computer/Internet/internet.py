"""
-*- test-case-name: PyHouse.src.Modules.Computer.Internet.test.test_internet -*-

@Name: PyHouse/src/Modules/Computer/Internet/internet.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2012-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Mar 20, 2012
@summary: This module determines the IP address of the ISP connection.


All nodes currently run this.  This is overkill!
We need a way to have only one of the nodes run this and if successful, block the other nodes from running.

Get the Internet address and make reports available for web interface.

Since PyHouse is always running (as a daemon) this module will get the IP-v4 address that is
assigned to our router by the ISP.
It will then take that IP address and update our Dynamic DNS provider(s) so we may browse to that
address from some external device and check on the status of the house.
"""

# Import system type stuff
from twisted.application import service

# Import PyMh files and modules.
from Modules.Computer.Internet import internet_xml, inet_find_external_ip, inet_update_dyn_dns
from Modules.Computer import logging_pyh as Logger


LOG = Logger.getLogger('PyHouse.Internet    ')
INITIAL_DELAY = 5
REPEAT_DELAY = 2 * 60 * 60



class Utility(object):
    """
    """

    m_pyhouse_obj = None
    m_snarAPI = None
    m_freednsAPI = None


    def stop_internet_discovery(self, _p_pyhouse_obj):
        pass


    def _create_internet_discovery_service(self, p_pyhouse_obj):
        """
        Create the twisted service for Internet discovery.
        """
        try:
            p_pyhouse_obj.Services.InternetDiscoveryService = service.Service()
            p_pyhouse_obj.Services.InternetDiscoveryService.setName('NodeDiscovery')
            p_pyhouse_obj.Services.InternetDiscoveryService.setServiceParent(p_pyhouse_obj.Twisted.Application)
        except RuntimeError:  # The service is already installed
            LOG.warning('Internet Discovery Service already loaded.')
        self.m_service_installed = True


    def _internet_loop(self, p_pyhouse_obj):
        API.FindExternalIp(p_pyhouse_obj)
        API.UpdateDynDnsSites(p_pyhouse_obj)
        self.m_pyhouse_obj.Twisted.Reactor.callLater(REPEAT_DELAY, self._internet_loop, p_pyhouse_obj)



class API(Utility):
    """
    """

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

    def Start(self, p_pyhouse_obj):
        """
        Start async operation of the Internet module.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pyhouse_obj.Computer.InternetConnection = internet_xml.API().read_internet_xml(p_pyhouse_obj)
        self._create_internet_discovery_service(p_pyhouse_obj)
        self.m_pyhouse_obj.Twisted.Reactor.callLater(INITIAL_DELAY, self._internet_loop, p_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        """
        Stop async operations.
        """
        self.stop_internet_discovery(self.m_pyhouse_obj)
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        p_xml.append(internet_xml.API().write_internet_xml(self.m_pyhouse_obj.Computer.InternetConnection))
        LOG.info('Saved XML')

# ## END DBK
