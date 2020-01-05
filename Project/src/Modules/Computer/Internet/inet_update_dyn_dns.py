"""
@Name:      Modules/Computer/Internet/inet_update_dyn_dns.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2012-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 20, 2012
@summary:   This module sends our external IP to freedns.

"""

__updated__ = '2020-01-03'
__version_info__ = (20, 1, 3)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
from twisted.web.client import getPage
from twisted.internet.defer import Deferred

# Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Computer.Internet.__init__ import InternetInformation

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Internet    ')

CONFIG_NAME = 'internet'
INITIAL_DELAY = 1 * 60


class DynDnsApi(object):
    """Update zero or more dynamic DNS sites.
    This is a repeating two stage process.
    First get our current External IP address.
    Second, update zero or more Dyn DNS sites with our address
    Then wait UpdateInterval time and repeat forever.
    Allow for missing responses so as to not break the chain of events.
    """

    def XX__init__(self, p_internet_obj, p_reactor):
        """
        Wait a bit to avoid all the starting chaos.
        """
        self.m_internet_obj = p_internet_obj
        self.m_reactor = p_reactor
        self.m_reactor.callLater(INITIAL_DELAY, self.update_start_process, None)

    def update_start_process(self, _ignore):
        """After waiting for the initial startup activities to die down, this is invoked
        to start up a loop for each dynamic service being updated.
        """
        self.m_running = True
        for l_dyn_obj in self.m_internet_obj.DynDns.values():
            l_cmd = lambda x = l_dyn_obj.UpdateInterval, y = l_dyn_obj: self.update_loop(x, y)
            self.m_reactor.callLater(l_dyn_obj.UpdateInterval, l_cmd, None)

    def stop_dyndns_process(self):
        self.m_running = False

    def update_loop(self, _p_interval, p_dyn_obj):
        """Fetching the page from afraid.org using this url will update the IP address
        using this computers PUBLIC ip address.
        Other methods may be required if using some other dyn dns servicee.
        """
        if not self.m_running:
            return
        LOG.info("Update DynDns - {}, {}".format(p_dyn_obj.Name, p_dyn_obj.UpdateUrl))
        self.m_dyn_obj = p_dyn_obj
        self.m_deferred = getPage(p_dyn_obj.UpdateUrl)
        self.m_deferred.addCallback(self.cb_parse_dyndns)
        self.m_deferred.addErrback(self.eb_parse_dyndns)
        self.m_deferred.addBoth(self.cb_do_delay)

    def cb_parse_dyndns(self, _p_response):
        """Update the external web site with our external IP address.
        In the case of afraid.org, nothing needs to be done to respond to the web page fetched.
        """
        return

    def eb_parse_dyndns(self, p_response):
        """Afraid.org has no errors except no response in which case we can do nothing anyhow.
        """
        LOG.warning("Update DynDns for House:{} failed ERROR - {}.".format(self.m_pyhouse_obj.House.Name, p_response))

    def cb_do_delay(self, _p_response):
        l_cmd = lambda x = self.m_dyn_obj.UpdateInterval, y = self.m_dyn_obj: self.update_loop(x, y)
        self.m_reactor.callLater(self.m_dyn_obj.UpdateInterval, l_cmd, None)


class LocalConfig:
    """
    """
    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_house_info(self, p_config):
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
                LOG.warning('house.yaml is missing an entry for "{}"'.format(l_key))
        return l_obj

    def load_yaml_config(self):
        """ Read the house.yaml file.
         """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Name = 'Unknown House Name'
        l_yaml = self.m_config.read_config_file(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['House']
        except:
            LOG.warning('The config file does not start with "House:"')
            return None
        l_house = self._extract_house_info(l_yaml)
        self.m_pyhouse_obj.House.Name = l_house.Name
        return l_house  # for testing purposes


class Api(DynDnsApi):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        """
        """
        LOG.info('Initializing - Version:{}'.format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()

    def _add_storage(self):
        """
        """
        self.m_pyhouse_obj.Computer.Internet = InternetInformation()

    def LoadConfig(self):
        """ The house is always present but the components of the house are plugins and not always present.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_local_config.load_yaml_config()

    def Start(self, p_pyhouse_obj, p_ix):
        self.m_internet_obj = p_pyhouse_obj.Computer.Internet[p_ix]
        self.m_reactor = p_pyhouse_obj._Twisted.Reactor
        self.m_dyn_loop = DynDnsApi(self.m_internet_obj, self.m_reactor)

    def Stop(self, _ignore1, _ignore2):
        # self.m_dyn_loop.stop_dyndns_process()
        pass

    def UpdateAllDynDns(self, p_pyhouse_obj):
        l_defer = Deferred()
        for _l_internet in p_pyhouse_obj.Computer.Internet.UpdateUrls:
            pass
        return l_defer
        pass

# ## END DBK
