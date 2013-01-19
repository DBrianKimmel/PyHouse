#!/usr/bin/env python

from Tkinter import Frame, Toplevel, Button, IntVar, StringVar, DoubleVar, W, DISABLED, SUNKEN, RAISED

import gui
import gui_tools
import main.house as house
import config_xml
from operator import attrgetter

HouseData = house.HouseData
House_Data = house.House_Data
LocationData = house.LocationData
XLocation_Data = house.Location_Data
RoomData = house.RoomData
XRoom_Data = house.Room_Data


g_debug = 3
FG = 'red'

class HouseUtils(object):
    """
    """

    def get_house_object(self, p_key):
        """Load the object for a given house.

        @param p_key: is the key of the house in House_Data.
        """
        try:
            l_obj = House_Data[p_key]
        except:
            l_obj = HouseData()
            l_obj.Key = p_key
            l_obj.Buttons = {}
            l_obj.Controllers = {}
            l_obj.Lights = {}
            l_obj.Location = {}
            l_obj.Rooms = {}
            l_obj.Schedule = {}
        return l_obj


class HouseWindow(gui_tools.GuiTools):
    """Displays all defined houses and handles house add/change/delete.
    """

    def __init__(self, p_root):
        self.m_frame = Frame(p_root)
        self.m_ix = 0
        self.m_frame.grid()
        self.show_all_houses()
        Button(self.m_frame, text = "ADD New House", fg = FG, bg = gui_tools.BG_BOTTOM, command = self.add_house).grid(row = self.m_ix, column = 0)
        Button(self.m_frame, text = "Back", fg = FG, bg = gui_tools.BG_BOTTOM, command = self.main_screen).grid(row = self.m_ix, column = 1)

    def show_all_houses(self):
        l_house = []
        self.m_max = 0
        for l_obj in sorted(House_Data.itervalues(), key = attrgetter('Name')):
            if l_obj.Key > self.m_max:
                self.m_max = l_obj.Key
            l_relief = SUNKEN
            if l_obj.Active: l_relief = RAISED
            if g_debug > 0:
                print l_obj.Name, l_obj.Key
            h = Button(self.m_frame, text = l_obj.Name, bg = gui_tools.BG_TOP, relief = l_relief, command = lambda x = l_obj.Key: self.edit_house(x))
            l_house.append(h)
            l_house[self.m_ix].grid(row = self.m_ix, sticky = W)
            self.m_ix += 1
        self.m_ix += 1

    def add_house(self):
        if g_debug > 2:
            print "gui_house.add_house() # ", self.m_ix
        HouseDialog(self.m_frame, self.m_ix, "Adding House")

    def add_room(self):
        if g_debug > 2:
            print "gui_house.add_room() # ", self.m_ix
        RoomDialog(self.m_frame, self.m_ix, "Adding Room")

    def edit_house(self, p_key):
        if g_debug > 2:
            print "gui_house.edit_house() # ", p_key
        HouseDialog(self.m_frame, p_key, "Editing House")

    def main_screen(self):
        self.frame_delete(self.m_frame)
        gui.MainWindow()



class HouseDialog(gui_tools.GuiTools, HouseUtils):
    """
    Add / edit / delete dialog window for a house.

    @param p_parent: is the parent frame for the new dialog frame.
    @param p_key: is the house key value.
    @param p_title: is the title to display on the dialog frame.
    """

    m_obj = None  # the house object

    def __init__(self, p_parent, p_key, p_title = None):
        self.m_top = Toplevel(p_parent)
        if p_title:
            self.m_top.title(p_title)
        _l_adding = "normal"
        if p_title.startswith("Edit"):
            _l_adding = 'disabled'
        self.m_parent = p_parent
        self.create_vars()
        self.m_obj = self.get_house_object(p_key)
        self.load_vars(self.m_obj)
        self.m_frame = Frame(self.m_top)
        self.m_frame.grid(padx = 5, pady = 5)
        self.get_entry_str(self.m_frame, 1, 'Key', self.Key, state = DISABLED)
        self.get_entry_bol(self.m_frame, 2, 'Active', self.Active)
        self.get_entry_str(self.m_frame, 3, 'Name', self.Name, width = 50)
        self.get_entry_str(self.m_frame, 4, 'Street', self.Street, width = 50)
        self.get_entry_str(self.m_frame, 5, 'City', self.City)
        self.get_entry_str(self.m_frame, 6, 'State', self.State)
        self.get_entry_str(self.m_frame, 7, 'Zip Code', self.Zip)
        self.get_entry_str(self.m_frame, 8, 'Time Zone', self.Timezone)
        self.get_entry_str(self.m_frame, 9, 'Savings Time', self.SavingTime)
        self.get_entry_str(self.m_frame, 10, 'Phone', self.Phone)
        self.get_entry_str(self.m_frame, 11, 'Latitude', self.Latitude)
        self.get_entry_str(self.m_frame, 12, 'Longitude', self.Longitude)
        self.show_all_rooms(self.m_obj)
        l_text = "Add"
        if p_title.startswith("Edit"):
            l_text = "Save"
            Button(self.m_frame, text = 'Delete', bg = gui_tools.BG_BOTTOM, command = self.delete_house).grid(row = 91, column = 1)
        Button(self.m_frame, text = l_text, fg = "blue", bg = gui_tools.BG_BOTTOM, command = self.add_save_house).grid(row = 91, column = 0)
        Button(self.m_frame, text = 'Add Room', bg = gui_tools.BG_BOTTOM, command = self.add_room).grid(row = 91, column = 2)
        Button(self.m_frame, text = "Cancel", fg = "red", bg = gui_tools.BG_BOTTOM, command = self.quit_house).grid(row = 91, column = 3)

    def show_all_rooms(self, p_obj):
        """Display all the rooms in a house on the dialog so they may be edited.

        @param p_obj: is the house object with rooms lights schedules ...
        """
        l_name = self.Name.get()
        l_frame = Frame(self.m_frame)
        l_ix = 0
        self.m_room_count = 0
        for l_obj in sorted(p_obj.Rooms.itervalues(), key = attrgetter('Name')):
            self.m_room_count += 1
            if l_obj.HouseName != l_name: continue
            l_row, l_col = self.columnize(l_ix, 5)
            Button(l_frame, text = l_obj.Name, bg = gui_tools.BG_TOP, command = lambda x = l_obj.Key: self.edit_room(x)).grid(row = l_row, column = l_col)
            l_ix += 1
        l_frame.grid(row = 31, column = 0, columnspan = 3)

    def add_save_house(self):
        """Merge the location(in vars) into the house
        """
        l_obj = self.get_vars()
        House_Data[l_obj.Key] = l_obj
        if g_debug > 1:
            print "gui_house.add_save_house() - Name:{0:}, Key:{1:}".format(l_obj.Name, l_obj.Key)
        config_xml.WriteConfig().write_houses()
        self.quit_house()

    def add_room(self):
        if g_debug > 2:
            print "gui_house.add_room() # ", self.m_room_count + 1
        RoomDialog(self.m_frame, self.m_room_count + 1, self.HouseName, "Adding Room")

    def edit_room(self, p_key):
        if g_debug > 2:
            print "gui_house.edit_room() # ", p_key
        RoomDialog(self.m_frame, p_key, self.HouseName, "Editing Room")

    def delete_house(self):
        l_key = self.Key.get()
        if g_debug > 2:
            print "gui_house.delete_house() # ", l_key
        del House_Data[l_key]
        config_xml.WriteConfig().write_houses()
        self.quit_house()

    def quit_house(self):
        self.m_top.destroy()

    def create_vars(self):
        self.Active = IntVar()
        self.Key = IntVar()
        self.Name = StringVar()
        #
        self.Street = StringVar()
        self.City = StringVar()
        self.State = StringVar()
        self.Zip = StringVar()
        self.Timezone = StringVar()
        self.SavingTime = StringVar()
        self.Phone = StringVar()
        self.Latitude = DoubleVar()
        self.Longitude = DoubleVar()

    def load_vars(self, p_obj):
        """Load the variables for a given house.

        @param p_obj: is the house object in House_Data.
        """
        self.Active.set(self.get_bool(p_obj.Active))
        self.Key.set(p_obj.Key)
        self.HouseName = p_obj.Name
        self.Name.set(p_obj.Name)
        #
        l_obj = p_obj.Location[0]
        self.Street.set(l_obj.Street)
        self.City.set(l_obj.City)
        self.State.set(l_obj.State)
        self.Zip.set(l_obj.ZipCode)
        self.Timezone.set(l_obj.TimeZone)
        self.SavingTime.set(l_obj.SavingTime)
        self.Phone.set(l_obj.Phone)
        self.Latitude.set(l_obj.Latitude)
        self.Longitude.set(l_obj.Longitude)

    def get_vars(self):
        """Get the on screen vars and save them in the original house object.
        This will preserve the rest of the information.
        """
        l_obj = self.m_obj
        l_obj.Active = self.Active.get()
        l_obj.Key = self.Key.get()
        l_obj.Name = self.Name.get()
        #
        l_obj.Location[0] = LocationData()
        l_obj.Location[0].Street = self.Street.get()
        l_obj.Location[0].City = self.City.get()
        l_obj.Location[0].State = self.State.get()
        l_obj.Location[0].ZipCode = self.Zip.get()
        l_obj.Location[0].TimeZone = self.Timezone.get()
        l_obj.Location[0].SavingTime = self.SavingTime.get()
        l_obj.Location[0].Phone = self.Phone.get()
        l_obj.Location[0].Latitude = self.Latitude.get()
        l_obj.Location[0].Longitude = self.Longitude.get()
        return l_obj

class RoomDialog(gui_tools.GuiTools, HouseUtils):
    """
    Add / edit / delete dialog window for a room.

    TODO: Fix this section to preserve the lights and schedule data within a house.
    """

    def __init__(self, p_parent, p_key, p_house_name, p_title = None):
        """

        @param p_parent: is the parent frame that this dialog comes from.
        @param p_key: is the room key(index)
        @param p_house_name: is the name of the house
        @param p_title: is the title of the dialog to be shown.
        """
        self.m_top = Toplevel(p_parent)
        if p_title:
            self.m_top.title(p_title)
        self.m_parent = p_parent
        self.l_result = None
        self.create_vars()
        l_obj = self.get_house_object(p_key)
        self.load_vars(l_obj, p_house_name)
        self.m_frame = Frame(self.m_top)
        self.m_frame.grid(padx = 5, pady = 5)
        self.get_entry_str(self.m_frame, 1, 'Key', self.Key, state = DISABLED)
        self.get_entry_bol(self.m_frame, 2, 'Active', self.Active)
        self.get_entry_str(self.m_frame, 3, 'Name', self.Name, width = 50)
        self.get_entry_str(self.m_frame, 4, 'Comment', self.Comment, width = 50)
        self.get_entry_str(self.m_frame, 5, 'Size', self.Size)
        self.get_entry_str(self.m_frame, 6, 'Corner', self.Corner)
        self.get_entry_str(self.m_frame, 7, 'House Name', self.HouseName, state = DISABLED)
        l_text = "Add"
        if p_title.startswith("Edit"):
            l_text = "Save"
            self.get_entry_btn(self.m_frame, 91, 1, 'Delete', self.delete_room, bg = gui_tools.BG_BOTTOM)
        self.get_entry_btn(self.m_frame, 91, 0, l_text, self.add_save_room, fg = "blue", bg = gui_tools.BG_BOTTOM)
        self.get_entry_btn(self.m_frame, 91, 2, "Cancel", self.quit_room, fg = "red", bg = gui_tools.BG_BOTTOM)

    def delete_room(self):
        l_key = self.Key.get()
        del Room_Data[l_key]
        config_xml.WriteConfig().write_houses()
        self.quit_room()

    def add_save_room(self):
        """store the new or edited room.
        """
        l_obj = self.get_vars()
        Room_Data[l_obj.Key] = l_obj
        config_xml.WriteConfig().write_houses()
        self.quit_room()

    def quit_room(self):
        self.m_top.destroy()

    def create_vars(self):
        self.Active = IntVar()
        self.Comment = StringVar()
        self.Corner = StringVar()
        self.HouseName = StringVar()
        self.Key = IntVar()
        self.Name = StringVar()
        self.Size = StringVar()

    def load_vars(self, p_obj):
        l_obj = p_obj.Rooms
        self.Active.set(l_obj.Active)
        self.Comment.set(l_obj.Comment)
        self.Corner.set(l_obj.Corner)
        self.HouseName.set(p_obj.Name)
        self.Key.set(l_obj.Key)
        self.Name.set(l_obj.Name)
        self.Size.set(l_obj.Size)

    def get_vars(self):
        l_obj = house.RoomData()
        l_obj.Active = self.Active.get()
        l_obj.Comment = self.Comment.get()
        l_obj.Corner = self.Corner.get()
        l_obj.HouseName = self.HouseName.get()
        l_obj.Key = self.Key.get()
        l_obj.Name = self.Name.get()
        l_obj.Size = self.Size.get()
        return l_obj

# ## END
