#!/usr/bin/env python

from Tkinter import *
# import Pmw

import gui
import gui_tools
import lighting.lighting as lighting
import config_xml
import main.house as house
from operator import attrgetter


g_debug = 0
Light_Data = lighting.Light_Data
Button_Data = lighting.Button_Data
Controller_Data = lighting.Controller_Data
Location_Data = house.Location_Data
Room_Data = house.Room_Data

VAL_FAM = lighting.VALID_FAMILIES
VAL_INTER = lighting.VALID_INTERFACES
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
        self.button = Button(self.m_frame, text = "Back", fg = "red", bg = gui_tools.BG_BOTTOM, command = self.main_screen)
        self.button.grid(row = self.m_ix, column = 3)

    def show_all_lights(self):
        l_light = []
        self.m_max_light = 0
        for l_obj in sorted(Light_Data.itervalues(), key = attrgetter('Name')):
            if l_obj.Key > self.m_max_light: self.m_max_light = l_obj.Key
            l_relief = SUNKEN
            if l_obj.Active: l_relief = RAISED
            l = Button(self.m_frame, text = l_obj.Name, bg = BG_LIGHT, relief = l_relief,
                       command = lambda x = l_obj.Key, y = 1: self.edit_lights(x, y))
            l_light.append(l)
            l_row = self.m_ix // 4
            l_col = self.m_ix % 4
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        self.m_max_controller = 0
        for l_obj in Controller_Data.itervalues():
            if l_obj.Key > self.m_max_controller: self.m_max_controller = l_obj.Key
            l_relief = SUNKEN
            if l_obj.Active: l_relief = RAISED
            c = Button(self.m_frame, fg = "red", text = l_obj.Name, bg = BG_CTLR, relief = l_relief,
                       command = lambda x = l_obj.Key, y = 2: self.edit_controllers(x, y))
            l_light.append(c)
            l_row = self.m_ix // 4
            l_col = self.m_ix % 4
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        self.m_max_button = 0
        for l_obj in Button_Data.itervalues():
            if l_obj.Key > self.m_max_button: self.m_max_button = l_obj.Key
            l_relief = SUNKEN
            if l_obj.Active: l_relief = RAISED
            b = Button(self.m_frame, fg = "blue", text = l_obj.Name, bg = BG_BUTTN, relief = l_relief,
                       command = lambda x = l_obj.Key, y = 3: self.edit_buttons(x, y))
            l_light.append(b)
            l_row = self.m_ix // 4
            l_col = self.m_ix % 4
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        self.m_ix += 2

    def edit_lights(self, p_arg, p_kind):
        if g_debug > 0:
            print "Edit lights", p_arg, p_kind
        LightingDialog(self.m_frame, p_arg, p_kind, "Editing Light")
        self.save_lights()

    def edit_controllers(self, p_arg, p_kind):
        if g_debug > 0:
            print "Edit Controllers", p_arg, p_kind
        LightingDialog(self.m_frame, p_arg, p_kind, "Editing Controller")
        self.save_lights()

    def edit_buttons(self, p_arg, p_kind):
        if g_debug > 0:
            print "Edit Buttons", p_arg, p_kind
        LightingDialog(self.m_frame, p_arg, p_kind, "Editing Button")
        self.save_lights()

    def add_light(self):
        if g_debug > 0:
            print "Adding lights"
        LightingDialog(self.m_frame, self.m_max_light + 1, 4, "Adding Light")
        self.save_lights()

    def add_controller(self):
        if g_debug > 0:
            print "Adding controller"
        LightingDialog(self.m_frame, self.m_max_controller + 1, 5, "Adding Controller")
        self.save_lights()

    def add_button(self):
        if g_debug > 0:
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
        if g_debug > 3:
            print "LightingDialog.__init__()", p_parent, p_key, p_kind, p_title
        self.m_top = Toplevel(p_parent)
        if p_title:
            self.m_top.title(p_title)
        self.m_parent = p_parent
        self.l_result = None
        self.create_vars()
        l_type, l_family, l_interface = self.load_vars(p_key, p_kind)
        self.m_frame = Frame(self.m_top)
        self.m_frame.grid_columnconfigure(0, minsize = 130)
        self.m_frame.grid_columnconfigure(1, minsize = 300)
        self.m_frame.grid(padx = 5, pady = 5)
        # Common Part - Light
        self.get_entry_str(self.m_frame, 1, 'Key', self.Key, state = DISABLED)
        self.get_entry_bol(self.m_frame, 2, 'Active', self.Active)
        self.get_entry_str(self.m_frame, 3, 'Type', self.Type, state = DISABLED)
        self.get_entry_str(self.m_frame, 4, 'Name', self.Name, width = 50)
        self.get_entry_pdb(self.m_frame, 5, 'Family', self.Family, VAL_FAM, self.Family, self.get_family)
        self.get_entry_str(self.m_frame, 6, 'Comment', self.Comment, width = 50)
        self.get_entry_str(self.m_frame, 7, 'Coords', self.Coords)
        self.get_entry_pdb(self.m_frame, 8, 'House Name', self.HouseName, self.build_names(Location_Data), self.HouseName, self.get_housename)
        self.get_entry_pdb(self.m_frame, 9, 'Room Name', self.RoomName, self.build_names(Room_Data), self.RoomName, self.get_roomname)
        self.get_entry_bol(self.m_frame, 10, 'Dimmable', self.Dimmable)
        # nothing extra for buttons yet.
        if l_type == 'Button':
            pass
        # controllers have a lot more.
        elif l_type == 'Controller':
            self.get_entry_pdb(self.m_frame, 31, 'Interface', self.Interface, VAL_INTER, self.Interface, self.get_interface)
            self.get_entry_str(self.m_frame, 32, 'Port', self.Port, width = 50)
            self.get_entry_hex(self.m_frame, 33, 'Vendor', self.Vendor)
            self.get_entry_hex(self.m_frame, 34, 'Product', self.Product)
            if l_interface == 'Serial':
                self.get_entry_str(self.m_frame, 41, 'Baud Rate', self.BaudRate)
                self.get_entry_str(self.m_frame, 42, 'Byte Size', self.ByteSize)
                self.get_entry_str(self.m_frame, 43, 'Parity', self.Parity)
                self.get_entry_str(self.m_frame, 44, 'Stop Bits', self.StopBits)
                self.get_entry_str(self.m_frame, 45, 'Timeout', self.Timeout)
            elif l_interface == 'USB':
                pass
            elif l_interface == 'Ethernet':
                pass
        # Now for interfaces add the following:
        if l_family == 'Insteon':
            self.get_entry_str(self.m_frame, 61, 'Address', self.Address)
            self.get_entry_bol(self.m_frame, 62, 'Controller', self.Controller)
            self.get_entry_str(self.m_frame, 63, 'DevCat', self.DevCat)
            self.get_entry_str(self.m_frame, 64, 'Group Number', self.GroupNumber)
            self.get_entry_str(self.m_frame, 65, 'Group List', self.GroupList)
            self.get_entry_str(self.m_frame, 66, 'Master', self.Master)
            self.get_entry_str(self.m_frame, 67, 'Product Key', self.ProductKey)
            self.get_entry_bol(self.m_frame, 68, 'Responder', self.Responder)
        elif l_family == 'UPB':
            self.get_entry_str(self.m_frame, 61, 'Unit ID', self.UnitID)
            self.get_entry_str(self.m_frame, 62, 'Network ID', self.NetworkID)
            self.get_entry_str(self.m_frame, 63, 'Password', self.Password)
        elif l_family == 'X10':
            pass
        l_text = "Add"
        if p_title.startswith("Edit"):
            l_text = "Save"
            self.get_entry_btn(self.m_frame, 91, 1, 'Delete', self.delete_entry, bg = gui_tools.BG_BOTTOM)
        self.get_entry_btn(self.m_frame, 91, 0, l_text, self.get_vars, fg = "blue", bg = gui_tools.BG_BOTTOM)
        self.get_entry_btn(self.m_frame, 91, 3, "Cancel", self.quit_dialog, fg = "blue", bg = gui_tools.BG_BOTTOM)

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
        self.RoomName = StringVar()
        self.HouseName = StringVar()
        self.Type = StringVar()
        # Controllers
        self.Interface = StringVar()
        self.Port = StringVar()
        self.Vendor = StringVar()
        self.Product = StringVar()
        # Interface USB
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
        self.ProductKey = StringVar()
        self.Responder = IntVar()

    def load_vars(self, p_key, p_kind):
        """put the values in the gui boxes
        """
        # print "LoadVars key, Kind = {0:} - {1:}".format(p_key, p_kind)
        l_interface = None
        try:
            if p_kind == 1 or p_kind == 4:
                l_type = "Light"
                try:
                    l_obj = Light_Data[p_key]
                except KeyError:
                    l_obj = lighting.LightingData()
                    l_obj.Key = p_key
                    l_obj.Family = 'Insteon'
                    l_obj.Address = ''
            elif p_kind == 2 or p_kind == 5:
                l_type = "Controller"
                try:
                    l_obj = Controller_Data[p_key]
                except KeyError:
                    l_obj = lighting.ControllerData()
                    l_obj.Family = 'Insteon'
                l_interface = l_obj.Interface
            else:
                l_type = "Button"
                try:
                    l_obj = Button_Data[p_key]
                except KeyError:
                    l_obj = lighting.ButtonData()
                    l_obj.Family = 'Insteon'
        except Exception, e:  # KeyError
            print "Load vars exception", sys.exc_info()[0], e
            l_obj = lighting.LightingData()
            l_obj.Key = p_key
            l_obj.Family = 'Insteon'
        l_family = l_obj.Family
#        l_interface = l_obj.Interface
        # print "LoadVars", l_type, l_family, p_key, l_obj.Active
        #
        self.Active.set(self.get_bool(l_obj.Active))
        self.Comment.set(l_obj.Comment)
        self.Coords.set(l_obj.Coords)
        self.Dimmable.set(self.get_bool(l_obj.Dimmable))
        self.Family.set(l_family)
        self.Key.set(l_obj.Key)
        self.Name.set(l_obj.Name)
        self.RoomName.set(l_obj.RoomName)
        self.HouseName.set(l_obj.HouseName)
        self.Type.set(l_type)
        if l_type == 'Controller':
            if g_debug > 0:
                print "gui_lighting() - Interface =", l_obj.Interface
            self.Interface.set(l_obj.Interface)
            self.Port.set(l_obj.Port)
            self.Vendor.set(self.put_hex(int(str(l_obj.Vendor), 0)))  # Displays hex
            self.Product.set(self.put_hex(int(str(l_obj.Product), 0)))  # Displays hex
            if l_obj.Interface == 'USB':
                # USB
                # self.Vendor.set(l_obj.Vendor)
                # self.Product.set(l_obj.Product)
                pass
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
            self.DevCat.set(self.put_hex(int(str(l_obj.DevCat), 0)))  # Displays hex
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
        return l_type, l_family, l_interface

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
        l_obj.RoomName = self.RoomName.get()
        l_obj.HouseName = self.HouseName.get()
        l_obj.Type = l_type
        if l_family == 'Insteon':
            l_obj.Address = self.Address.get()
            l_obj.Controller = int(self.Controller.get())
            l_obj.DevCat = self.DevCat.get()
            l_obj.GroupList = self.GroupList.get()
            l_obj.GroupNumber = self.GroupNumber.get()
            l_obj.Master = int(self.Master.get())
            l_obj.ProductKey = self.ProductKey.get()
            l_obj.Responder = int(self.Responder.get())
        elif l_family == 'UPB':
            l_obj.NetworkID = int(self.NetworkID.get())
            l_obj.Password = int(self.Password.get())
            l_obj.UnitID = int(self.UnitID.get())
        #
        if l_interface == 'USB':
            l_obj.Vendor = self.Vendor.get()
            l_obj.Product = self.Product.get()
        elif l_interface == 'Serial':
            l_obj.BaudRate = int(self.BaudRate.get())
            l_obj.ByteSize = self.ByteSize.get()
            l_obj.Parity = self.Parity.get()
            l_obj.StopBits = self.StopBits.get()
            l_obj.Timeout = self.Timeout.get()
            pass
        else:
            pass
        #
        if l_type == 'Light':
            Light_Data[l_key] = l_obj
        elif l_type == 'Controller':
            l_obj.Interface = self.Interface.get()
            l_obj.Port = self.Port.get()
            Controller_Data[l_key] = l_obj
        else:
            Button_Data[l_key] = l_obj
        # print "lighting dialog get_vars", l_obj.Active
        config_xml.WriteConfig().write_lights()
        self.quit_dialog()

    def quit_dialog(self):
        self.m_top.destroy()

    def get_family(self, p_val):
        self.Family.set(p_val)
        if g_debug > 0:
            print "get family - ", p_val

    def get_housename(self, p_val):
        self.HouseName.set(p_val)
        if g_debug > 0:
            print "get house name - ", p_val

    def get_interface(self, p_val):
        self.Interface.set(p_val)
        if g_debug > 0: print "get interface - ", p_val

    def get_roomname(self, p_val):
        self.RoomName.set(p_val)
        if g_debug > 0:
            print "get room name - ", p_val

# ## END
