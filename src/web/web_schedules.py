'''
Created on Jun 3, 2013

@author: briank
'''

# Import system type stuff
import logging
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from src.web import web_utils
from src.scheduling import schedule

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
g_logger = logging.getLogger('PyHouse.webSched')


class SchedulesElement(athena.LiveElement):
    """ a 'live' schedules element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'schedulesElement.html'))
    jsClass = u'schedules.SchedulesWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_schedules.SchedulesElement()"

    @athena.expose
    def getScheduleData(self, p_index):
        """ A JS client has requested all the schedule information for a given house.

        Return the information via a remote call to the client.

        @param p_index: is the house index number.
        """
        if g_debug >= 3:
            print "web_schedules.SchedulesElement.getScheduleData() - HouseIndex:", p_index
        g_logger.info("getSchedulesEntry called {0:}".format(self))
        l_schedules = self.m_pyhouses_obj.HousesData[int(p_index)].HouseObject.Schedules
        l_obj = {}
        for l_key, l_val in l_schedules.iteritems():
            l_obj[l_key] = l_val
        l_json = web_utils.JsonUnicode().encode_json(l_obj)
        if g_debug >= 4:
            print "web_schedules.SchedulesElement.getScheduleData() - JSON:", l_json
        return unicode(l_json)

    @athena.expose
    def saveScheduleData(self, p_json):
        """A new/changed schedule is returned.  Process it and update the internal data via schedule.py
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_ix = int(l_json['HouseIx'])
        if g_debug >= 4:
            print "web_schedules.SchedulesElement.saveScheduleData() - JSON:", l_json
        l_obj = schedule.ScheduleData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_json['Key']
        l_obj.Level = l_json['Level']
        l_obj.LightName = l_json['LightName']
        l_obj.Rate = l_json['Rate']
        l_obj.RoomName = l_json['RoomName']
        l_obj.Time = l_json['Time']
        l_obj.Type = l_json['Type']
        self.m_pyhouses_obj.HousesData[l_ix].HouseObject.ScheduleAPI.update_data(l_obj)

# ## END DBK
