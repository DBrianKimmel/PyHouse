'''
Created on Jun 3, 2013

@author: briank
'''

# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.web import web_utils
from Modules.scheduling import schedule
from Modules.utils import pyh_log

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Dump JSON
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.webSchedule ')


class SchedulesElement(athena.LiveElement):
    """ a 'live' schedules element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'schedulesElement.html'))
    jsClass = u'schedules.SchedulesWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHouseData(self, p_index):
        """ A JS client has requested all the information for a given house.

        @param p_index: is the house index number.
        """
        l_ix = int(p_index)
        l_house = self.m_pyhouse_obj.HouseData
        l_json = web_utils.JsonUnicode().encode_json(l_house)
        return unicode(l_json)

    @athena.expose
    def saveScheduleData(self, p_json):
        """A new/changed schedule is returned.  Process it and update the internal data via schedule.py
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_delete = l_json['Delete']
        l_house_ix = int(l_json['HouseIx'])
        l_schedule_ix = int(l_json['Key'])
        if l_delete:
            try:
                del self.m_pyhouse_obj.HouseData.Schedules[l_schedule_ix]
            except AttributeError as e:
                LOG.warning('Failed to delete schedule: {0:}, ix:{1:}').format(e, l_schedule_ix)
            return
        try:
            l_obj = self.m_pyhouse_obj.HouseData.Schedules[l_schedule_ix]
        except KeyError:
            l_obj = schedule.ScheduleData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = int(l_json['Key'])
        l_obj.Level = int(l_json['Level'])
        l_obj.LightName = l_json['LightName']
        l_obj.Rate = l_json['Rate']
        l_obj.RoomName = l_json['RoomName']
        l_obj.Time = l_json['Time']
        l_obj.ScheduleType = l_json['Type']
        l_obj.UUID = l_json['UUID']
        l_obj.DeleteFlag = l_json['Delete']
        l_obj.HouseIx = l_house_ix
        self.m_pyhouse_obj.HouseData.Schedules[l_schedule_ix] = l_obj

# ## END DBK
