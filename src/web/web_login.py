"""
Created on Jul 27, 2013

@author: briank
"""

# Import system type stuff
from twisted.python.filepath import FilePath
from nevow import loaders
from nevow import athena
import json

# Import PyMh files and modules.
from src.web import web_rootMenu
from src import web

# Handy helper for finding external resources nearby.
webdir = FilePath(web.__file__).parent().preauthChild

g_debug = 4
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# + = NOT USED HERE


class LoginData(object):
    """ Allowed logins

    Stage 1 - Username only.
    Stage 2 - Username and password (stored password will be encrypted)
    Stage 3 - Username and some sort of common login identifier from some secure external site.
    """


class Login(object):
    """Actual login procedures.
    """

    def validate_user(self, p_login, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        #TODO: validate user - add password for security 
        l_json = json.loads(p_login)
        if g_debug >= 2:
            print "web_login.validate_user() ", l_json
        self.load_rootMenu_page()

    def load_rootMenu_page(self):
        if g_debug >= 2:
            print "web_login.load_rootMenu_page()"
        web_rootMenu.RootMenuPage('Root_Menu_1', self.m_pyhouses_obj)


class LoginElement(athena.LiveElement):
    """ a 'live' login element containing a username and password.
    """
    docFactory = loaders.xmlfile(webdir('template/loginElement.xml').path)
    jsClass = u'login.LoginElement'

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 2:
            print "web_login.LoginElement()"

    @athena.expose
    def loginUser(self, p_login):
        """ A JS receiver for login information from the client.
        """
        if g_debug >= 3:
            print "web_login.LoginElement.login() - ", p_login
        Login().validate_user(p_login, self.m_pyhouses_obj)


class LoginPage(athena.LivePage):
    """
    """
    docFactory = loaders.xmlfile('login.xml', templateDir = 'src/web/template')

    def __init__(self, p_name, p_pyhouses_obj, *args, **kwargs):
        self.m_name = p_name
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 2:
            print "web_login.LoginPage() - Name =", p_name
        super(LoginPage, self).__init__(*args, **kwargs)

    def child_(self, p_context):
        if g_debug >= 3:
            print "web_login.LoginPage.child_() "
            print "    Context =", p_context
        return LoginPage('LoginPage 2', self.m_pyhouses_obj)

    def render_livePage(self, p_context, p_data):
        if g_debug >= 3:
            print "web_login.LoginPage.render_livePage() "
            print "    Context =", p_context
            print "    Data =", p_data
        l_element = LoginElement(self.m_pyhouses_obj)
        l_element.setFragmentParent(self)
        return p_context.tag[l_element]

    def render_debug(self, p_context, p_data):
        if g_debug >= 3:
            print "web_login.LoginPage.render_debug() "
            print "    Context =", p_context
            print "    Data =", p_data
        l_fragment = athena.IntrospectionFragment()
        l_fragment.setFragmentParent(self)
        return p_context.tag[l_fragment]

# ## END DBK
