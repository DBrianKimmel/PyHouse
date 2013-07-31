"""
Created on Jul 27, 2013

@author: briank
"""

# Import system type stuff
from nevow import loaders
from nevow import athena
from src.web import web_utils
from src.web import web_rootMenu


g_debug = 4
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# + = NOT USED HERE


class LoginElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile('loginElement.xml', templateDir = 'src/web/template')
    jsClass = u'login.LoginElement'

    def __init__(self):
        if g_debug > +2:
            print "web_login.LoginElement()"
        pass

    def login(self, text):
        if g_debug >= 3:
            print "web_login.LoginElement.login() - ", text
        pass
    login = athena.expose(login)

    def hear(self, sayer, text):
        if g_debug >= 3:
            print "web_login.LoginElement.hear() ", sayer, text
        self.callRemote("hear", sayer, text)
    hear = athena.expose(hear)


class LoginPage(athena.LivePage): # , web_utils.ManualFormMixin):
    """Put the result liveElement onto a nevow.athena.LivePage.
        Be sure to have the liveElement render method.
    """
    docFactory = loaders.xmlfile('login.xml', templateDir = 'src/web/template')

    def __init__(self, p_name, p_pyhouses_obj, *args, **kwargs):
        self.m_name = p_name
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 2:
            print "web_login.LoginPage()"
            print "    Name =", p_name
        super(LoginPage, self).__init__(*args, **kwargs)
#
    def child_(self, p_context):
        if g_debug >= 3:
            print "web_login.LoginPage.child_() "
            print "    Context =", p_context
        return LoginPage('LoginPage 2', self.m_pyhouses_obj)
        #return web_rootMenu.RootMenuPage('RootMenuPage_2', self.m_pyhouses_obj)

    def data_liveElement(self, p_context, p_data):
        if g_debug >= 3:
            print "web_login.LoginPage.data_liveElement() "
            print "    Context =", p_context
            print "    Data =", p_data

    def data_myElement(self, p_context, p_data):
        if g_debug >= 3:
            print "web_login.LoginPage.data_myElement() "
            print "    Context =", p_context
            print "    Data =", p_data

    def render_action(self, _ctx, _data):
        if g_debug >= 3:
            print "web_login.LoginPage.render_action() "
        return web_utils.action_url()

    def render_debug(self, p_context, p_data):
        if g_debug >= 3:
            print "web_login.LoginPage.render_debug() "
            print "    Context =", p_context
            print "    Data =", p_data
        l_fragment = athena.IntrospectionFragment()
        l_fragment.setFragmentParent(self)
        return p_context.tag[l_fragment]

    def render_liveElement(self, p_context, p_data):
        if g_debug >= 3:
            print "web_login.LoginPage.render_liveElement() "
            print "    Context =", p_context
            print "    Data =", p_data
        l_element = LoginElement()
        l_element.setFragmentParent(self)
        return p_context.tag[l_element]

    def render_livePage(self, p_context, p_data):
        if g_debug >= 3:
            print "web_login.LoginPage.render_livePage() "
            print "    Context =", p_context
            print "    Data =", p_data
        l_element = LoginElement()
        l_element.setFragmentParent(self)
        return p_context.tag[l_element]

    def render_loginElement(self, p_context, p_data):
        if g_debug >= 3:
            print "web_login.LoginPage.render_loginElement() "
            print "    Context =", p_context
            print "    Data =", p_data
        l_element = LoginElement()
        l_element.setFragmentParent(self)
        return p_context.tag[l_element]

    def form_post(self, *args, **kwargs):
        if g_debug >= 2:
            print "web_login.form_post() - args={0:}, kwargs={1:}".format(args, kwargs)
        return web_rootMenu.RootMenuPage('RootMenu', self.m_pyhouses_obj)

    def form_post_quit(self, *args, **kwargs):
        """Quit the GUI - this also means quitting all of PyHouse !!
        """
        if g_debug >= 2:
            print "web_login.form_post_quit() - args={0:}, kwargs={1:}".format(args, kwargs)
        self.m_pyhouses_obj.API.Quit()

# ## END DBK
