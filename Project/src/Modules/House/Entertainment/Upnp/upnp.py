"""
Created on Mar 1, 2014

@author: briank


Get the internet address and make reports available for web interface.

Since PyHouse is always running (as a daemon) this module will get the IP-v4 address that is
assigned to our router by the ISP.
It will then take that IP address and update our Dynamic DNS provider so we may browse to that
address from some external device and check on the status of the house.

This module will try to be fully twisted like and totally async (except for read/write of xml).
"""

__updated__ = '2020-02-14'

# Import system type stuff
import netifaces
import xml.etree.ElementTree as ET
from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.defer import Deferred
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from Modules.Core.Utilities import convert
from Modules.Core import logging_pyh as Logger

g_debug = 1
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config XML read / write file handling
# 4 = External IP execution
# 5 = Dump Objects
# + = NOT USED HERE
LOG = Logger.getLogger('PyHouse.Internet    ')

callLater = reactor.callLater

#======================================
#
# Data classes for this module
#
#======================================


class InternetData(object):
    """Check our external IP-v4 address
    """

    def __init__(self):
        self.Name = ''
        self.Key = 0
        self.Active = False
        self.ExternalDelay = 0
        self.ExternalIP = None  # returned from url to check our external IPv4 address
        self.ExternalUrl = None
        self.DynDns = {}

    def reprJSON(self):
        return dict(Name=self.Name, Key=self.Key, Active=self.Active,
                    ExternalDelay=self.ExternalDelay,
                    ExternalIP=self.ExternalIP, ExternalUrl=self.ExternalUrl,
                    DynDns=self.DynDns
                    )


class DynDnsData(object):

    def __init__(self):
        self.Name = ''
        self.Key = 0
        self.Active = False
        self.UpdateInterval = 0
        self.UpdateUrl = None

    def reprJSON(self):
        return dict(Name=self.Name, Key=self.Key, Active=self.Active,
                    Interval=self.UpdateInterval, Url=self.UpdateUrl
                    )


class InterfaceIpAddresses(object):

    def __init__(self):
        self.Name = ''
        self.Key = 0
        self.Active = False
        self.MacAddress = ''
        self.V4Address = ''
        self.V6Address = ''

#======================================
#
# Synchronous portion
#
# We don't want to take off and run until ALL XML is read in.
# Also halt all asynchronous operations and write out the XML when requested.
#
#======================================


class FindAllInterfaceData(object):
    """Loop thru all the interfaces and extract the info
    """

    def __init__(self):
        l_interfaces = netifaces.interfaces()
        l_count = 0
        for l_interface in l_interfaces:
            if l_interface == 'lo':
                continue
# TODO: this only allows for one address per interface dur to the [0] below
            m_interface = InterfaceIpAddresses()
            m_interface.Name = l_interface
            m_interface.Key = l_count
            for l_af in netifaces.ifaddresses(l_interface):
                if netifaces.address_families[l_af] == 'AF_PACKET':
                    m_interface.MacAddress = netifaces.ifaddresses(l_interface)[l_af][0]['addr']
                if netifaces.address_families[l_af] == 'AF_INET':
                    m_interface.V4Address = netifaces.ifaddresses(l_interface)[l_af][0]['addr']
                if netifaces.address_families[l_af] == 'AF_INET6':
                    m_interface.V6Address = netifaces.ifaddresses(l_interface)[l_af][0]['addr']
            LOG.info("Interface:{}, Mac:{}, V4:{}, V6:{}".format(m_interface.Name, m_interface.MacAddress, m_interface.V4Address, m_interface.V6Address))
            l_count += 1
        pass


class ReadWriteConfigXml:
    """
    """

    m_external_ip = None
    m_external_url = None
    m_external_delay = None

    def extract_dyn_dns(self, p_internet_xml):
        pass

    def insert_dyn_dns(self):
        pass

    def read_internet_xml(self, p_house_obj, p_house_xml):
        """
        """
        p_house_obj.Internet = InternetData()
        l_sect = p_house_xml.find('Internet')
        p_house_obj.Internet.ExternalIP = self.m_external_ip
        p_house_obj.Internet.ExternalUrl = self.m_external_url
        p_house_obj.Internet.ExternalDelay = self.m_external_delay
        LOG.debug("Got external IP params.  URL:{}, Delay:{}".format(self.m_external_url, self.m_external_delay))
        try:
            l_list = l_sect.iterfind('DynamicDNS')
        except AttributeError:
            l_list = []
        l_count = 0
        for l_entry in l_list:
            l_dyndns = self.extract_dyn_dns(l_entry)
            l_dyndns.Key = l_count  # Renumber
            p_house_obj.Internet.DynDns[l_count] = l_dyndns
            l_count += 1
        LOG.info('Loaded UpdateUrl:{}, Delay:{}'.format(self.m_external_url, self.m_external_delay))
        return p_house_obj.Internet

    def write_internet(self, p_house_obj):
        """Create a sub tree for 'Internet' - the sub elements do not have to be present.
        @return: a sub tree ready to be appended to "something"
        """
        l_internet_xml = ET.Element('Internet')
        return l_internet_xml

#======================================
#
# Now all asynchronous code
#
#======================================


class MyProtocol(Protocol):
    """
    """

    def __init__(self, p_finished):
        self.m_finished = p_finished

    def dataReceived(self, p_bytes):
        if self.m_remaining:
            l_display = p_bytes[:self.m_remaining]
            self.m_remaining -= len(l_display)

    def connectionLost(self, p_reason):
        self.m_finished.callback(None)


class MyClientFactory(ClientFactory):

    protocol = MyProtocol

    def __init__(self, deferred):
        self.deferred = deferred

    def poem_finished(self, poem):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.callback(poem)

    def clientConnectionFailed(self, _connector, reason):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.errback(reason)


class MyGet(object):
    """
    """

    def __init__(self):
        pass

    def my_getPage(self, p_url):
        l_d = Agent(reactor).request('GET', p_url, Headers({'User-Agent': ['twisted']}), None)
        l_d.addCallbacks(self.handleResponse, self.handleError)
        return l_d

    def handleResponse(self, p_r):
        l_whenFinished = Deferred()
        p_r.deliverBody(MyProtocol(l_whenFinished))
        return l_whenFinished

    def handleError(self, p_reason):
        p_reason.printTraceback()


class UpdateDnsSites(object):
    """
    """


class FindExternalIpAddress(object):
    """Find our external dynamic IP address.
    Keep the house object up to date.

    Methods:
        SNMP to the router
        External site returning IP address (may need scraping)
    """

    m_url = None

    def __init__(self, p_house_obj):
        self.m_house_obj = p_house_obj
        callLater(3 * 60, self.get_public_ip)

    def get_public_ip(self):
        """Get the public IP address for the house.
        """
        l_delay = self.m_house_obj.Internet.ExternalDelay
        if l_delay < 600:
            l_delay = 600
            self.m_house_obj.Internet.ExternalDelay = l_delay
        callLater(l_delay, self.get_public_ip)
        self.m_url = self.m_house_obj.Internet.ExternalUrl
        if self.m_url == None:
            LOG.error("URL is missing for House:{}".format(self.m_house_obj.Name))
            return
        LOG.debug("About to get URL:{}".format(self.m_url))
        l_ip_page_defer = getPage(self.m_url)
        l_ip_page_defer.addCallbacks(self.cb_parse_page, self.eb_no_page)

    def cb_parse_page(self, p_ip_page):
        """This gets the page with the IP in it and returns it.
        Different sites will need different page scraping to get the IP address.
        dotted quad IPs are converted to 4 byte addresses
        IP V-6 is not handled yet.

        @param p_ip_page: is the web page as a string
        """
        # This is for Shawn Powers page - http://snar.co/ip
        l_quad = p_ip_page
        self.m_house_obj.Internet.ExternalIP = l_quad
        l_addr = convert.str_to_long(l_quad)
        LOG.info("Got External IP page for House:{}, Page:{}".format(self.m_house_obj.Name, p_ip_page))
        callLater(self.m_house_obj.Internet.ExternalDelay, self.get_public_ip)
        return l_addr

    def eb_no_page(self, p_reason):
        LOG.error("Failed to Get External IP page for House:{}, {}".format(self.m_house_obj.Name, p_reason))
        callLater(self.m_house_obj.Internet.ExternalDelay, self.get_public_ip)


class DynDnsApi(object):
    """Update zero or more dynamic DNS sites.
    This is a repeating two stage process.
    First get our current External IP address.
    Second, update zero or more Dyn DNS sites with our address
    Then wait UpdateInterval time and repeat forever.
    Allow for missing responses so as to not break the chain of events.
    """

    def __init__(self, p_house_obj):
        self.m_house_obj = p_house_obj
        # Wait a bit to avoid all the starting chaos
        callLater(3 * 60, self.update_start_process)

    def update_start_process(self):
        """After waiting for the initial startup activities to die down, this is invoked
        to start up a loop for each dynamic service being updated.
        """
        self.m_running = True
        for l_dyn_obj in self.m_house_obj.Internet.DynDns.values():
            l_cmd = lambda x = l_dyn_obj.UpdateInterval, y = l_dyn_obj: self.update_loop(x, y)
            callLater(l_dyn_obj.UpdateInterval, l_cmd)

    def stop_dyndns_process(self):
        self.m_running = False

    def update_loop(self, _p_interval, p_dyn_obj):
        """Fetching the page from afraid.org using this url will update the IP address
        using this computers PUBLIC ip address.
        Other methods may be required if using some other dyn dns servicee.
        """
        if not self.m_running:
            return
        LOG.info("Update DynDns for House:{}, {}, {}".format(self.m_house_obj.Name, p_dyn_obj.Name, p_dyn_obj.UpdateUrl))
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
        LOG.warning("Update DynDns for House:{} failed ERROR - {}.".format(self.m_house_obj.Name, p_response))

    def cb_do_delay(self, _p_response):
        l_cmd = lambda x = self.m_dyn_obj.UpdateInterval, y = self.m_dyn_obj: self.update_loop(x, y)
        callLater(self.m_dyn_obj.UpdateInterval, l_cmd)


class Api(ReadWriteConfigXml):

    m_house_obj = None

    def __init__(self):
        pass

    def Start(self, p_house_obj, p_house_xml):
        """Start async operation of the internet module.
        """
        self.read_internet_xml(p_house_obj, p_house_xml)
        self.m_house_obj = p_house_obj
        if p_house_obj.Active:
            LOG.info("Starting for house:{}.".format(p_house_obj.Name))
            FindAllInterfaceData()
            FindExternalIpAddress(p_house_obj)
            self.m_dyn_loop = DynDnsApi(p_house_obj)

    def Stop(self):
        """Stop async operations
        write out the XML file.
        """
        if self.m_house_obj.Active:
            LOG.info("Stopping for house:{}.".format(self.m_house_obj.Name))
            self.dyndns.stop_dyndns_process()

# ## END DBK
