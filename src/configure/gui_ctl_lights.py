'''
Created on Oct 7, 2012

@author: briank
'''
from Tkinter import *
import lighting.lighting as lighting
import gui
import gui_tools
from configure.gui_tools import GuiTools


Light_Data = lighting.Light_Data
g_debug = False

FG = 'red'
BG_LIGHT = '#C0C090'


class CtlLightsWindow(GuiTools):
    '''
    classdocs
    '''


    def __init__(self, p_root):
        '''
        Constructor
        '''
        self.m_frame = Frame(p_root)
        self.m_ix = 0
        self.m_frame.grid()
        self.show_all_lights()
        Button(self.m_frame, text = "Back", fg = FG, bg = gui_tools.BG_BOTTOM, command = self.main_screen).grid(row = self.m_ix, column = 1)

    def show_all_lights(self):
        l_light = []
        self.m_max_light = 0
        for l_obj in Light_Data.itervalues():
            if l_obj.Key > self.m_max_light: self.m_max_light = l_obj.Key
            l_relief = SUNKEN
            if l_obj.Active: l_relief = RAISED
            l = Button(self.m_frame, text = l_obj.Name, bg = BG_LIGHT, relief = l_relief,
                       command = lambda x = l_obj.Key, y = 1: self.ctl_lights(x, y))
            l_light.append(l)
            l_row = self.m_ix // 4
            l_col = self.m_ix % 4
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1

    def ctl_lights(self, p_arg, p_kind):
        print "Edit lights", p_arg, p_kind
        LightingDialog(self.m_frame, p_arg, p_kind, "Editing Light")

    def main_screen(self):
        self.frame_delete(self.m_frame)
        gui.MainWindow()


class LightingDialog(gui_tools.GuiTools):
    """
    """
    def __init__(self, p_parent, p_key, p_kind, p_title = None):
        self.m_top = Toplevel(p_parent)
        if p_title:
            self.m_top.title(p_title)
        self.m_parent = p_parent
        self.l_result = None
        self.create_vars()
        l_type, l_family = self.load_vars(p_key, p_kind)
        Button(self.m_dia_frame, text = "Cancel", fg = "red", bg = gui_tools.BG_BOTTOM, command = self.quit_dialog).grid(row = 91, column = 2)

    def create_vars(self):
        """Create everything - used or not.
        """
        # Common / Lights, Buttons
        self.Active = IntVar()
        self.Comment = StringVar()
        self.Coords = StringVar()
        self.Dimmable = IntVar()
        self.Family = StringVar()
        self.Key = IntVar()
        self.Name = StringVar()
        self.Room = StringVar()
        self.Type = StringVar()
        # Controllers
        self.Interface = StringVar()
        self.Port = StringVar()
        # Interface USB
        self.Vendor = IntVar()
        self.Product = IntVar()
        # Interface Serial
        self.BaudRate = IntVar()
        self.ByteSize = IntVar()
        self.Parity = StringVar()
        self.StopBits = DoubleVar()
        self.Timeout = DoubleVar()
        # Family - UPB
        self.NetworkID = IntVar()
        self.Password = IntVar()
        self.UnitID = IntVar()
        # Family - Insteon
        self.Address = StringVar()
        self.Controller = IntVar()
        self.DevCat = StringVar()
        self.GroupList = StringVar()
        self.GroupNumber = StringVar()
        self.Master = IntVar()
        self.ProductKey = IntVar()
        self.Responder = IntVar()

    def load_vars(self, p_key, p_kind):
        #print "LoadVars key, Kind = {0:} - {1:}".format(p_key, p_kind)
        pass

    def get_vars(self):
        pass

    def quit_dialog(self):
        self.m_top.destroy()

### END
