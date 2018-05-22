"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Computer/Web/websocket_server.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/Web/websocket_server.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@note:      Created on Apr 17, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2017-07-24'

#  Import system type stuff
import http.cookies  #
import json
import urllib
from twisted.internet import ssl
from twisted.web.static import File
from twisted.web.server import Site
from autobahn.util import newid, utcnow
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

WEBSOCKET_PORT = 8581
ENDPOINT_WEBSOCKET_SERVER = 'tcp:port={}'.format(WEBSOCKET_PORT)
LOG = Logger.getLogger('PyHouse.WebSockets     ')


class WebSockServerProtocol(WebSocketServerProtocol):
    """
    Inherits from autobahn.twisted.websocket

    This is the protocol for the PyHouse Websocket server
    """

    def onConnect(self, request):
        """
        This is called during the initial WebSocket opening handshake.
        """
        LOG.debug("some request connected {}".format(request))
        protocol, headers = None, {}
        # our cookie tracking ID
        self._cbtid = None
        # see if there already is a cookie set ..
        if 'cookie' in request.headers:
            try:
                cookie = http.cookies.SimpleCookie()
                cookie.load(str(request.headers['cookie']))
            except http.cookies.CookieError:
                pass
            else:
                if 'cbtid' in cookie:
                    cbtid = cookie['cbtid'].value
                    if cbtid in self.factory._cookies:
                        self._cbtid = cbtid
                        LOG.warn("Cookie already set: %s" % self._cbtid)
        # if no cookie is set, create a new one ..
        if self._cbtid is None:
            self._cbtid = newid()
            maxAge = 86400
            cbtData = {'created': utcnow(),
                       'authenticated': None,
                       'maxAge': maxAge,
                       'connections': set()}
            self.factory._cookies[self._cbtid] = cbtData
            # do NOT add the "secure" cookie attribute! "secure" refers to the scheme of the Web page that triggered the WS, not WS itself!!
            headers['Set-Cookie'] = 'cbtid=%s;max-age=%d' % (self._cbtid, maxAge)
            LOG.warn("Setting new cookie: %s" % self._cbtid)
        # add this WebSocket connection to the set of connections associated with the same cookie
        self.factory._cookies[self._cbtid]['connections'].add(self)
        # accept the WebSocket connection, speaking subprotocol `protocol` and setting HTTP headers `headers`
        return (protocol, headers)

    def onOpen(self):
        """
        This is called when initial WebSocket opening handshake has been completed.
        """
        # see if we are authenticated ..
        authenticated = self.factory._cookies[self._cbtid]['authenticated']
        if not authenticated:
            # .. if not, send authentication request
            self.sendMessage(json.dumps({'cmd': 'AUTHENTICATION_REQUIRED'}))
        else:
            # .. if yes, send info on authenticated user
            self.sendMessage(json.dumps({'cmd': 'AUTHENTICATED', 'email': authenticated}))

    def onClose(self, wasClean, code, reason):
        """
        This is called when WebSocket connection is gone
        """
        # remove this connection from list of connections associated with same cookie
        self.factory._cookies[self._cbtid]['connections'].remove(self)
        # if list gets empty, possibly do something ..
        if not self.factory._cookies[self._cbtid]['connections']:
            LOG.warn("All connections for {} gone".format(self._cbtid))

    def onMessage(self, payload, isBinary):
        """
        This is called when we receive a WebSocket message
        """
        if not isBinary:
            msg = json.loads(payload)
            if msg['cmd'] == 'AUTHENTICATE':
                # The client did it's Mozilla Persona authentication thing and now wants to verify the authentication and login.
                assertion = msg.get('assertion')
                audience = msg.get('audience')
                # To verify the authentication, we need to send a HTTP/POST to Mozilla Persona.
                # When successful, Persona will send us back something like:
                # {
                #    "audience": "http://192.168.1.130:8080/",
                #    "expires": 1393681951257,
                #    "issuer": "gmail.login.persona.org",
                #    "email": "tobias.oberstein@gmail.com",
                #    "status": "okay"
                # }
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                body = urllib.parse.urlencode({'audience': audience, 'assertion': assertion})
                from twisted.web.client import getPage
                d = getPage(url = "https://verifier.login.persona.org/verify",
                            method = 'POST',
                            postdata = body,
                            headers = headers)
                LOG.warn("Authentication request sent.")

                def done(res):
                    res = json.loads(res)
                    if res['status'] == 'okay':
                        # Mozilla Persona successfully authenticated the user
                        # remember the user's email address. this marks the cookie as authenticated
                        self.factory._cookies[self._cbtid]['authenticated'] = res['email']
                        # inform _all_ WebSocket connections of the successful auth.
                        msg = json.dumps({'cmd': 'AUTHENTICATED', 'email': res['email']})
                        for proto in self.factory._cookies[self._cbtid]['connections']:
                            proto.sendMessage(msg)
                        LOG.warn("Authenticated user {}".format(res['email']))
                    else:
                        LOG.warn("Authentication failed: {}".format(res.get('reason')))
                        self.sendMessage(json.dumps({'cmd': 'AUTHENTICATION_FAILED', 'reason': res.get('reason')}))
                        self.sendClose()

                def error(err):
                    LOG.warn("Authentication request failed: {}".format(err.value))
                    self.sendMessage(json.dumps({'cmd': 'AUTHENTICATION_FAILED', 'reason': str(err.value)}))
                    self.sendClose()

                d.addCallbacks(done, error)
            elif msg['cmd'] == 'LOGOUT':
                # user wants to logout ..
                if self.factory._cookies[self._cbtid]['authenticated']:
                    self.factory._cookies[self._cbtid]['authenticated'] = False
                    # inform _all_ WebSocket connections of the logout
                    msg = json.dumps({'cmd': 'LOGGED_OUT'})
                    for proto in self.factory._cookies[self._cbtid]['connections']:
                        proto.sendMessage(msg)
            else:
                LOG.debug("unknown command {}".format(msg))
        LOG.debug("websocket message rxed {}".format(payload))


class ClientConnections(object):
    """This class keeps track of all the connected browsers.
    We can update the browser via COMET when a controlled device changes.
    (Light On/Off, Pool water low, Garage Door open/Close ...)
    """

    def __init__(self):
        self.ConnectedBrowsers = []

    def add_browser(self, p_login):
        self.ConnectedBrowsers.append(p_login)
        LOG.warn('Connected to: {}'.format(PrettyFormatAny.form(p_login, 'Login')))


class Utility(ClientConnections):

    def start_websocket_server(self, p_pyhouse_obj):
        """ Setup for starting a web socket server (encrypted or not).
        """
        l_port = WEBSOCKET_PORT  # p_pyhouse_obj.Computer.Web.WebPort
        l_addr = u'ws://127.0.0.1:{}'.format(l_port)
        l_factory = WebSocketServerFactory(l_addr)
        l_factory.protocol = WebSockServerProtocol
        # websockets resource on "/ws" path
        l_resource = WebSocketResource(l_factory)
        l_root = File('.')
        l_root.putChild(u"ws", l_resource)
        l_site = Site(l_root)
        self.m_pyhouse_obj.Twisted.Reactor.listenTCP(l_port, l_site)
        l_site_dir = None
        l_msg = "Port:{}, Path:{}".format(l_port, l_site_dir)
        LOG.info("Started - {}".format(l_msg))

    def start_non_tls(self, p_pyhouse_obj, p_site, p_port):
        """ Start a non-encrypted websocket server.
        """
        p_pyhouse_obj.Twisted.Reactor.listenTCP(p_port, p_site)

    def start_tls(self, p_pyhouse_obj):
        """ Start an encrypted websocket server.
        """
        # l_certData = getModule(__name__).filePath.sibling('server.pem').getContent()
        # l_certificate = ssl.PrivateCertificate.loadPEM(l_certData)
        # l_factory = protocol.Factory.forProtocol(echoserv.Echo)
        # p_pyhouse_obj.Twisted.Reactor.listenSSL(WEBSOCKET_PORT, l_factory, l_certificate.options())
        # return defer.Deferred()
        pass


class API(Utility):

    m_contextFactory = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized.')
        try:
            self.m_contextFactory = ssl.DefaultOpenSSLContextFactory('/etc/pyhouse/keys/server.key', '/etc/pyhouse/keys/server.crt')
        except:
            LOG.warn("SSL not available.")
            self.m_contextFactory = None

    def LoadXml(self, p_pyhouse_obj):
        pass

    def Start(self):
        LOG.info('Starting websocket server.')
        self.start_websocket_server(self.m_pyhouse_obj)
        LOG.info('Started.')

    def SaveXml(self, p_xml):
        pass

    def Stop(self):
        LOG.info('Stopped.')

# ## END DBK
