"""
-*- test-case-name: PyHouse.Modules.Web.test.test_web_server -*-

@name:      PyHouse/src/Modules/Web/web_server.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2012-2019 by D. Brian Kimmel
@note:      Created on Apr 3, 2012
@license:   MIT License
@summary:   This module provides the web server(s) service of PyHouse.

This is a Main Module - always present.

Open 2 web servers.
    open server on port 8580.
    Secure (TLS) server on port 8588 (optional)

Present a Login screen.  A successful login is required to get a main menu screen.
Failure to log in will keep the user on a login screen.

On initial startup allow a house to be created
    then rooms
    then light controllers
        and lights
        and buttons
        and scenes
    then schedules

Do not require reloads, auto change PyHouse on the fly.
"""

__updated__ = '2019-06-25'

#  Import system type stuff
from twisted.internet import endpoints
# from twisted.web.resource import Resource
from twisted.web.server import Site
# from twisted.web.template import Element, XMLString, renderer
# from werkzeug.contrib.jsrouting import render_template
from klein import Klein  # , route

#  Import PyMh files and modules.
from Modules.Computer.Web import web_utils
from Modules.Computer.Web.web_mainpage import MainPage

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.WebServer      ')

klein_app = Klein()


@klein_app.route('/')
def root(_request):
    return MainPage()


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

    def start_webservers(self, p_pyhouse_obj):
        """ Start Kline web server()
        We will always start a TCP server (for now)
        We may optionally start a TLS server.
        """
        self.start_tcp(p_pyhouse_obj, 'localhost', p_pyhouse_obj.Computer.Web.WebPort)
        self.start_tls(p_pyhouse_obj, None, p_pyhouse_obj.Computer.Web.SecurePort)
        LOG.info("Started Web Server(s)")

    def start_tcp(self, p_pyhouse_obj, p_interface, p_port):
        """ Start an HTTP server

        Supported arguments: port, interface, backlog.
        interface and backlog are optional.
        interface is an IP address (belonging to the IPv4 address family) to bind to.

        For example:
        tcp:port=80:interface=192.168.1.1.
        """

        def cb_listen(p_arg):
            # LOG.debug('{}'.format(PrettyFormatAny.form(p_arg, 'Arg', 190)))
            pass

        def eb_listen_error(p_reason):
            LOG.error(p_reason)
            pass

        l_reactor = p_pyhouse_obj._Twisted.Reactor
        _l_app = p_pyhouse_obj._Twisted.Application
        # l_app = Klein()
        p_pyhouse_obj._Twisted.Application = klein_app
        # LOG.debug('{}'.format(PrettyFormatAny.form(klein_app, 'KleinApp', 190)))
        l_endpoint_description = 'tcp'
        l_endpoint_description += ':port={}'.format(p_port)
        if p_interface != None:
            l_endpoint_description += ':interface={}'.format(p_interface)
        LOG.debug("TCP Endpoint: {}".format(l_endpoint_description))

        l_endpoint = endpoints.serverFromString(l_reactor, l_endpoint_description)
        # LOG.debug('{}'.format(PrettyFormatAny.form(l_endpoint, 'Endpoint', 190)))

        l_server = l_endpoint.listen(Site(klein_app.resource()))
        l_server.addCallback(cb_listen)
        l_server.addErrback(eb_listen_error)
        # LOG.debug('{}'.format(PrettyFormatAny.form(l_server, 'Server', 190)))

        p_pyhouse_obj.Computer.Web.WebServer = l_server
        # print(PrettyFormatAny.form(l_server, 'WebServer'))
        LOG.info("Started TCP web server - {}".format(l_endpoint))

    def start_tls(self, p_pyhouse_obj, p_host, p_port):
        """ Start an HTTPS server (TLS)

        All TCP arguments are supported, plus: certKey, privateKey, extraCertChain, sslmethod, and dhParameters.

        certKey (optional, defaults to the value of privateKey) gives a filesystem path to a certificate (PEM format).
        privateKey gives a filesystem path to a private key (PEM format).
        extraCertChain gives a filesystem path to a file with one or more concatenated certificates in PEM format that establish the chain from a root CA to the one that signed your certificate.
        sslmethod indicates which SSL/TLS version to use (a value like TLSv1_METHOD).
        dhParameters gives a filesystem path to a file in PEM format with parameters that are required for Diffie-Hellman key exchange.

        Since the this is required for the DHE-family of ciphers that offer perfect forward secrecy (PFS), it is recommended to specify one.

        Such a file can be created using openssl dhparam -out dh_param_1024.pem -2 1024.
        Please refer to OpenSSL’s documentation on dhparam for further details.

        For example,;
            ssl:port=443:privateKey=/etc/ssl/server.pem:extraCertChain=/etc/ssl/chain.pem:sslmethod=SSLv3_METHOD:dhParameters=dh_param_1024.pem.

        You can use the endpoint: feature with TCP if you want to connect to a host name;
         for example, if your DNS is not working, but you know that the IP address 7.6.5.4 points to awesome.site.example.com, you could specify:
            tls:awesome.site.example.com:443:endpoint=tcp\:7.6.5.4\:443.
        """
        _l_reactor = p_pyhouse_obj._Twisted.Reactor
        _l_app = p_pyhouse_obj._Twisted.Application
        l_endpoint_description = 'tls:'
        if p_host != None:
            l_endpoint_description += '{}:'.format(p_host)
        if p_port != None:
            l_endpoint_description += '{}'.format(p_port)
        LOG.debug("TLS Endpoint: {}".format(l_endpoint_description))
        # l_certData = getModule(__name__).filePath.sibling('server.pem').getContent()
        # l_certificate = ssl.PrivateCertificate.loadPEM(l_certData)
        # l_factory = protocol.Factory.forP rotocol(echoserv.Echo)
        # p_pyhouse_obj._Twisted.Reactor.listenSSL(8000, l_factory, l_certificate.options())
        return


class API(Utility):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.State = web_utils.WS_IDLE
        self.m_web_running = False
        p_pyhouse_obj._Twisted.Application = Klein()
        LOG.info('Initialized.')

    def LoadXml(self, p_pyhouse_obj):
        pass

    def Start(self):
        LOG.info('Starting web servers.')
        self.start_webservers(self.m_pyhouse_obj)
        LOG.info('Started.')

    def SaveXml(self, p_xml):
        pass

    def Stop(self):
        LOG.info('Stopped.')

#  ## END DBK
