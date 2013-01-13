#!/usr/bin/env python

from Tkinter import Tk, Frame, Button, Label, SUNKEN, W
from twisted.internet import tksupport

import gui_tools
import gui_ctl_lights
import gui_house
import gui_lighting
import gui_logs
import gui_schedule
import gui_web
import config_xml

g_debug = 1
g_root = None  # TkInter root window.
g_parent = None

class MainWindow(object):
    """
    A dispatch (menu button) window.
    """
    def __init__(self):
        self.m_main = Frame(g_root)
        g_root.title('PyHouse Main Menu')
        self.m_main.grid(padx = 5, pady = 5)
        self.m_main.grid_columnconfigure(0, minsize = 120)
        self.m_main.grid_columnconfigure(1, minsize = 120)
        self.m_main.grid_columnconfigure(2, minsize = 120)
        self.m_main.grid_columnconfigure(3, minsize = 120)
        self.m_main.grid_columnconfigure(4, minsize = 120)
        self.m_main.grid_columnconfigure(5, minsize = 120)
        self.m_main.grid_columnconfigure(6, minsize = 120)
        self.m_main.grid_columnconfigure(7, minsize = 120)
        self.m_main.grid_columnconfigure(8, minsize = 120)
        self.m_main.grid_columnconfigure(0, minsize = 120)
        Button(self.m_main, text = "House", bg = gui_tools.BG_TOP, command = self.house_screen).grid(row = 0, column = 0)
        Button(self.m_main, text = "Lighting", bg = gui_tools.BG_TOP, command = self.lighting_screen).grid(row = 0, column = 1)
        Button(self.m_main, text = "Schedule", bg = gui_tools.BG_TOP, command = self.schedule_screen).grid(row = 0, column = 2)
        Button(self.m_main, text = "Logging", bg = gui_tools.BG_TOP, command = self.logging_screen).grid(row = 0, column = 3)
        Button(self.m_main, text = "Web Server", bg = gui_tools.BG_TOP, command = self.webserv_screen).grid(row = 0, column = 4)
        Button(self.m_main, text = "UPnP", bg = gui_tools.BG_TOP, command = self.upnp_screen).grid(row = 0, column = 5)
        Button(self.m_main, text = "Weather", bg = gui_tools.BG_TOP, command = self.weather_screen).grid(row = 0, column = 6)
        Button(self.m_main, text = "Internet", bg = gui_tools.BG_TOP, command = self.internet_screen).grid(row = 0, column = 7)
#
        Button(self.m_main, text = "Scenes", bg = gui_tools.BG_TOP, command = self.scene_screen).grid(row = 1, column = 0)
        Button(self.m_main, text = "Ctl Lights", bg = gui_tools.BG_TOP, command = self.ctl_lights_screen).grid(row = 1, column = 1)
#
        Button(self.m_main, text = "QUIT", fg = "red", bg = gui_tools.BG_BOTTOM, command = self.main_quit).grid(row = 91, column = 1)
        Button(self.m_main, text = "Restart", fg = "red", bg = gui_tools.BG_BOTTOM, command = self.main_restart).grid(row = 91, column = 2)

    def ctl_lights_screen(self):
        self.m_main.grid_forget()  # Main Window
        gui_ctl_lights.CtlLightsWindow(g_root)

    def house_screen(self):
        self.m_main.grid_forget()  # Main Window
        gui_house.HouseWindow(g_root)

    def internet_screen(self):
        self.m_main.grid_forget()  # Main Window
        DummyWindow(g_root)

    def lighting_screen(self):
        self.m_main.grid_forget()  # Main Window
        gui_lighting.LightingWindow(g_root)

    def logging_screen(self):
        self.m_main.grid_forget()  # Main Window
        gui_logs.LogsWindow(g_root)

    def scene_screen(self):
        self.m_main.grid_forget()  # Main Window
        DummyWindow(g_root)

    def schedule_screen(self):
        self.m_main.grid_forget()  # Main Window
        gui_schedule.ScheduleWindow(g_root, self.m_main)

    def upnp_screen(self):
        self.m_main.grid_forget()  # Main Window
        DummyWindow(g_root)

    def weather_screen(self):
        self.m_main.grid_forget()  # Main Window
        DummyWindow(g_root)

    def webserv_screen(self):
        self.m_main.grid_forget()  # Main Window
        gui_web.WebWindow(g_root)

    def main_restart(self):
        self.Stop()
        self.Start()

    def main_quit(self):
        config_xml.WriteConfig()
        self.m_main.grid_forget()  # Main Window
        g_root.withdraw()
        if g_debug > 0:
            print "Gui/daemon Quit"
        g_parent.Quit()


class DummyWindow(gui_tools.GuiTools):
    def __init__(self, p_root):
        if g_debug > 1:
            print "DummyWindow.__init__"
        self.m_frame = Frame(p_root)
        self.m_frame.grid(padx = 5, pady = 5)
        self.button = Button(self.m_frame, text = "Back", fg = "red", command = self.main_screen)
        self.button.grid(row = 0, column = 0)

    def main_screen(self):
        self.frame_delete(self.m_frame)
        MainWindow()


class StatusBar(Frame):
    """
    Status bar.
    """

    def __init__(self, master):
        if g_debug > 1:
            print "StatusBar.__init__"
        Frame.__init__(self, master)
        self.label = Label(self, bd = 1, relief = SUNKEN, anchor = W)
        self.label.grid()

    def set(self, _format, *args):
        self.label.config(text = format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text = "")
        self.label.update_idletasks()


class API(MainWindow):
    """
    """

    def __init__(self, p_parent):
        if g_debug > 0:
            print "gui.API.__init__() - Parent = ", p_parent
        global g_root, g_parent
        g_root = Tk()
        g_parent = p_parent
        tksupport.install(g_root)
        MainWindow()

    def Start(self):
        g_parent.Start()

    def Stop(self):
        g_parent.Stop()

# ## END
