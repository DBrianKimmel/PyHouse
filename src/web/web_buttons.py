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
from src.web import web_rooms


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = Basic data

g_logger = None

class ButtonsPage(web_utils.ManualFormMixin):
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
                T_script(type = 'text/javascript', src = 'buttonspage.js')["\n"],
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
                            T_td[ T_input(type = 'submit', value = 'Schedule', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Control Lights', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Internet', name = BUTTON), ],
                            ]
                        ]  # table
                    ]  # form
                ]  # body
            ]  # html
        )  # stan

    def __init__(self, p_parent, p_name, p_house_obj):
        self.m_name = p_name
        self.m_parent = p_parent
        self.m_house_obj = p_house_obj
        if g_debug >= 1:
            print "web_buttons.ButtonPage()"
        if g_debug >= 5:
            print self.m_house_obj
        rend.Page.__init__(self)
        setattr(ButtonsPage, 'child_lightpage.css', static.File('web/css/lightpage.css'))
        setattr(ButtonsPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(ButtonsPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(ButtonsPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(ButtonsPage, 'child_controllerspage.js', static.File('web/js/controllerspage.js'))
        #------------------------------------
        setattr(ButtonsPage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(ButtonsPage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(ButtonsPage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(ButtonsPage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(ButtonsPage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(ButtonsPage, 'child_topRight.gif', static.File('web/images/top_right.gif'))
        setattr(ButtonsPage, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))

        setattr(ButtonsPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))

    def form_post_rooms(self, **kwargs):
        if g_debug >= 2:
            print "form_post_rooms()", kwargs
        return web_rooms.RoomsPage(self, self.m_name, self.m_house_obj)

    def form_post_lights(self, **kwargs):
        if g_debug >= 2:
            print "form_post_lights", kwargs
        return ButtonsPage(self.m_name, self.m_house_obj)

    def form_post_schedules(self, **kwargs):
        if g_debug >= 2:
            print "form_post_schedules()", kwargs
        return ButtonsPage(self.m_name, self.m_house_obj)


    def form_post_house(self, **kwargs):
        if g_debug >= 2:
            print "form_post_house (HousePage)", kwargs
        return ButtonsPage(self.m_name, self.m_house_obj)

# ## END DBK
