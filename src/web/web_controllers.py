'''
Created on Apr 8, 2013

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


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Dump JSON
# + = NOT USED HERE


class ControllersPage(web_utils.ManualFormMixin):
    """Define the page layout of the lighting selection web page.
    """
    addSlash = True
    docFactory = loaders.xmlfile('controllers.xml', templateDir = 'src/web/template')

    def __init__(self, p_parent, p_name, p_house_obj):
        self.m_name = p_name
        self.m_parent = p_parent
        self.m_house_obj = p_house_obj
        if g_debug >= 2:
            print "web_controllers.ControllersPage()"
        rend.Page.__init__(self)
        l_css = ['src/web/css/lightPage.css', 'src/web/css/mainPage.css']
        l_js = ['src/web/js/ajax.js', 'src/web/js/floatingWindow.js',
                'src/web/js/controllersPage.js']
        web_utils.add_attr_list(ControllersPage, l_css)
        web_utils.add_attr_list(ControllersPage, l_js)
        web_utils.add_float_page_attrs(ControllersPage)

    def data_controllerslist(self, _context, _data):
        """Build up a list of controllers.
        """
        if g_debug >= 2:
            print "web_controllers.data_controllerslist()"
        l_controller = {}
        for l_key, l_obj in self.m_house_obj.Controllers.iteritems():
            l_controller[l_key] = l_obj
        return l_controller

    def render_action(self, _ctx, _data):
        return web_utils.action_url()

    def render_controllerslist(self, _context, links):
        """Place buttons for each light on the page.
        """
        if g_debug >= 2:
            print "web_controllers.render_controllerslist()"
        l_ret = []
        l_cnt = 0
        for l_key, l_obj in sorted(links.iteritems()):
            l_json = json.dumps(repr(l_obj))
            if g_debug >= 4:
                print "    json = ", l_json
                print "    vars = ", vars(l_obj)
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'button', value = l_key, name = BUTTON,
                    onclick = "createChangeControllerWindow({0:})".format(l_json))
                         [ l_obj.Name])
            l_cnt += 1
        return l_ret

    def _store_controller(self, **kwargs):
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
        # lighting.LightingUtility().update_all_lighting_families()

    def form_post(self, **kwargs):
        print " - form_post - ", kwargs
        self._store_light(**kwargs)
        return ControllersPage(self.m_name, self.m_house_obj)

    def form_post_add(self, **kwargs):
        print " - form_post_add - ", kwargs
        self._store_light(**kwargs)
        return ControllersPage(self.m_name, self.m_house_obj)

    def form_post_back(self, **kwargs):
        print " - form_post_back - ", kwargs
        self._store_light(**kwargs)
        return ControllersPage(self.m_name, self.m_house_obj)

    def form_post_cancel(self, **kwargs):
        print " - form_post_cancel - ", kwargs
        self._store_light(**kwargs)
        return ControllersPage(self.m_name, self.m_house_obj)

# ## END DBK
