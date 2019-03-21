"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_schedules -*-

@name:      PyHouse/src/Modules/web/web_schedules.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Web interface to schedules for the selected house.

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2019-03-20'

#  Import system type stuff
import os
# from nevow import athena
# from nevow import loaders

#  Import PyMh files and modules.
from Modules.Core.data_objects import ScheduleBaseData
from Modules.Computer.Web.web_utils import GetJSONHouseInfo
from Modules.Computer import logging_pyh as Logger
from Modules.Core.Utilities import json_tools

#  Handy helper for finding external resources nearby.
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
        l_json = json_tools.decode_json_unicode(p_json)
        l_delete = l_json['Delete']
        l_schedule_ix = int(l_json['Key'])
        if l_delete:
            try:
                del self.m_pyhouse_obj.House.Schedules[l_schedule_ix]
            except AttributeError as e:
                LOG.warning('Failed to delete schedule: {}, ix:{}').format(e, l_schedule_ix)
            return
        try:
            l_obj = self.m_pyhouse_obj.House.Schedules[l_schedule_ix]
        except KeyError:
            l_obj = ScheduleBaseData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_schedule_ix
        #
        l_obj.ScheduleType = l_json['ScheduleType']
        l_obj.Time = l_json['Time']
        l_obj.DayOfWeek = l_json['DayOfWeek']
        l_obj.ScheduleMode = l_json['ScheduleMode']
        #
        if l_obj.ScheduleType == 'Lighting':
            l_obj = self._save_light(l_obj, l_json)
        elif l_obj.ScheduleType == 'Irrigation':
            l_obj = self._save_irrigation(l_obj, l_json)
        #
        l_obj._DeleteFlag = l_json['Delete']
        self.m_pyhouse_obj.House.Schedules[l_schedule_ix] = l_obj
        self.m_pyhouse_obj.APIs.House.ScheduleAPI.RestartSchedule()

    def _save_light(self, p_obj, p_json):
        LOG.info(PrettyFormatAny.form(p_json, 'JSON'))
        p_obj.Level = int(p_json['Level'])
        p_obj.LightName = p_json['LightName']
        p_obj.Rate = p_json['Rate']
        p_obj.RoomName = p_json['RoomName']
        return p_obj

    def _save_irrigation(self, p_obj, p_jason):
        p_obj.Duration = int(p_jason['Duration'])

#  ## END DBK
