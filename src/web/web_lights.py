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


g_debug = 4
# 0 = off
# 1 = major routine entry
# 2 = Basic data

g_logger = None

class LightsPage(web_utils.ManualFormMixin):
    """
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - Lights Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                T_script(type = 'text/javascript', src = 'housepage.js')["\n"],
                ],  # head
            T_body[
                T_h1['PyHouse Schedule'],
                T_p['Select the schedule:'],
                T_form(name = 'mainmenuofbuttons',
                       action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post') [
                    T_table(style = 'width: 100%;', border = 0)["\n",
                        T_invisible(data = T_directive('lightslist'), render = T_directive('lightslist')),
                        T_tr[
                            T_td[
                            T_input(type = "button", onclick = "createNewLightWindow('-1', )", value = "Add Light"),
                            T_input(type = "submit", value = "Back", name = BUTTON),
                                ],  # td
                            ],  # tr
                        ],  # table
                   ]  # form
                ]  # body
            ]  # html
        )  # stan

    def __init__(self, p_parent, p_name, p_house_obj):
        self.m_name = p_name
        self.m_parent = p_parent
        self.m_house_obj = p_house_obj
        if g_debug >= 1:
            print "web_lights.LightsPage()"
        if g_debug >= 5:
            print self.m_house_obj
        rend.Page.__init__(self)
        setattr(LightsPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(LightsPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(LightsPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(LightsPage, 'child_lightpage.js', static.File('web/js/lightpage.js'))
        #------------------------------------
        setattr(LightsPage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(LightsPage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(LightsPage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(LightsPage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(LightsPage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(LightsPage, 'child_topRight.gif', static.File('web/images/top_right.gif'))
        setattr(LightsPage, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))

    def data_lightslist(self, _context, _data):
        """Build up a list of lights.
        @param _context: is a tag that we are building an object to render
        @param _data: is the page object we are extracting for.
        @return: an object to render.
        """
        if g_debug >= 4:
            print "web_lights.data_lightslist() ", self.m_house_obj
        l_lights = {}
        for l_key, l_obj in self.m_house_obj.Lights.iteritems():
            l_lights[l_key] = l_obj
        return l_lights

    def render_lightslist(self, _context, links):
        """
        @param: _context is ...
        @param: links are ...
        @return: the list to be added into the stan.dom
        """
        if g_debug >= 1:
            print "web_lights.render_lightslist()"
        l_ret = []
        l_cnt = 0
        for l_key, l_obj in sorted(links.iteritems()):
            l_json = json.dumps(repr(l_obj))
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON,
                    onclick = "createChangeLightWindow({0:})".format(l_json))
                         [ l_obj.Name, "\n" ])
            l_cnt += 1
        return l_ret



    def form_post_rooms(self, **kwargs):
        if g_debug >= 2:
            print "form_post_rooms()", kwargs
        return LightsPage(self, self.m_name, self.m_house_obj)

    def form_post_lights(self, **kwargs):
        if g_debug >= 2:
            print "form_post_lights", kwargs
        return LightsPage(self.m_name, self.m_house_obj)

    def form_post_schedules(self, **kwargs):
        if g_debug >= 2:
            print "form_post_schedules()", kwargs
        return LightsPage(self.m_name, self.m_house_obj)


    def form_post_house(self, **kwargs):
        if g_debug >= 2:
            print "form_post_house (HousePage)", kwargs
        return LightsPage(self.m_name, self.m_house_obj)

# ## END DBK
