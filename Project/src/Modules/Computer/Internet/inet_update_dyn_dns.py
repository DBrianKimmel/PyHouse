"""
@Name:      Modules/Computer/Internet/inet_update_dyn_dns.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2012-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 20, 2012
@summary:   This module sends our external IP to freedns.

"""

__updated__ = '2019-12-30'

# Import system type stuff
from twisted.web.client import getPage
from twisted.internet.defer import Deferred

# Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Internet    ')
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


class Api(DynDnsApi):

    def UpdateAllDynDns(self, p_pyhouse_obj):
        l_defer = Deferred()
        for _l_internet in p_pyhouse_obj.Computer.InternetConnection.UpdateUrls:
            pass
        return l_defer
        pass

    def Start(self, p_pyhouse_obj, p_ix):
        self.m_internet_obj = p_pyhouse_obj.Computer.InternetConnection[p_ix]
        self.m_reactor = p_pyhouse_obj._Twisted.Reactor
        self.m_dyn_loop = DynDnsApi(self.m_internet_obj, self.m_reactor)

    def Stop(self, _ignore1, _ignore2):
        # self.m_dyn_loop.stop_dyndns_process()
        pass

# ## END DBK
