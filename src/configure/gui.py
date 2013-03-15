#!/usr/bin/env python

"""Top level GUI to allow editing and control of everything within PyHouse.

Someday this may be a web based section but for now it is a TkInter GUI.

Create a top level window that initially contains a frame showing the main menu.

Each menu selection will bring up a menu frame for that selection type (schedule e.g.).
The main menu frame will be hidden.

Selecting a button from the selection menu will bring up a new top level dialog window to allow
editing etc of the selected item.
When this is complete, the dialog window is deleted and the selection menu will re-appear and
be populated with the new information.
"""

from Tkinter import Tk, Frame, Button
from twisted.internet import tksupport

from configure.gui_tools import GuiTools, GuiData, BG_TOP, BG_BOTTOM, BG_UNDONE
import gui_ctl_lights
import gui_house
import gui_lighting
import gui_logs
import gui_schedule
import gui_web
from utils import config_xml

# For the testing function
from families.Insteon import Insteon_PLM

g_debug = 0

g_root_window = None  # TkInter root window.
g_parent = None

class MainWindow(object):

    m_houses_api = None
    m_houses_obj = None
    m_gui_obj = None
    m_main_menu_frame = None  # the top level gui menu window

    """
    A dispatch (menu button) window.
    @param p_houses_api: access to the singleton instance of houses.
    """
    def __init__(self, p_houses_api, p_gui_obj):
        self.m_gui_obj = p_gui_obj
        self.m_houses_api = p_houses_api
        self.m_houses_obj = p_houses_api.get_houses_obj()
        p_gui_obj.MainMenuFrame = Frame(p_gui_obj.RootWindow)
        if g_debug > 0:
            print "gui.MainWindow.__init__() - Display PyHouse Main Menu window. -  main_menu_frame :{0:}".format(p_gui_obj.MainMenuFrame)
        g_root_window.title('PyHouse Main Menu')
        p_gui_obj.MainMenuFrame.grid(padx = 5, pady = 5)
        p_gui_obj.MainMenuFrame.grid_columnconfigure(0, minsize = 120)
        p_gui_obj.MainMenuFrame.grid_columnconfigure(1, minsize = 120)
        p_gui_obj.MainMenuFrame.grid_columnconfigure(2, minsize = 120)
        p_gui_obj.MainMenuFrame.grid_columnconfigure(3, minsize = 120)
        p_gui_obj.MainMenuFrame.grid_columnconfigure(4, minsize = 120)
        p_gui_obj.MainMenuFrame.grid_columnconfigure(5, minsize = 120)
        p_gui_obj.MainMenuFrame.grid_columnconfigure(6, minsize = 120)
        p_gui_obj.MainMenuFrame.grid_columnconfigure(7, minsize = 120)
        p_gui_obj.MainMenuFrame.grid_columnconfigure(8, minsize = 120)
        p_gui_obj.MainMenuFrame.grid_columnconfigure(0, minsize = 120)
        Button(p_gui_obj.MainMenuFrame, text = "House", bg = BG_TOP,
               command = lambda x = p_gui_obj: self.house_screen(x)).grid(row = 0, column = 0)
        Button(p_gui_obj.MainMenuFrame, text = "Lighting", bg = BG_TOP,
               command = lambda x = p_gui_obj: self.lighting_screen(x)).grid(row = 0, column = 1)
        Button(p_gui_obj.MainMenuFrame, text = "Schedule", bg = BG_TOP,
               command = lambda x = p_gui_obj: self.schedule_screen(x)).grid(row = 0, column = 2)
        Button(p_gui_obj.MainMenuFrame, text = "Logging", bg = BG_TOP,
               command = lambda x = p_gui_obj: self.logging_screen(x)).grid(row = 0, column = 3)
        Button(p_gui_obj.MainMenuFrame, text = "Web Server", bg = BG_UNDONE,
               command = lambda x = p_gui_obj: self.webserv_screen(x)).grid(row = 0, column = 4)
        Button(p_gui_obj.MainMenuFrame, text = "UPnP", bg = BG_UNDONE,
               command = lambda x = p_gui_obj: self.upnp_screen(x)).grid(row = 0, column = 5)
        Button(p_gui_obj.MainMenuFrame, text = "Weather", bg = BG_UNDONE,
               command = lambda x = p_gui_obj: self.weather_screen(x)).grid(row = 0, column = 6)
        Button(p_gui_obj.MainMenuFrame, text = "Internet", bg = BG_UNDONE,
               command = lambda x = p_gui_obj: self.internet_screen(x)).grid(row = 0, column = 7)
#
        Button(p_gui_obj.MainMenuFrame, text = "Scenes", bg = BG_UNDONE,
               command = lambda x = p_gui_obj: self.scene_screen(x)).grid(row = 1, column = 0)
        Button(p_gui_obj.MainMenuFrame, text = "Ctl Lights", bg = BG_TOP,
               command = lambda x = p_gui_obj: self.ctl_lights_screen(x)).grid(row = 1, column = 1)
        Button(p_gui_obj.MainMenuFrame, text = "Test", bg = BG_TOP,
               command = lambda x = p_gui_obj: self.test_screen(x)).grid(row = 1, column = 2)
#
        Button(p_gui_obj.MainMenuFrame, text = "QUIT", fg = "red", bg = BG_BOTTOM,
               command = lambda x = p_gui_obj: self.main_quit(x)).grid(row = 91, column = 1)
        Button(p_gui_obj.MainMenuFrame, text = "Restart", fg = "red", bg = BG_BOTTOM,
               command = self.main_restart).grid(row = 91, column = 2)

    def ctl_lights_screen(self, p_gui_obj):
        if g_debug > 1:
            print "gui.ctl_lights_screen() "
        p_gui_obj.MainMenuFrame.grid_forget()  # Main Window
        gui_ctl_lights.CtlLightsWindow(p_gui_obj, self.m_houses_obj)

    def house_screen(self, p_gui_obj):
        if g_debug > 1:
            print "gui.house_screen() "
        p_gui_obj.MainMenuFrame.grid_forget()  # Main Window
        gui_house.HouseWindow(p_gui_obj, self.m_houses_obj)

    def internet_screen(self, p_gui_obj):
        if g_debug > 1:
            print "gui.internet_screen() "
        p_gui_obj.MainMenuFrame.grid_forget()  # Main Window
        DummyWindow(p_gui_obj, self.m_houses_obj)

    def lighting_screen(self, p_gui_obj):
        if g_debug > 1:
            print "gui.lighting_screen() "
        p_gui_obj.MainMenuFrame.grid_forget()  # Main Window
        gui_lighting.LightingWindow(p_gui_obj, self.m_houses_obj)

    def logging_screen(self, p_gui_obj):
        if g_debug > 1:
            print "gui.logging_screen() "
        p_gui_obj.MainMenuFrame.grid_forget()  # Main Window
        gui_logs.LogsWindow(p_gui_obj, self.m_houses_obj)

    def scene_screen(self, p_gui_obj):
        if g_debug > 1:
            print "gui.scene_screen() "
        p_gui_obj.MainMenuFrame.grid_forget()  # Main Window
        DummyWindow(p_gui_obj, self.m_houses_obj)

    def schedule_screen(self, p_gui_obj):
        if g_debug > 1:
            print "gui.schedule_screen() "
        p_gui_obj.MainMenuFrame.grid_forget()  # Main Window
        gui_schedule.ScheduleWindow(p_gui_obj, self.m_houses_obj)

    def test_screen(self, p_gui_obj):
        if g_debug > 1:
            print "gui.test_screen() "
        self.m_houses_obj[0].HouseAPI.SpecialTest()

    def upnp_screen(self, p_gui_obj):
        if g_debug > 1:
            print "gui.upnp_screen() "
        p_gui_obj.MainMenuFrame.grid_forget()  # Main Window
        DummyWindow(p_gui_obj, self.m_houses_obj)

    def weather_screen(self, p_gui_obj):
        if g_debug > 1:
            print "gui.weather_screen() "
        p_gui_obj.MainMenuFrame.grid_forget()  # Main Window
        DummyWindow(p_gui_obj, self.m_houses_obj)

    def webserv_screen(self, p_gui_obj):
        if g_debug > 1:
            print "gui.webserv_screen() "
        p_gui_obj.MainMenuFrame.grid_forget()  # Main Window
        gui_web.WebWindow(p_gui_obj, self.m_houses_obj)

    def main_restart(self):
        if g_debug > 1:
            print "gui.main_restart() "
        g_parent.Stop()
        g_parent.Start()

    def main_quit(self, p_gui_obj):
        """Quit the GUI - this also means quitting all of PyHouse !!
        """
        if g_debug > 1:
            print "gui.main_quit() "
        config_xml.WriteConfig()
        p_gui_obj.MainMenuFrame.grid_forget()  # Main Window
        g_root_window.withdraw()
        if g_debug > 0:
            print "Gui/daemon Quit"
        g_parent.Quit()


class DummyWindow(GuiTools):
    def __init__(self, p_gui_obj, _p_houses_obj):
        if g_debug > 1:
            print "DummyWindow.__init__"
        self.m_frame = Frame(p_gui_obj.RootWindow)
        self.m_frame.grid(padx = 5, pady = 5)
        self.button = Button(self.m_frame, text = "Back", fg = "red", command = self.main_screen)
        self.button.grid(row = 0, column = 0)

    def main_screen(self):
        self.frame_delete(self.m_frame)
        MainWindow()


class API(MainWindow):
    """
    """

    def __init__(self, p_parent, p_houses_api):
        """
        @param p_parent: is self from where called ( PyHouse.API() )
        """
        if g_debug > 0:
            print "gui.API.__init__() - Parent = ", p_parent
        global g_root_window, g_parent
        l_gui_obj = GuiData()
        l_gui_obj.RootWindow = g_root_window = Tk()
        g_parent = p_parent
        tksupport.install(l_gui_obj.RootWindow)
        MainWindow(p_houses_api, l_gui_obj)

# ## END
