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

# Import PyMh files and modules.
from src.utils import xml_tools
from src.web.web_tagdefs import *


g_debug = 0
# 0 = off
# 1 = major routine entry
# 4 = display XML parse fields
# 9 = dump


class WebData(object):
    """
    """
    def __init__(self):
        self.WebPort = 8580


class WebUtilities(xml_tools.ConfigFile):
    """
    """

    def read_web_xml(self, p_web_obj, p_root_xml):
        if g_debug >= 1:
            print "web_utils.WebUtilities().read_web_xml()"
        if g_debug >= 9:
            print xml_tools.prettify(p_root_xml)
        try:
            l_sect = p_root_xml.find('Web')
        except AttributeError:
            if g_debug >= 1:
                print "web_utils.read_web_xml() - ERROR in finding Web/WebPort, Creating entry", l_sect
            l_sect = ET.SubElement(p_root_xml, 'Web')
        p_web_obj.WebPort = self.get_int_from_xml(l_sect, 'WebPort')
        if g_debug >= 4:
            print "web_utils.read_web_xml() - Port:{0:}".format(p_web_obj.WebPort)

    def write_web_xml(self):
        if g_debug >= 2:
            print "web_server.write_web_xml()"
        l_xml = ET.Element("Web")
        self.put_int_attribute(l_xml, 'WebPort', WebData.WebPort)
        return l_xml



class ManualFormMixin(rend.Page):
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
            method = getattr(self, 'form_' + name, None)
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
            if g_debug >= 7:
                print "web_utils.ManualFormMixin.onManualPost.redirectAfterPost() -1- Start - ctx:", ctx, ", method:", method, ", bindingName:", bindingName, ", kwargs", kwargs
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
            if g_debug >= 7:
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
            if g_debug >= 7:
                print "web_utils.ManualFormMixin.onManualPost.redirectAfterPost() -3- refpath:", refpath
            if l_handler is not None or aspects.get(iformless.IFormErrors) is not None:
                magicCookie = '%s%s%s' % (datetime.datetime.now(), request.getClientIP(), random.random())
                refpath = refpath.replace('_nevow_carryover_', magicCookie)
                _CARRYOVER[magicCookie] = C = tpc.Componentized()
                for k, v in aspects.iteritems():
                    C.setComponent(k, v)
            destination = flat.flatten(refpath, ctx)
            request.redirect(destination)
            if g_debug >= 1:
                print "web_utils.ManualFormMixin.onManualPost.redirectAfterPost() -4- Posted a form to >", bindingName, "<"
            return static.Data('You posted a form to %s' % bindingName, 'text/plain'), ()

        request = inevow.IRequest(ctx)
        if g_debug >= 1:
            print "web_utils.ManualFormMixin.onManualPost.redirectAfterPost() -5- defer ", kwargs
        return util.maybeDeferred(method, **kwargs
            ).addCallback(self.onPostSuccess, request, ctx, bindingName, redirectAfterPost
            ).addErrback(self.onPostFailure, request, ctx, bindingName, redirectAfterPost)

# ## END DBK
