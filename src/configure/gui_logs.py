#!/usr/bin/env python

from Tkinter import Frame, Label, Entry, Button, StringVar, E, W

import gui
from configure.gui_tools import GuiTools, BG_BOTTOM
from utils import config_xml
from utils import log

g_debug = 0

Log_Data = log.Log_Data

class LogsWindow(GuiTools):
    """Display a log location window.
    """

    def __init__(self, p_gui_obj, p_houses_obj):
        if g_debug > 0:
            print "gui_logs - Show select house window"
        self.m_gui_obj = p_gui_obj
        self.m_frame.grid(padx = 5, pady = 5)
        self.m_frame.grid_columnconfigure(0, minsize = 120)
        self.m_frame.grid_columnconfigure(1, minsize = 300)
        self.Debug = StringVar()
        self.Debug.set(Log_Data[0].Debug)
        self.Error = StringVar()
        self.Error.set(Log_Data[0].Error)
        Label(self.m_frame, text = "Debug Log Location").grid(row = 1, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Debug).grid(row = 1, column = 1, sticky = W)
        Label(self.m_frame, text = "Error Log Location").grid(row = 2, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Error).grid(row = 2, column = 1, sticky = W)
        Button(self.m_frame, text = "Update", bg = BG_BOTTOM, command = self.update_logs).grid(row = 91, column = 0)
        Button(self.m_frame, text = "Back", fg = "red", bg = BG_BOTTOM, command = self.main_screen).grid(row = 91, column = 1)

    def update_logs(self):
        l_obj = log.LogData
        l_obj.Debug = self.Debug.get()
        l_obj.Error = self.Error.get()
        Log_Data[0] = l_obj
        config_xml.WriteConfig().write_log_web()
        self.main_screen()

    def main_screen(self):
        """Exit the logging screen.
        """
        self.frame_delete(self.m_frame)
        gui.MainWindow()

# ## END
