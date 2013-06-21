'''
Created on Jun 1, 2013

@author: briank
'''

# Import system type stuff
from nevow import loaders
from nevow import rend
from nevow import static

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.web import web_housemenu


g_debug = 4
# 0 = off
# 1 = major routine entry
# 2 = Basic data


class SelectHousePage(web_utils.ManualFormMixin):
    """
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - House Select Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                # T_script(type = 'text/javascript', src = 'mainpage.js'),
                ],
            T_body[
                T_h1['PyHouse House Selection'],
                T_p['\n'],
                T_p['Select the house:'],
                T_form(name = 'mainmenuofbuttons',
                    action = U_H_child('_submit!!post'),
                    enctype = "multipart/form-data",
                    method = 'post')
                    [
                    T_table(style = 'width: 100%;', border = 0)["\n",
                        T_invisible(data = T_directive('houselist'), render = T_directive('houselist'))
                        ],  # table
                    ]  # form
                ]  # body
            ]  # html
        )  # stan

    def __init__(self, p_name, p_pyhouses_obj):
        self.m_name = p_name
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 1:
            print "web_selecthouse.SelectHousePage()"
        if g_debug >= 2:
            print "    ", p_pyhouses_obj
        rend.Page.__init__(self)
        setattr(SelectHousePage, 'child_mainpage.css', static.File('web/css/mainpage.css'))

    def data_houselist(self, _context, _data):
        l_house = {}
        for l_key, l_houses_obj in self.m_pyhouses_obj.HousesData.iteritems():
            l_house[l_key] = l_houses_obj.Object
        return l_house

    def render_houselist(self, _context, links):
        l_ret = []
        l_cnt = 0
        for l_key, l_value in sorted(links.iteritems()):
            l_name = l_value.Name
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON)
                         [ l_name])
            l_cnt += 1
        return l_ret

    def form_post_add(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_add() (HousePage)", kwargs
        return SelectHousePage(self.m_name, self.m_pyhouses_obj)

    def form_post_0(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_0()", kwargs
        if g_debug >= 5:
            print vars(self.m_pyhouses_obj)
        return web_housemenu.HouseMenuPage(self.m_name, self.m_pyhouses_obj, 0)

    def form_post_1(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_1()", kwargs
        return web_housemenu.HouseMenuPage(self.m_name, self.m_pyhouses_obj, 1)

    def form_post_2(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_2()", kwargs
        return web_housemenu.HouseMenuPage(self.m_name, self.m_pyhouses_obj, 2)

    def form_post_3(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_3()", kwargs
        return web_housemenu.HouseMenuPage(self.m_name, self.m_pyhouses_obj, 3)

    def form_post_change_house(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_change_house() (HousePage)", kwargs
        return SelectHousePage(self.m_name, self.m_pyhouses_obj)

    def form_post_deletehouse(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_deletehouse() (HousePage)", kwargs
        return SelectHousePage(self.m_name, self.m_pyhouses_obj)

    def form_post_house(self, **kwargs):
        if g_debug >= 2:
            print "web_selecthouse.form_post_house() (HousePage)", kwargs
        return SelectHousePage(self.m_name, self.m_pyhouses_obj)

# ## END DBK
