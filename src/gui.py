#!/usr/bin/env python

from Tkinter import *
from twisted.internet import tksupport

import gui_tools
import gui_house
import gui_lighting
import gui_schedule

g_root = None # TkInter root window.

class MainWindow(object):
    """
    A dispatch (menu button) window.
    """
    def __init__(self):
        print "MainWindow.__init__"
        self.m_main = Frame(g_root, bg='#600000')
        g_root.title('PyHouse Main Menu')
        self.m_main.grid(padx = 5, pady = 5)
        self.m_main.grid_columnconfigure(0, minsize=70)
        self.m_main.grid_columnconfigure(1, minsize=70)
        self.m_main.grid_columnconfigure(2, minsize=70)
        self.m_main.grid_columnconfigure(3, minsize=70)
        self.m_main.grid_columnconfigure(4, minsize=70)
        Button(self.m_main, text = "House", command = self.house_screen).grid(row = 0, column = 0)
        Button(self.m_main, text = "Lighting", command = self.lighting_screen).grid(row = 0, column = 1)
        Button(self.m_main, text = "Schedule", command = self.schedule_screen).grid(row = 0, column = 2)
        Button(self.m_main, text = "Logging", command = self.logging_screen).grid(row = 0, column = 3)
        Button(self.m_main, text = "Web Server", command = self.webserv_screen).grid(row = 0, column = 4)
        Button(self.m_main, text = "QUIT", fg = "red", command = self.main_quit).grid(row = 91, column = 1)

    def house_screen(self):
        self.m_main.grid_forget() # Main Window
        h = gui_house.HouseWindow(g_root)

    def lighting_screen(self):
        self.m_main.grid_forget() # Main Window
        h = gui_lighting.LightingWindow(g_root)

    def schedule_screen(self):
        self.m_main.grid_forget() # Main Window
        h = gui_schedule.ScheduleWindow(g_root, self.m_main)

    def logging_screen(self):
        self.m_main.grid_forget() # Main Window
        h = DummyWindow(g_root)

    def webserv_screen(self):
        self.m_main.grid_forget() # Main Window
        h = DummyWindow(g_root)

    def main_quit(self):
        self.m_main.grid_forget() # Main Window
        g_root.withdraw()


class DummyWindow(gui_tools.GuiTools):
    def __init__(self, p_root):
        print "DummyWindow.__init__"
        self.m_frame = Frame(p_root)
        self.m_frame.grid(padx = 5, pady = 5)
        self.button = Button(self.m_frame, text = "Back", fg = "red", command = self.main_screen)
        self.button.grid(row = 0, column = 0)

    def main_screen(self):
        self.frame_delete(self.m_frame)
        m = MainWindow()

    
class StatusBar(Frame):
    """
    Status bar.
    """

    def __init__(self, master):
        print "StatusBar.__init__"
        Frame.__init__(self, master)
        self.label = Label(self, bd = 1, relief = SUNKEN, anchor = W)
        self.label.grid()

    def set(self, format, *args):
        self.label.config(text = format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text = "")
        self.label.update_idletasks()


global g_root
g_root = Tk()
tksupport.install(g_root)

app = MainWindow()

### END
