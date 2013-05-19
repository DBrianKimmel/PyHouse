#!/usr/bin/env python

# Import system type stuff
from Tkinter import Frame, Label, Entry, Button, StringVar, E, W

# Import PyMh files
from src.configure.gui_tools import GuiTools, BG_BOTTOM
from src.utils import config_xml
from src.utils import log

g_debug = 0

Log_Data = log.Log_Data

class LogsWindow(GuiTools):
    """Display a log location window.
    """

    def __init__(self, p_gui_obj, p_houses_obj):
        if g_debug > 0:
            print "gui_logs"
        self.m_gui_obj = p_gui_obj
        p_gui_obj.ModuleMenuFrame = Frame(p_gui_obj.RootWindow)
        self.m_gui_obj.ModuleMenuFrame.grid(padx = 5, pady = 5)
        self.m_gui_obj.ModuleMenuFrame.grid_columnconfigure(0, minsize = 120)
        self.m_gui_obj.ModuleMenuFrame.grid_columnconfigure(1, minsize = 300)
        self.Debug = StringVar()
        self.Debug.set(Log_Data[0].Debug)
        self.Error = StringVar()
        self.Error.set(Log_Data[0].Error)
        Label(self.m_gui_obj.ModuleMenuFrame, text = "Debug Log Location").grid(row = 1, column = 0, sticky = E)
        Entry(self.m_gui_obj.ModuleMenuFrame, textvar = self.Debug).grid(row = 1, column = 1, sticky = W)
        Label(self.m_gui_obj.ModuleMenuFrame, text = "Error Log Location").grid(row = 2, column = 0, sticky = E)
        Entry(self.m_gui_obj.ModuleMenuFrame, textvar = self.Error).grid(row = 2, column = 1, sticky = W)
        Button(self.m_gui_obj.ModuleMenuFrame, text = "Update", bg = BG_BOTTOM, command = self.update_logs).grid(row = 91, column = 0)
        Button(self.m_gui_obj.ModuleMenuFrame, text = "Back", fg = "red", bg = BG_BOTTOM, command = self.main_screen).grid(row = 91, column = 1)

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

# ## END DBK
