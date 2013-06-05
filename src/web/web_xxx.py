'''
Created on Jun 2, 2013

@author: briank
'''

'''
Created on May 30, 2013

@author: briank
'''
#!/usr/bin/python

"""Web server module.
This is a Main Module - always present.

TODO: format doc strings to Epydoc standards.
"""

# Import system type stuff
import datetime
import logging
import os
import random
import xml.etree.ElementTree as ET
import twisted.python.components as tpc
# from twisted.internet import protocol
from twisted.internet import reactor
# from twisted.protocols import basic
from nevow import appserver
from nevow import flat
from nevow import inevow
from nevow import loaders
from nevow import rend
from nevow import static
from nevow import tags as Tag
from nevow import url
from nevow import util
from nevow.rend import _CARRYOVER
from formless import iformless

# Import PyMh files and modules.
from src.utils import xml_tools
from src.lights import lighting
from src.scheduling import schedule
from src.utils import config_xml


g_debug = 8

g_port = 8580
g_logger = None
g_houses_obj = None

SUBMIT = '_submit'
BUTTON = 'post_btn'

# Entertainment = {}
Lights = {}
XLight_Data = {}

# Only to move the eclipse error flags to one small spot
T_p = Tag.p
T_h1 = Tag.h1
T_td = Tag.td
T_tr = Tag.tr
T_html = Tag.html
T_head = Tag.head
T_body = Tag.body
T_form = Tag.form
T_link = Tag.link
T_table = Tag.table
T_title = Tag.title
T_input = Tag.input
T_script = Tag.script
U_R_child = url.root.child
U_H_child = url.here.child

listenTCP = reactor.listenTCP

class WebLightData(lighting.LightData): pass
class WebLightingAPI(lighting.LightingAPI): pass

class WebSceneData(lighting.SceneData): pass
class WebSceneAPI(lighting.SceneAPI): pass

class WebException(Exception):
    """Raised when there is a web error of some sort.
    """

class WebData(object):
    """
    """
    def __init__(self):
        self.WebPort = 8580


class EntertainmentPage(rend.Page):
    """
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html[
            T_title['PyHouse - Entertainment Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
            T_body[
                T_h1['PyHouse Entertainment'],
                T_p['Select the entertainment:'],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )[
                    T_input(type = 'submit', value = 'Add Entertainment', name = BUTTON),
                    T_input(type = 'submit', value = 'Delete Entertainment', name = BUTTON)
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

class HousePage(rend.Page):
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
                T_script(type = 'text/javascript', src = 'housepage.js')["\n"],
                ],
            T_body[
                T_h1['PyHouse Houses'],
                T_p['\n'],
                T_p['Select the house to control:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    Tag.invisible(data = Tag.directive('houselist'), render = Tag.directive('houselist'))
                    ],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )["\n",
                    T_input(type = 'button', onclick = "createNewHouseWindow('1')", value = 'add')
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

    def data_houselist(self, _context, _data):
        l_house = {}
        for l_key, l_obj in g_houses_obj.iteritems():
            l_house[l_key] = l_obj.Object
        return l_house

    def render_houselist(self, _context, links):
        l_ret = []
        l_cnt = 0
        for l_key, l_value in sorted(links.iteritems()):
            l_name = l_value.Name
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON, onclick = "createChangeHouseWindow(\'{0:}\', \'{1:}\' )".format(
                        l_value.Name, l_value.Active))
                         [ l_name])
            l_cnt += 1
        return l_ret

    def form_post_add(self, **kwargs):
        print "form_post_addhouse (HousePage)", kwargs
        return HousePage(self.name)

    def form_post_change_house(self, **kwargs):
        print "form_post_change_house (HousePage)", kwargs
        return HousePage(self.name)

    def form_post_deletehouse(self, **kwargs):
        print "form_post_deletehouse (HousePage)", kwargs
        return HousePage(self.name)

    def form_post_house(self, **kwargs):
        print "form_post_house (HousePage)", kwargs
        return HousePage(self.name)

class LightingPage(rend.Page, WebLightData, WebLightingAPI):
    """Define the page layout of the lighting selection web page.
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - Lighting Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                T_script(type = 'text/javascript', src = 'lightpage.js')["\n"],
                ],
            T_body[
                T_h1['PyHouse Lighting'],
                T_p['\n'],
                T_p['Select the light to control:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    Tag.invisible(data = Tag.directive('lightlist'), render = Tag.directive('lightlist'))
                    ],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )["\n",
                    T_input(type = 'button', onclick = "createNewLightWindow('1234')", value = 'Add Light'),
                    T_input(type = 'submit', value = 'Scan Lights', name = BUTTON)
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

    def data_lightlist(self, _context, _data):
        """Build up a list of lights.
        Omit controllers and buttons (scenes???)
        """
        l_light = {}
        for l_key, l_obj in lighting.Light_Data.iteritems():
            if l_obj.Family != 'Insteon': continue
            if l_obj.Type != 'Light': continue
            # l_obj.CurLevel = lighting.Light_Data[l_key].CurLevel
            # if l_obj.Type == 'Light':
            l_light[l_key] = l_obj
        return l_light

    def render_lightlist(self, _context, links):
        """Place buttons for each light on the page.
        """
        global l_ret
        l_ret = []
        l_cnt = 0
        for l_key, l_value in sorted(links.iteritems()):
            l_cur_lev = l_value.CurLevel
            l_family = l_value.Family
            l_type = l_value.Type
            l_name = l_value.Name
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON, onclick = "createChangeLightWindow(\'{0:}\',\'{1:}\',\'{2:}\')".format(l_key, l_cur_lev, l_family))
                         [ l_family, '-', l_type, ':', l_name, ' ', l_cur_lev])
            l_cnt += 1
        return l_ret

    def load_all_light_info(self):
        global Light_Data
        pass

    def _store_light(self, **kwargs):
        """Send the updated lighting info back to the lighting module.
        Update the lighting page with the new information.
        """
        global Lights
        l_name = kwargs['Name']
        Lights[l_name] = {}
        Lights[l_name]['Address'] = kwargs['Address']
        Lights[l_name]['Family'] = kwargs['Family']
        Lights[l_name]['Type'] = kwargs['Type']
        Lights[l_name]['Controller'] = kwargs['Controller']
        Lights[l_name]['Dimmable'] = kwargs['Dimmable']
        Lights[l_name]['Coords'] = kwargs['Coords']
        Lights[l_name]['Master'] = kwargs['Master']
        lighting.LightingUtility().update_all_lighting_families()

    def form_post_addlight(self, **kwargs):
        print " - form_post_addlight - ", kwargs
        self._store_light(**kwargs)
        return LightingPage(self.name)

    def form_post_changelight(self, **kwargs):
        """Browser user changed a light (on/off/dim)
        Now send the change to the light.
        """
        print " - form_post_changelight - kwargs=", kwargs
        return LightingPage(self.name)

    def form_post_deletelight(self, **kwargs):
        print " - form_post_delete - ", kwargs
        global Lights
        del Lights[kwargs['Name']]
        lighting.LightingUtility().update_all_lighting_families()
        return LightingPage(self.name)

    def form_post_scan(self, **kwargs):
        """Trigger a scan of all lights and then update light info.
        """
        print " - form_post_scan- ", kwargs
        return LightingPage(self.name)

    def form_post_lighting(self, **kwargs):
        print " - form_post_lighting - ", kwargs
        return LightingPage(self.name)

class LocationPage(rend.Page): pass

class ScenesPage(rend.Page):
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - Scenes Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                T_script(type = 'text/javascript', src = 'scenepage.js')["\n"],
                ],
            T_body[
                T_h1['PyHouse Scenes'],
                T_p['\n'],
                T_p['Select the scene:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    Tag.invisible(data = Tag.directive('scenelist'), render = Tag.directive('scenelist'))
                    ],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )["\n",
                    T_input(type = 'button', onclick = "createNewSceneWindow()", value = 'Add Scene'),
                    T_input(type = 'submit', value = 'Scan Lights', name = BUTTON)
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

    def _store_scene(self, **kwargs):
        pass

    def data_scenelist(self, _context, _data):
        """Build up a list of Scenes.
        """
        l_scene = {}
        for l_key, l_obj in lighting.Scene_Data.iteritems():
            l_scene[l_key] = l_obj
        return l_scene

    def render_scenelist(self, _context, links):
        """Place buttons for each scene on the page.
        """
        global l_ret
        l_ret = []
        l_cnt = 0
        for l_key, l_value in sorted(links.iteritems()):
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON, onclick = "createChangeSceneWindow(\'{0:}\', '100', '2s')".format(l_key))
                         [ l_value.Name, "\n" ])
            l_cnt += 1
        return l_ret

    def form_post_addscene(self, **kwargs):
        print " - form_post_add - ", kwargs
        self._store_scene(**kwargs)
        return ScenesPage(self.name)

    def form_post_changescene(self, **kwargs):
        pass

    def form_post_deletescene(self, **kwargs):
        print " - form_post_deleteScene - ", kwargs


class API(object):

    def __init__(self, p_parent, p_houses_api):
        global g_logger
        g_logger = logging.getLogger('PyHouse.WebServ ')
        global g_parent, g_houses_api
        g_parent = p_parent
        g_houses_api = p_houses_api
        if g_debug >= 1:
            print "web_server.API.__init__()"
        Web_Data[0] = WebData()
        Web_Data[0].WebPort = 8580
        g_logger.info("Initialized - Start the web server on port {0:}".format(g_port))

    def Start(self, p_houses_obj):
        global g_houses_obj
        g_houses_obj = p_houses_obj
        if g_debug >= 1:
            print "web_server.Start()", p_houses_obj
        g_site_dir = os.path.split(os.path.abspath(__file__))[0]
        print "Webserver path = ", g_site_dir
        l_site = appserver.NevowSite(RootPage('/'))
        WebUtilities().build_child_tree()
        listenTCP(g_port, l_site)
        g_logger.info("Started.")

    def Stop(self):
        if g_debug >= 1:
            print "web_server.Stop()"


Web_Data = {}

# ## END DBK
