#!/usr/bin/env python

"""
# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php
# Copyright 2005, Tim Potter <tpot@samba.org>
# Copyright 2006 John-Mark Gurney <jmg@funkthat.com>

0.  Addressing - Obtain IP address (already done before UPnP starting)
1.  Discovery - Using SSDP to advertise and discover other UPnP thingies.
2.  Description - XML queries back and forth to provide details of UPnP workings.
3.  Control - A UPnP control point controls UPnP devices.
4.  Eventing - How a device gets notified about happenings in the UPnP network.
5.  Presentation - How to retrieve content from a UPnP device.

DBK Notes:

1. requires directory 'media' in this source directory.
"""

from upnp import __version__
import os.path
import socket
import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.web import server, resource, static
import configure
import debug  # my debugging module
from uuid_x import UUID
from FSStorage import FSDirectory
from SSDP import SSDPServer, SSDP_PORT, SSDP_ADDR
from ContentDirectory import ContentDirectoryServer
from ConnectionManager import ConnectionManagerServer

#===============================================================================
# Create some globals for other modules to use.
#===============================================================================
UPnP_Data = {}
UPnPCount = 0
listenAddr = '127.0.0.1'  # DBK easier to debug this way
listenPort = 12345  # DBK Forced for easier debugging
urlbase = 'http://%s:%d/' % (listenAddr, listenPort)

g_uuid = None
g_ssdp = None

class UPnPData(object):
    """Data for UPNP
    """

    def __init__(self):
        global UPnPCount
        UPnPCount += 1
        self.Port = 12345

class Utilities(object):

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        l_ipaddr = s.getsockname()[0]
        print("UPNP_core - My IP Address is ", l_ipaddr)
        s.close()
        return l_ipaddr

    # Modules to import, maybe config file or something?
    def tryloadmodule(self, p_mod):
        try:
            return __import__(p_mod)
        except ImportError:
            pass

    def load_modules(self):
        # ZipStorage w/ tar support should be last as it will gobble up empty files.
        # These should be sorted by how much work they do, the least work the earlier.
        # mpegtsmod can be really expensive.
        l_modules = [
        	'shoutcast',
        	'pyvr',
        	'dvd',
        	'ZipStorage',
        	'mpegtsmod',
        	]
        l_modmap = {}
        for i in l_modules:
            l_modmap[i] = self.tryloadmodule(i)

        for i in l_modules:
            debug.insertnamespace(i, l_modmap[i])


class WebServer(resource.Resource):
    """ Create SOAP server
    """
    def __init__(self):
        resource.Resource.__init__(self)


class RootDevice(static.Data):
    def __init__(self):
        global g_uuid
        l_root_dict = {
            'hostname': socket.gethostname(),
            'uuid': g_uuid,
            'urlbase': urlbase,
        }
        l_d = file(os.path.expanduser('~/media/root-device.xml')).read() % l_root_dict
        static.Data.__init__(self, l_d, 'text/xml')


class CreateServers(object):
    """
    """

    def __init__(self):
        # Create SSDP server
        self.create_ssdp_server()
        global g_uuid
        g_uuid = str(UUID())
        self.create_soap_server()

    def create_ssdp_server(self):
        global g_ssdp
        g_ssdp = SSDPServer()
        debug.insertnamespace('s', g_ssdp)
        l_port = reactor.listenMulticast(SSDP_PORT, g_ssdp, listenMultiple = True)
        l_port.joinGroup(SSDP_ADDR)
        l_port.setLoopbackMode(0)  # don't get our own sends

    def create_soap_server(self):
        l_wsroot = WebServer()
        debug.insertnamespace('root', l_wsroot)
        content = resource.Resource()
        mediapath = os.path.expanduser('~/media')
        # mediapath = os.path.expanduser('~/')
        if not os.path.isdir(mediapath):
            print >> sys.stderr, 'Sorry, %s is not a directory, no content to serve.' % `mediapath`
            sys.exit(1)

        # This sets up the root to be the media dir so we don't have to
        # enumerate the directory
        l_cds = ContentDirectoryServer('My Media Server', klass = FSDirectory,
            path = mediapath, urlbase = os.path.join(urlbase, 'content'), webbase = content)
        debug.insertnamespace('cds', l_cds)
        l_wsroot.putChild('ContentDirectory', l_cds)
        l_cds = l_cds.control
        l_wsroot.putChild('ConnectionManager', ConnectionManagerServer())
        l_wsroot.putChild('root-device.xml', RootDevice())
        l_wsroot.putChild('content', content)

        # Purely to ensure some sane mime-types.  On MacOSX I need these.
        medianode = static.File('pymediaserv')
        medianode.contentTypes.update({
            # From: http://support.microsoft.com/kb/288102
            '.asf':    'video/x-ms-asf',
            '.asx':    'video/x-ms-asf',
            '.wma':    'audio/x-ms-wma',
            '.wax':    'audio/x-ms-wax',
            '.wmv':    'video/x-ms-wmv',
            '.wvx':    'video/x-ms-wvx',
            '.wm':    'video/x-ms-wm',
            '.wmx':    'video/x-ms-wmx',
            '.ts':    'video/mpeg',  # we may want this instead of mp2t
            '.m2t':    'video/mpeg',
            '.m2ts':    'video/mpeg',
            '.mp4':    'video/mp4',
            '.dat':    'video/mpeg',  # VCD tracks
            '.ogm':    'application/ogg',
            '.vob':    'video/mpeg',
        })
        del medianode

        l_site = server.Site(l_wsroot)
        reactor.listenTCP(listenPort, l_site)


def Init():
    print("UPnP_core Init")
    # make sure debugging is initalized first, other modules can be pulled in
    # before the "real" debug stuff is setup.
    log.startLogging(sys.stdout)
    debug.doDebugging(True)  # open up debugging port
    l_util = Utilities()
    l_util.load_modules()
    l_util.get_ip_address()
    CreateServers()

def Start():
    print("UPnP_core Start")
    # we need to do this after the children are there, since we send notifies
    g_ssdp.register('%s::upnp:rootdevice' % g_uuid,
                    'upnp:rootdevice',
                    urlbase + 'root-device.xml')
    g_ssdp.register(g_uuid,
                    g_uuid,
                    urlbase + 'root-device.xml')
    g_ssdp.register('%s::urn:schemas-upnp-org:device:MediaServer:1' % g_uuid,
                    'urn:schemas-upnp-org:device:MediaServer:1',
                    urlbase + 'root-device.xml')
    g_ssdp.register('%s::urn:schemas-upnp-org:service:ConnectionManager:1' % g_uuid,
                    'urn:schemas-upnp-org:device:ConnectionManager:1',
                    urlbase + 'root-device.xml')
    g_ssdp.register('%s::urn:schemas-upnp-org:service:ContentDirectory:1' % g_uuid,
                    'urn:schemas-upnp-org:device:ContentDirectory:1',
                    urlbase + 'root-device.xml')
    g_ssdp.register('%s::urn:schemas-upnp-org:service:LightingControl:1' % g_uuid,
                    'urn:schemas-upnp-org:device:LightingControl:1',
                    urlbase + 'root-device.xml')

def Stop():
    print("UPnP_core Stop")

# ## END
