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


g_debug = 3
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Dump JSON
# + = NOT USED HERE


class LightsPage(web_utils.ManualFormMixin):
    """
    """
    addSlash = True
    docFactory = loaders.xmlfile('lights.xml', templateDir = 'src/web/template')

    def __init__(self, p_parent, p_name, p_house_obj):
        self.m_name = p_name
        self.m_parent = p_parent
        self.m_house_obj = p_house_obj
        if g_debug >= 2:
            print "web_lights.LightsPage()"
        l_css = ['src/web/css/lightPage.css', 'src/web/css/mainPage.css']
        l_js = ['src/web/js/ajax.js', 'src/web/js/floatingWindow.js',
                'src/web/js/lightPage.js']
        web_utils.add_attr_list(LightsPage, l_css)
        web_utils.add_attr_list(LightsPage, l_js)
        web_utils.add_float_page_attrs(LightsPage)
        rend.Page.__init__(self)

    def data_lightslist(self, _context, _data):
        """Build up a list of lights.
        @param _context: is a tag that we are building an object to render
        @param _data: is the page object we are extracting for.
        @return: an object to render.
        """
        if g_debug >= 2:
            print "web_lights.data_lightslist() ", self.m_house_obj
        l_lights = {}
        for l_key, l_obj in self.m_house_obj.Lights.iteritems():
            l_lights[l_key] = l_obj
        return l_lights

    def render_action(self, _ctx, _data):
        return web_utils.action_url()

    def render_lightslist(self, context, links):
        """
        @param: _context is ...
        @param: links are ...
        @return: the list to be added into the stan.dom
        """
        if g_debug >= 2:
            print "web_lights.render_lightslist()"
        l_ret = "<tr>\n"
        l_cnt = 0
        for l_key, l_obj in sorted(links.iteritems()):
            l_json = json.dumps(repr(l_obj))
            if l_cnt > 0 and l_cnt % 3 == 0:
                l_ret += "</tr><tr>\n"
            # l_ret += "<td><button onclick='createChangeLightWindow({0:})'>".format(l_json)
            # l_ret += "{0:}</button></td>\n".format(l_key)
            l_ret += "<td>..."
            l_ret += "</td>\n"
            l_cnt += 1
        l_ret += '</tr>\n'
        l_ret = context.tag()
        if g_debug >= 2:
            print "    ", l_ret
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
