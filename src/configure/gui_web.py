#!/usr/bin/env python

'''
Created on Sep 22, 2012

@author: briank
'''

from Tkinter import Frame, Label, Entry, Button, IntVar, E, W

import gui
from configure.gui_tools import GuiTools, BG_BOTTOM
from utils import config_xml
# from web import web_server

# Web_Data = web_server.Web_Data

class WebWindow(GuiTools):
    """Display a log location window.
    """

    def __init__(self, p_gui_obj, p_houses_obj):
        self.m_gui_obj = p_gui_obj
        self.show_house_select_window(p_gui_obj, p_houses_obj)
        self.m_frame.grid(padx = 5, pady = 5)
        self.m_frame.grid_columnconfigure(0, minsize = 120)
        self.m_frame.grid_columnconfigure(1, minsize = 300)
        self.Port = IntVar()
        # self.Port.set(Web_Data[0].WebPort)
        Label(self.m_frame, text = "Web Server Port").grid(row = 1, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Port).grid(row = 1, column = 1, sticky = W)
        Button(self.m_frame, text = "Update", bg = BG_BOTTOM, command = self.update_logs).grid(row = 91, column = 0)
        Button(self.m_frame, text = "Back", fg = "red", bg = BG_BOTTOM, command = self.main_screen).grid(row = 91, column = 1)

    def update_logs(self):
        l_obj = None  # web_server.WebData
        l_obj.WebPort = self.Port.get()
        # Web_Data[0] = l_obj
        config_xml.WriteConfig().write_log_web()
        self.main_screen()

    def main_screen(self):
        """Exit the logging screen.
        """
        self.frame_delete(self.m_frame)
        gui.MainWindow()

# ## END
