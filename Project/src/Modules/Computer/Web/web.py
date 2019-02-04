"""
@name:      PyHouse/src/Modules/Web/web.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 27, 2015
@Summary:

Setup and run web services.
    Webserver straight & TLS
    Websocket Server

PyHouse.Computer.Web
            Logins
            Port

"""

__updated__ = '2019-02-03'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.data_objects import WebData, LoginData
from Modules.Computer.Web.web_xml import Xml as webXml
from Modules.Computer.Web.web_server import API as WebAPI
# from Modules.Computer.Web.websocket_server import API as WebSocketAPI

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Web            ')


class WorkspaceData(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj


class API(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized.')

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Mqtt xml info.
        """
        p_pyhouse_obj.Computer.Web = WebData()  # Clear before loading.
        p_pyhouse_obj.Computer.Web.Logins = LoginData()  # Clear before loading.
        l_ret = webXml.read_web_xml(p_pyhouse_obj)
        p_pyhouse_obj.Computer.Web = l_ret
        LOG.info('Loaded XML')

    def Start(self):
        #  l_obj = self.LoadXml(self.m_pyhouse_obj)
        #  self.m_pyhouse_obj.Computer.Web = l_obj
        WebAPI(self.m_pyhouse_obj).Start()
        # WebSocketAPI(self.m_pyhouse_obj).Start()
        LOG.info('Started.')

    def SaveXml(self, p_xml):
        l_xml = webXml.write_web_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved Web XML.")

    def Stop(self):
        LOG.info('Stopped.')

#  ## END DBK
