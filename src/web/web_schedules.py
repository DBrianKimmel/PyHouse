'''
Created on Jun 3, 2013

@author: briank
'''

# Import system type stuff
import logging
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from src.web import web_utils
from src.scheduling import schedule

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 5
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
            #print "    self = ", self  #, vars(self)
            #print "    workspace_obj = ", p_workspace_obj  #, vars(p_workspace_obj)

    @athena.expose
    def getScheduleEntries(self, p_index):
        """ A JS receiver for controllers information from the client.
        """
        if g_debug >= 3:
            print "web_schedules.SchedulesElement.getScheduleEntries() - HouseIndex:", p_index
        g_logger.info("getSchedules called {0:}".format(self))
        l_schedules = self.m_pyhouses_obj.HousesData[int(p_index)].HouseObject.Schedules
        l_obj = {}
        for l_key, l_val in l_schedules.iteritems():
            l_obj[l_key] = l_val
            #l_obj[l_key] = {}
            #l_obj[l_key]['Name'] = l_val.Name
            #l_obj[l_key]['Key'] = l_key
            #l_obj[l_key]['Active'] = l_val.Active
        l_json = web_utils.JsonUnicode().encode_json(l_obj)
        if g_debug >= 3:
            print "web_schedules.SchedulesElement.getScheduleEntries() - json:", l_json
        self.callRemote('ShowButtons', unicode(l_json))  # call client @ schedules.js

# ## END DBK
