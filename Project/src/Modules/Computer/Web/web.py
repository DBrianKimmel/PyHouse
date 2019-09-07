"""
@name:      Modules/Computer/Web/web.py
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

__updated__ = '2019-07-10'
__version_info__ = (19, 5, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.data_objects import LoginData, WebInformation
from Modules.Computer.Web.web_xml import Xml as webXml
from Modules.Computer.Web.web_server import API as WebAPI
# from Modules.Computer.Web.websocket_server import API as WebSocketAPI

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Web            ')


class WorkspaceData(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj


class API(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """ Load the Mqtt xml info.
        """
        self.m_pyhouse_obj.Computer.Web = WebInformation()  # Clear before loading.
        self.m_pyhouse_obj.Computer.Web.Logins = LoginData()  # Clear before loading.
        l_ret = webXml.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Web = l_ret
        LOG.info('Loaded Web Config')

    def Start(self):
        #  l_obj = self.LoadXml(self.m_pyhouse_obj)
        #  self.m_pyhouse_obj.Computer.Web = l_obj
        WebAPI(self.m_pyhouse_obj).Start()
        # WebSocketAPI(self.m_pyhouse_obj).Start()
        LOG.info('Started.')

    def SaveConfig(self):
        webXml.write_web_xml(self.m_pyhouse_obj)
        LOG.info("Saved Web Config.")

    def Stop(self):
        LOG.info('Stopped.')

#  ## END DBK
