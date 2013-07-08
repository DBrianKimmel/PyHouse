"""
Created on May 30, 2013

@author: briank
"""

# Import system type stuff
from nevow import loaders
from nevow import rend
from nevow import athena

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.web import web_houseSelect



# import echothing

g_debug = 4
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# + = NOT USED HERE


class ChatRoom(object):

    def __init__(self):
        self.chatters = []

    def wall(self, message):
        for chatter in self.chatters:
            chatter.wall(message)

    def tellEverybody(self, who, what):
        for chatter in self.chatters:
            chatter.hear(who.username, what)

    def makeChatter(self):
        elem = MyElement(self)
        self.chatters.append(elem)
        return elem

# element to be run with twistd
chat = ChatRoom().makeChatter


class MyElement(athena.LiveElement):
    docFactory = loaders.xmlfile('rootMenu.xml', templateDir = 'src/web/template')
    jsClass = u'rootMenu.ChatterBox'

def say(self, text):
    # for chatter in chatRoom:
    #    chatter.youHeardSomething(text)
    pass

say = athena.expose(say)

def hear(self, sayer, text):
    self.callRemote("hear", sayer, text)


class AjaxPage(athena.LivePage):
    docFactory = loaders.xmlfile('rootMenu.xml', templateDir = 'src/web/template')

    def __init__(self, p_name, p_pyhouses_obj, *args, **kwargs):
        self.m_name = p_name
        self.m_pyhouses_obj = p_pyhouses_obj
        super(AjaxPage, self).__init__(*args, **kwargs)
        if g_debug >= 2:
            print "web_rootMenu.AjaxPage()"
        l_css = ['src/web/css/mainPage.css']
        l_js = ['src/web/js/ajax.js', 'src/web/js/floatingWindow.js',
                'src/web/js/addHouse.js', 'src/web/js/webServer.js',
                'src/web/js/logs.js',
                'src/web/js/rootMenu.js']
        web_utils.add_attr_list(AjaxPage, l_css)
        web_utils.add_attr_list(AjaxPage, l_js)
        web_utils.add_float_page_attrs(AjaxPage)

    def render_myElement(self, ctx, _data):
        f = MyElement()
        f.setFragmentParent(self)
        return ctx.tag[f]

    def child_(self, _ctx):
        return AjaxPage('Root', self.m_pyhouses_obj)


class RootPage(web_utils.ManualFormMixin):
    """The main page of the web server.
    """
    addSlash = True
    docFactory = loaders.xmlfile('rootMenu.xml', templateDir = 'src/web/template')

    def __init__(self, p_name, p_pyhouses_obj):
        self.m_name = p_name
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 2:
            print "web_rootMenu.RootPage()"
        if g_debug >= 4:
            print "    ", p_pyhouses_obj
        l_css = ['src/web/css/mainPage.css']
        l_js = ['src/web/js/ajax.js', 'src/web/js/floatingWindow.js',
                'src/web/js/addHouse.js', 'src/web/js/webServer.js',
                'src/web/js/logs.js']
        web_utils.add_attr_list(RootPage, l_css)
        web_utils.add_attr_list(RootPage, l_js)
        web_utils.add_float_page_attrs(RootPage)
        rend.Page.__init__(self)
        if g_debug > -0:
            print "    Vars=", vars(RootPage)

    def render_action(self, _ctx, _data):
        return web_utils.action_url()

    def form_post(self, *args, **kwargs):
        if g_debug >= 2:
            print "web_rootMenu.form_post() - args={0:}, kwargs={1:}".format(args, kwargs)
        return RootPage('Root', self.m_pyhouses_obj)

    def form_post_add(self, **kwargs):
        """Add House button post processing.
        """
        if g_debug >= 2:
            print "web_rootMenu.form_post_add()", kwargs
        # TODO: validate and create a new house.
        return RootPage('House', self.m_pyhouses_obj)

    def form_post_change_logs(self, **kwargs):
        """Log change form.
        """
        if g_debug >= 2:
            print "web_rootMenu.form_post_change_logs()", kwargs
        return RootPage('House', self.m_pyhouses_obj)

    def form_post_change_web(self, **kwargs):
        """Web server button post processing.
        """
        if g_debug >= 2:
            print "web_rootMenu.form_post_change_web()", kwargs
        self.m_pyhouses_obj.WebData.WebPort = kwargs['WebPort']
        return RootPage('House', self.m_pyhouses_obj)

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
        return RootPage('Root', self.m_pyhouses_obj)

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
