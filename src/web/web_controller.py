'''
Created on Apr 8, 2013

@author: briank
'''

from nevow import loaders
from nevow import rend
from nevow import tags as Tag
from nevow import url

from src.lights import lighting

BUTTON = 'post_btn'

# Only to move the eclipse error flags to one small spot
T_body = Tag.body
T_form = Tag.form
T_h1 = Tag.h1
T_head = Tag.head
T_html = Tag.html
T_input = Tag.input
T_link = Tag.link
T_p = Tag.p
T_script = Tag.script
T_table = Tag.table
T_td = Tag.td
T_title = Tag.title
T_tr = Tag.tr

U_R_child = url.root.child
U_H_child = url.here.child

class WebLightData(lighting.LightData): pass
class WebLightingAPI(lighting.LightingAPI): pass

class ControllerPage(rend.Page, WebLightData, WebLightingAPI):
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

