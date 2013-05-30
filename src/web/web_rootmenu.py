'''
Created on May 30, 2013

@author: briank
'''

# Import system type stuff
from nevow import loaders
from nevow import rend
from nevow import static

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web.web_server import ManualFormMixin
from src.web.web_server import SelectHousePage
from src.web.web_server import LogsPage
from src.web.web_server import WebServerPage
from src.utils import config_xml


g_debug = 8

SUBMIT = '_submit'
BUTTON = 'post_btn'


class RootPage(ManualFormMixin):
    """The main page of the web server.
    """
    setattr(self, 'child_mainpage.css', static.File('web/css/mainpage.css'))
    setattr(self, 'child_ajax.js', static.File('web/js/ajax.js'))
    setattr(self, 'child_floating_window.js', static.File('web/js/floating-window.js'))
    setattr(self, 'child_housepage.js', static.File('web/js/housepage.js'))
    setattr(self, 'child_mainpage.js', static.File('web/js/mainpage.js'))
    #------------------------------------
    setattr(self, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
    setattr(self, 'child_close.gif', static.File('web/images/close.gif'))
    setattr(self, 'child_minimize.gif', static.File('web/images/minimize.gif'))
    setattr(self, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
    setattr(self, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
    setattr(self, 'child_topRight.gif', static.File('web/images/top_right.gif'))
    setattr(self, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))

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
        # g_parent.Quit()

# ## END DBK
