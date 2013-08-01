"""
Created on May 30, 2013

@author: briank
"""

# Import system type stuff
from nevow import loaders
# from nevow import rend
from nevow import athena
# from nevow import appserver
# from nevow import tags as T
# Import PyMh files and modules.
# from src.web.web_tagdefs import *
from src.web import web_utils
from src.web import web_houseSelect


g_debug = 4
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# + = NOT USED HERE


class Username(object):
    """
    """


class RootMenuElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile('rootMenuElement.xml', templateDir = 'src/web/template')


class RootMenuPage(athena.LivePage):
    """Put the result liveElement onto a nevow.athena.LivePage.
        Be sure to have the liveElement render method.
    """
    docFactory = loaders.xmlfile('rootMenu.xml', templateDir = 'src/web/template')

    def __init__(self, p_name, p_pyhouses_obj, *args, **kwargs):
        self.m_name = p_name
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 2:
            print "web_rootMenu.RootMenuPage() - Name =", p_name
            print "    PyHouses = {0:}".format(p_pyhouses_obj)
        super(RootMenuPage, self).__init__(*args, **kwargs)

    def child_(self, p_context):
        if g_debug >= 3:
            print "web_rootMenu.RootMenuPage.child_() "
            print "    Context =", p_context
        return RootMenuPage('Root_Menu_2', self.m_pyhouses_obj)

    def render_livePage(self, p_context, p_data):
        if g_debug >= 3:
            print "web_rootMenu.render_livePage() "
            print "    Context =", p_context
            print "    Data =", p_data
        l_element = RootMenuElement(self.m_pyhouses_obj)
        l_element.setFragmentParent(self)
        return p_context.tag[l_element]

    def render_username(self, p_context, p_data):
        """
        Replace the tag with a new L{RootMenuElement}.
        """
        if g_debug >= 3:
            print "web_rootMenu.render_username() "
        l_div = RootMenuElement(Username())
        l_div.setFragmentParent(self)
        return l_div


    def render_action(self, _ctx, _data):
        return web_utils.action_url()

    def form_post(self, *args, **kwargs):
        if g_debug >= 2:
            print "web_rootMenu.form_post() - args={0:}, kwargs={1:}".format(args, kwargs)
        return RootMenuPage('Root', self.m_pyhouses_obj)

    def form_post_add(self, **kwargs):
        """Add House button post processing.
        """
        if g_debug >= 2:
            print "web_rootMenu.form_post_add()", kwargs
        # TODO: validate and create a new house.
        return RootMenuPage('House', self.m_pyhouses_obj)

    def form_post_change_logs(self, **kwargs):
        """Log change form.
        """
        if g_debug >= 2:
            print "web_rootMenu.form_post_change_logs()", kwargs
        return RootMenuPage('House', self.m_pyhouses_obj)

    def form_post_change_web(self, **kwargs):
        """Web server button post processing.
        """
        if g_debug >= 2:
            print "web_rootMenu.form_post_change_web()", kwargs
        self.m_pyhouses_obj.WebData.WebPort = kwargs['WebPort']
        return RootMenuPage('House', self.m_pyhouses_obj)

    def form_post_quit(self, *args, **kwargs):
        """Quit the GUI - this also means quitting all of PyHouse !!
        """
        if g_debug >= 2:
            print "web_rootMenu.form_post_quit() - args={0:}, kwargs={1:}".format(args, kwargs)
        # TODO: config_xml.WriteConfig()
        self.m_pyhouses_obj.API.Quit()

    def form_post_reload(self, *args, **kwargs):
        if g_debug >= 2:
            print "web_rootMenu.form_post_reload() - args={0:}, kwargs={1:}".format(args, kwargs)
        self.m_pyhouses_obj.API.Reload(self.m_pyhouses_obj)
        return RootMenuPage('Root', self.m_pyhouses_obj)

    def form_post_select(self, **kwargs):
        """Select House button post processing.
        """
        if g_debug >= 2:
            print "web_rootMenu.form_post_select()", kwargs
        return web_houseSelect.SelectHousePage('House', self.m_pyhouses_obj)

    def form_post_select_house(self, **kwargs):
        """Select_House button post processing.
        """
        if g_debug >= 2:
            print "web_rootMenu.form_post_select_house()", kwargs
        return web_houseSelect.SelectHousePage('House', self.m_pyhouses_obj)

# ## END DBK
