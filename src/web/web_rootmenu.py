'''
Created on May 30, 2013

@author: briank
'''

# Import system type stuff
from nevow import loaders
from nevow import rend
from nevow import static
# from nevow import url as Url
from nevow import athena
from nevow import tags as T

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.web import web_selecthouse


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# + = NOT USED HERE


# class MyElement(athena.LiveElement):
#    docFactory = loaders.stan(T.div(render = T.directive('liveElement')))


# class AjaxPage(athena.LivePage):
#    docFactory = loaders.stan(T.html[
#        T.head(render = T.directive('liveglue')),
#        T.body(render = T.directive('myElement'))])
#    jsModuleRoot = None
#    cssModuleRoot = None
#    transportRoot = None
#    _cssDepsMemo = None
#    _jsDepsMemo = None
#    _includedModules = None

#    def __init__(self, p_name, p_pyhouses_obj):
#        self.m_name = p_name
#        self.m_pyhouses_obj = p_pyhouses_obj
#        # setattr(AjaxPage, 'child_jsModuleRoot', static.File('src/web/plugins.js'))

#    def render_myElement(self, ctx, _data):
#        f = MyElement()
#        f.setFragmentParent(self)
#        return ctx.tag[f]

#    def child_(self, _ctx):
#        return AjaxPage('Root', self.m_pyhouses_obj)


class RootPage(web_utils.ManualFormMixin):
    """The main page of the web server.
    """
    addSlash = True
    docFactory = loaders.xmlfile('rootmenu.xml', templateDir = 'src/web/template')

    def __init__(self, p_name, p_pyhouses_obj):
        self.m_name = p_name
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 2:
            print "web_rootmenu.RootPage()"
        if g_debug >= 4:
            print "    ", p_pyhouses_obj
        rend.Page.__init__(self)
        setattr(RootPage, 'child_mainpage.css', static.File('src/web/css/mainpage.css'))
        setattr(RootPage, 'child_ajax.js', static.File('src/web/js/ajax.js'))
        setattr(RootPage, 'child_floating_window.js', static.File('src/web/js/floating-window.js'))
        setattr(RootPage, 'child_addhouse.js', static.File('src/web/js/addhouse.js'))
        setattr(RootPage, 'child_webserver.js', static.File('src/web/js/webserver.js'))
        setattr(RootPage, 'child_logs.js', static.File('src/web/js/logs.js'))
        #
        # setattr(RootPage, 'child_rootmenu.js', static.File('src/web/js/rootmenu.js'))
        #------------------------------------
        setattr(RootPage, 'child_bottomRight.gif', static.File('src/web/images/bottom_right.gif'))
        setattr(RootPage, 'child_close.gif', static.File('src/web/images/close.gif'))
        setattr(RootPage, 'child_minimize.gif', static.File('src/web/images/minimize.gif'))
        setattr(RootPage, 'child_topCenter.gif', static.File('src/web/images/top_center.gif'))
        setattr(RootPage, 'child_topLeft.gif', static.File('src/web/images/top_left.gif'))
        setattr(RootPage, 'child_topRight.gif', static.File('src/web/images/top_right.gif'))
        setattr(RootPage, 'child_handle.horizontal.png', static.File('src/web/images/handle.horizontal.png'))

    def render_action(self, _ctx, _data):
        return web_utils.action_url()

    def form_post(self, *args, **kwargs):
        if g_debug >= 2:
            print "web_rootmenu.form_post() - args={0:}, kwargs={1:}".format(args, kwargs)
        return RootPage('Root', self.m_pyhouses_obj)

    def form_post_add(self, **kwargs):
        """Add House button post processing.
        """
        if g_debug >= 2:
            print "web_rootmenu.form_post_add()", kwargs
        # TODO: validate and create a new house.
        return RootPage('House', self.m_pyhouses_obj)

    def form_post_change_logs(self, **kwargs):
        """Log change form.
        """
        if g_debug >= 2:
            print "web_rootmenu.form_post_change_logs()", kwargs
        return RootPage('House', self.m_pyhouses_obj)

    def form_post_change_web(self, **kwargs):
        """Web server button post processing.
        """
        if g_debug >= 2:
            print "web_rootmenu.form_post_change_web()", kwargs
        self.m_pyhouses_obj.WebData.WebPort = kwargs['WebPort']
        return RootPage('House', self.m_pyhouses_obj)

    def form_post_quit(self, *args, **kwargs):
        """Quit the GUI - this also means quitting all of PyHouse !!
        """
        if g_debug >= 2:
            print "web_rootmenu.form_post_quit() - args={0:}, kwargs={1:}".format(args, kwargs)
        # TODO: config_xml.WriteConfig()
        self.m_pyhouses_obj.API.Quit()

    def form_post_reload(self, *args, **kwargs):
        if g_debug >= 2:
            print "web_rootmenu.form_post_reload() - args={0:}, kwargs={1:}".format(args, kwargs)
        self.m_pyhouses_obj.API.Reload(self.m_pyhouses_obj)
        return RootPage('Root', self.m_pyhouses_obj)

    def form_post_select(self, **kwargs):
        """Select House button post processing.
        """
        if g_debug >= 2:
            print "web_rootmenu.form_post_select()", kwargs
        return web_selecthouse.SelectHousePage('House', self.m_pyhouses_obj)

    def form_post_select_house(self, **kwargs):
        """Select_House button post processing.
        """
        if g_debug >= 2:
            print "web_rootmenu.form_post_select_house()", kwargs
        return web_selecthouse.SelectHousePage('House', self.m_pyhouses_obj)

# ## END DBK
