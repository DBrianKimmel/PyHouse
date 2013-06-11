#!/usr/bin/python
'''
Created on May 30, 2013

@author: briank
'''

# Import system type stuff
from nevow import loaders
from nevow import rend
from nevow import static

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.web import web_schedules
from src.web import web_rooms
from src.web import web_location
from src.web import web_lights
from src.web import web_buttons
from src.web import web_controllers
from src.web import web_control
from src.web import web_internet


g_debug = 5
# 0 = off
# 1 = major routine entry
# 2 = Basic data

g_logger = None

class HouseMenuPage(web_utils.ManualFormMixin):
    """
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - House Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                ],  # head
            T_body[
                T_h1['PyHouse Houses'],
                T_p['\n'],
                T_p['Select house option:'],
                T_form(name = 'mainmenuofbuttons',
                    action = U_H_child('_submit!!post'),
                    enctype = "multipart/form-data",
                    method = 'post')
                    [
                    T_table(style = 'width: 100%;', border = 0)["\n",
                        T_tr[
                            T_td[ T_input(type = 'submit', value = 'Location', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Rooms', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Lights', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Buttons', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Controllers', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Schedules', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Control Lights', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Internet', name = BUTTON), ],
                            ]
                        ]  # table
                    ]  # form
                ]  # body
            ]  # html
        )  # stan

    def __init__(self, name, p_pyhouses_obj, p_index):
        self.name = name
        self.m_houses_obj = p_pyhouses_obj.HousesData[p_index]
        self.m_index = p_index
        if g_debug >= 1:
            print "web_housemenu.HouseMenuPage()"
        if g_debug >= 2:
            print "    ", self.m_houses_obj
        rend.Page.__init__(self)
        setattr(HouseMenuPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))

    def form_post_rooms(self, **kwargs):
        if g_debug >= 2:
            print "web_housemenu.HouseMenuPage.form_post_rooms()", kwargs
        return web_rooms.RoomsPage(self.name, self.m_houses_obj.Object)

    def form_post_lights(self, **kwargs):
        if g_debug >= 2:
            print "web_housemenu.HouseMenuPage.form_post_lights", kwargs
        return web_lights.LightsPage(self.name, self.m_houses_obj.Object)

    def form_post_buttons(self, **kwargs):
        if g_debug >= 2:
            print "web_housemenu.HouseMenuPage.form_post_buttons", kwargs
        return web_buttons.ButtonsPage(self.name, self.m_houses_obj.Object)

    def form_post_controllers(self, **kwargs):
        if g_debug >= 2:
            print "web_housemenu.HouseMenuPage.form_post_controllers", kwargs
        return web_controllers.ControllersPage(self.name, self.m_houses_obj.Object)

    def form_post_schedules(self, **kwargs):
        if g_debug >= 2:
            print "web_housemenu.HouseMenuPage.form_post_schedules()", kwargs
        return web_schedules.SchedulesPage(self.name, self.m_houses_obj.Object)

    def form_post_control(self, **kwargs):
        if g_debug >= 2:
            print "web_housemenu.HouseMenuPage.form_post_control()", kwargs
        return web_control.ControlPage(self.name, self.m_houses_obj.Object)

    def form_post_location(self, **kwargs):
        if g_debug >= 2:
            print "web_housemenu.HouseMenuPage.form_post_location()", kwargs
        return web_location.LocationPage(self.name, self.m_houses_obj.Object)

    def form_post_internet(self, **kwargs):
        if g_debug >= 2:
            print "web_housemenu.HouseMenuPage.form_post_internet()", kwargs
        return web_internet.InternetPage(self.name, self.m_houses_obj.Object)


    def form_post_house(self, **kwargs):
        if g_debug >= 2:
            print "web_housemenu.HouseMenuPage.form_post_house (HousePage)", kwargs
        return HouseMenuPage(self.name, self.m_houses_obj.Object)

# ## END DBK
