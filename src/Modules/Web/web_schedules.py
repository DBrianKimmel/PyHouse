"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_schedules -*-

@name: PyHouse/src/Modules/web/web_schedules.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 3, 2013
@summary: Web interface to schedules for the selected house.

"""

# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.Core.data_objects import ScheduleBaseData
from Modules.Web.web_utils import JsonUnicode, GetJSONHouseInfo
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.tools import PrettyPrintAny

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webSchedule ')


class SchedulesElement(athena.LiveElement):
    """ a 'live' schedules element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'schedulesElement.html'))
    jsClass = u'schedules.SchedulesWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHouseData(self):
        l_house = GetJSONHouseInfo(self.m_pyhouse_obj)
        return l_house

    @athena.expose
    def saveScheduleData(self, p_json):
        """A new/changed schedule is returned.  Process it and update the internal data via schedule.py
        """
        l_json = JsonUnicode().decode_json(p_json)
        # PrettyPrintAny(l_json, 'JSON')
        l_delete = l_json['Delete']
        l_schedule_ix = int(l_json['Key'])
        if l_delete:
            try:
                del self.m_pyhouse_obj.House.OBJs.Schedules[l_schedule_ix]
            except AttributeError as e:
                LOG.warning('Failed to delete schedule: {0:}, ix:{1:}').format(e, l_schedule_ix)
            return
        try:
            l_obj = self.m_pyhouse_obj.House.OBJs.Schedules[l_schedule_ix]
        except KeyError:
            l_obj = ScheduleBaseData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_schedule_ix
        l_obj.UUID = l_json['UUID']
        #
        l_obj.ScheduleType = l_json['ScheduleType']
        l_obj.Time = l_json['Time']
        l_obj.DOW = l_json['DOW']
        l_obj.Mode = l_json['Mode']
        #
        l_obj.Level = int(l_json['Level'])
        l_obj.LightName = l_json['LightName']
        l_obj.Rate = l_json['Rate']
        l_obj.RoomName = l_json['RoomName']
        #
        l_obj._DeleteFlag = l_json['Delete']
        self.m_pyhouse_obj.House.OBJs.Schedules[l_schedule_ix] = l_obj
        # PrettyPrintAny(l_obj, 'ScheduleObject')

# ## END DBK
