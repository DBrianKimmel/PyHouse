"""
Created on Jun 3, 2013

@author: briank

Web interface to control lights for the selected house.
"""

# Import system type stuff
from nevow import loaders
from nevow import rend
import json

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.web import web_rooms


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Dump JSON
# + = NOT USED HERE


class ControlLightsPage(web_utils.ManualFormMixin):
    """
    """
    addSlash = True
    docFactory = loaders.xmlfile('controlLights.xml', templateDir = 'src/web/template')

    def __init__(self, p_parent, p_name, p_house_obj):
        self.m_name = p_name
        self.m_parent = p_parent
        self.m_house_obj = p_house_obj
        if g_debug >= 2:
            print "web_controlLights.ControllPage()"
        if g_debug >= 4:
            print self.m_house_obj
        l_css = ['src/web/css/mainPage.css',
                 'src/web/lightPage.css'
                 ]
        l_js = ['src/web/js/lightControlPage.js',
                'src/web/js/floatingWindow.js'
                ]
        web_utils.add_attr_list(ControlLightsPage, l_css)
        web_utils.add_attr_list(ControlLightsPage, l_js)
        web_utils.add_float_page_attrs(ControlLightsPage)
        rend.Page.__init__(self)

    def data_controllist(self, _context, _data):
        """Build up a list of lights.
        @param _context: is a tag that we are building an object to render
        @param _data: is the page object we are extracting for.
        @return: an object to render.
        """
        l_lights = {}
        for l_key, l_obj in self.m_house_obj.Lights.iteritems():
            l_lights[l_key] = l_obj
        return l_lights

    def render_action(self, _ctx, _data):
        return web_utils.action_url()

    def render_controllist(self, _context, links):
        """
        """
        l_ret = []
        l_cnt = 0
        for l_key, l_obj in sorted(links.iteritems()):
            l_json = json.dumps(repr(l_obj))
            # print "   ", l_json
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON,
                    onclick = "createChangeControlWindow({0:})".format(l_json))
                    [ l_obj.RoomName, '_', l_obj.Name, '_',
                     l_obj.CurLevel, "\n" ])
            l_cnt += 1
        return l_ret

    def form_post_changelight(self, **kwargs):
        if g_debug >= 3:
            print "form_post_changelight()", kwargs
        l_key = int(kwargs['LightKey'])
        l_light_obj = self.m_house_obj.Lights[l_key]
        self.m_house_obj.LightingAPI.change_light_setting(self.m_house_obj, l_light_obj, int(kwargs['Level']))
        return ControlLightsPage(self, self.m_name, self.m_house_obj)

# ## END DBK
