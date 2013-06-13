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


g_debug = 5
# 0 = off
# 1 = major routine entry
# 2 = Basic data


class SchedulesPage(web_utils.ManualFormMixin):
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - Schedule Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_H_child('lightpage.css'))["\n"],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js')["\n"],
                T_script(type = 'text/javascript', src = 'slider.js')["\n"],
                T_script(type = 'text/javascript', src = 'range.js')["\n"],
                T_script(type = 'text/javascript', src = 'schedpage.js'),
                ],  # head
            T_body[
                T_h1['PyHouse Schedule'],
                T_p['Select the schedule:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    T_invisible(data = T_directive('schedlist'), render = T_directive('schedlist')),
                    T_invisible(data = T_directive('lightlist'), render = T_directive('lightlist')),
                    ],  # table
                T_input(type = "button", onclick = "createNewSchedule('1234')", value = "Add Schedule")
                ]  # body
            ]  # html
        )  # stan

    def __init__(self, name, p_pyhouse_obj):
        self.name = name
        self.m_pyhouse_obj = p_pyhouse_obj
        if g_debug >= 1:
            print "web_schedule.SchedulePage.__init__()"
        if g_debug >= 2:
            print "    ", self.m_pyhouse_obj
        rend.Page.__init__(self)
        setattr(SchedulesPage, 'child_lightpage.css', static.File('web/css/lightpage.css'))
        setattr(SchedulesPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))

        setattr(SchedulesPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(SchedulesPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(SchedulesPage, 'child_slider.js', static.File('web/js/slider.js'))
        setattr(SchedulesPage, 'child_range.js', static.File('web/js/range.js'))
        setattr(SchedulesPage, 'child_schedpage.js', static.File('web/js/schedpage.js'))
        #------------------------------------
        setattr(SchedulesPage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(SchedulesPage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(SchedulesPage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(SchedulesPage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(SchedulesPage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(SchedulesPage, 'child_topRight.gif', static.File('web/images/top_right.gif'))
        setattr(SchedulesPage, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))

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

    def render_schedlist(self, _context, links):
        """
        """
        if g_debug >= 1:
            print "web_schedules.render_schedlist()"
        l_ret = []
        l_cnt = 0
        for l_key, l_obj in sorted(links.iteritems()):
            l_json = json.dumps(repr(l_obj))
        #    if g_debug >= 4:
        #        print "    json = ", l_json
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON,
                    onclick = "createChangeScheduleWindow({0:})".format(l_json))
                    [ l_obj.Name, '_', l_obj.RoomName, '_', l_obj.LightName, "_'",
                     l_obj.Time, "'_", l_obj.Level, '_', "\n" ])
            l_cnt += 1
        return l_ret

    def data_lightlist(self, _context, _data):
        l_lights = {}
        for l_key, l_obj in self.m_pyhouse_obj.Lights.iteritems():
            l_lights[l_key] = l_obj.Name
        return l_lights

    def render_lightlist(self, _context, links):
        l_ret = []
        return l_ret

    def data_roomlist(self, _context, _data):
        l_rooms = {}
        for l_key, l_obj in self.m_pyhouse_obj.Rooms.iteritems():
            l_rooms[l_key] = l_obj.Name
        return l_rooms

    def render_roomlist(self, _context, links):
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
        return SchedulesPage(self.name, self.m_pyhouse_obj)

    def form_post_changeschedule(self, **kwargs):
        print "web_schedule.SchedulePage.form_post_changeschedule - kwargs=", kwargs
        self._store_schedule(**kwargs)
        # schedule.ScheduleAPI().update_schedule(schedule.Schedule_Data)
        return SchedulesPage(self.name, self.m_pyhouse_obj)

    def form_post_deleteschedule(self, **kwargs):
        print "web_schedule.SchedulePage.form_post_deleteschedule() - kwargs=", kwargs
        del self.m_pyhouse_obj.Schedules['Key']
        # schedule.ScheduleAPI().update_schedule(schedule.Schedule_Data)
        return SchedulesPage(self.name, self.m_pyhouse_obj)

# ## END DBK
