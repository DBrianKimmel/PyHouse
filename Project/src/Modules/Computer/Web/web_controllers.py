"""
@name:      Modules/Web/web_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Web interface to controllers for the selected house.

"""

__updated__ = '2019-12-30'

#  Import system type stuff
import os
from nevow import loaders
from nevow import athena

#  Import PyMh files and modules.
from Modules.Core.data_objects import ControllerInformation
from Modules.Computer.Web import web_family, web_utils
from Modules.Computer.Web.web_utils import GetJSONHouseInfo
from Modules.Drivers import VALID_INTERFACES
from Modules.Core import logging_pyh as Logger
from Modules.Core.Utilities import json_tools

#  Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webCntlr    ')


class ControllersElement(athena.LiveElement):
    """ a 'live' controllers element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'controllersElement.html'))
    jsClass = u'controllers.ControllersWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHouseData(self):
        l_house = GetJSONHouseInfo(self.m_pyhouse_obj)
        return l_house

    @athena.expose
    def getInterfaceData(self):
        """ A JS request for information has been received from the client.
        """
        l_interfaces = VALID_INTERFACES
        l_obj = {}
        for l_interface in l_interfaces:
            _l_name = l_interface + 'Data'
        l_json = json_tools.encode_json(l_obj)
        return unicode(l_json)

    @athena.expose
    def saveControllerInformation(self, p_json):
        """A new/changed controller is returned.  Process it and update the internal data via controller.py
        """
        l_json = json_tools.decode_json_unicode(p_json)
        l_ix = int(l_json['Key'])
        l_delete = l_json['Delete']
        if l_delete:
            try:
                del self.m_pyhouse_obj.House.Lighting.Controllers[l_ix]
            except AttributeError:
                LOG.error("web_controllers - Failed to delete - JSON: {}".FORMAT(l_json))
            return
        l_obj = ControllerInformation()
        try:
            l_obj = self.m_pyhouse_obj.House.Lighting.Controllers[l_ix]
        except KeyError:
            LOG.warning('Creating a new controller {}'.format(l_ix))
        web_utils.get_base_info(l_obj, l_json)
        l_obj.Comment = l_json['Comment']
        l_obj.DeviceFamily = l_json['DeviceFamily']
        l_obj.DeviceType = 1
        l_obj.DeviceSubType = 2
        l_obj.InterfaceType = l_json['InterfaceType']
        l_obj.Port = l_json['Port']
        if l_obj.InterfaceType == 'Serial':
            l_obj.BaudRate = l_json['BaudRate']
        web_family.get_family_json_data(l_obj, l_json)
        web_utils.get_room_info(l_obj, l_json)
        self.m_pyhouse_obj.House.Lighting.Controllers[l_ix] = l_obj
        LOG.info('Controller Added - {}'.format(l_obj.Name))

#  ## END DBK
