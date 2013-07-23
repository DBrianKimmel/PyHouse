#!/usr/bin/python
'''
Created on May 30, 2013

@author: briank
'''

# Import system type stuff
from nevow import loaders
from nevow import rend

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.web import web_schedules
from src.web import web_location
from src.web import web_lights
from src.web import web_buttons
from src.web import web_controllers
from src.web import web_controlLights
from src.web import web_internet
from src.web import web_rooms


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = Basic data

g_logger = None

class HouseMenuPage(web_utils.ManualFormMixin):
    """
    """
    addSlash = True
    docFactory = loaders.xmlfile('houseMenu.xml', templateDir = 'src/web/template')

    def __init__(self, p_name, p_pyhouses_obj, p_index):
        self.m_name = p_name
        self.m_house_obj = p_pyhouses_obj.HousesData[p_index]
        self.m_index = p_index
        if g_debug >= 1:
            print "web_houseMenu.HouseMenuPage()"
        if g_debug >= 2:
            print "    ", self.m_house_obj
        l_css = ['src/web/css/mainPage.css']
        l_js = ['src/web/js/ajax.js', 'src/web/js/floatingWindow.js']
        web_utils.add_attr_list(HouseMenuPage, l_css)
        web_utils.add_attr_list(HouseMenuPage, l_js)
        rend.Page.__init__(self)

    def render_action(self, _ctx, _data):
        return web_utils.action_url()

    def form_post_buttons(self, **kwargs):
        if g_debug >= 2:
            print "web_houseMenu.HouseMenuPage.form_post_buttons", kwargs
        return web_buttons.ButtonsPage(self, self.m_name, self.m_house_obj.HouseObject)

    def form_post_control_lights(self, **kwargs):
        if g_debug >= 2:
            print "web_houseMenu.HouseMenuPage.form_post_control()", kwargs
        return web_controlLights.ControlLightsPage(self, self.m_name, self.m_house_obj.HouseObject)

    def form_post_controllers(self, **kwargs):
        if g_debug >= 2:
            print "web_houseMenu.HouseMenuPage.form_post_controllers", kwargs
        return web_controllers.ControllersPage(self, self.m_name, self.m_house_obj.HouseObject)

    def form_post_lights(self, **kwargs):
        if g_debug >= 2:
            print "web_houseMenu.HouseMenuPage.form_post_lights", kwargs
        return web_lights.LightsPage(self, self.m_name, self.m_house_obj.HouseObject)

    def form_post_internet(self, **kwargs):
        if g_debug >= 2:
            print "web_houseMenu.HouseMenuPage.form_post_internet()", kwargs
        return web_internet.InternetPage(self, self.m_name, self.m_house_obj.HouseObject)

    def form_post_location(self, **kwargs):
        if g_debug >= 2:
            print "web_houseMenu.HouseMenuPage.form_post_location()", kwargs
        return web_location.LocationPage(self, self.m_name, self.m_house_obj.HouseObject)

    def form_post_rooms(self, **kwargs):
        if g_debug >= 2:
            print "web_houseMenu.HouseMenuPage.form_post_rooms()", kwargs
        return web_rooms.RoomsPage(self, self.m_name, self.m_house_obj.HouseObject)

    def form_post_schedules(self, **kwargs):
        if g_debug >= 2:
            print "web_houseMenu.HouseMenuPage.form_post_schedules()", kwargs
        return web_schedules.SchedulesPage(self, self.m_name, self.m_house_obj.HouseObject)

# ## END DBK
