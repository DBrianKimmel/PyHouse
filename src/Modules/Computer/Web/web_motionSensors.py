"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Computer/Web/web_motionSensors.py -*-

@name:      /home/briank/PyHouse/src/Modules/Computer/Web/web_motionSensors.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@note:      Created on Oct 23, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2016-11-01'



#  Import system type stuff
import os
from nevow import loaders
from nevow import athena

#  Import PyMh files and modules.
from Modules.Core.data_objects import MotionSensorData
from Modules.Computer.Web.web_utils import GetJSONHouseInfo
from Modules.Computer import logging_pyh as Logger
from Modules.Families.Insteon import Insteon_utils
from Modules.Utilities import json_tools


#  Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webMotion   ')


class MotionSensorsElement(athena.LiveElement):
    """ a 'live' controllers element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'motionSensorsElement.html'))
    jsClass = u'motionSensors.MotionSensorsWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHouseData(self):
        l_house = GetJSONHouseInfo(self.m_pyhouse_obj)
        return l_house

    @athena.expose
    def saveMotionSensorData(self, p_json):
        """A new/changed controller is returned.  Process it and update the internal data via controller.py
        """
        l_json = json_tools.decode_json_unicode(p_json)
        l_ix = int(l_json['Key'])
        l_delete = l_json['Delete']
        if l_delete:
            try:
                del self.m_pyhouse_obj.House.Security.MotionSensors[l_ix]
            except AttributeError:
                LOG.error("web_controllers - Failed to delete - JSON: {}".FORMAT(l_json))
            return
        try:
            l_obj = self.m_pyhouse_obj.House.Security.MotionSensors[l_ix]
        except KeyError:
            l_obj = MotionSensorData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_ix
        l_obj.Comment = l_json['Comment']
        l_obj.RoomCoords = l_json['RoomCoords']
        l_obj.DeviceFamily = l_json['DeviceFamily']
        l_obj.RoomName = l_json['RoomName']
        l_obj.DeviceType = 3
        l_obj.DeviceSubType = 2
        l_obj.UUID = l_json['UUID']
        l_obj.Status = l_json['Status']
        if l_obj.DeviceFamily == 'Insteon':
            Insteon_utils.Util().get_json_data(l_obj, l_json)
        self.m_pyhouse_obj.House.Security.MotionSensors[l_ix] = l_obj
        LOG.info('Motion Sensor Added - {}'.format(l_obj.Name))

# ## END DBK
