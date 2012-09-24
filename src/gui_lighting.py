#!/usr/bin/env python

from Tkinter import *
import Pmw

import gui
import gui_tools
import lighting
import config_xml


Light_Data = lighting.Light_Data
Button_Data = lighting.Button_Data
Controller_Data = lighting.Controller_Data

VAL_FAM = lighting.VALID_FAMILIES
BG_LIGHT = '#C0C090'
BG_CTLR = '#90C090'
BG_BUTTN = '#C09090'

class LightingWindow(gui_tools.GuiTools):
    """
    """

    def __init__(self, p_root):
        self.m_frame = Frame(p_root)
        self.m_ix = 0
        self.m_frame.grid(padx = 5, pady = 5)
        self.show_all_lights()
        self.light_button = Button(self.m_frame, text = "ADD New Light", bg = BG_LIGHT, command = self.add_light)
        self.light_button.grid(row = self.m_ix, column = 0)
        self.light_button = Button(self.m_frame, text = "ADD New Controller", bg = BG_CTLR, command = self.add_controller)
        self.light_button.grid(row = self.m_ix, column = 1)
        self.light_button = Button(self.m_frame, text = "ADD New Button", bg = BG_BUTTN, command = self.add_button)
        self.light_button.grid(row = self.m_ix, column = 2)
        self.button = Button(self.m_frame, text = "Back", fg = "red", command = self.main_screen)
        self.button.grid(row = self.m_ix, column = 3)

    def show_all_lights(self):
        l_light = []
        self.m_max_light = 0
        for l_obj in Light_Data.itervalues():
            if l_obj.Key > self.m_max_light: self.m_max_light = l_obj.Key
            l = Button(self.m_frame, text = l_obj.Name, bg = BG_LIGHT,
                       command = lambda x = l_obj.Key, y = 1: self.edit_lights(x, y))
            l_light.append(l)
            l_row = self.m_ix // 4
            l_col = self.m_ix % 4
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        self.m_max_controller = 0
        for l_obj in Controller_Data.itervalues():
            if l_obj.Key > self.m_max_controller: self.m_max_controller = l_obj.Key
            c = Button(self.m_frame, fg = "red", text = l_obj.Name, bg = BG_CTLR,
                       command = lambda x = l_obj.Key, y = 2: self.edit_controllers(x, y))
            l_light.append(c)
            l_row = self.m_ix // 4
            l_col = self.m_ix % 4
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        self.m_max_button = 0
        for l_obj in Button_Data.itervalues():
            if l_obj.Key > self.m_max_button: self.m_max_button = l_obj.Key
            b = Button(self.m_frame, fg = "blue", text = l_obj.Name, bg = BG_BUTTN,
                       command = lambda x = l_obj.Key, y = 3: self.edit_buttons(x, y))
            l_light.append(b)
            l_row = self.m_ix // 4
            l_col = self.m_ix % 4
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        self.m_ix += 2

    def edit_lights(self, p_arg, p_kind):
        print "Edit lights", p_arg, p_kind
        LightingDialog(self.m_frame, p_arg, p_kind, "Editing Light")
        self.save_lights()

    def edit_controllers(self, p_arg, p_kind):
        print "Edit Controllers", p_arg, p_kind
        LightingDialog(self.m_frame, p_arg, p_kind, "Editing Controller")
        self.save_lights()

    def edit_buttons(self, p_arg, p_kind):
        print "Edit Buttons", p_arg, p_kind
        LightingDialog(self.m_frame, p_arg, p_kind, "Editing Button")
        self.save_lights()

    def add_light(self):
        print "Adding lights"
        LightingDialog(self.m_frame, self.m_max_light + 1, 4, "Adding Light")
        self.save_lights()

    def add_controller(self):
        print "Adding controller"
        LightingDialog(self.m_frame, self.m_max_controller + 1, 5, "Adding Controller")
        self.save_lights()

    def add_button(self):
        print "Adding button"
        LightingDialog(self.m_frame, self.m_max_button + 1, 6, "Adding Button")
        self.save_lights()

    def save_lights(self):
        config_xml.WriteConfig().write_lights()
        self.main_screen()
        
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
        self.m_dia_frame = Frame(self.m_top)
        self.m_dia_frame.grid_columnconfigure(0, minsize=130)
        self.m_dia_frame.grid_columnconfigure(1, minsize=300)
        self.m_dia_frame.grid(padx = 5, pady = 5)
        Label(self.m_dia_frame, text = "Key").grid(row = 1, column = 0, sticky = E)
        Entry(self.m_dia_frame, textvar = self.Key, state = DISABLED).grid(row = 1, column = 1, sticky = W)
        Label(self.m_dia_frame, text = "Active").grid(row = 2, column = 0, sticky = E)
        self.yes_no_radio(self.m_dia_frame, self.Active).grid(row = 2, column = 1, sticky = W)
        Label(self.m_dia_frame, text = "Name").grid(row = 3, column = 0, sticky = E)
        Entry(self.m_dia_frame, textvar = self.Name).grid(row = 3, column = 1, sticky = W)
        Label(self.m_dia_frame, text = "Family").grid(row = 5, column = 0, sticky = E)
        self.pulldown_box(self.m_dia_frame, VAL_FAM, self.Family).grid(row = 5, column = 1, sticky = W)
        Label(self.m_dia_frame, text = "Comment").grid(row = 7, column = 0, sticky = E)
        Entry(self.m_dia_frame, textvar = self.Comment).grid(row = 7, column = 1, sticky = W)
        Label(self.m_dia_frame, text = "Type").grid(row = 11, column = 0, sticky = E)
        Entry(self.m_dia_frame, textvar = self.Type).grid(row = 11, column = 1, sticky = W)
        Label(self.m_dia_frame, text = "Coords").grid(row = 13, column = 0, sticky = E)
        Entry(self.m_dia_frame, textvar = self.Coords).grid(row = 13, column = 1, sticky = W)
        Label(self.m_dia_frame, text = "Room").grid(row = 15, column = 0, sticky = E)
        Entry(self.m_dia_frame, textvar = self.Room).grid(row = 15, column = 1, sticky = W)
        Label(self.m_dia_frame, text = "Dimmable").grid(row = 17, column = 0, sticky = E)
        Entry(self.m_dia_frame, textvar = self.Dimmable).grid(row = 17, column = 1, sticky = W)
        if l_type == 'Controller':
            Label(self.m_dia_frame, text = 'Interface').grid(row = 31, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.Interface).grid(row = 31, column = 1, sticky = W)
            Label(self.m_dia_frame, text = 'Port').grid(row = 33, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.Port).grid(row = 33, column = 1, sticky = W)
        if l_family == 'Insteon':
            Label(self.m_dia_frame, text = 'Address').grid(row = 41, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.Address).grid(row = 41, column = 1, sticky = W)
            Label(self.m_dia_frame, text = 'Controller').grid(row = 42, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.Controller).grid(row = 42, column = 1, sticky = W)
            Label(self.m_dia_frame, text = 'DevCat').grid(row = 43, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.DevCat).grid(row = 43, column = 1, sticky = W)
            Label(self.m_dia_frame, text = 'GroupList').grid(row = 44, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.GroupList).grid(row = 44, column = 1, sticky = W)
            Label(self.m_dia_frame, text = 'GroupNumber').grid(row = 45, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.GroupNumber).grid(row = 45, column = 1, sticky = W)
            Label(self.m_dia_frame, text = 'Master').grid(row = 46, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.Master).grid(row = 46, column = 1, sticky = W)
            Label(self.m_dia_frame, text = 'ProductKey').grid(row = 47, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.ProductKey).grid(row = 47, column = 1, sticky = W)
            Label(self.m_dia_frame, text = 'Responder').grid(row = 48, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.Responder).grid(row = 48, column = 1, sticky = W)
        elif l_family == 'UPB':
            Label(self.m_dia_frame, text = 'UnitID').grid(row = 51, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.UnitID).grid(row = 51, column = 1, sticky = W)
            Label(self.m_dia_frame, text = 'NetworkID').grid(row = 52, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.NetworkID).grid(row = 52, column = 1, sticky = W)
            Label(self.m_dia_frame, text = 'Password').grid(row = 53, column = 0, sticky = E)
            Entry(self.m_dia_frame, textvar = self.Password).grid(row = 53, column = 1, sticky = W)
        l_text = "Add"
        if p_title.startswith("Edit"):
            l_text = "Save"
            Button(self.m_dia_frame, text = 'Delete', command = self.delete_entry).grid(row = 91, column = 1)
        Button(self.m_dia_frame, text = l_text, fg = "blue", command = self.get_vars).grid(row = 91, column = 0)
        Button(self.m_dia_frame, text = "Cancel", fg = "red", command = self.quit_dialog).grid(row = 91, column = 2)

    def family_box(self, p_parent):
        l_list = lighting.VALID_FAMILIES
        l_family_box = Pmw.ComboBox(p_parent,
                        scrolledlist_items = l_list,
                        )
        l_entry = self.Family.get()
        l_sel = l_list.index(l_entry)
        l_family_box.selectitem(l_sel)
        return l_family_box

    def delete_entry(self):
        l_type = self.Type.get()
        l_key = self.Key.get()
        if l_type == 'Light':
            del Light_Data[l_key]
        elif l_type == 'Controller':
            del Controller_Data[l_key]
        else:
            del Button_Data[l_key]
        config_xml.WriteConfig().write_lights()
        self.quit_dialog()
    
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
        try:
            if p_kind == 1 or p_kind == 4:
                l_type = "Light"
                try:
                    l_obj = Light_Data[p_key]
                except KeyError:
                    l_obj = lighting.LightingData()
            elif p_kind == 2 or p_kind == 5:
                l_type = "Controller"
                try:
                    l_obj = Controller_Data[p_key]
                except KeyError:
                    l_obj = lighting.ControllerData()
            else:
                l_type = "Button"
                try:
                    l_obj = Button_Data[p_key]
                except KeyError:
                    l_obj = lighting.ButtonData()
        except Exception, e: # KeyError
            print "Load vars exception", sys.exc_info()[0], e
            l_obj = lighting.LightingData()
            l_obj.Key = p_key
        l_family = l_obj.Family
        #print "LoadVars", l_type, l_family, p_key, l_obj.Active
        #
        self.Active.set(self.get_bool(l_obj.Active))
        self.Comment.set(l_obj.Comment)
        self.Coords.set(l_obj.Coords)
        self.Dimmable.set(self.get_bool(l_obj.Dimmable))
        self.Family.set(l_family)
        self.Key.set(l_obj.Key)
        self.Name.set(l_obj.Name)
        self.Room.set(l_obj.Room)
        self.Type.set(l_type)
        if l_type == 'Controller':
            self.Interface.set(l_obj.Interface)
            self.Port.set(l_obj.Port)
            if l_obj.Interface == 'USB':
                # USB
                self.Vendor.set(l_obj.Vendor)
                self.Product.set(l_obj.Product)
            if l_obj.Interface == 'Serial':
                # Serial
                self.BaudRate.set(l_obj.BaudRate)
                self.ByteSize.set(l_obj.ByteSize)
                self.Parity.set(l_obj.Parity)
                self.StopBits.set(l_obj.StopBits)
                self.Timeout.set(l_obj.Timeout)
        if l_family == 'Insteon':
            # Family - Insteon
            self.Address.set(l_obj.Address)
            self.Controller.set(self.get_bool(l_obj.Controller))
            self.DevCat.set(l_obj.DevCat)
            self.GroupList.set(l_obj.GroupList)
            self.GroupNumber.set(l_obj.GroupNumber)
            self.Master.set(self.get_bool(l_obj.Master))
            self.ProductKey.set(l_obj.ProductKey)
            self.Responder.set(self.get_bool(l_obj.Responder))
        elif l_family == 'UPB':
            # Family - UPB
            self.NetworkID.set(l_obj.NetworkID)
            self.Password.set(l_obj.Password)
            self.UnitID.set(l_obj.UnitID)
        return l_type, l_family

    def get_vars(self):
        l_type = self.Type.get()
        l_key = self.Key.get()
        l_family = self.Family.get()
        l_interface = self.Interface.get()
        l_obj = lighting.LightingData()
        l_obj.Active = int(self.Active.get())
        l_obj.Comment = self.Comment.get()
        l_obj.Coords = self.Coords.get()
        l_obj.Dimmable = self.Dimmable.get()
        l_obj.Family = l_family
        l_obj.Key = l_key
        l_obj.Name = self.Name.get()
        l_obj.Room = self.Room.get()
        l_obj.Type = l_type
        if l_family == 'Insteon':
            l_obj.Address = self.Address.get()
            l_obj.Controller = int(self.Controller.get())
            l_obj.DevCat = int(self.DevCat.get())
            l_obj.GroupList = self.GroupList.get()
            l_obj.GroupNumber = self.GroupNumber.get()
            l_obj.Master = int(self.Master.get())
            l_obj.ProductKey = int(self.ProductKey.get())
            l_obj.Responder = int(self.Responder.get())
        elif l_family == 'UPB':
            l_obj.NetworkID = int(self.NetworkID.get())
            l_obj.Password = int(self.Password.get())
            l_obj.UnitID = int(self.UnitID.get())
        if l_interface == 'USB':
            pass
        elif l_interface == 'Serial':
            pass
        else:
            pass
        if l_type == 'Light':
            Light_Data[l_key] = l_obj
        elif l_type == 'Controller':
            l_obj.Interface = self.Interface.get()
            l_obj.Port = self.Port.get()
            Controller_Data[l_key] = l_obj
        else:
            Button_Data[l_key] = l_obj
        #print "lighting dialog get_vars", l_obj.Active
        config_xml.WriteConfig().write_lights()
        self.quit_dialog()

    def quit_dialog(self):
        self.m_top.destroy()

### END
