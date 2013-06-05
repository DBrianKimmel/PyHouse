'''
Created on Jun 3, 2013

@author: briank
'''

# Import system type stuff
from nevow import loaders
from nevow import rend
from nevow import static
from nevow import tags as Tag

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.scheduling import schedule


g_debug = 8
# 0 = off
# 1 = major routine entry
# 2 = Basic data


class SchedulesPage(web_utils.ManualFormMixin):
    addSlash = True
    docFactory = loaders.stan(
        T_html[
            T_head[
                T_title['PyHouse - Schedule Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js')["\n"],
                T_script(type = 'text/javascript', src = 'schedpage.js'),
                ],
            T_body[
                T_h1['PyHouse Schedule'],
                T_p['Select the schedule:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    Tag.invisible(data = Tag.directive('schedlist'), render = Tag.directive('schedlist'))
                    ],
                T_input(type = "button", onclick = "createNewSchedule('1234')", value = "Add Slot")
                ]
            ]
        )

    def __init__(self, name, p_pyhouse_obj):
        self.name = name
        self.m_pyhouse_obj = p_pyhouse_obj.Object
        if g_debug >= 1:
            print "web_schedule.SchedulePage.__init__()"
        if g_debug >= 5:
            print self.m_pyhouse_obj
        rend.Page.__init__(self)
        setattr(SchedulesPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(SchedulesPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(SchedulesPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
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
        l_sched = {}
        for l_key, l_obj in self.m_pyhouse_obj.Schedules.iteritems():
            l_sched[l_key] = l_obj
        return l_sched

    def render_schedlist(self, _context, links):
        """
        @param: _context is ...
        @param: links are ...
        @return: the list to be added into the stan.dom
        """
        global l_ret
        l_ret = []
        l_cnt = 0
        for l_key, l_obj in sorted(links.iteritems()):
            l_level = l_obj.Level
            l_name = l_obj.Name
            l_light = l_obj.LightName
            l_room = l_obj.RoomName
            l_rate = l_obj.Rate
            l_time = l_obj.Time
            l_type = l_obj.Type
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON, onclick = "createChangeScheduleWindow(\'{0:}\', \'{1:}\', \'{2:}\', \'{3:}\', \'{4:}\', \'{5:}\')".format(
                                                    l_key, l_type, l_name, l_time, l_level, l_rate))
                         [ l_name, '_', l_room, '_', l_light, "_'", l_time, "'_", l_level, '_', "\n" ])
            l_cnt += 1
        return l_ret

    def _store_schedule(self, **kwargs):
        if g_debug >= 1:
            print "web_schedule.SchedulePage._store_schedule() - ", kwargs
        l_slot = kwargs['Slot']
        # schedule.Schedule_Data[l_slot] = {}
        # schedule.Schedule_Data[l_slot]['Name'] = kwargs['Name']
        # schedule.Schedule_Data[l_slot]['Type'] = kwargs['Type']
        # schedule.Schedule_Data[l_slot]['Time'] = kwargs['Time']
        # schedule.Schedule_Data[l_slot]['Level'] = kwargs['Level']
        # schedule.Schedule_Data[l_slot]['Rate'] = kwargs['Rate']

    def form_post_changesched(self, **kwargs):
        """Browser user changed a schedule
        Now send the change to the light.
        """
        print "web_schedule.SchedulePage.form_post_changesched() - kwargs=", kwargs
        self._store_schedule(**kwargs)

    def form_post_addslot(self, **kwargs):
        print "web_schedule.SchedulePage.form_post_addslot - kwargs=", kwargs
        self._store_schedule(**kwargs)
        return SchedulesPage(self.name)

    def form_post_changeschedule(self, **kwargs):
        print "web_schedule.SchedulePage.form_post_changeschedule (add) - kwargs=", kwargs
        self._store_schedule(**kwargs)
        schedule.ScheduleAPI().update_schedule(schedule.Schedule_Data)
        return SchedulesPage(self.name)

    def form_post_deleteschedule(self, **kwargs):
        print "web_schedule.SchedulePage.form_post_deleteschedule() - kwargs=", kwargs
        del schedule.Schedule_Data[kwargs['Slot']]
        schedule.ScheduleAPI().update_schedule(schedule.Schedule_Data)
        return SchedulesPage(self.name)

# ## END DBK
