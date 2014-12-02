"""
Created on Jul 27, 2013

@author: briank

When a user wants to connect to PyHouse to monitor or control the system, they open a browser to the configured port (default is 8580).
Since internet access is possible, a login screen is presented first and authentication takes place.
Then a menu is presented that allows non house things to be selected or a the user may select to work with a house,
the house select screen also allows for a house to be added so starting with no houses is possible.



This module creates a main page and a workspace.
The mainpage is an athena Live page and the workspace is a live element.
This allows ajax/comet actions and also allows other live element pages to be added dynamically.




Note - A big hunk of the Core was derived from code kindly sent to me by Werner Thie.
This portion involves the creation of a mainpage and within it a workspace.
All the rest of the web page are segments that appear when needed and are deleted
when finished.

Here is Werner's opening comment:
mainpage.py - this is the place where everything is happening, the user will never
              ever see a page change during the whole visit. Everything the user is
              shown is injected as a LiveElement into the page and deleted after it
              has served its purpose.

              The main element which resides in this page and handles all aspects of
              user interaction is the workspace. It has a first go at the arguments
              and then injects whatever is needed.

              Due to the fact that webapps are highly user driven, the main interaction
              points are usually triggered from the client, whereas things such as status
              updates or realtime data delivery is handled by the server at its own pace

"""

# Import system type stuff
import gc
import os
import time
from twisted.python import util
from nevow import loaders
from nevow import athena

try:
    from twisted.web import http
except ImportError:
    from twisted.protocols import http

from zope.interface import implements
from nevow import rend
from nevow import static
from nevow import url
from nevow import inevow
from nevow import guard
from nevow.compression import parseAcceptEncoding
from nevow.inevow import IRequest
from twisted.internet import defer

# Import PyMh files and modules.
from Modules.Web import web_buttons
from Modules.Web import web_clock
from Modules.Web import web_controllers
from Modules.Web import web_controlLights
from Modules.Web import web_house
from Modules.Web import web_houseMenu
from Modules.Web import web_houseSelect
from Modules.Web import web_internet
from Modules.Web import web_lights
from Modules.Web import web_login
from Modules.Web import web_rooms
from Modules.Web import web_rootMenu
from Modules.Web import web_schedules
from Modules.Web import web_thermostats
from Modules.Web import web_webs
from Modules.Computer import logging_pyh as Logger


# Handy helper for finding external resources nearby.
modulepath = os.path.join(os.path.split(__file__)[0], '..')
webpath = os.path.join(os.path.split(__file__)[0])
csspath = os.path.join(webpath, 'css')
imagepath = os.path.join(webpath, 'images')
jspath = os.path.join(webpath, 'js')
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webMainpage ')


class FileNoListDir(static.File):

    def directoryListing(self):
        print("ERROR - web_mainpage.directoryListing() - Forbidden resource")
        # return error.ForbiddenResource()


class FourOfour(athena.LiveElement):
    jsClass = u'mainPage.FourOfour'
    docFactory = loaders.xmlfile(os.path.join(templatepath, '404Element.html'))


class TheRoot(rend.Page):
    """This is the root - given to the app server!
    """

    def __init__(self, staticpath, p_pyhouse_obj, *args, **kw):
        self.m_pyhouse_obj = p_pyhouse_obj
        if staticpath == None:
            l_jspath = util.sibpath(jspath, 'js')
            staticpath = os.path.join(l_jspath, '', 'resource')
        super(TheRoot, self).__init__(*args, **kw)
        self.children = {
          'resource'          : FileNoListDir(os.path.join(staticpath)),
          'Line.png'          : FileNoListDir(os.path.join(imagepath, 'Line.png')),
          'favicon.ico'       : FileNoListDir(os.path.join(imagepath, 'favicon.ico')),
          'waitroller.gif'    : FileNoListDir(os.path.join(imagepath, 'waitroller.gif'))
        }

    def locateChild(self, ctx, segments):
        l_resource, l_segments = factory(ctx, segments, self.m_pyhouse_obj)
        if l_resource == None:
            l_resource, l_segments = super(TheRoot, self).locateChild(ctx, segments)
        return l_resource, l_segments

#==============================================================================

class mainPageFactory:
    """
    """

    def __init__(self):
        """
        The basic underlying plugin mechanism does not work in vhost situation where everything sits in the same basic namespace.
        The final trick was to update the module global mapping in jsDeps with my collections.
        """
        self.Clients = {}
        l_siteJSPackage = athena.AutoJSPackage(jspath)
        _l_siteCSSPackage = athena.AutoCSSPackage(csspath)
        LOG.info('CSS - {}'.format(_l_siteCSSPackage))
        athena.jsDeps.mapping.update(l_siteJSPackage.mapping)

    def addClient(self, client):
        l_clientID = self._newClientID()
        self.Clients[l_clientID] = client
        return l_clientID

    def getClient(self, p_clientID):
        return self.Clients[p_clientID]

    def removeClient(self, p_clientID):
        """
        State-tracking bugs may make it tempting to make the next line a 'pop', but it really shouldn't be;
        if the Page instance with this client ID is already gone, then it should be gone, which means that
        this method can't be called with that argument.
        """
        del self.Clients[p_clientID]

    def _newClientID(self):
        """Get a new UUID type id (dynamic) for the client.
        """
        return guard._sessionCookie()

# This instance is built once
_mainPageFactory = mainPageFactory()

#==============================================================================






"""
mainpage.py - this is the place where everything is happening, the user will never
              ever see a page change during the whole visit. Everything the user is
              shown is injected as a LiveElement into the page and deleted after it
              has served its purpose.

              The main element which resides in this page and handles all aspects of
              user interaction is the workspace. It has a first go at the arguments
              and then injects whatever is needed.

              Due to the fact that webapps are highly user driven, the main interaction
              points are usually triggered from the client, whereas things such as status
              updates or realtime data delivery is handled by the server at its own pace

author   : Werner Thie, wth
last edit: wth, 20.01.2011
modhistory:
  20.01.2011 - wth, pruned for minimal demo app
"""


COOKIEKEY = 'minimal'


class MappingCompressedResource(athena.MappingResource):
    """
    L{inevow.IResource} which looks up segments in a mapping between symbolic
    names and the files they correspond to. Additionally if a compressed version
    is present and content negotiation allows zipped resources, the zipped
    file is preferred

    @type mapping: C{dict}
    @ivar mapping: A map between symbolic, requestable names (eg,
    'Nevow.Athena') and C{str} instances which name files containing data
    which should be served in response.
    """
    implements(inevow.IResource)

    def __init__(self, mapping):
        self.mapping = mapping

    def canCompress(self, req):
        """
        Check whether the client has negotiated a content encoding we support.
        """
        value = req.getHeader('accept-encoding')
        if value is not None:
            encodings = parseAcceptEncoding(value)
            return encodings.get('gzip', 0.0) > 0.0
        return False

    def resourceFactory(self, fileName):
        """
        Retrieve a possibly  L{inevow.IResource} which will render the contents of
        C{fileName}.
        """
        f = open(fileName, 'rb')
        js = f.read()
        return static.Data(js, 'text/javascript')

    def locateChild(self, ctx, segments):
        try:
            impl = self.mapping[segments[0]]
        except KeyError:
            return rend.NotFound
        else:
            req = IRequest(ctx)
        implgz = impl + '.gz'
        if self.canCompress(req) and os.path.exists(implgz):
            impl = implgz
            req.setHeader('content-encoding', 'gzip')
        return self.resourceFactory(impl), []

#==============================================================================


class MainPage(athena.LivePage):
    addSlash = True
    factory = _mainPageFactory
    jsClass = u'mainPage.mainPage'
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'mainpage.html'))

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        super(MainPage, self).__init__()
        LOG.info('Main Page Initializing')

    def child_jsmodule(self, _ctx):
        return MappingCompressedResource(self.jsModules.mapping)

    def data_title(self, _ctx, _data):
        return self.pageTitle

    def beforeRender(self, _ctx):
        """If you need a place where to keep things during the livePage being up, please do it here and only here.
        Storing states someplace deeper in the hierarchy makes it extremely difficult to release memory properly due to circular object references.
        """
        self.page.lang = 0
        self.uid = None
        self.username = ''
        self.pageTitle = 'PyHouse Access'
        self.selectedHouse = -1
        l_defer = self.notifyOnDisconnect()
        l_defer.addErrback(self.eb_disconnect)

    def render_workspace(self, ctx, _data):
        f = Workspace(self.m_pyhouse_obj, self.uid)
        f.setFragmentParent(self)
        return ctx.tag[f]

    def eb_disconnect(self, reason):
        """
        We will be called back when the client disconnects.
        Clean up whatever needs cleaning serverside.
        """
        pass


#==============================================================================

REQ_404 = -1
REQ_ROOT = 0
REQ_WITHID = 2

class Workspace(athena.LiveElement):
    """WARNING:
        The names of the @athena.expose methods seem to have to match the js file name.
        They are called from browser when elements are attached to the workspace.
    """
    jsClass = u'workspace.Workspace'
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'workspaceElement.html'))
    PG_UNKNOWN = -1
    PG_INITED = 0

    def __init__(self, p_pyhouse_obj, uid = None):
        self.m_pyhouse_obj = p_pyhouse_obj
        super(Workspace, self).__init__()
        LOG.info('Workspace initialized.')
        self.state = self.PG_INITED
        self.uid = uid

    def detached(self):
        # clean up whatever needs cleaning...
        LOG.info('workspace object was detached cleanly')


#-----------------
# Calls from browser JS to load an element (fragment)

    @athena.expose
    def inject_404(self):
        LOG.info("404 called from browser")
        f = FourOfour()
        f.setFragmentParent(self)
        return f

    @athena.expose
    def buttons(self, p_params):
        LOG.info("Buttons loaded into browser")
        l_element = web_buttons.ButtonsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def clock(self, _p_params):
        LOG.info("Clock loaded into browser")
        l_element = web_clock.ClockElement()
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def controllers(self, p_params):
        LOG.info("Controllers loaded into browser")
        l_element = web_controllers.ControllersElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def controlLights(self, p_params):
        LOG.info("Control Lights loaded into browser")
        l_element = web_controlLights.ControlLightsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def house(self, _p_params):
        LOG.info("House loaded into browser")
        l_element = web_house.HouseElement(self)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def houseMenu(self, _p_params):
        LOG.info("House Menu loaded into browser")
        l_element = web_houseMenu.HouseMenuElement(self)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def houseSelect(self, _p_params):
        LOG.info("House Select loaded into browser")
        l_element = web_houseSelect.HouseSelectElement(self)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def internet(self, p_params):
        LOG.info("Internet loaded into browser")
        l_element = web_internet.InternetElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def lights(self, p_params):
        LOG.info("Lights loaded into browser")
        l_element = web_lights.LightsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def login(self, _p_params):
        """ Place and display the login widget.
        """
        LOG.info("Login loaded into browser")
        l_element = web_login.LoginElement(self)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def rooms(self, p_params):
        LOG.info("Rooms loaded into browser")
        l_element = web_rooms.RoomsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def rootMenu(self, _p_params):
        LOG.info("Root Menu loaded into browser")
        l_element = web_rootMenu.RootMenuElement(self)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def schedules(self, p_params):
        LOG.info("schedules loaded into browser")
        l_element = web_schedules.SchedulesElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def thermostats(self, p_params):
        LOG.info("Thermostats loaded into browser")
        l_element = web_thermostats.ThermostatsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def webs(self, p_params):
        LOG.info("Web-s loaded into browser")
        l_element = web_webs.WebsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

#-----------------

    @athena.expose
    def guiready(self):
        def cb_usermatch(p_user):  # select usually returns a list, knowing that we have unique results
            reqtype = REQ_404  # the result is unpacked already and a single item returned
            udata = {}
            if len(p_user) > 0:
                self.page.userid = p_user['id']
                reqtype = REQ_WITHID
                for k in p_user.keys():
                    if type(p_user[k]) == type(''):
                        udata[uc(k)] = uc(p_user[k])
                    else:
                        udata[uc(k)] = p_user[k]
            return reqtype, udata
        def cb_rootmatch(_res):  # select usually returns a list, knowing that we have unique results
            reqtype = REQ_ROOT  # the result is unpacked already and a single item returned
            udata = {}
            user = {}
            user['id'] = self.page.username
            for k in user.keys():
                if type(user[k]) == type(''):
                    udata[uc(k)] = uc(user[k])
                else:
                    udata[uc(k)] = user[k]
            return reqtype, udata
        def eb_nomatch():
            pass
        LOG.info('GuiReady called')
        if self.uid and len(self.uid) == 32:
            l_defer = self.page.userstore.getUserWithUID(self.uid)
            l_defer.addCallback(cb_usermatch)
            l_defer.addErrback(eb_nomatch)
        else:
            l_defer = defer.succeed(0)
            l_defer.addCallback(cb_rootmatch)
            l_defer.addErrback(eb_nomatch)
        return l_defer


#==============================================================================

def factory(ctx, segments, p_pyhouse_obj):
    """ If segments contains a liveID (len = 32) the page stored in self.Clients will be returned.
    Status of the given page is stored in the page object itself and nowhere else.
    """
    seg0 = segments[0]
    if seg0 == '':
        # Starting page - no segments yet
        return MainPage(p_pyhouse_obj), segments[1:]
    elif _mainPageFactory.Clients.has_key(seg0):
        # xxx
        return _mainPageFactory.Clients[seg0], segments[1:]
    elif len(seg0) == 32:
        # We have a liveID
        IRequest(ctx).addCookie(COOKIEKEY, seg0, http.datetimeToString(time.time() + 30.0))
        return url.URL.fromString('/'), ()
    else:
        #
        return None, segments


#==============================================================================

"""
helper funcs and classes

author   : Werner Thie, wth
last edit: wth, 20.01.2011
modhistory:
  20.01.2011 - wth, pruned for minimal
"""

def uc(msg):
    if type(msg) == type(''):
        return unicode(msg, 'iso-8859-1')
    else:
        return msg

def dc(msg):
    if type(msg) == type(''):
        return msg
    else:
        return msg.encode('iso-8859-1')


def dumpObjects(delta = True, limit = 0, include = [], exclude = []):
    global prev
    if include != [] and exclude != []:
        return
    objects = {}
    gc.collect()
    oo = gc.get_objects()
    for o in oo:
        if getattr(o, "__class__", None):
            name = o.__class__.__name__
            if ((exclude == [] and include == [])       or \
                (exclude != [] and name not in exclude) or \
                (include != [] and name in include)):
                objects[name] = objects.get(name, 0) + 1
    pk = prev.keys()
    pk.sort()
    names = objects.keys()
    names.sort()
    for name in names:
        if limit == 0 or objects[name] > limit:
            if not prev.has_key(name):
                prev[name] = objects[name]
            dt = objects[name] - prev[name]
            if delta or dt != 0:
                print('%0.6d -- %0.6d -- ' % (dt, objects[name]), name)
            prev[name] = objects[name]


def getObjects(oname):
    """
    gets an object list with all the named objects out of the sea of gc'ed objects
    """
    l_obj_list = []
    gc.collect()
    oo = gc.get_objects()
    for o in oo:
        if getattr(o, "__class__", None):
            name = o.__class__.__name__
            if (name == oname):
                l_obj_list.append(o)
    return l_obj_list

# ## END DBK
