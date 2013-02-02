#!/usr/bin/env python

'''
Created on Sep 28, 2012

@author: briank
'''

from Tkinter import Frame, Label, Entry, Button, IntVar, E, W

import gui
import gui_tools
import config_xml

g_debug = 5


class UPnPWindow(gui_tools.GuiTools):
    """Display a log location window.
    """
    def __init__(self, p_root, p_main_window):
        if g_debug > 0:
            print "gui_upnp - Show select house window"
        self.m_root = p_root
        self.m_frame = Frame(p_root)
        self.m_frame.grid(padx = 5, pady = 5)
        self.m_frame.grid_columnconfigure(0, minsize = 120)
        self.m_frame.grid_columnconfigure(1, minsize = 300)
        self.Port = IntVar()
        # self.Port.set(Web_Data[0].WebPort)
        Label(self.m_frame, text = "Web Server Port").grid(row = 1, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Port).grid(row = 1, column = 1, sticky = W)
        Button(self.m_frame, text = "Update", bg = gui_tools.BG_BOTTOM, command = self.update_logs).grid(row = 91, column = 0)
        Button(self.m_frame, text = "Back", fg = "red", bg = gui_tools.BG_BOTTOM, command = self.main_screen).grid(row = 91, column = 1)

    def update_logs(self):
        l_obj = web.web_server.WebData
        l_obj.WebPort = self.Port.get()
        web.Web_Data[0] = l_obj
        config_xml.WriteConfig().write_log_web()
        self.main_screen()

    def main_screen(self):
        """Exit the logging screen.
        """
        self.frame_delete(self.m_frame)
        gui.MainWindow()


# ## END