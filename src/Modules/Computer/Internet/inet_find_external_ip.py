"""
-*- test-case-name: PyHouse.src.Modules.Computer.Internet.test.test_inet_find_external_ip -*-

@Name: PyHouse/src/Modules/Computer/Internet/inet_find_external_ip.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2012-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 27, 2014
@summary: This module determines our external IPv4 address asynchronously.

We use an external site that sees the IP we are coming from and returns it to us as a web page.
This module is for Shawn Powers page - http://snar.co/ip

This is because most ISP's use NAT to expand the IPv4 address space.

When the IPv4 address is found, it will update:
    pyhouse_obj.Computer.InternetConnection[ix].ExternalIPv4
where 'ix' is the internet connection number.
'IX' is zero for most sites but there can be more than one Internet connection and therefore 'ix' exists.
"""

# Import system type stuff
import re
from pprint import pformat
from twisted.internet.defer import Deferred
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers


# Import PyMh files and modules.
from Modules.Computer import logging_pyh
from Modules.Utilities import convert
# from Modules.Utilities.tools import PrettyPrintAny


LOG = logging_pyh.getLogger('PyHouse.InternetFnd ')


class FindExternalIpAddress(object):
    """
    Find our external dynamic IP address using an external site returning our IP address.
    """

    m_url = None
    m_reactor = None

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

    def _get_url(self, p_key):
        l_ret = [
                 'http://snar.co/ip/',
                 'http://checkip.dyndns.com/'
                 ]
        return l_ret[p_key]


class Utility(FindExternalIpAddress):
    """
    """

    def _scrape_body(self, p_body):
        l_ip = re.compile(r'(\d+\.\d+\.\d+\.\d+)').search(p_body).group(1)
        return l_ip

    def _print_responses(self, p_response):
        print('Response received {}'.format(p_response))
        print 'Response version:', p_response.version
        print 'Response code:', p_response.code
        print 'Response phrase:', p_response.phrase
        print 'Response headers:'
        print pformat(list(p_response.headers.getAllRawHeaders()))


    def _get_body(self, p_response):
        """
        Loop thru the given external sites until one of them gets an external IPv4 address.
        return that address

        @return: a deferred
        """

        def cb_body(p_body):
            LOG.info('Response body:\n{}'.format(p_body))
            self._snar_scrape(p_body)

        def eb_body(p_reason):
            LOG.error('ERROR - failed to fetch body - {}'.format(p_reason))

        l_body_defer = readBody(p_response)
        l_body_defer.addCallback(cb_body)
        return l_body_defer


    def get_public_ip(self, p_pyhouse_obj, p_key):
        """
        Loop thru the given external sites until one of them gets an external IPv4 address.
        return that address

        @return: a deferred
        """

        def cb_response(p_response):
            self.m_headers = p_response
            l_body_defer = self._get_body(p_response)
            return l_body_defer

        def eb_response(p_reason):
            LOG.error('ERROR  -failed to fetch Url - {}'.format(p_reason))

        l_agent = Agent(p_pyhouse_obj.Twisted.Reactor)
        l_url = self._get_url(p_key)
        l_defer = l_agent.request(
            'GET',
            l_url,
            Headers({'User-Agent': ['Twisted Web Client Example']}),
            None)
        l_defer.addCallback(cb_response)
        l_defer.addErrback(eb_response)
        return l_defer



class API(Utility):

    def FindExternalIP(self, p_pyhouse_obj):
        """
        Loop thru the given external sites until one of them gets an external IPv4 address.
        return that address
        return a defered that fires with an external IP address or errors with a none found error
        """
        l_defer = Deferred()
        for l_key in p_pyhouse_obj.Computer.InternetConnection.LocateUrls.iterkeys():
            self.get_public_ip(p_pyhouse_obj, l_key)
        return l_defer

# ## END DBK
