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



# import echothing

g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# + = NOT USED HERE


class ABCChatRoom(object):

    def __init__(self):
        if g_debug >= 3:
            print "web_rootMenu.ChatRoom() "
        self.chatters = []

    def wall(self, p_message):
        if g_debug >= 3:
            print "web_rootMenu.ChatRoom.wall() ", p_message
        for chatter in self.chatters:
            chatter.wall(p_message)

    def tellEverybody(self, p_who, p_what):
        if g_debug >= 3:
            print "web_rootMenu.ChatRoom.tellEverybody() ", p_who, p_what
        for chatter in self.chatters:
            chatter.hear(p_who.username, p_what)

    def makeChatter(self):
        if g_debug >= 3:
            print "web_rootMenu.ChatRoom.makeChatter() "
        elem = MyElement(self)
        self.chatters.append(elem)
        return elem

# element to be run with twistd
# chat = ChatRoom().makeChatter


class MyElement(athena.LiveElement):
    """Subclass nevow.athena.LiveElement and provide a docFactory which uses the liveElement renderer.
            docFactory = loaders.stan(T.div(render=T.directive('liveElement')))
    """

    docFactory = loaders.xmlfile('rootMenuElement.xml', templateDir = 'src/web/template')

    # jsClass = u'web_rootMenu.ChatRoom'

    def say(self, text):
        if g_debug >= 3:
            print "web_rootMenu.MyElement.say() - ", text
        pass

    say = athena.expose(say)

    def hear(self, sayer, text):
        if g_debug >= 3:
            print "web_rootMenu.MyElement.hear() ", sayer, text
        self.callRemote("hear", sayer, text)


class MyLiveAjaxPage(athena.LivePage):
    """
    """

    def handle_log_request(self, p_context, p_data):
        pass


class AjaxPage(athena.LivePage, web_utils.ManualFormMixin):
    """Put the result liveElemebt onto a nevow.athena.LivePage.
        Be sure to have the liveElement render method.
    """
    docFactory = loaders.xmlfile('rootMenu.xml', templateDir = 'src/web/template')

    def __init__(self, p_name, p_pyhouses_obj, *args, **kwargs):
        self.m_name = p_name
        self.m_pyhouses_obj = p_pyhouses_obj
        # kwargs['cssModuleRoot'] = 'src/web/css/'
        # kwargs['cssModules'] = 'mainPage.css'
        # kwargs['jsModuleRoot'] = '/home/briank/workspace/PyHouse/src/web/js/'
        # kwargs['jsModules'] = [
        #        'floatingWindow.js',
        #        'addHouse.js',
        #        'webServer.js',
        #        'logs.js',
        #        'rootMenu.js'
        # ]
        if g_debug >= 2:
            print "web_rootMenu.AjaxPage()"
            print "    Name =", p_name
        #    print "    PyHouses_org =", p_pyhouses_obj
        #    print "    Args =", args
        #    print "    KwArgs =", kwargs
        super(AjaxPage, self).__init__(*args, **kwargs)
        l_css = ['src/web/css/mainPage.css']
        l_js = [
                'src/web/js/floatingWindow.js',
                'src/web/js/addHouse.js',
                'src/web/js/webServer.js',
                'src/web/js/logs.js',
                'src/web/js/rootMenu.js'
                ]
        web_utils.add_attr_list(AjaxPage, l_css)
        web_utils.add_attr_list(AjaxPage, l_js)
        web_utils.add_float_page_attrs(AjaxPage)

    def child_(self, p_context):
        if g_debug >= 3:
            print "web_rootMenu.AjaxPage.child_() "
            print "    Context =", p_context
        return AjaxPage('RootAjax', self.m_pyhouses_obj)

    def data_liveElement(self, p_context, p_data):
        if g_debug >= 3:
            print "web_rootMenu.AjaxPage.data_liveElement() "
            print "    Context =", p_context
            print "    Data =", p_data

    def data_myElement(self, p_context, p_data):
        if g_debug >= 3:
            print "web_rootMenu.AjaxPage.data_myElement() "
            print "    Context =", p_context
            print "    Data =", p_data

    def render_action(self, _ctx, _data):
        return web_utils.action_url()

    def render_liveElement(self, p_context, p_data):
        if g_debug >= 3:
            print "web_rootMenu.AjaxPage.render_liveElement() "
            print "    Context =", p_context
            print "    Data =", p_data
        l_element = MyElement()
        l_element.setFragmentParent(self)
        return p_context.tag[l_element]

    def render_myElement(self, p_context, p_data):
        if g_debug >= 3:
            print "web_rootMenu.AjaxPage.render_myElement() "
            print "    Context =", p_context
            print "    Data =", p_data
        l_element = MyElement()
        l_element.setFragmentParent(self)
        return p_context.tag[l_element]

    def form_post(self, *args, **kwargs):
        if g_debug >= 2:
            print "web_rootMenu.form_post() - args={0:}, kwargs={1:}".format(args, kwargs)
        return AjaxPage('Root', self.m_pyhouses_obj)

    def form_post_add(self, **kwargs):
        """Add House button post processing.
        """
        if g_debug >= 2:
            print "web_rootMenu.form_post_add()", kwargs
        # TODO: validate and create a new house.
        return AjaxPage('House', self.m_pyhouses_obj)

    def form_post_change_logs(self, **kwargs):
        """Log change form.
        """
        if g_debug >= 2:
            print "web_rootMenu.form_post_change_logs()", kwargs
        return AjaxPage('House', self.m_pyhouses_obj)

    def form_post_change_web(self, **kwargs):
        """Web server button post processing.
        """
        if g_debug >= 2:
            print "web_rootMenu.form_post_change_web()", kwargs
        self.m_pyhouses_obj.WebData.WebPort = kwargs['WebPort']
        return AjaxPage('House', self.m_pyhouses_obj)

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
        return AjaxPage('Root', self.m_pyhouses_obj)

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
