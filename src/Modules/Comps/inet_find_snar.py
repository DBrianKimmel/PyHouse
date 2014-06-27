"""
-*- test-case-name: PyHouse.src.Modules.Comps.test.test_inet_find_snar -*-

@Name: PyHouse/src/Modules/Comps/inet_find_snar.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2012-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 27, 2014
@summary: This module determines our external IPv4 address using snar.co

We use an external site that sees the IP we are coming from and returns it to us as a web page.

This is because most ISP's use NAT to expand the IPv4 address space.

When the IPv4 address is found, it will update:
    pyhouse_obj.Computer.InternetConnection[ix].ExternalIPv4
where 'ix' is the internet connection number.
'IX' is zero for most sites but there can be more than one Internet connection and therefore 'ix' exists.
"""

# Import system type stuff
from twisted.web.client import getPage

# Import PyMh files and modules.
from Modules.utils import convert
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

g_debug = 1
LOG = pyh_log.getLogger('PyHouse.InternetFnd ')




class FindExternalIpAddress(object):
    """Find our external dynamic IP address.
    Keep the house object up to date.

    Methods:
        SNMP to the router
        External site returning IP address (may need scraping)
    """

    m_url = None
    m_reactor = None

    def __init__(self, p_internet_obj, p_reactor):
        """Delay a bit so we are not too busy with initialization and then start the IPv4 query process.
        """
        self.m_internet_obj = p_internet_obj
        self.m_reactor = p_reactor
        self.m_reactor.callLater(1 * 60, self.get_public_ip)

    def get_public_ip(self):
        """Get the public IP address for the house.
        """
        # PrettyPrintAny(p_internet_connection, 'InetFindSnar - GetOnePublicIp - p_internet_connection')
        if self.m_internet_obj.ExternalDelay < 600:
            self.m_internet_obj.ExternalDelay = 600
        self.m_reactor.callLater(self.m_internet_obj.ExternalDelay, self.get_public_ip)
        self.m_url = self.m_internet_obj.ExternalUrl
        if self.m_url == None:
            LOG.error("URL is missing.")
            return
        LOG.debug("About to get URL:{0:}".format(self.m_url))
        l_ip_page_defer = getPage(self.m_url)
        l_ip_page_defer.addCallbacks(self.cb_parse_page, self.eb_no_page)

    def cb_parse_page(self, p_ip_page):
        """This gets the page with the IP in it and returns it.
        Different sites will need different page scraping to get the IP address.
        dotted quad IPs are converted to 4 byte IPv4 addresses
        IP V-6 is not handled yet.

        @param p_ip_page: is the web page as a string
        """
        # This is for Shawn Powers page - http://snar.co/ip
        l_quad = p_ip_page
        self.m_internet_obj.ExternalIPv4 = l_quad
        l_addr = convert.ConvertEthernet().dotted_quad2long(l_quad)
        LOG.info("Got External IP page - {0:}".format(p_ip_page))
        return l_addr

    def eb_no_page(self, p_reason):
        LOG.error("Failed to Get External IP page - {0:}".format(p_reason))


class API(FindExternalIpAddress):

    m_reactor = None

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj, p_ix):
        self.m_internet_obj = p_pyhouse_obj.Computer.InternetConnection[p_ix]
        self.m_reactor = p_pyhouse_obj.Twisted.Reactor
        FindExternalIpAddress(self.m_internet_obj, self.m_reactor)

    def Stop(self, ignore1, ignore2):
        pass

# ## END DBK
