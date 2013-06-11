"""
Created on Jun 3, 2013

@author: briank

Web interface to control lights for the selected house.
"""

# Import system type stuff
from nevow import loaders
from nevow import rend
from nevow import static
import json

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.web import web_rooms


g_debug = 4
# 0 = off
# 1 = major routine entry
# 2 = Basic data

g_logger = None

class ControlPage(web_utils.ManualFormMixin):
    """
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - House Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_H_child('lightpage.css'))["\n"],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                T_script(type = 'text/javascript', src = 'controlpage.js')["\n"],
                ],  # head
            T_body[
                T_h1['PyHouse Houses'],
                T_p['Select Light:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    T_invisible(data = T_directive('lightlist'), render = T_directive('lightlist'))
                    ]  # table
                ]  # body
            ]  # html
        )  # stan

    def __init__(self, name, p_house_obj):
        self.name = name
        self.m_house_obj = p_house_obj
        if g_debug >= 1:
            print "web_housemenu.HouseMenuPage.__init__()"
        if g_debug >= 5:
            print self.m_house_obj
        rend.Page.__init__(self)

        setattr(ControlPage, 'child_lightpage.css', static.File('web/css/lightpage.css'))
        setattr(ControlPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(ControlPage, 'child_controlpage.js', static.File('web/js/schedpage.js'))
        setattr(ControlPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(ControlPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        #------------------------------------
        setattr(ControlPage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(ControlPage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(ControlPage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(ControlPage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(ControlPage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(ControlPage, 'child_topRight.gif', static.File('web/images/top_right.gif'))
        setattr(ControlPage, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))

    def data_lightlist(self, _context, _data):
        """Build up a list of lights.
        @param _context: is a tag that we are building an object to render
        @param _data: is the page object we are extracting for.
        @return: an object to render.
        """
        l_lights = {}
        for l_key, l_obj in self.m_house_obj.Lights.iteritems():
            l_lights[l_key] = l_obj
        return l_lights

    def render_lightlist(self, _context, links):
        """
        """
        l_ret = []
        l_cnt = 0
        for l_key, l_obj in sorted(links.iteritems()):
            l_dict = {'Name':l_obj.Name, 'Key':l_obj.Key, 'Active':l_obj.Active,
                      'CurLevel': l_obj.CurLevel, 'RoomName': l_obj.RoomName,
                      }
            l_json = json.dumps(l_dict)
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON,
                    onclick = "createChangeScheduleWindow('{0:}')".format(l_json))
                    [ l_obj.Name, '_', l_obj.RoomName, '_',
                     l_obj.CurLevel, "\n" ])
            l_cnt += 1
        return l_ret

    def form_post_rooms(self, **kwargs):
        if g_debug >= 2:
            print "form_post_rooms()", kwargs
        return web_rooms.RoomsPage(self.name, self.m_house_obj)

    def form_post_lights(self, **kwargs):
        if g_debug >= 2:
            print "form_post_lights", kwargs
        return ControlPage(self.name, self.m_house_obj)

    def form_post_schedules(self, **kwargs):
        if g_debug >= 2:
            print "form_post_schedules()", kwargs
        return ControlPage(self.name, self.m_house_obj)


    def form_post_house(self, **kwargs):
        if g_debug >= 2:
            print "form_post_house (HousePage)", kwargs
        return ControlPage(self.name, self.m_house_obj)

# ## END DBK
