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
                T_script(type = 'text/javascript', src = 'slider.js'),
                T_script(type = 'text/javascript', src = 'range.js'),
                T_script(type = 'text/javascript', src = 'controlpage.js')["\n"],
                ],  # head
            T_body[
                T_h1['PyHouse Houses'],
                T_p['Select Light:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    T_invisible(data = T_directive('controllist'), render = T_directive('controllist'))
                    ]  # table
                ]  # body
            ]  # html
        )  # stan

    def __init__(self, p_parent, p_name, p_house_obj):
        self.m_name = p_name
        self.m_parent = p_parent
        self.m_house_obj = p_house_obj
        if g_debug >= 1:
            print "web_control.ControllPage()"
        if g_debug >= 5:
            print self.m_house_obj
        rend.Page.__init__(self)

        setattr(ControlPage, 'child_lightpage.css', static.File('web/css/lightpage.css'))
        setattr(ControlPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(ControlPage, 'child_controlpage.js', static.File('web/js/controlpage.js'))
        setattr(ControlPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(ControlPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(ControlPage, 'child_slider.js', static.File('web/js/slider.js'))
        setattr(ControlPage, 'child_range.js', static.File('web/js/range.js'))
        #------------------------------------
        setattr(ControlPage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(ControlPage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(ControlPage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(ControlPage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(ControlPage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(ControlPage, 'child_topRight.gif', static.File('web/images/top_right.gif'))
        setattr(ControlPage, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))

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
        if g_debug >= 2:
            print "form_post_changelight()", kwargs
        return web_rooms.RoomsPage(self, self.m_name, self.m_house_obj)

# ## END DBK
