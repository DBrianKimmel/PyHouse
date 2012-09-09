# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2005, Tim Potter <tpot@samba.org>

# Connection Manager service

"""
The ConnectionManager service is used by the ControlPoint to carry out the following three actions:

Perform capability matching between source/server devices and sink/renderer devices
Find information about currently ongoing transfers in the network
Setup and teardown connections between devices (when required by the streaming protocol)

"""

from twisted.python import log
from twisted.web import resource, static, soap
from UPnP_upnp import UPnPPublisher

class ConnectionManagerControl(UPnPPublisher):
	def soap_GetProtocolInfo(self, *args, **kwargs):
		log.msg('GetProtocolInfo(%s, %s)' % (`args`, `kwargs`))

	def soap_PrepareForConnection(self, *args, **kwargs):
		log.msg('PrepareForConnection(%s, %s)' % (`args`, `kwargs`))

	def soap_ConnectionComplete(self, *args, **kwargs):
		log.msg('ConnectionComplete(%s, %s)' % (`args`, `kwargs`))

	def soap_GetCurrentConnectionIDs(self, *args, **kwargs):
		log.msg('GetCurrentConnectionIDs(%s, %s)' % (`args`, `kwargs`))

	def soap_GetCurrentConnectionInfo(self, *args, **kwargs):
		log.msg('GetProtocolInfo(%s, %s)' % (`args`, `kwargs`))

class ConnectionManagerServer(resource.Resource):
	def __init__(self):
		resource.Resource.__init__(self)
		self.putChild('scpd.xml', static.File('connection-manager-scpd.xml'))
		self.putChild('control', ConnectionManagerControl())
