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

__updated__ = '2020-01-03'
__version_info__ = (20, 1, 3)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Computer.Internet.inet_find_external_ip import Api as findApi
from Modules.Computer.Internet.inet_update_dyn_dns import Api as updateApi
from Modules.Computer.Internet.__init__ import InternetInformation

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Internet       ')

CONFIG_NAME = 'internet'

INITIAL_DELAY = 5
REPEAT_DELAY = 2 * 60 * 60


class lightingUtilityInter:
    """
    """

    @staticmethod
    def _internet_loop(p_pyhouse_obj):
        # Api.FindExternalIp(p_pyhouse_obj)
        # Api.UpdateDynDnsSites(p_pyhouse_obj)
        p_pyhouse_obj._Twisted.Reactor.callLater(REPEAT_DELAY, lightingUtilityInter._internet_loop, p_pyhouse_obj)


class LocalConfig:
    """
    """
    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_internet_info(self, p_config):
        """
        """
        l_required = ['Name']
        l_obj = InternetInformation()
        for l_key, l_value in p_config.items():
            if l_key == 'Modules':
                pass
            setattr(l_obj, l_key, l_value)
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('internet.yaml is missing an entry for "{}"'.format(l_key))
        return l_obj

    def load_yaml_config(self):
        """ Read the house.yaml file.
         """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        l_yaml = self.m_config.read_config_file(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Internet']
        except:
            LOG.warning('The config file does not start with "Internet:"')
            return None
        l_internet = self._extract_internet_info(l_yaml)
        return l_internet  # for testing purposes


class Api:
    """
    """

    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        LOG.info('Initializing - Version:{}'.format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)

    def _add_storage(self):
        """
        """
        self.m_pyhouse_obj.Computer.Internet = InternetInformation()

    def LoadConfig(self):
        self.m_local_config.load_yaml_config()
        LOG.info('Loaded Internet Config')

    def Start(self):
        """
        Start async operation of the Internet module.
        """
        self.m_pyhouse_obj._Twisted.Reactor.callLater(INITIAL_DELAY, lightingUtilityInter._internet_loop, self.m_pyhouse_obj)
        LOG.info("Started Internet.")

    def SaveConfig(self):
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
