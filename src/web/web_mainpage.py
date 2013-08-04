#! /usr/bin/env python
#-*- coding: iso-8859-1 -*-
"""
Created on Jul 27, 2013

@author: briank
"""

# Import system type stuff
import gc
import os
import time
from twisted.python.filepath import FilePath
from twisted.python import util
from nevow import loaders
from nevow import athena

try:
    import hashlib
    md5_constructor = hashlib.md5
except ImportError:
    import md5
    md5_constructor = md5.md5

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
from nevow.useragent import UserAgent

#import minimal
#from minimal.common.i18n    import _TStr
#from minimal.web.playground import Playground

# Import PyMh files and modules.
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


mobileClients = {}
exc = [
    "function",
    "type",
    "list",
    "dict",
    "tuple",
    "wrapper_descriptor",
    "module",
    "method_descriptor",
    "member_descriptor",
    "instancemethod",
    "builtin_function_or_method",
    "frame",
    "classmethod",
    "classmethod_descriptor",
    "_Environ",
    "MemoryError",
    "_Printer",
    "_Helper",
    "getset_descriptor",
    "weakreaf"
]
inc = [
]
prev = {}


class FileNoListDir(static.File):
    def directoryListing(self):
        return error.ForbiddenResource()

class TheRoot(rend.Page):
    def __init__(self, staticpath, *args, **kw):
        super(TheRoot, self).__init__(*args, **kw)
        self.children = {
          'resource'          : FileNoListDir(os.path.join(staticpath)),
          'favicon.ico'       : FileNoListDir(os.path.join(staticpath, 'images', 'favicon.ico')),
          'waitroller.gif'    : FileNoListDir(os.path.join(staticpath, 'images', 'waitroller.gif'))
        }
        print #separate package hinting from logging

    def locateChild(self, ctx, segments):
        rsrc, segs = factory(ctx, segments)
        if rsrc == None:
            rsrc, segs = super(TheRoot, self).locateChild(ctx, segments)
        return rsrc, segs

class fourOfour(athena.LiveElement):
    jsClass = u'mainPage.fourOfour'
    docFactory = loaders.xmlstr("""
    <div xmlns:nevow="http://nevow.com/ns/nevow/0.1" nevow:render="liveElement">
    </div>
    """)


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
        modulepath = os.path.join(os.path.split(__file__)[0], '..')
        l_jspath = util.sibpath(modulepath, 'js')
        l_siteJSPackage = athena.AutoJSPackage(l_jspath)
        athena.jsDeps.mapping.update(l_siteJSPackage.mapping)

    def addClient(self, client):
        clientID = self._newClientID()
        self.clients[clientID] = client
        if g_debug >= 4:
            print "web_mainpage.addClient() - Rendered new mainPage %r: %r" % (client, clientID)
            print "    Number of active pages currently: %d" % len(self.clients)
        return clientID

    def getClient(self, clientID):
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
            print "web_login.MainPage() - Name =", p_name
        super(MainPage, self).__init__(*args, **kwargs)

    def child_(self, p_context):
        if g_debug >= 3:
            print "web_login.MainPage.child_() "
            print "    Context =", p_context
        return MainPage('MainPage 2', self.m_pyhouses_obj)

    def render_livePage(self, p_context, p_data):
        if g_debug >= 3:
            print "web_login.MainPage.render_livePage() "
            print "    Context =", p_context
            print "    Data =", p_data
        l_element = Playground(self.m_pyhouses_obj)
        l_element.setFragmentParent(self)
        return p_context.tag[l_element]



    def child_jsmodule(self, ctx):
        return MappingCompressedResource(self.jsModules.mapping)

    def data_title(self, ctx, data):
        return self.pageTitle

    #if you need a place where to keep things during the LifePage being up, please
    #do it here and only here. Storing states someplace deeper in the hierarchy makes
    #it extremely difficult to release memory properly due to circular object refs 
    def beforeRender(self, ctx):
        self.page.lang = 0
        self.uid = None
        self.username = ''
        self.pageTitle = 'WelcomeTitle'
        d = self.notifyOnDisconnect()
        d.addErrback(self.disconn)

    def render_playground(self, ctx, data):
        f = Playground(self.uid)
        f.setFragmentParent(self)
        return ctx.tag[f]

    def disconn(self, reason):
        """
        we will be called back when the client disconnects, clean up whatever needs
        cleaning serverside
        """
        pass

# ## END DBK


"""
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
        return MappingCompressedResource(self.jsModules.mapping)

    def data_title(self, ctx, data):
        return self.pageTitle

    #if you need a place where to keep things during the LifePage being up, please
    #do it here and only here. Storing states someplace deeper in the hierarchy makes
    #it extremely difficult to release memory properly due to circular object refs 
    def beforeRender(self, ctx):
        self.page.lang = 0
        self.uid = None
        self.username = ''
        self.pageTitle = 'WelcomeTitle'
        d = self.notifyOnDisconnect()
        d.addErrback(self.disconn)

    def render_playground(self, ctx, data):
        f = Playground(self.uid)
        f.setFragmentParent(self)
        return ctx.tag[f]

    def disconn(self, reason):
        """
        we will be called back when the client disconnects, clean up whatever needs
        cleaning serverside
        """
        pass





from twisted.internet import defer

#from minimal.common.i18n    import _TStr
#from minimal.common.helpers import uc
#from minimal.web.clock      import Clock

REQ_404 = -1
REQ_ROOT = 0
REQ_WITHID = 2

class Playground(athena.LiveElement):
    jsClass = u'mainPage.Playground'
    docFactory = loaders.xmlstr("""
    <div xmlns:nevow="http://nevow.com/ns/nevow/0.1" nevow:render="liveElement"
      class="playground" name="playground"
      style="width: 100%; height: 100%; min-height: 100%; position: absolute; left: 0px; top: 0px; background-color: #c2c2c2;">
      <img id="waitroller" src="images/waitroller.gif" style="width: 100px; height: 100px; top: 50%; left: 50%; position: absolute; margin-left: -50px; margin-top: -50px;"/>
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
        log.msg('playground object was detached cleanly')

    @athena.expose
    def inject_404(self):
        f = fourOfourMsg()
        f.setFragmentParent(self)
        return f

    @athena.expose
    def clock(self, params):
        if g_debug > -3:
            print "web_mainpage.Playground.clock() - called from browser"
        f = Clock()
        f.setFragmentParent(self)
        return f

    @athena.expose
    def guiready(self):
        if g_debug > -3:
            print "web_mainpage.Playground.guiready() - called from browser ", self.uid

        def usermatch(user):  #select usually returns a list, knowing that we have unique results
            reqtype = REQ_404   #the result is unpacked already and a single item returned
            udata = {}
            if len(user) > 0:
                self.page.userid = user['id']
                reqtype = REQ_WITHID
                for k in user.keys():
                    if type(user[k]) == type(''):
                        udata[uc(k)] = uc(user[k])
                    else:
                        udata[uc(k)] = user[k]
            return reqtype, udata

        def rootmatch(res):    #select usually returns a list, knowing that we have unique results
            reqtype = REQ_ROOT   #the result is unpacked already and a single item returned
            udata = {}
            user = {}
            if g_debug >= 3:
                print "web_mainpage.Playground.rootmatch() <callback> res:{0:}".format(res)
                print "    page=", self.page
            user['id'] = self.page.username
            for k in user.keys():
                if type(user[k]) == type(''):
                    udata[uc(k)] = uc(user[k])
                else:
                    udata[uc(k)] = user[k]
            return reqtype, udata

        if self.uid and len(self.uid) == 32:
            d = self.page.userstore.getUserWithUID(self.uid)
            d.addCallback(usermatch)
            d.addErrback(nomatch)
        else:
            d = defer.succeed(0)
            d.addCallback(rootmatch)
        return d







def isMobileClient(request):
    agentString = request.getHeader("user-agent")
    if agentString is None:
        return False
    agent = UserAgent.fromHeaderValue(agentString)
    if agent is None:
        return False
    requiredVersion = mobileClients.get(agent.browser, None)
    if requiredVersion is not None:
        return agent.version >= requiredVersion
    return False

def factory(ctx, segments):
    """
    If segments contains a liveID the page stored in self.clients will be returned. Status
    of the given page is stored in the page object itself and nowhere else.
    """
    seg0 = segments[0]
    if seg0 == '':
        if isMobileClient(inevow.IRequest(ctx)):
            return mobilePage(), segments[1:]
        else:
            return MainPage2(), segments[1:]
    elif _mainPageFactory.clients.has_key(seg0):
        return _mainPageFactory.clients[seg0], segments[1:]
    elif len(seg0) == 32:
        IRequest(ctx).addCookie(COOKIEKEY, seg0, http.datetimeToString(time.time() + 30.0))
        return url.URL.fromString('/'), ()
    else:
        return None, segments






#! /usr/bin/env python
#-*- coding: iso-8859-1 -*-

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

def dumpObjects(delta = True, limit = 0, include = inc, exclude = []):
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

dumpObject = dumpobj.dumpObj








