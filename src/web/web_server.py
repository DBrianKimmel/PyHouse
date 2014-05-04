"""
@name: PyHouse/src/web/web_seever.py

# -*- test-case-name: PyHouse.src.web.test.test_web_server -*-

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2012-2014 by D. Brian Kimmel
@license: MIT License

@summary: This module provides the web server service of PyHouse.

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
from twisted.application import service
from nevow import appserver
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from src.web import web_utils
from src.web import web_mainpage
from src.utils import pyh_log
from src.utils import xml_tools

# Handy helper for finding external resources nearby.
# webpath = os.path.join(os.path.split(__file__)[0])
# templatepath = os.path.join(webpath, 'template')
# imagepath = os.path.join(webpath, 'images')
# jspath = os.path.join(webpath, 'js')


ENDPOINT_WEB_SERVER = 'tcp:port=8580'

g_debug = 0
# 0 = off
# 1 = log extra info
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.WebServer   ')


class WebData(object):
    """
    """
    def __init__(self):
        self.WebPort = 8580
        self.Service = None
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


class Utility(xml_tools.ConfigFile):

    def read_web_xml(self, p_pyhouses_obj):
        p_pyhouses_obj.WebData = WebData()
        try:
            l_sect = p_pyhouses_obj.XmlRoot.find('Web')
            l_sect.find('WebPort')
        except AttributeError:
            if g_debug >= 0:
                LOG.error("web_server.read_web_xml() - ERROR in finding Web/WebPort, Creating entry {0:}".format(l_sect))
            l_sect = ET.SubElement(p_pyhouses_obj.XmlRoot, 'Web')
            ET.SubElement(l_sect, 'Port').text = '8580'
            self.put_int_attribute(l_sect, 'WebPort', 8580)
            p_pyhouses_obj.WebData.WebPort = 8580
            l_logs = ET.SubElement(l_sect, 'Logins')
            l_login = ET.SubElement(l_logs, 'Login')
            l_login.set('Name', 'admin')
            l_login.set('Key', '0')
            l_login.set('Active', True)
            ET.SubElement(l_login, 'Password').text = '12admin34'
            return
        p_pyhouses_obj.WebData.WebPort = l_sect.findtext('WebPort')
        p_pyhouses_obj.WebData.WebPort = 8580
        # l_web_data.WebPort = self.get_int_from_xml(l_sect, 'WebPort')
        return

    def write_web_xml(self, p_pyhouses_obj):
        l_web_xml = ET.Element("Web")
        self.put_int_attribute(l_web_xml, 'WebPort', p_pyhouses_obj.WebData.WebPort)
        return l_web_xml

    def start_webserver(self, p_pyhouses_obj):
        p_pyhouses_obj.WebData.Service = service.Service()
        p_pyhouses_obj.WebData.Service.setName('Web')
        p_pyhouses_obj.WebData.Service.setServiceParent(p_pyhouses_obj.Application)
        #
        l_site_dir = None
        l_site = appserver.NevowSite(web_mainpage.TheRoot(l_site_dir, p_pyhouses_obj))
        if not p_pyhouses_obj.WebData.Service.running:
            p_pyhouses_obj.Reactor.listenTCP(p_pyhouses_obj.WebData.WebPort, l_site)
            p_pyhouses_obj.WebData.Service.startService()
        l_msg = "Port:{0:}, Path:{1:}".format(p_pyhouses_obj.WebData.WebPort, l_site_dir)
        LOG.info("Started - {0:}".format(l_msg))


class API(Utility, ClientConnections):

    def __init__(self):
        self.State = web_utils.WS_IDLE
        LOG.info("Initialized.\n")
        self.m_web_running = False

    def Start(self, p_pyhouses_obj):
        p_pyhouses_obj.WebData = WebData()
        self.m_pyhouses_obj = p_pyhouses_obj
        self.read_web_xml(p_pyhouses_obj)
        self.start_webserver(p_pyhouses_obj)

    def Stop(self, p_xml):
        self.m_pyhouses_obj.WebData.Service.stopService()
        p_xml.append(self.write_web_xml(self.m_pyhouses_obj))
        LOG.info("XML appended.")

# ## END DBK
