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

__version__ = '1.00.00'

#import os
import os.path
import random
import socket
import string
import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.web import server, resource, static

import UPnP_debug		# my debugging module
#from UPnP_DIDLLite import TextItem, AudioItem, VideoItem, ImageItem, Resource, StorageFolder
from UPnP_FSStorage import FSDirectory
from UPnP_SSDP import SSDPServer, SSDP_PORT, SSDP_ADDR
from UPnP_ContentDirectory import ContentDirectoryServer
from UPnP_ConnectionManager import ConnectionManagerServer

listenAddr = '127.0.0.1'    # DBK easier to debug this way
listenPort = 12345  # DBK Forced for easier debugging
urlbase = 'http://%s:%d/' % (listenAddr, listenPort)

g_uuid = None
g_ssdp = None

# Modules to import, maybe config file or something?
def tryloadmodule(mod):
    try:
        return __import__(mod)
    except ImportError:
        #import traceback
        #traceback.print_exc()
        pass

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
    l_modmap[i] = tryloadmodule(i)

for i in l_modules:
    UPnP_debug.insertnamespace(i, l_modmap[i])

def generateuuid():
    if False: return 'uuid:asdflkjewoifjslkdfj'
    return ''.join([
	'uuid:'] + map(lambda x:
	random.choice(string.letters), xrange(20)))

log.startLogging(sys.stdout)







# Create SOAP server
class WebServer(resource.Resource):
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

l_wsroot = WebServer()
UPnP_debug.insertnamespace('root', l_wsroot)
content = resource.Resource()
mediapath = os.path.expanduser('~/media')
if not os.path.isdir(mediapath):
    print >>sys.stderr, \
	    'Sorry, %s is not a directory, no content to serve.' % `mediapath`
    sys.exit(1)

# This sets up the root to be the media dir so we don't have to
# enumerate the directory
l_cds = ContentDirectoryServer('My Media Server', klass=FSDirectory,
    path=mediapath, urlbase=os.path.join(urlbase, 'content'), webbase=content)
UPnP_debug.insertnamespace('cds', l_cds)
l_wsroot.putChild('ContentDirectory', l_cds)
l_cds = l_cds.control
l_wsroot.putChild('ConnectionManager', ConnectionManagerServer())
l_wsroot.putChild('root-device.xml', RootDevice())
l_wsroot.putChild('content', content)


# Purely to ensure some sane mime-types.  On MacOSX I need these.
medianode = static.File('pymediaserv')
medianode.contentTypes.update( {
	# From: http://support.microsoft.com/kb/288102
	'.asf':	'video/x-ms-asf',
	'.asx':	'video/x-ms-asf',
	'.wma':	'audio/x-ms-wma',
	'.wax':	'audio/x-ms-wax',
	'.wmv':	'video/x-ms-wmv',
	'.wvx':	'video/x-ms-wvx',
	'.wm':	'video/x-ms-wm',
	'.wmx':	'video/x-ms-wmx',
	'.ts':	'video/mpeg',	# we may want this instead of mp2t
	'.m2t':	'video/mpeg',
	'.m2ts':	'video/mpeg',
	'.mp4':	'video/mp4',
	'.dat':	'video/mpeg',	# VCD tracks
	'.ogm':	'application/ogg',
	'.vob':	'video/mpeg',
})
del medianode

l_site = server.Site(l_wsroot)
reactor.listenTCP(listenPort, l_site)

class CreateServers(object):
    """
    """

    def __init__(self):
        # Create SSDP server
        self.create_ssdp_server()
        global g_uuid
        g_uuid = generateuuid()

    def create_ssdp_server(self):
        global g_ssdp
        g_ssdp = SSDPServer()
        UPnP_debug.insertnamespace('s', g_ssdp)
        l_port = reactor.listenMulticast(SSDP_PORT, g_ssdp, listenMultiple = True)
        l_port.joinGroup(SSDP_ADDR)
        l_port.setLoopbackMode(0)		# don't get our own sends


def Init():
    print "UPnP_core Init"
    # make sure debugging is initalized first, other modules can be pulled in
    # before the "real" debug stuff is setup.
    UPnP_debug.doDebugging(True)	# open up debugging port
    CreateServers()

def Start():
    print "UPnP_core Start"
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
    print "UPnP_core Stop"

### END
