"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_buttons -*-

@name:      PyHouse/src/Modules/web/web_buttons.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Web interface to buttons for the selected house.

"""
from Modules.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2016-11-01'

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Computer.Web.web_utils import GetJSONHouseInfo
from Modules.Housing.Lighting import lighting_buttons
from Modules.Computer import logging_pyh as Logger
from Modules.Families.Insteon import Insteon_utils
from Modules.Utilities import json_tools

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

LOG = Logger.getLogger('PyHouse.webButton   ')


class ButtonsElement(athena.LiveElement):
    """ a 'live' login element containing a username and password.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'buttonsElement.html'))
    jsClass = u'buttons.ButtonsWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHouseData(self):
        l_house = GetJSONHouseInfo(self.m_pyhouse_obj)
        return l_house

    @athena.expose
    def saveButtonData(self, p_json):
        """A new/changed button is returned.
        """
        l_json = json_tools.decode_json_unicode(p_json)
        l_delete = l_json['Delete']
        l_ix = int(l_json['Key'])
        if l_delete:
            try:
                del self.m_pyhouse_obj.House.Lighting.Buttons[l_ix]
            except AttributeError:
                LOG.error("Failed to delete - JSON: {}".format(l_json))
            return
        l_obj = lighting_buttons.ButtonData()
        try:
            l_obj = self.m_pyhouse_obj.House.Lighting.Buttons[l_ix]
        except KeyError:
            LOG.warning('Creating a new button {}'.format(l_ix))
        #
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_json['Key']
        l_obj.UUID = l_json['UUID']
        l_obj.DeviceType = 1
        l_obj.DeviceSubType = 1
        l_obj.Comment = l_json['Comment']
        l_obj.RoomCoords = l_json['RoomCoords']
        l_obj.DeviceFamily = l_json['DeviceFamily']
        l_obj.RoomCoords = l_json['RoomCoords']
        l_obj.RoomName = l_json['RoomName']
        l_obj.RoomUUID = l_json['RoomUUID']
        if l_obj.DeviceFamily == 'Insteon':
            Insteon_utils.Util.get_json_data(l_obj, l_json)
        self.m_pyhouse_obj.House.Lighting.Buttons[l_obj.Key] = l_obj
        LOG.info('Button Added - {}'.format(l_obj.Name))
        LOG.info(PrettyFormatAny.form(l_obj, 'Button'))

# ## END DBK
