"""
@name:      Modules/Housing/Scheduling/auto_update.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@note:      Created on Dec 31, 2013
@license:   MIT License
@summary:   Handle the automatic updating of PyHouse

This module automatically updates PyHouse

"""

__updated__ = '2019-07-09'
__version_info__ = (19, 5, 1)
__version__ = '.'.join(map(str, __version_info__))

# strategy:
#
# if there is a VERSION file, use its contents. otherwise, call git to
# get a version string. if that also fails, use 'latest'.
#

# Import system type stuff
import jsonpickle
# from twisted.web.client import getPage
from twisted.internet import ssl, task, protocol, endpoints
from twisted.internet.defer import Deferred, inlineCallbacks  # , succeed
from twisted.internet.protocol import ClientFactory, Factory, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.python.filepath import FilePath
from twisted.python.modules import getModule
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

# Import PyHouse files

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Auto_Update    ')

VERSION_PATH = '../../../../../VERSION'
REPOSITORY = b'https://raw.github.com/DBrianKimmel/PyHouse/Project/Version'
REPOSITORY_PATH = 'Project/VERSION'


def _find_pyhouse_version_file():
    """
    Find the normalized VERSION file name
    PyHouse/Project/src/VERSION
    """
    l_file = FilePath(VERSION_PATH)
    return l_file


class FindLocalVersion(object):
    """ Find out what version that we are.
    """

    def __init__(self):
        l_name = self.get_filename()
        _l_version = self.get_version(l_name)

    def get_filename(self):
        return FilePath(VERSION_PATH)

    def get_version(self, p_name):
        """
        @return: a bytestream of the version
        """
        l_file = p_name.open()
        l_version = l_file.read()
        return l_version


class GithubProtocol(Protocol):
    """ A minimal protocol for the Hue Hub.
    """

    m_finished = None
    m_remaining = 0

    def __init__(self, p_finished):
        """
        @param p_finished: is a deferred that ????
        """
        self.m_finished = p_finished
        self.m_remaining = 1024 * 10  # Allow for 10kb response

    def dataReceived(self, p_bytes):
        if self.m_remaining > 0:
            l_display = p_bytes[:self.m_remaining].decode("utf8")  # Get the string
            l_json = jsonpickle.decode(l_display)
            LOG.debug('\n===== Body =====\n{}\n'.format(l_json))
            print('\n===== Body =====\n{}\n'.format(l_json))
            self.m_remaining -= len(l_display)

    def connectionLost(self, p_reason):
        l_msg = p_reason.getErrorMessage()  # this gives a tuple of messages (I think)
        LOG.debug('Finished receiving body: {}'.format(p_reason))
        print('Finished receiving body: {}'.format(p_reason))
        LOG.debug('Finished receiving body: {}'.format("\t".join(str(x) for x in l_msg)))
        print('Finished receiving body: {}'.format("\t".join(str(x) for x in l_msg)))
        self.m_finished.callback(None)


class FindRepositoryVersion(object):
    """ Check the version in the repository
    """

    def __init__(self, p_pyhouse_obj):
        """
        Agent is a very basic HTTP client.  It supports I{HTTP} and I{HTTPS} scheme URIs.

        """
        self.m_headers = Headers({'User-Agent': ['AutoUpdate Web Client']})
        if p_pyhouse_obj != None:
            self.m_pyhouse_obj = p_pyhouse_obj
            self.m_hue_agent = Agent(p_pyhouse_obj._Twisted.Reactor)
            LOG.info('Initialized')
            print('Initialized')
        self.m_version = '0.0.0'

    def get_uri(self):
        return REPOSITORY

    def get_repository(self):
        """ Issue a request for information
        It will arrive later via a deferred.
        """

        def cb_Response(p_response):
            LOG.debug('Response Code: {} {}'.format(p_response.code, p_response.phrase))
            print('Response Code: {} {}'.format(p_response.code, p_response.phrase))
            d_finished = Deferred()
            p_response.deliverBody(GithubProtocol(d_finished))
            return d_finished

        l_agent_d = self.m_hue_agent.request(
            b'GET',
            self.get_uri(),
            self.m_headers,
            None)
        l_agent_d.addCallback(cb_Response)
        # HueDecode().decode_get()
        return l_agent_d

    def get_file(self):
        l_file = self.get_repository()
        return l_file

    def print_page(self, p_html):
        """
        """
        print(p_html)
        pass

    def get_page(self):
        """
        """
        l_defer = self.get_uri
        l_defer.addCallback(self.print_page)

    def get_version(self):
        return self.m_version

    def parseHtml(self, p_html):
        # l_parser = etree.HTMLParser(encoding='utf8')
        # tree = etree.parse(StringIO.StringIO(html), parser)
        # return tree
        pass

    def extractTitle(self, p_tree):
        # titleText = unicode(tree.xpath("//title/text()")[0])
        # return titleText
        pass

    # d = getPage('http://www.google.com')
    # d.addCallback(parseHtml)
    # d.addCallback(extraTitle)
    # d.addBoth(println)


class Utility(object):
    """
    """

    def compare_versions(self, _p_local_ver, _p_repos_ver):
        return True


class EchoClient(LineReceiver):
    end = b"Bye-bye!"

    def connectionMade(self):
        self.sendLine(b"Hello, world!")
        self.sendLine(b"What a fine day it is.")
        self.sendLine(self.end)

    def lineReceived(self, line):
        print("receive:", line)
        if line == self.end:
            self.transport.loseConnection()


class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)

    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)


class API(Utility):
    """
    """

    @inlineCallbacks
    def do_ssl(self, p_reactor):
        l_factory = Factory.forProtocol(self.EchoClient)
        l_certData = getModule(__name__).filePath.sibling('public.pem').getContent()
        l_authority = ssl.Certificate.loadPEM(l_certData)
        l_options = ssl.optionsForClientTLS(u'example.com', l_authority)
        l_endpoint = endpoints.SSL4ClientEndpoint(p_reactor, 'localhost', 8000, l_options)
        echoClient = yield l_endpoint.connect(l_factory)
        d_done = Deferred()
        echoClient.connectionLost = lambda reason: d_done.callback(None)
        yield d_done

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

# ## END DBK
