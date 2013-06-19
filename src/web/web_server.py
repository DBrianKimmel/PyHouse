#!/usr/bin/python

"""Web server module.
This is a Main Module - always present.

TODO: format doc strings to Epydoc standards.
"""

# Import system type stuff
import logging
import os
from twisted.internet import reactor
from twisted.python import util
from nevow import appserver
from nevow import athena
from twisted.python.util import sibpath
from nevow.loaders import xmlfile
from nevow.athena import LiveElement, expose

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.web import web_rootmenu



g_debug = 5
# 0 = off
# 1 = Additional logging
# 2 = major routine entry
# 3 = Basic data

g_logger = None

SUBMIT = '_submit'
BUTTON = 'post_btn'

# Only to move the eclipse error flags to one small spot
listenTCP = reactor.listenTCP


"""

<div xmlns:nevow="http://nevow.com/ns/nevow/0.1"
    xmlns:athena="http://divmod.org/ns/athena/0.7"
    nevow:render="liveElement">
    <h2>Chatter Element</h2>
    <form name="chatBox">
        <athena:handler event="onsubmit" handler="doSay" />
        <div name="scrollArea"
             style="border: 1px solid gray; padding: 5; margin: 5">
        </div>
        <div name="sendLine" style="display: none">
      <input name="userMessage" /><input type="submit" value="Send" />
    </div>
    </form>
    <form name="chooseBox">
        <athena:handler event="onsubmit" handler="doSetUsername" />
        Choose your username: <input name="username" />
        <input type="submit" name="GO" value="Enter"/>
    </form>
    <div name="loggedInAs" style="display:none"><span>Logged in as </span></div>
</div>

"""

class WebData(object):
    """
    """
    def __init__(self):
        self.WebPort = 8580


class ChatterElement(LiveElement):

    docFactory = xmlfile(sibpath(__file__, 'template.html'))
    jsClass = u'ChatThing.ChatterWidget'

    def __init__(self, room):
        self.room = room

    def setUsername(self, username):
        self.username = username
        message = ' * user ' + username + ' has joined the room'
        self.room.wall(message)

    setUsername = expose(setUsername)

    def say(self, message):
        self.room.tellEverybody(self, message)

    say = expose(say)

    def wall(self, message):
        self.callRemote('displayMessage', message)

    def hear(self, username, what):
        self.callRemote('displayUserMessage', username, what)


class API(object):

    def __init__(self):
        global g_logger
        g_logger = logging.getLogger('PyHouse.WebServ ')
        self.web_data = WebData()
        if g_debug >= 2:
            print "web_server.API()"
        g_logger.info("Initialized")

    def Start(self, p_pyhouses_obj):
        if g_debug >= 2:
            print "web_server.API.Start()"
        if g_debug >= 3:
            print "    ", p_pyhouses_obj
        self.m_pyhouses_obj = p_pyhouses_obj
        web_utils.WebUtilities().read_web_xml(self.web_data, p_pyhouses_obj.XmlRoot)
        l_site_dir = os.path.split(os.path.abspath(__file__))[0]
        l_site = appserver.NevowSite(web_rootmenu.RootPage('/', p_pyhouses_obj))
        listenTCP(self.web_data.WebPort, l_site)
        if g_debug >= 2:
            print "web_server.Start() - Port:{0:}, Path:{1:}".format(self.web_data.WebPort, l_site_dir)
        g_logger.info("Started.")
        return self.web_data

    def Stop(self):
        if g_debug >= 2:
            print "web_server.API.Stop()"

    def Reload(self, p_pyhouses_obj):
        if g_debug >= 2:
            print "web_server.API.Reload()"

# ## END DBK
