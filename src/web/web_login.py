"""
Created on Jul 27, 2013

@author: briank
"""

# Import system type stuff
from nevow import loaders
from nevow import athena
from src.web import web_utils


g_debug = 4
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# + = NOT USED HERE


class LoginElement(athena.LiveElement):
    """Subclass nevow.athena.LiveElement and provide a docFactory which uses the liveElement renderer.
            docFactory = loaders.stan(T.div(render=T.directive('liveElement')))
    """

    docFactory = loaders.xmlfile('loginElement.xml', templateDir = 'src/web/template')
    jsClass = u'login.LoginElement'
    cssModules = u'mainPage'

    def say(self, text):
        if g_debug >= 3:
            print "web_login.LoginElement.say() - ", text
        pass

    say = athena.expose(say)

    def hear(self, sayer, text):
        if g_debug >= 3:
            print "web_login.LoginElement.hear() ", sayer, text
        self.callRemote("hear", sayer, text)

    say = athena.expose(say)


class MyLiveLoginPage(athena.LivePage):
    """
    """

    def handle_log_request(self, p_context, p_data):
        pass


class LoginPage(athena.LivePage): # , web_utils.ManualFormMixin):
    """Put the result liveElemebt onto a nevow.athena.LivePage.
        Be sure to have the liveElement render method.
    """
    docFactory = loaders.xmlfile('login.xml', templateDir = 'src/web/template')
    jsClass = u'login.LoginElement'
    #cssModules = u'mainPage.css'

    def __init__(self, p_name, p_pyhouses_obj, *args, **kwargs):
        self.m_name = p_name
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 2:
            print "web_login.LoginPage()"
            print "    Name =", p_name
        super(LoginPage, self).__init__(*args, **kwargs)
#        l_css = ['src/web/css/mainPage.css']
#        l_js = ['src/web/js/login.js']
#        web_utils.add_attr_list(LoginPage, l_css)
#        web_utils.add_attr_list(LoginPage, l_js)
#        web_utils.add_float_page_attrs(LoginPage)

    def child_(self, p_context):
        if g_debug >= 3:
            print "web_login.LoginPage.child_() "
            print "    Context =", p_context
        return LoginPage('RootAjax', self.m_pyhouses_obj)

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
        return web_utils.action_url()

    def render_liveElement(self, p_context, p_data):
        if g_debug >= 3:
            print "web_login.LoginPage.render_liveElement() "
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
        return LoginPage('Root', self.m_pyhouses_obj)

    def form_post_quit(self, *args, **kwargs):
        """Quit the GUI - this also means quitting all of PyHouse !!
        """
        if g_debug >= 2:
            print "web_login.form_post_quit() - args={0:}, kwargs={1:}".format(args, kwargs)
        self.m_pyhouses_obj.API.Quit()

# ## END DBK
