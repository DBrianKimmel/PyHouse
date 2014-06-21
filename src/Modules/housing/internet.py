"""
-*- test-case-name: PyHouse.src.Modules.housing.test.test_internet -*-

@Name: PyHouse/src/Modules/housing/internet.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2012-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Mar 20, 2012
@summary: This module determines the IP address of the ISP connection.


Get the internet address and make reports available for web interface.

Since PyHouse is always running (as a daemon) this module will get the IP-v4 address that is
assigned to our router by the ISP.
It will then take that IP address and update our Dynamic DNS provider so we may browse to that
address from some external device and check on the status of the house.
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.defer import Deferred
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

# Import PyMh files and modules.
from Modules.Core.data_objects import InternetConnectionData, InternetConnectionDynDnsData
from Modules.utils import xml_tools
from Modules.utils import convert
from Modules.utils import pyh_log

g_debug = 1
# 0 = off
# 1 = log extra info
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.Internet    ')

#======================================
#
# Data classes for this module
#
#======================================

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

class ReadWriteXML(xml_tools.ConfigTools):
    """
    """

    m_count = 0

    def read_one_dyn_dns_xml(self, p_entry_xml):
        l_dyndns_obj = InternetConnectionDynDnsData()
        self.read_base_object_xml(l_dyndns_obj, p_entry_xml)
        l_dyndns_obj.Interval = self.get_int_from_xml(p_entry_xml, 'Interval')
        l_dyndns_obj.Url = self.get_text_from_xml(p_entry_xml, 'Url')
        return l_dyndns_obj

    def read_dyn_dns_xml(self, p_internet_xml):
        self.m_count = 0
        l_ret = {}
        for l_entry_xml in p_internet_xml.iterfind('DynamicDNS'):
            l_dyndns = self.read_one_dyn_dns_xml(l_entry_xml)
            l_dyndns.Key = self.m_count  # Renumber
            l_ret[self.m_count] = l_dyndns
            self.m_count += 1
        return l_ret

    def write_one_dyn_dns_xml(self, p_entry_obj):
        l_entry = self.write_base_object_xml('Internet', p_entry_obj)
        self.put_text_element(l_entry, 'Url', p_entry_obj.Url)
        self.put_int_element(l_entry, 'Interval', p_entry_obj.Interval)
        return l_entry

    def write_dyn_dns_xml(self, p_dns_obj):
        l_dns_xml = ET.Element('DynamicDNS')
        self.m_count = 0
        for l_dns in p_dns_obj.itervalues():
            l_entry = self.write_one_room(l_dns)
            l_dns_xml.append(l_entry)
            self.m_count += 1
        return l_dns_xml

    def read_internet_xml(self, p_house_xml):
        """
        """
        l_internet_obj = InternetConnectionData()
        l_sect = p_house_xml.find('Internet')
        try:
            l_internet_obj.ExternalIPv4 = self.get_text_from_xml(p_house_xml, 'ExternalIP')
            l_internet_obj.ExternalDelay = self.get_int_from_xml(l_sect, 'ExternalDelay')
            l_internet_obj.ExternalUrl = self.get_text_from_xml(l_sect, 'ExternalUrl')
        except AttributeError:
            LOG.error('internet section missing - using defaults.')
            l_internet_obj.ExternalDelay = 600
        try:
            l_list = l_sect.iterfind('DynamicDNS')
        except AttributeError:
            l_list = []
        l_count = 0
        for l_entry in l_list:
            l_dyndns = self.read_one_dyn_dns_xml(l_entry)
            l_dyndns.Key = l_count  # Renumber
            l_internet_obj.DynDns[l_count] = l_dyndns
            l_count += 1
        LOG.info('Loaded Url:{0:}, Delay:{1:}'.format(l_internet_obj.ExternalUrl, l_internet_obj.ExternalDelay))
        return l_internet_obj

    def write_internet_xml(self, p_internet_obj):
        """Create a sub tree for 'Internet' - the sub elements do not have to be present.
        @return: a sub tree ready to be appended to house
        """
        l_internet_xml = ET.Element('Internet')
        self.put_text_attribute(l_internet_xml, 'ExternalIP', p_internet_obj.ExternalIPv4)
        self.put_int_attribute(l_internet_xml, 'ExternalDelay', p_internet_obj.ExternalDelay)
        self.put_text_attribute(l_internet_xml, 'ExternalUrl', p_internet_obj.ExternalUrl)
        try:
            for l_dyndns_obj in p_internet_obj.DynDns.itervalues():
                l_entry = self.write_base_object_xml('DynamicDNS', l_dyndns_obj)
                self.put_int_element(l_entry, 'Interval', l_dyndns_obj.Interval)
                self.put_text_element(l_entry, 'Url', l_dyndns_obj.Url)
                l_internet_xml.append(l_entry)
        except AttributeError:
            pass
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

    def connectionLost(self, _p_reason):
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
        if g_debug >= 1:
            LOG.debug("Requesting {0:}".format(p_url))
        l_d = Agent(reactor).request('GET', p_url, Headers({'User-Agent': ['twisted']}), None)
        l_d.addCallbacks(self.handleResponse, self.handleError)
        return l_d

    def handleResponse(self, p_r):
        LOG.debug("version={0:}\ncode={1:}\nphrase='{2:}'".format(p_r.version, p_r.code, p_r.phrase))
        for k, v in p_r.headers.getAllRawHeaders():
            print("%s: %s" % (k, '\n  '.join(v)))
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

    def __init__(self, p_pyhouses_obj, p_house_obj):
        self.m_pyhouse_obj = p_pyhouses_obj
        self.m_house_obj = p_house_obj
        self.m_pyhouse_obj.Twisted.Reactor.callLater(1 * 60, self.get_public_ip)

    def get_public_ip(self):
        """Get the public IP address for the house.
        """
        if self.m_house_obj.Internet.ExternalDelay < 600:
            self.m_house_obj.Internet.ExternalDelay = 600
        self.m_pyhouse_obj.Twisted.Reactor.callLater(self.m_house_obj.Internet.ExternalDelay, self.get_public_ip)
        self.m_url = self.m_house_obj.Internet.ExternalUrl
        if self.m_url == None:
            LOG.error("URL is missing for House:{0:}".format(self.m_house_obj.Name))
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
        self.m_house_obj.Internet.ExternalIPv4 = l_quad
        l_addr = convert.ConvertEthernet().dotted_quad2long(l_quad)
        LOG.info("Got External IP page for House:{0:}, Page:{1:}".format(self.m_house_obj.Name, p_ip_page))
        return l_addr

    def eb_no_page(self, p_reason):
        LOG.error("Failed to Get External IP page for House:{0:}, {1:}".format(self.m_house_obj.Name, p_reason))


class DynDnsAPI(object):
    """Update zero or more dynamic DNS sites.
    This is a repeating two stage process.
    First get our current External IP address.
    Second, update zero or more Dyn DNS sites with our address
    Then wait Interval time and repeat forever.
    Allow for missing responses so as to not break the chain of events.
    """

    def __init__(self, p_pyhouses_obj, p_house_obj):
        self.m_house_obj = p_house_obj
        self.m_pyhouse_obj = p_pyhouses_obj
        # Wait a bit to avoid all the starting chaos
        self.m_pyhouse_obj.Twisted.Reactor.callLater(3 * 60, self.update_start_process)

    def update_start_process(self):
        """After waiting for the initial startup activities to die down, this is invoked
        to start up a loop for each dynamic service being updated.
        """
        self.m_running = True
        for l_dyn_obj in self.m_house_obj.Internet.DynDns.itervalues():
            l_cmd = lambda x = l_dyn_obj.Interval, y = l_dyn_obj: self.update_loop(x, y)
            self.m_pyhouse_obj.Twisted.Reactor.callLater(l_dyn_obj.Interval, l_cmd)

    def stop_dyndns_process(self):
        self.m_running = False

    def update_loop(self, _p_interval, p_dyn_obj):
        """Fetching the page from afraid.org using this url will update the IP address
        using this computers PUBLIC ip address.
        Other methods may be required if using some other dyn dns servicee.
        """
        if not self.m_running:
            return
        LOG.info("Update DynDns for House:{0:}, {1:}, {2:}".format(self.m_house_obj.Name, p_dyn_obj.Name, p_dyn_obj.Url))
        self.m_dyn_obj = p_dyn_obj
        self.m_deferred = getPage(p_dyn_obj.Url)
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
        LOG.warning("Update DynDns for House:{0:} failed ERROR - {1:}.".format(self.m_house_obj.Name, p_response))

    def cb_do_delay(self, _p_response):
        l_cmd = lambda x = self.m_dyn_obj.Interval, y = self.m_dyn_obj: self.update_loop(x, y)
        self.m_pyhouse_obj.Twisted.Reactor.callLater(self.m_dyn_obj.Interval, l_cmd)


class API(ReadWriteXML):

    m_house_obj = None

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj):
        """Start async operation of the internet module.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_house_obj = self.m_pyhouse_obj.House.OBJs
        l_house_xml = self.m_pyhouse_obj.Xml.XmlParsed.find('Houses/House')
        self.m_house_obj.Internet = self.read_internet_xml(l_house_xml)
        LOG.info("Starting for house:{0:}.".format(self.m_house_obj.Name))
        FindExternalIpAddress(p_pyhouse_obj, self.m_house_obj)
        self.m_dyn_loop = DynDnsAPI(p_pyhouse_obj, self.m_house_obj)

    def Stop(self, p_xml):
        """Stop async operations
        write out the XML file.
        """
        LOG.info("Stopping dyndns for house:{0:}.".format(self.m_house_obj.Name))
        self.m_dyn_loop.stop_dyndns_process()
        p_xml.append(self.write_internet_xml(self.m_house_obj.Internet))

# ## END DBK
