#! /usr/bin/env python
#-*- coding: iso-8859-1 -*-
"""
Created on Jul 27, 2013

@author: briank

Note - A big hunk of the core was derived from code kindly sent to me by Werner Thie.
This portion involves the creation of a mainpage and within it a playground.
All the rest of the web page are segments that appear when needed and are deleted
when finished.

Here is Werner's opening comment:
mainpage.py - this is the place where everything is happening, the user will never
              ever see a page change during the whole visit. Everything the user iw
              shown is injected as a LiveElement into the page and deleted after it
              has served its purpose.

              The main element which resides in this page and handles all aspects of
              user interaction is the playground. It has a first go at the arguments
              and then injects whatever is needed.

              Due to the fact that webapps are highly user driven, the main interaction
              points are usually triggered from the client, whereas things such as status
              updates or realtime data delivery is handled by the server at its own pace

"""

# Import system type stuff
import logging
import gc
import os
import time
from twisted.python.filepath import FilePath
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
from src import web
from src.web import web_login


# Handy helper for finding external resources nearby.
webdir = FilePath(web.__file__).parent().preauthChild
imagepath = webdir('images').path
jspath = webdir('js').path
templatepath = webdir('template').path

g_debug = 4
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# 5 = Detail Data
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.webMain ')


class FileNoListDir(static.File):

    def directoryListing(self):
        print "ERROR - web_mainpage.directoryListing() - Forbidden resource"
        #return error.ForbiddenResource()


class FourOfour(athena.LiveElement):
    jsClass = u'mainPage.FourOfour'
    docFactory = loaders.xmlstr("""
        <div xmlns:nevow="http://nevow.com/ns/nevow/0.1" nevow:render="liveElement">
        </div>
    """)


class TheRoot(rend.Page):
    """This is the root - given to the app server!
    """

    def __init__(self, p_pyhouses_obj, staticpath, *args, **kw):
        if staticpath == None:
            l_jspath = util.sibpath(jspath, 'js')
            staticpath = os.path.join(l_jspath, '', 'resource')
        if g_debug >= 3:
            print "web_mainpage.TheRoot() - ", jspath, imagepath
        super(TheRoot, self).__init__(*args, **kw)
        self.children = {
          'resource'          : FileNoListDir(os.path.join(staticpath)),
          'favicon.ico'       : FileNoListDir(os.path.join(imagepath, 'favicon.ico')),
          'waitroller.gif'    : FileNoListDir(os.path.join(imagepath, 'waitroller.gif'))
        }
        print #separate package hinting from logging

    def locateChild(self, p_context, p_segments):
        l_resource, l_segments = factory(p_context, p_segments)
        if l_resource == None:
            l_resource, l_segments = super(TheRoot, self).locateChild(p_context, p_segments)
        return l_resource, l_segments


class mainPageFactory:
    noisy = True

    def __init__(self):
        self.clients = {}
        """
        Was one hell of an expensive line, the basic underlying plugin mechanism does not work in
        vhost situation where everything sits in the same basic namespace, clashes are preprogrammed.
        I decided to fiddle with the package mappings and arrived at a clean version of my packages but,
        my mappings didn't connect with the mappings collected by other mechanisms. The final trick was
        to update the module global mapping in jsDeps with my collection, the lonely line below does the trick
        """
        if g_debug >= 3:
            print "web_mainpage.mainPageFactory()"
        modulepath = os.path.join(os.path.split(__file__)[0], '..')
        l_jspath = util.sibpath(modulepath, 'js')
        l_siteJSPackage = athena.AutoJSPackage(l_jspath)
        athena.jsDeps.mapping.update(l_siteJSPackage.mapping)

    def addClient(self, client):
        clientID = self._newClientID()
        self.clients[clientID] = client
        if g_debug >= 3:
            print "web_mainpage.mainPageFactory.addClient() - Rendered new mainPage %r: %r" % (client, clientID)
            print "    Number of active pages currently: %d" % len(self.clients)
        return clientID

    def getClient(self, clientID):
        if g_debug >= 3:
            print "web_mainpage.mainPageFactory.getClient()  %r" % (self.clients[clientID])
        return self.clients[clientID]

    def removeClient(self, clientID):
        # State-tracking bugs may make it tempting to make the next line a
        # 'pop', but it really shouldn't be; if the Page instance with this
        # client ID is already gone, then it should be gone, which means that
        # this method can't be called with that argument.
        del self.clients[clientID]
    #      if self.noisy:
    #        log.msg("Disconnected old LivePage %r" % (clientID,))

    def _newClientID(self):
        return guard._sessionCookie()

_mainPageFactory = mainPageFactory()
_mainPageFactory.noisy = False


class MainPage(athena.LivePage):
    """DBK
    """
    addSlash = True
    factory = _mainPageFactory
    docFactory = loaders.xmlfile('mainpage.xml', templateDir = 'src/web/template')

    def __init__(self, p_name, p_pyhouses_obj, *args, **kwargs):
        self.m_name = p_name
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 2:
            print "web_mainpage.MainPage() - Name =", p_name
        super(MainPage, self).__init__(*args, **kwargs)

    def child_(self, p_context):
        if g_debug >= 3:
            print "web_mainpage.MainPage.child_() "
            print "    Context =", p_context
        return MainPage('MainPage 2', self.m_pyhouses_obj)

    def render_livePage(self, p_context, p_data):
        if g_debug >= 3:
            print "web_mainpage.MainPage.render_livePage() "
            print "    Context =", p_context
            print "    Data =", p_data
        l_element = Playground(self.m_pyhouses_obj)
        l_element.setFragmentParent(self)
        return p_context.tag[l_element]

    def child_jsmodule(self, ctx):
        if g_debug >= 3:
            print "web_mainpage.MainPage.child_jsmodule() ", MappingCompressedResource(self.jsModules.mapping)
        return MappingCompressedResource(self.jsModules.mapping)

    def data_title(self, ctx, data):
        return self.pageTitle

    # If you need a place where to keep things during the LivePage being up, please do it here and only here.
    # Storing states someplace deeper in the hierarchy makes it extremely difficult to release memory properly due to circular object references.
    def beforeRender(self, ctx):
        if g_debug >= 3:
            print "web_mainpage.MainPage.beforeRender() "
        self.uid = None
        self.username = ''
        self.pageTitle = 'Welcome to PyHouse'
        d = self.notifyOnDisconnect()
        d.addErrback(self.eb_disconnect)

    def render_playground(self, ctx, data):
        if g_debug >= 3:
            print "web_mainpage.MainPage.render_playground() "
        f = Playground(self.uid)
        f.setFragmentParent(self)
        return ctx.tag[f]

    def eb_disconnect(self, reason):
        """ We will be called back when the client disconnects, clean up whatever needs cleaning serverside.
        """
        if g_debug >= 3:
            print "web_mainpage.MainPage.eb_disconnect() "
        pass



"""
mainpage.py - this is the place where everything is happening, the user will never
              ever see a page change during the whole visit. Everything the user is
              shown is injected as a LiveElement into the page and deleted after it
              has served its purpose.

              The main element which resides in this page and handles all aspects of
              user interaction is the playground. It has a first go at the arguments
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
        if g_debug >= 3:
            print "web_mainpage.MappingCompressedResources() ", self.mapping.keys

    def canCompress(self, req):
        """
        Check whether the client has negotiated a content encoding we support.
        """
        value = req.getHeader('accept-encoding')
        if g_debug >= 3:
            print "web_mainpage.MappingCompressedResources.canCompress() ", value
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


class MainPage2(athena.LivePage):
    addSlash = True
    factory = _mainPageFactory
    jsClass = u'mainPage.Mainpage'
    docFactory = loaders.xmlstr("""
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns:nevow="http://nevow.com/ns/nevow/0.1">
            <head>
                <title nevow:data="title" nevow:render="data">Page Title</title>
                <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
                <nevow:invisible nevow:render="liveglue" />
                <style type="text/css">
            html {
              height: 100%;
            }
            body {
              min-height: 100%;
            }
            * html body {
              height: 100%;
            }
                </style>
            </head>
            <body style="margin: 0px; padding: 0px; overflow: hidden; height: 100%; width: 100%;">
                <nevow:invisible nevow:render="playground" />
            </body>
        </html>
        """)

    def child_jsmodule(self, ctx):
        if g_debug >= 3:
            print "web_mainpage.MainPage2.child_jsmodule"
        return MappingCompressedResource(self.jsModules.mapping)

    def data_title(self, ctx, data):
        return self.pageTitle

    # If you need a place where to keep things during the LifePage being up, please do it here and only here.
    # Storing states someplace deeper in the hierarchy makes it extremely difficult to release memory properly due to circular object refs.
    def beforeRender(self, ctx):
        if g_debug >= 3:
            print "web_mainpage.MainPage2.beforeRender()"
        self.page.lang = 0
        self.uid = None
        self.username = ''
        self.pageTitle = 'Welcome to PyHouse'
        d = self.notifyOnDisconnect()
        d.addErrback(self.eb_disconnect)

    def render_playground(self, ctx, data):
        if g_debug >= 3:
            print "web_mainpage.MainPage2.render_playground()", ctx, data
        f = Playground(self.uid)
        f.setFragmentParent(self)
        return ctx.tag[f]

    def eb_disconnect(self, reason):
        """
        we will be called back when the client disconnects, clean up whatever needs
        cleaning serverside
        """
        if g_debug >= 3:
            print "web_mainpage.MainPage2.eb_disconnect()"
        pass



REQ_404 = -1
REQ_ROOT = 0
REQ_WITHID = 2

class Playground(athena.LiveElement):
    jsClass = u'playground.Playground'
    docFactory = loaders.xmlstr("""
        <div
            xmlns:nevow = "http://nevow.com/ns/nevow/0.1"
            nevow:render = "liveElement"
            class = "playground" name = "playground"
            style = "width: 100%; height: 100%; min-height: 100%; position: absolute; left: 0px; top: 0px; background-color: #c2c2c2;"
            >
            <h1>PyHouse</h1>
            <img id = "waitroller" src = "images/waitroller.gif"
                style = "width: 100px; height: 100px; top: 50%; left: 50%; position: absolute; margin-left: -50px; margin-top: -50px;"/>

        </div>
        """)

    PG_UNKNOWN = -1
    PG_INITED = 0

    def __init__(self, p_pyhouses_obj, uid = None):
        if g_debug >= 3:
            print "web_mainpage.Playground()"
        super(Playground, self).__init__()
        self.state = self.PG_INITED
        self.uid = uid

    def detached(self):
        #clean up whatever needs cleaning...
        if g_debug >= 3:
            print "web_mainpage.Playground.detached()"
        #log.msg('playground object was detached cleanly')

    @athena.expose
    def inject_404(self):
        if g_debug >= 3:
            print "web_mainpage.Playground.inject_404() - called from browser"
        f = FourOfour()
        f.setFragmentParent(self)
        return f

    @athena.expose
    def clock(self, params):
        if g_debug >= 3:
            print "web_mainpage.Playground.clock() - called from browser"
        f = Clock()
        f.setFragmentParent(self)
        return f

    @athena.expose
    def login(self, p_params):
        if g_debug >= 3:
            print "web+mainpage.Playground.login() - called from browser."
        l_element = web_login.LoginElement()
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def guiready(self):
        if g_debug > -3:
            print "web_mainpage.Playground.guiready() - called from browser ", self.uid

        def cb_usermatch(user):  #select usually returns a list, knowing that we have unique results
            reqtype = REQ_404   #the result is unpacked already and a single item returned
            udata = {}
            if g_debug >= 3:
                print "web_mainpage.Playground.cb_usermatch() <callback> res:{0:}".format(res)
                #print "    page=", self.page
            if len(user) > 0:
                self.page.userid = user['id']
                reqtype = REQ_WITHID
                for k in user.keys():
                    if type(user[k]) == type(''):
                        udata[uc(k)] = uc(user[k])
                    else:
                        udata[uc(k)] = user[k]
            return reqtype, udata

        def cb_rootmatch(res):    #select usually returns a list, knowing that we have unique results
            reqtype = REQ_ROOT   #the result is unpacked already and a single item returned
            udata = {}
            user = {}
            if g_debug >= 3:
                print "web_mainpage.Playground.cb_rootmatch() <callback> res:{0:}".format(res)
                #print "    page=", self.page
            user['id'] = self.page.username
            for k in user.keys():
                if type(user[k]) == type(''):
                    udata[uc(k)] = uc(user[k])
                else:
                    udata[uc(k)] = user[k]
            return reqtype, udata

        def eb_nomatch():
            print "ERROR - No Match"

        if self.uid and len(self.uid) == 32:
            d = self.page.userstore.getUserWithUID(self.uid)
            d.addCallback(cb_usermatch)
            d.addErrback(eb_nomatch)
        else:
            d = defer.succeed(0)
            d.addCallback(cb_rootmatch)
        return d

class Clock(athena.LiveElement):
    jsClass = u'clock.Clock'
    docFactory = loaders.xmlstr("""
        <div xmlns:nevow="http://nevow.com/ns/nevow/0.1" nevow:render="liveElement"
          class="clock" name="clock"
          style="background-color:#000000; color:#ffffff; font-size:600%; width: 350px; height: 100px; top: 50%; left: 50%; position: absolute; margin-left: -175px; margin-top: -50px;">
        </div>
        """)

    @athena.expose
    def getTimeOfDay(self):
        if g_debug > -3:
            print "web_mainpage.Clock.getTimeOfDay() - called from browser"
        return uc(time.strftime("%I:%M:%S", time.localtime(time.time())))


def factory(ctx, segments):
    """ If segments contains a liveID (len = 32) the page stored in self.clients will be returned.
    Status of the given page is stored in the page object itself and nowhere else.
    """
    if g_debug >= 5:
        print "web_mainpage.factory(1) ", segments
    seg0 = segments[0]
    if seg0 == '':
        # Starting page - no segments yet
        if g_debug >= 5:
            print "web_mainpage.factory(3) - MainPage2: ", MainPage2(), segments[1:]
        return MainPage2(), segments[1:]
    elif _mainPageFactory.clients.has_key(seg0):
        # xxx
        if g_debug >= 5:
            print "web_mainpage.factory(4) - has_key: ", _mainPageFactory.clients[seg0], segments[1:]
        return _mainPageFactory.clients[seg0], segments[1:]
    elif len(seg0) == 32:
        # We have a liveID 
        IRequest(ctx).addCookie(COOKIEKEY, seg0, http.datetimeToString(time.time() + 30.0))
        if g_debug >= 5:
            print "web_mainpage.factory(5) - liveID: ", url.URL.fromString('/'), ()
        return url.URL.fromString('/'), ()
    else:
        #
        if g_debug >= 5:
            print "web_mainpage.factory(6) - None: ", None, segments
        return None, segments


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
        print 'cannot use include and exclude at the same time'
        return
    print 'working with:'
    print '   delta: ', delta
    print '   limit: ', limit
    print ' include: ', include
    print ' exclude: ', exclude
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
                print '%0.6d -- %0.6d -- ' % (dt, objects[name]), name
            prev[name] = objects[name]

def getObjects(oname):
    """
    gets an object list with all the named objects out of the sea of
    gc'ed objects
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

### END DBK
