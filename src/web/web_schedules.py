'''
Created on Jun 3, 2013

@author: briank
'''

# Import system type stuff
from nevow import loaders
from nevow import rend
from nevow import static
import json

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Dump JSON
# + = NOT USED HERE


class SchedulesPage(web_utils.ManualFormMixin):
    addSlash = True
    docFactory = loaders.xmlfile('buttons.xml', templateDir = 'src/web/template')

    def __init__(self, p_parent, p_name, p_pyhouse_obj):
        self.m_name = p_name
        self.m_parent = p_parent
        self.m_pyhouse_obj = p_pyhouse_obj
        if g_debug >= 1:
            print "web_schedule.SchedulePage.__init__()"
        if g_debug >= 2:
            print "    ", self.m_pyhouse_obj
        l_css = ['src/web/css/mainPage.css']
        l_js = ['src/web/js/ajax.js', 'src/web/js/floatingWindow.js',
                'src/web/js/schedulePage.js']
        web_utils.add_attr_list(SchedulesPage, l_css)
        web_utils.add_attr_list(SchedulesPage, l_js)
        web_utils.add_float_page_attrs(SchedulesPage)
        rend.Page.__init__(self)

    def data_schedlist(self, _context, _data):
        """Build up a list of schedule slots.
        @param _context: is a tag that we are building an object to render
        @param _data: is the page object we are extracting for.
        @return: an object to render.
        """
        if g_debug >= 1:
            print "web_schedules.data_schedlist()"
        l_sched = {}
        for l_key, l_obj in self.m_pyhouse_obj.Schedules.iteritems():
            l_sched[l_key] = l_obj
        return l_sched

    def render_action(self, _ctx, _data):
        return web_utils.action_url()

    def render_schedlist(self, _context, links):
        """
        """
        if g_debug >= 1:
            print "web_schedules.render_schedlist()"
        l_ret = []
        l_cnt = 0
        for l_key, l_obj in sorted(links.iteritems()):
            l_json = json.dumps(repr(l_obj))
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON,
                    onclick = "createChangeScheduleWindow({0:})".format(l_json))
                    [ l_obj.Name, '_', l_obj.RoomName, '_', l_obj.LightName, "_'",
                     l_obj.Time, "'_", l_obj.Level, '_', l_obj.Key, "\n" ])
            l_cnt += 1
        return l_ret

    def data_lightlist(self, _context, _data):
        l_lights = {}
        for l_key, l_obj in self.m_pyhouse_obj.Lights.iteritems():
            l_lights[l_key] = l_obj.Name
        return l_lights

    def render_lightlist(self, _context, _links):
        l_ret = []
        return l_ret

    def data_roomlist(self, _context, _data):
        l_rooms = {}
        for l_key, l_obj in self.m_pyhouse_obj.Rooms.iteritems():
            l_rooms[l_key] = l_obj.Name
        return l_rooms

    def render_roomlist(self, _context, _links):
        l_ret = []
        return l_ret

    def _store_schedule(self, **kwargs):
        """Save the info we got back.

        TODO: restart the scheduler to use the changed info we just got!
        """
        if g_debug >= 1:
            print "web_schedule.SchedulePage._store_schedule() - ", kwargs
            print self.m_pyhouse_obj.Schedules
        l_key = int(kwargs['Key'])
        self.m_pyhouse_obj.Schedules[l_key].Name = kwargs['Name']
        self.m_pyhouse_obj.Schedules[l_key].Key = l_key
        self.m_pyhouse_obj.Schedules[l_key].Active = (kwargs['Active'] == 'True')
        self.m_pyhouse_obj.Schedules[l_key].LightName = kwargs['LightName']
        self.m_pyhouse_obj.Schedules[l_key].RoomName = kwargs['RoomName']
        self.m_pyhouse_obj.Schedules[l_key].Time = kwargs['Time']
        self.m_pyhouse_obj.Schedules[l_key].Level = int(kwargs['Level'])
        self.m_pyhouse_obj.Schedules[l_key].Rate = int(kwargs['Rate'])
        self.m_pyhouse_obj.Schedules[l_key].Type = kwargs['Type']

    def form_post_changesched(self, **kwargs):
        """Browser user changed a schedule
        Now send the change to the light.
        """
        print "web_schedule.SchedulePage.form_post_changesched() - kwargs=", kwargs
        self._store_schedule(**kwargs)

    def form_post_addslot(self, **kwargs):
        print "web_schedule.SchedulePage.form_post_addslot - kwargs=", kwargs
        self._store_schedule(**kwargs)
        return SchedulesPage(self.m_name, self.m_pyhouse_obj)

    def form_post_changeschedule(self, **kwargs):
        print "web_schedule.SchedulePage.form_post_changeschedule - kwargs=", kwargs
        self._store_schedule(**kwargs)
        # schedule.ScheduleAPI().update_schedule(schedule.Schedule_Data)
        return SchedulesPage(self.m_name, self.m_pyhouse_obj)

    def form_post_deleteschedule(self, **kwargs):
        print "web_schedule.SchedulePage.form_post_deleteschedule() - kwargs=", kwargs
        del self.m_pyhouse_obj.Schedules['Key']
        # schedule.ScheduleAPI().update_schedule(schedule.Schedule_Data)
        return SchedulesPage(self.m_name, self.m_pyhouse_obj)

# ## END DBK
