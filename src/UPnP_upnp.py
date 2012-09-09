# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2005, Tim Potter <tpot@samba.org>
# Copyright 2006-2007 John-Mark Gurney <jmg@funkthat.com>

__version__ = '$Change: 1227 $'
# $Id: //depot/python/pymeds/pymeds-0.5/upnp.py#1 $

from twisted.web import soap
from twisted.python import log

from types import *

import UPnP_soap_lite

class errorCode(Exception):
	def __init__(self, status):
		self.status = status

class UPnPPublisher(soap.SOAPPublisher):
	"""UPnP requires OUT parameters to be returned in a slightly
	different way than the SOAPPublisher class does."""

	namespace = None

	def _gotResult(self, result, request, methodName):
		ns = self.namespace
		if ns:
			meth = "{%s}%s" % (ns, methodName)
		else:
			meth = methodName
		response = soap_lite.build_soap_call(meth, result,
		    is_response=True, p_encoding=None)
		self._sendResponse(request, response)

	def _gotError(self, failure, request, methodName):
		e = failure.value
		status = 500
		if isinstance(e, errorCode):
			status = e.status
		else:
			failure.printTraceback(file = log.logfile)
		response = soap_lite.build_soap_error(status)
		self._sendResponse(request, response, status=status)
