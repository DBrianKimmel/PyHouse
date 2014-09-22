"""
-*- test-case-name: PyHouse.src.Modules.Computer.test.test_inet_find_snar -*-

@Name: PyHouse/src/Modules/Computer/inet_find_snar.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2012-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 27, 2014
@summary: This module determines our external IPv4 address using snar.co

We use an external site that sees the IP we are coming from and returns it to us as a web page.
This module is for Shawn Powers page - http://snar.co/ip

This is because most ISP's use NAT to expand the IPv4 address space.

When the IPv4 address is found, it will update:
    pyhouse_obj.Computer.InternetConnection[ix].ExternalIPv4
where 'ix' is the internet connection number.
'IX' is zero for most sites but there can be more than one Internet connection and therefore 'ix' exists.
"""

# Import system type stuff
from twisted.web.client import getPage

from twisted.internet.endpoints import HostnameEndpoint
from twisted.web.client import ProxyAgent


# Import PyMh files and modules.
from Modules.Utilities import convert
from Modules.Computer import logging_pyh
# from Modules.Utilities.tools import PrettyPrintAny


LOG = logging_pyh.getLogger('PyHouse.InternetFnd ')
INITIAL_DELAY = 35
REPEAT_DELAY = 2 * 60 * 60  # 2 Hours
MINIMUM_DELAY = 30 * 60  # 30 Minutes

class FindExternalIpAddress(object):
    """
    Find our external dynamic IP address using an external site returning our IP address.
    """

    m_url = None
    m_reactor = None

    def __init__(self, p_pyhouse_obj, p_internet_obj):
        """
        Delay a bit so we are not too busy with initialization and then start the IPv4 query process.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_internet_obj = p_internet_obj
        p_pyhouse_obj.Twisted.Reactor.callLater(INITIAL_DELAY, self.get_public_ip, None)

    def _get_delay(self, p_internet_obj):
        if p_internet_obj.ExternalDelay < MINIMUM_DELAY:
            p_internet_obj.ExternalDelay = MINIMUM_DELAY
        return p_internet_obj.ExternalDelay

    def _extract_ip(self, p_string):
        l_quad = p_string
        l_addr = convert.ConvertEthernet().dotted_quad2long(l_quad)
        return l_addr, l_quad

    def _snar_scrape(self, p_page):
        """
        For snar - the only thing is to use the page as a string.
        """
        l_string = p_page
        return l_string

    def get_public_ip(self, _ignore):
        """
        Get the public IP address for the house.

        This gets the page with the IP in it and returns it.
        Different sites will need different page scraping to get the IP address.
        dotted quad IPs are converted to 4 byte IPv4 addresses
        IP V-6 is not handled yet.

        @param p_ip_page: is the web page as a string
        """
        def cb_parse_page(p_ip_page):
            LOG.info("Got External IP page - {0:}".format(p_ip_page))
            l_string = self._snar_scrape(p_ip_page)
            l_addr_str, _l_quad = self._extract_ip(l_string)
            return l_addr_str

        def eb_no_page(p_reason):
            LOG.error("Failed to Get External IP page - {0:}".format(p_reason))

        self.m_pyhouse_obj.Twisted.Reactor.callLater(self._get_delay(self.m_internet_obj), self.get_public_ip, None)
        self.m_url = self.m_internet_obj.ExternalUrl
        if self.m_url == None:
            LOG.error("URL is missing.")
            return
        # LOG.debug("About to get URL:{0:}".format(self.m_url))
        l_ip_page_defer = getPage(self.m_url)
        l_ip_page_defer.addCallbacks(cb_parse_page, eb_no_page)

    def get_public_ip2(self, _ignore):
        def cb_1():
            pass

        p_hostname = 'snar.co'
        endpoint = HostnameEndpoint(self.m_pyhouse_obj.Twisted.Reactor, p_hostname, 80)
        l_agent = ProxyAgent(endpoint)
        l_defer = l_agent.request(b"GET", b"http://google.com/")
        l_defer.addCallback(cb_1)


class Utility(FindExternalIpAddress):
    """
    """

class API(Utility):

    m_reactor = None

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj, p_ix):
        self.m_internet_obj = p_pyhouse_obj.Computer.InternetConnection[p_ix]
        self.m_reactor = p_pyhouse_obj.Twisted.Reactor
        FindExternalIpAddress(p_pyhouse_obj, self.m_internet_obj)

    def Stop(self, ignore1, ignore2):
        pass

    def SaveXml(self, p_xml):
        return p_xml

# ## END DBK
