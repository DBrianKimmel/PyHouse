#!/usr/bin/python

"""Web server module.
This is a Main Module - always present.

TODO: format doc strings to Epydoc standards.
"""

# Import system type stuff
import datetime
import logging
import os
import random
import xml.etree.ElementTree as ET
import twisted.python.components as tpc
from twisted.internet import reactor
from nevow import appserver
from nevow import flat
from nevow import inevow
from nevow import loaders
from nevow import rend
from nevow import static
from nevow import url
from nevow import util
from nevow.rend import _CARRYOVER
from formless import iformless

# Import PyMh files and modules.
from src.utils import xml_tools
from src.lights import lighting
from src.utils import config_xml
from src.web.web_tagdefs import *


g_debug = 8

g_port = 8580
g_logger = None
g_houses_obj = None

SUBMIT = '_submit'
BUTTON = 'post_btn'

# Entertainment = {}
Lights = {}
XLight_Data = {}

# Only to move the eclipse error flags to one small spot
listenTCP = reactor.listenTCP

class WebLightData(lighting.LightData): pass
class WebLightingAPI(lighting.LightingAPI): pass

class WebSceneData(lighting.SceneData): pass
class WebSceneAPI(lighting.SceneAPI): pass

class WebException(Exception):
    """Raised when there is a web error of some sort.
    """

class WebData(object):
    """
    """
    def __init__(self):
        self.WebPort = 8580

class WebUtilities(WebData):
    """
    """

    def read_web(self, p_web_obj, p_web_xml):
        if g_debug >= 5:
            print "web_server.read_web()"
            print xml_tools.prettify(self.m_root)
        try:
            l_sect = self.m_root.find('Web')
            l_sect.find('WebPort')
        except AttributeError:
            l_sect = ET.SubElement(self.m_root, 'Web')
            ET.SubElement(l_sect, 'WebPort').text = 'None'
        l_obj = WebData()
        l_obj.WebPort = l_sect.findtext('WebPort')
        Web_Data[0] = l_obj

    def write_web(self, p_parent, p_web_obj):
        if g_debug >= 2:
            print "web_server.write_web()"
        l_sect = self.write_create_empty('Web')
        l_obj = Web_Data[0]
        ET.SubElement(l_sect, 'WebPort').text = str(Web_Data[0].WebPort)
        # self.write_file()

    def build_child_tree(self):
        """Build a tree of pages for nevow.
        """
        # These are real files on disk
        setattr(RootPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(RootPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(RootPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(RootPage, 'child_housepage.js', static.File('web/js/housepage.js'))
        setattr(RootPage, 'child_mainpage.js', static.File('web/js/mainpage.js'))
        #------------------------------------
        setattr(RootPage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(RootPage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(RootPage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(RootPage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(RootPage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(RootPage, 'child_topRight.gif', static.File('web/images/top_right.gif'))
        setattr(RootPage, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))

        setattr(SelectHousePage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(SelectHousePage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(SelectHousePage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(SelectHousePage, 'child_housepage.js', static.File('web/js/housepage.js'))
        setattr(SelectHousePage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(SelectHousePage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(SelectHousePage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(SelectHousePage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(SelectHousePage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(SelectHousePage, 'child_topRight.gif', static.File('web/images/top_right.gif'))


class ManualFormMixin(rend.Page, WebUtilities):
    """
    """

    def locateChild(self, context, segments):
        """Add to the standard find child to handle POST of forms

        def form_post_lighting for a submit button valued 'lighting'
        def form_post for the form without a key
        """
        if segments[0].startswith(SUBMIT):  # Handle the form post
            # Get a method name from the action in the form plus the first word in the button name,
            #  or simply the form action if no button name is specified
            kwargs = {}
            args = inevow.IRequest(context).args
            bindingName = ''
            for key in args:
                if key != BUTTON:
                    if args[key] != ['']:
                        kwargs[key] = (args[key][0], args[key])[len(args[key]) > 1]
                else:
                    bindingName = args[key][0]
            name_prefix = segments[0].split('!!')[1]
            if bindingName == '':
                name = name_prefix
            else:
                name = name_prefix + '_' + bindingName.split()[0].lower()
            # print "locateChild - name:", name
            method = getattr(self, 'form_' + name, None)
            # print "locateChild - method:", method
            if method is not None:
                return self.onManualPost(context, method, bindingName, kwargs)
            else:
                raise WebException("You should define a form_action_button method for {0:}".format(name))
        (l_child, l_segments) = super(ManualFormMixin, self).locateChild(context, segments)
        return (l_child, l_segments)

    def onManualPost(self, ctx, method, bindingName, kwargs):
        """
        """

        def redirectAfterPost(aspects):
            """See: nevow.rend.Page.WebFormPost
            """
            if g_debug >= 9:
                print "web_server.ManualFormMixin.onManualPost.redirectAfterPost() -- Start - ctx:", ctx, ", method:", method, ", bindingName:", bindingName, ", kwargs", kwargs
            l_handler = aspects.get(inevow.IHand)
            refpath = None
            ref = None
            if l_handler is not None:
                if isinstance(l_handler, rend.Page):
                    refpath = url.here
                    if 'freeform_hand' not in inevow.IRequest(ctx).prepath:
                        refpath = refpath.child('freeform_hand')
                if isinstance(l_handler, (url.URL, url.URLOverlay)):
                    refpath, l_handler = l_handler, None
            # print " -- refpath-1:", refpath
            if refpath is None:
                redirectAfterPost = request.getComponent(iformless.IRedirectAfterPost, None)
                if redirectAfterPost is None:
                    ref = request.getHeader('referer')
                    if ref:
                        refpath = url.URL.fromString(ref)
                    else:
                        refpath = url.here
                else:
                    self.m_logger.warn("[0.5] IRedirectAfterPost is deprecated. Return a URL instance from your autocallable instead.", DeprecationWarning, 2)
                    # # Use the redirectAfterPost url
                    ref = str(redirectAfterPost)
                    refpath = url.URL.fromString(ref)
            # print " -- refpath-2:", refpath
            if l_handler is not None or aspects.get(iformless.IFormErrors) is not None:
                magicCookie = '%s%s%s' % (datetime.datetime.now(), request.getClientIP(), random.random())
                refpath = refpath.replace('_nevow_carryover_', magicCookie)
                _CARRYOVER[magicCookie] = C = tpc.Componentized()
                for k, v in aspects.iteritems():
                    C.setComponent(k, v)
            destination = flat.flatten(refpath, ctx)
            request.redirect(destination)
            if g_debug >= 1:
                print "web_server.ManualFormMixin.onManualPost.redirectAfterPost() - Posted a form to >", bindingName, "<"
            return static.Data('You posted a form to %s' % bindingName, 'text/plain'), ()

        request = inevow.IRequest(ctx)
        if g_debug >= 1:
            print "web_server.ManualFormMixin.onManualPost.redirectAfterPost() - defer ", kwargs
        return util.maybeDeferred(method, **kwargs
            ).addCallback(self.onPostSuccess, request, ctx, bindingName, redirectAfterPost
            ).addErrback(self.onPostFailure, request, ctx, bindingName, redirectAfterPost)


class SelectHousePage(rend.Page):
    """
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - House Select Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                T_script(type = 'text/javascript', src = 'housepage.js')["\n"],
                ],
            T_body[
                T_h1['PyHouse House Selection'],
                T_p['\n'],
                T_p['Select the house:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    T_invisible(data = T_directive('houselist'), render = T_directive('houselist'))
                    ],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )["\n",
                    T_input(type = 'button', onclick = "createNewHouseWindow('1')", value = 'add')
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

    def data_houselist(self, _context, _data):
        l_house = {}
        for l_key, l_obj in g_houses_obj.iteritems():
            l_house[l_key] = l_obj.Object
        return l_house

    def render_houselist(self, _context, links):
        l_ret = []
        l_cnt = 0
        for l_key, l_value in sorted(links.iteritems()):
            l_name = l_value.Name
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON, onclick = "createChangeHouseWindow(\'{0:}\', \'{1:}\' )".format(
                        l_value.Name, l_value.Active))
                         [ l_name])
            l_cnt += 1
        return l_ret

    def form_post_add(self, **kwargs):
        print "form_post_addhouse (HousePage)", kwargs
        return SelectHousePage(self.name)

    def form_post_change_house(self, **kwargs):
        print "form_post_change_house (HousePage)", kwargs
        return SelectHousePage(self.name)

    def form_post_deletehouse(self, **kwargs):
        print "form_post_deletehouse (HousePage)", kwargs
        return SelectHousePage(self.name)

    def form_post_house(self, **kwargs):
        print "form_post_house (HousePage)", kwargs
        return SelectHousePage(self.name)


class WebServerPage(rend.Page):
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - WebServer Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                T_script(type = 'text/javascript', src = 'webserverpage.js')["\n"],
                ],
            T_body[
                T_h1['PyHouse Web Server'],
                T_p['\n'],
                T_p['abc'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    T_invisible(data = T_directive('houselist'), render = T_directive('houselist'))
                    ],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )["\n",
                    T_input(type = 'button', onclick = "createNewHouseWindow('1')", value = 'add')
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name


class LogsPage(rend.Page):
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - Logs Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                T_script(type = 'text/javascript', src = 'logspage.js')["\n"],
                ],
            T_body[
                T_h1['PyHouse Logs'],
                T_p['\n'],
                T_p['abc'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    T_invisible(data = T_directive('houselist'), render = T_directive('houselist'))
                    ],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )["\n",
                    T_input(type = 'button', onclick = "createNewHouseWindow('1')", value = 'add')
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name


class RootPage(ManualFormMixin, SelectHousePage, WebServerPage):
    """The main page of the web server.
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html(xmlns = 'http://www.w3.org/1999/xhtml', lang = 'en')[
            T_head[
                T_title['PyHouse - Main Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css')),
                T_script(type = 'text/javascript', src = 'mainpage.js'),
                ],
            T_body[
                T_h1['PyHouse'],
                T_form(name = 'mainmenuofbuttons',
                    action = U_H_child('_submit!!post'),
                    enctype = "multipart/form-data",
                    method = 'post')
                    [
                    T_table(style = 'width: 100%;', border = 0)[
                        T_tr[
                            T_td[ T_input(type = 'submit', value = 'Select House', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Web Server', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Logs', name = BUTTON), ],
                            ],
                         T_tr[
                            T_td[ T_input(type = 'submit', value = 'Quit', name = BUTTON) ],
                            T_td[ T_input(type = 'submit', value = 'Reload', name = BUTTON), ],
                            ],
                        ]  # table
                    ]  # form
                ]  # body
            ]  # html
        )  # stan

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

    def form_post_select(self, **kwargs):
        print "form_post_select (RootPage)", kwargs
        return SelectHousePage('House')

    def form_post_web(self, **kwargs):
        print "form_post_web (RootPage)", kwargs
        return WebServerPage('House')

    def form_post_logs(self, **kwargs):
        print "form_post_logs (RootPage)", kwargs
        return LogsPage('House')

    def form_post_quit(self, *args, **kwargs):
        if g_debug >= 2:
            print "web_server.form_post_quit() - args={0:}, kwargs={1:}".format(args, kwargs)
        self.main_quit()

    def form_post_reload(self, *args, **kwargs):
        print " - form_post_reload - args={0:}, kwargs={1:}".format(args, kwargs)
        return RootPage('Root')

    def form_post(self, *args, **kwargs):
        print " - form_post - args={0:}, kwargs={1:}".format(args, kwargs)
        return RootPage('Root')

    def main_quit(self):
        """Quit the GUI - this also means quitting all of PyHouse !!
        """
        if g_debug >= 1:
            print "web_server.RootPage.main_quit() "
        config_xml.WriteConfig()
        if g_debug >= 1:
            print "web_server.RootPage.main_quit - Quit"
        g_parent.Quit()


class API(object):

    def __init__(self, p_parent, p_houses_api):
        global g_logger
        g_logger = logging.getLogger('PyHouse.WebServ ')
        global g_parent, g_houses_api
        g_parent = p_parent
        g_houses_api = p_houses_api
        #
        if g_debug >= 1:
            print "web_server.API.__init__()"
        Web_Data[0] = WebData()
        Web_Data[0].WebPort = 8580
        l_msg = "Initialized - Start the web server on port {0:}".format(g_port)
        g_logger.info(l_msg)
        if g_debug >= 1:
            print "web_server.API ", l_msg

    def Start(self, p_houses_obj):
        global g_houses_obj
        g_houses_obj = p_houses_obj
        if g_debug >= 1:
            print "web_server.Start()"
        g_site_dir = os.path.split(os.path.abspath(__file__))[0]
        print "Webserver path = ", g_site_dir
        l_site = appserver.NevowSite(RootPage('/'))
        WebUtilities().build_child_tree()
        listenTCP(g_port, l_site)
        g_logger.info("Started.")

    def Stop(self):
        if g_debug >= 1:
            print "web_server.Stop()"


Web_Data = {}

# ## END DBK
