#!/usr/bin/env python

"""

DBK Notes:

1. requires directory 'media' in this source directory.
"""

# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php
# Copyright 2005, Tim Potter <tpot@samba.org>
# Copyright 2006 John-Mark Gurney <jmg@funkthat.com>

__version__ = '$Change: 1230 $'
# $Id: //depot/python/pymeds/pymeds-0.5/pymediaserv#2 $

# make sure debugging is initalized first, other modules can be pulled in
# before the "real" debug stuff is setup.  (hmm I could make this a two
# stage, where we simulate a namespace to either be thrown away when the
# time comes, or merge into the correct one)
import UPnP_debug		# my debugging module
UPnP_debug.doDebugging(True)	# open up debugging port

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
modules = [
	'shoutcast',
	'pyvr',
	'dvd',
	'ZipStorage',
	'mpegtsmod',
	]
modmap = {}
for i in modules:
    modmap[i] = tryloadmodule(i)

for i in modules:
    UPnP_debug.insertnamespace(i, modmap[i])

from UPnP_DIDLLite import TextItem, AudioItem, VideoItem, ImageItem, Resource, StorageFolder
from UPnP_FSStorage import FSDirectory
import os
import os.path
import random
import socket
import string
import sys
from twisted.python import log
from twisted.internet import reactor

def generateuuid():
    if False: return 'uuid:asdflkjewoifjslkdfj'
    return ''.join([
	'uuid:'] + map(lambda x:
	random.choice(string.letters), xrange(20)))

#listenAddr = sys.argv[1]
#listenAddr = '192.168.1.39'
listenAddr = '127.0.0.1'    # DBK easier to debug this way

if len(sys.argv) > 2:
    listenPort = int(sys.argv[2])
    if listenPort < 1024 or listenPort > 65535:
        raise ValueError, 'port out of range'
else:
    listenPort = random.randint(10000, 65000)

listenPort = 12345  # DBK Forced for easier debugging

log.startLogging(sys.stdout)

# Create SSDP server

from UPnP_SSDP import SSDPServer, SSDP_PORT, SSDP_ADDR

s = SSDPServer()
UPnP_debug.insertnamespace('s', s)

port = reactor.listenMulticast(SSDP_PORT, s, listenMultiple=True)
port.joinGroup(SSDP_ADDR)
port.setLoopbackMode(0)		# don't get our own sends

uuid = generateuuid()
urlbase = 'http://%s:%d/' % (listenAddr, listenPort)

# Create SOAP server

from twisted.web import server, resource, static
from UPnP_ContentDirectory import ContentDirectoryServer
from UPnP_ConnectionManager import ConnectionManagerServer

class WebServer(resource.Resource):
	def __init__(self):
		resource.Resource.__init__(self)

class RootDevice(static.Data):
	def __init__(self):
		r = {
			'hostname': socket.gethostname(),
			'uuid': uuid,
			'urlbase': urlbase,
		}
		d = file(os.path.expanduser('~/media/root-device.xml')).read() % r
		static.Data.__init__(self, d, 'text/xml')

root = WebServer()
UPnP_debug.insertnamespace('root', root)
content = resource.Resource()
mediapath = os.path.expanduser('~/media')
if not os.path.isdir(mediapath):
	print >>sys.stderr, \
	    'Sorry, %s is not a directory, no content to serve.' % `mediapath`
	sys.exit(1)

# This sets up the root to be the media dir so we don't have to
# enumerate the directory
cds = ContentDirectoryServer('My Media Server', klass=FSDirectory,
    path=mediapath, urlbase=os.path.join(urlbase, 'content'), webbase=content)
UPnP_debug.insertnamespace('cds', cds)
root.putChild('ContentDirectory', cds)
cds = cds.control
root.putChild('ConnectionManager', ConnectionManagerServer())
root.putChild('root-device.xml', RootDevice())
root.putChild('content', content)


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

	#'.ts':	'video/mp2t',
	'.ts':	'video/mpeg',	# we may want this instead of mp2t
	'.m2t':	'video/mpeg',
	'.m2ts':	'video/mpeg',
	'.mp4':	'video/mp4',
	#'.mp4':	'video/mpeg',
	'.dat':	'video/mpeg',	# VCD tracks
	'.ogm':	'application/ogg',
	'.vob':	'video/mpeg',
	#'.m4a': 'audio/mp4',   # D-Link can't seem to play AAC files.
})
del medianode

site = server.Site(root)
reactor.listenTCP(listenPort, site)

# we need to do this after the children are there, since we send notifies
s.register('%s::upnp:rootdevice' % uuid,
		'upnp:rootdevice',
		urlbase + 'root-device.xml')

s.register(uuid,
		uuid,
		urlbase + 'root-device.xml')

s.register('%s::urn:schemas-upnp-org:device:MediaServer:1' % uuid,
		'urn:schemas-upnp-org:device:MediaServer:1',
		urlbase + 'root-device.xml')

s.register('%s::urn:schemas-upnp-org:service:ConnectionManager:1' % uuid,
		'urn:schemas-upnp-org:device:ConnectionManager:1',
		urlbase + 'root-device.xml')

s.register('%s::urn:schemas-upnp-org:service:ContentDirectory:1' % uuid,
		'urn:schemas-upnp-org:device:ContentDirectory:1',
		urlbase + 'root-device.xml')

# Main loop

def Init():
    pass

#reactor.run()
