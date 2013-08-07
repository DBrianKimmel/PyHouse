#! /usr/bin/env python
#-*- coding: iso-8859-1 -*-

"""Web server module.

This is a Main Module - always present.

Open a port (8580 default) that will allow web browsers to control the
PyHouse system.  This will be an AJAX/COMET system using nevow athena.

On initial startup allow a house to be created
    then rooms
    then light controllers
        and lights
        and buttons
        and scenes
    then schedules

Do not require reloads, auto change PyHouse on the fly.
"""

# Import system type stuff
import logging
import os
from twisted.internet import reactor
from twisted.python.filepath import FilePath
from nevow import appserver

# Import PyMh files and modules.
from src import web
from src.web import web_utils
from src.web import web_mainpage

# Handy helper for finding external resources nearby.
webdir = FilePath(web.__file__).parent().preauthChild
# Some absolute paths to resources
imagepath = webdir('images').path
jspath = webdir('js').path
templatepath = webdir('template').path


g_debug = 0
# 0 = off
# 1 = Additional logging
# 2 = major routine entry
# 3 = Basic data
# 4 = ajax data
# + = NOT USED HERE
g_logger = None


# Only to move the eclipse error flags to one small spot
listenTCP = reactor.listenTCP


class WebData(object):
    """
    """
    def __init__(self):
        self.WebPort = 8580
        self.Logins = {} # a dict of login_names as keys and encrypted passwords as values - see web_login for details.

    def __str__(self):
        l_ret = "WebData:: "
        l_ret += "WebPort:{0:}\n".format(self.WebPort)
        return l_ret

    def __repr__(self):
        l_ret = "{"
        l_ret += "'WebPort':'{0:}'".format(self.WebPort)
        l_ret += "}"
        return l_ret


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
        self.web_data = web_utils.WebUtilities().read_web_xml(self.web_data, p_pyhouses_obj.XmlRoot)
        #l_site_dir = os.path.split(os.path.abspath(__file__))[0]
        l_site_dir = None
        l_site = appserver.NevowSite(web_mainpage.TheRoot('/', l_site_dir, p_pyhouses_obj))
        listenTCP(self.web_data.WebPort, l_site)
        l_msg = "Port:{0:}, Path:{1:}".format(self.web_data.WebPort, l_site_dir)
        if g_debug >= 2:
            print "web_server.Start() - {0:}".format(l_msg)
        g_logger.info("Started - {0:}".format(l_msg))
        return self.web_data

    def Stop(self):
        if g_debug >= 2:
            print "web_server.API.Stop()"
        l_xml = web_utils.WebUtilities().write_web_xml(self.web_data)
        return l_xml

    def Reload(self, _p_pyhouses_obj):
        if g_debug >= 2:
            print "web_server.API.Reload()"
        l_xml = web_utils.WebUtilities().write_web_xml(self.web_data)
        return l_xml

# ## END DBK
