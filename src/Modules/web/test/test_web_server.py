"""
@name: PyHouse/src/Modules/web/test/test_web_server.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on Apr 8, 2013
@license: MIT License
@summary: This module is for AMP request/response protocol

"""

# Import system type stuff
from twisted.trial import unittest
# from twisted.trial import itrial
from twisted.test import proto_helpers
# from twisted.internet.endpoints import SSL4ServerEndpoint
from twisted.internet.defer import succeed
from twisted.web import server
from twisted.web.test.test_web import DummyRequest

# Import PyMh files and modules.
from Modules.web import web_server


class SmartDummyRequest(DummyRequest):
    def __init__(self, method, url, args = None, headers = None):
        DummyRequest.__init__(self, url.split('/'))
        self.method = method
        self.headers.update(headers or {})

        # set args
        args = args or {}
        for k, v in args.items():
            self.addArg(k, v)


    def value(self):
        return "".join(self.written)


class DummySite(server.Site):
    def get(self, url, args = None, headers = None):
        return self._request("GET", url, args, headers)


    def post(self, url, args = None, headers = None):
        return self._request("POST", url, args, headers)


    def _request(self, method, url, args, headers):
        request = SmartDummyRequest(method, url, args, headers)
        resource = self.getResourceFor(request)
        result = resource.render(request)
        return self._resolveResult(request, result)


    def _resolveResult(self, request, result):
        if isinstance(result, str):
            request.write(result)
            request.finish()
            return succeed(request)
        elif result is server.NOT_DONE_YET:
            if request.finished:
                return succeed(request)
            else:
                return request.notifyFinish().addCallback(lambda _: request)
        else:
            raise ValueError("Unexpected return value: %r" % (result,))


class Test(unittest.TestCase):

    def setUp(self):
        self.web_server = web_server.API()
        factory = RemoteCalculationFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def tearDown(self):
        pass

    def test_001_Start(self):
        self.web_server.Start()

    def test_root_page(self):
        pass

# ## END DBK
