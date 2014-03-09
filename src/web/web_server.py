#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

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
from nevow import appserver
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from src.web import web_utils
from src.web import web_mainpage
from src.utils import xml_tools

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')
imagepath = os.path.join(webpath, 'images')
jspath = os.path.join(webpath, 'js')


g_debug = 0
# 0 = off
# 1 = Additional logging
# 2 = major routine entry
# 3 = Basic data
# 4 = ajax data
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.WebServer   ')


# Only to move the eclipse error flags to one small spot
listenTCP = reactor.listenTCP


class WebData(object):
    """
    """
    def __init__(self):
        self.WebPort = 8580
        self.Logins = {}  # a dict of login_names as keys and encrypted passwords as values - see web_login for details.

    def __str__(self):
        l_ret = "WebData:: "
        l_ret += "WebPort:{0:}\n".format(self.WebPort)
        return l_ret

    def reprJSON(self):
        return dict(Port = self.WebPort)


class ClientConnections(object):
    """This class keeps track of all the connected browsers.
    We can update the browser via COMET when a controlled device changes.
    (Light On/Off, Pool water low, Garage Door open/Close ...)
    """
    def __init__(self):
        self.ConnectedBrowsers = []

    def add_browser(self, p_login):
        self.ConnectedBrowsers.append(p_login)


class WebUtility(xml_tools.ConfigFile):

    def read_web_xml(self, p_web_obj, p_root_xml):
        try:
            l_sect = p_root_xml.find('Web')
            l_sect.find('WebPort')
        except AttributeError:
            if g_debug >= 0:
                g_logger.error("web_server.read_web_xml() - ERROR in finding Web/WebPort, Creating entry {0:}".format(l_sect))
            l_sect = ET.SubElement(p_root_xml, 'Web')
            ET.SubElement(l_sect, 'Port').text = '8580'
            self.put_int_attribute(l_sect, 'WebPort', 8580)
            p_web_obj.WebPort = 8580
            l_logs = ET.SubElement(l_sect, 'Logins')
            l_login = ET.SubElement(l_logs, 'Login')
            l_login.set('Name', 'admin')
            l_login.set('Key', '0')
            l_login.set('Active', True)
            ET.SubElement(l_login, 'Password').text = '12admin34'
            return
        p_web_obj.WebPort = l_sect.findtext('WebPort')
        p_web_obj.WebPort = 8580
        # p_web_obj.WebPort = self.get_int_from_xml(l_sect, 'WebPort')
        return

    def write_web_xml(self, p_web_data):
        l_web_xml = ET.Element("Web")
        self.put_int_attribute(l_web_xml, 'WebPort', p_web_data.WebPort)
        return l_web_xml


class API(WebUtility, ClientConnections):

    def __init__(self):
        self.State = web_utils.WS_IDLE
        g_logger.info("Initialized")
        self.web_running = False

    def Start(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        self.web_data = WebData()
        self.read_web_xml(self.web_data, p_pyhouses_obj.XmlRoot)
        l_site_dir = None
        l_site = appserver.NevowSite(web_mainpage.TheRoot('/', l_site_dir, p_pyhouses_obj))
        if not self.web_running:
            listenTCP(self.web_data.WebPort, l_site)
        self.web_running = True
        l_msg = "Port:{0:}, Path:{1:}".format(self.web_data.WebPort, l_site_dir)
        g_logger.info("Started - {0:}".format(l_msg))
        return self.web_data

    def Stop(self):
        l_xml = self.write_web_xml(self.web_data)
        return l_xml

    def UpdateXml(self, p_xml):
        p_xml.append(self.write_web_xml(self.web_data))
        return p_xml

    def Update(self, p_entry):
        l_obj = WebData()
        l_obj.Port = p_entry.Port
        self.m_house_obj.WebData = l_obj  # update schedule entry within a house

# ## END DBK
