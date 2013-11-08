'''
Created on May 30, 2013

@author: briank
'''

# Import system type stuff
import datetime
import random
import twisted.python.components as tpc
import xml.etree.ElementTree as ET
from nevow import flat
from nevow import inevow
from nevow import rend
from nevow import static
from nevow import url
from nevow import util
from nevow.rend import _CARRYOVER
from formless import iformless
import json


# Import PyMh files and modules.
from src.utils import xml_tools
# from src.web.web_tagdefs import *


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Debugging info
# 5 = dump
# + = NOT USED HERE


# Web States defined
WS_IDLE = 0  # Starting state
WS_LOGGED_IN = 1  # Successful login completed
WS_ROOTMENU = 2
WS_HOUSE_SELECTED = 3
# global things
WS_SERVER = 101
WS_LOGS = 102
# House things
WS_HOUSE = 201
WS_LOCATION = 202
WS_ROOMS = 203
WS_INTERNET = 204
# Light things
WS_BUTTONS = 501
WS_CONTROLLERS = 502
WS_LIGHTS = 503

SUBMIT = '_submit'
BUTTON = 'post_btn'


class WebData(object):
    """
    """
    def __init__(self):
        self.WebPort = 8580


class State(object):
    """The state of the web server
    """
    def __init__(self):
        self.State = WS_IDLE


class WebUtilities(xml_tools.ConfigFile):
    """
    """


class ComplexHandler(json.JSONEncoder):
    """
    """
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            try:
                l_ret = json.JSONEncoder.default(self, obj)
            except TypeError, e:
                print "ERROR web_utils.ComplexHandler.default() TypeError ", e
                l_ret = 'ERROR'
            return l_ret


class JsonUnicode(object):
    """Utilities for handling unicode and json
    """

    def convert_from_unicode(self, p_input):
        """Convert unicode strings to python 2 strings.
        """
        if isinstance(p_input, dict):
            return {self.convert_from_unicode(key): self.convert_from_unicode(value) for key, value in p_input.iteritems()}
        elif isinstance(p_input, list):
            return [self.convert_from_unicode(element) for element in p_input]
        elif isinstance(p_input, unicode):
            return p_input.encode('ascii')
        else:
            return p_input

    def convert_to_unicode(self, p_input):
        if isinstance(p_input, dict):
            return {self.convert_to_unicode(key): self.convert_to_unicode(value) for key, value in p_input.iteritems()}
        elif isinstance(p_input, list):
            return [self.convert_to_unicode(element) for element in p_input]
        elif isinstance(p_input, (int, bool)):
            return unicode(str(p_input), 'iso-8859-1')
        elif isinstance(p_input, unicode):
            return p_input
        else:
            return unicode(p_input, 'iso-8859-1')

    def decode_json(self, p_json):
        """Convert a json object to a python object
        """
        try:
            l_obj = self.convert_from_unicode(json.loads(p_json))
        except (TypeError, ValueError):
            l_obj = None
        return l_obj

    def encode_json(self, p_obj):
        """Convert a python object to a valid json object.
        """
        try:
            l_json = json.dumps(p_obj, cls = ComplexHandler)
        except (TypeError, ValueError):
            l_json = None
        return l_json


class ManualFormMixin(rend.Page):
    """
    """

    def locateChild(self, context, segments):
        """Add to the standard find child to handle POST of forms

        def form_post_lighting for a submit button valued 'lighting'
        def form_post for the form without a key
        """
        if g_debug >= 2:
            print "web_utils.locate_child() - 1",
            print "    segments: ", segments,
            print "    Context", context
        if segments[0].startswith(SUBMIT):  # Handle the form post
            # Get a method name from the action in the form plus the first word in the button name,
            #  or simply the form action if no button name is specified
            kwargs = {}
            bindingName = ''
            args = inevow.IRequest(context).args
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
            method = getattr(self, 'form_' + name, None)
            if g_debug >= 3:
                print "web_utils.locate_child() - 2"
                print "    Context: ", context
                print "    bindingName:{0:}, ".format(bindingName)
                print "    method: ", method
                print "    args: ", args
                print "    kwargs: ", kwargs
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
            if g_debug >= 3:
                print "web_utils.ManualFormMixin.onManualPost.redirectAfterPost() ",
                print "    aspects:{0:};".format(aspects)
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
            if g_debug >= 4:
                print "web_utils.ManualFormMixin.onManualPost.redirectAfterPost() -2- refpath:", refpath
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
            if g_debug >= 4:
                print "web_utils.ManualFormMixin.onManualPost.redirectAfterPost() -3"
                print "    refpath: ", refpath
                print "    l_handler: ", l_handler
            if l_handler is not None or aspects.get(iformless.IFormErrors) is not None:
                magicCookie = '%s%s%s' % (datetime.datetime.now(), request.getClientIP(), random.random())
                refpath = refpath.replace('_nevow_carryover_', magicCookie)
                _CARRYOVER[magicCookie] = C = tpc.Componentized()
                for k, v in aspects.iteritems():
                    C.setComponent(k, v)
            destination = flat.flatten(refpath, ctx)
            if g_debug >= 2:
                print "web_utils.ManualFormMixin.onManualPost.redirectAfterPost() -4- Posted a form to >{0:}<".format(bindingName)
                print "    destination: ", destination
                print "    refpath: ", refpath
                print "    ctx: ", ctx
            request.redirect(destination)
            return static.Data('You posted a form to %s' % bindingName, 'text/plain'), ()

        request = inevow.IRequest(ctx)
        if g_debug >= 2:
            print "web_utils.ManualFormMixin.onManualPost()"
            print "    Context:{0:}, ".format(ctx)
            print "    Method: ", method
            print "    BindingName:{0:}, ".format(bindingName)
            print "    kwargs: ", kwargs
            print "    request: ", request
        return util.maybeDeferred(method, **kwargs
            ).addCallback(self.onPostSuccess, request, ctx, bindingName, redirectAfterPost
            ).addErrback(self.onPostFailure, request, ctx, bindingName, redirectAfterPost)

def add_attr_list(p_class, p_list):
    """
    setattr(RootPage, 'child_mainpage.css', static.File('src/web/css/mainpage.css'))
    """
    if g_debug >= 2:
        print "web_utils.add_attr_list() - class:{0:}".format(p_class)
    for l_item in p_list:
        l_name = 'child_' + l_item.split('/')[-1]
        if g_debug >= 2:
            print "    Item:{0:} - Name:{1:}".format(l_item, l_name)
        setattr(p_class, l_name, static.File(l_item))
    if g_debug >= 3:
        print "    Dir=", dir(p_class)
        print "    Vars=", vars(p_class)

def add_float_page_attrs(p_class):
    l_list = ['src/web/images/bottomRight.gif', 'src/web/images/close.gif',
              'src/web/images/minimize.gif', 'src/web/images/topCenter.gif',
              'src/web/images/topLeft.gif', 'src/web/images/topRight.gif',
              'src/web/images/handle.horizontal.png']
    add_attr_list(p_class, l_list)

def action_url():
        return url.here.child('_submit!!post')

def dotted_hex2int(p_addr):
    """Convert A1.B2.C3 to int
    """
    l_hexn = ''.join(["%02X" % int(l_ix, 16) for l_ix in p_addr.split('.')])
    return int(l_hexn, 16)

def int2dotted_hex(p_int):
    """Convert 24 bit int to Dotted hex Insteon Address
    """
    l_ix = 256 * 256
    l_hex = []
    while l_ix > 0:
        l_byte, p_int = divmod(p_int, l_ix)
        l_hex.append("{0:02X}".format(l_byte))
        l_ix = l_ix / 256
    return '.'.join(l_hex)

# ## END DBK
