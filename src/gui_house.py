#!/usr/bin/env python

from Tkinter import *

import gui
import gui_tools
import house
import config_xml

Location_Data = house.Location_Data

class HouseWindow(gui_tools.GuiTools):
    """
    Displays all defined houses and handles house add/change/delete.
    """

    def __init__(self, p_root):
        self.m_frame = Frame(p_root)
        self.m_ix = 0
        self.m_frame.grid()
        self.show_all_houses()
        self.house_button = Button(self.m_frame, text = "ADD New House", command = self.add_house)
        self.house_button.grid(row = self.m_ix, column = 0)
        self.button = Button(self.m_frame, text = "Back", fg = "red", command = self.main_screen)
        self.button.grid(row = self.m_ix, column = 1)
        #status = gui.StatusBar(p_root)
        #status.grid()

    def show_all_houses(self):
        l_house = []
        self.m_max = 0
        for l_obj in Location_Data.itervalues():
            if l_obj.Key > self.m_max:
                self.m_max = l_obj.Key
            #print l_obj.Name, l_obj.Key
            h = Button(self.m_frame, text = l_obj.Name, command = lambda x = l_obj.Key: self.edit_house(x))
            l_house.append(h)
            l_house[self.m_ix].grid(row = self.m_ix)
            self.m_ix += 1
        self.m_ix += 2

    def add_house(self):
        print "Add house"
        d = HouseDialog(self.m_frame, self.m_ix, "Adding House")

    def edit_house(self, p_key):
        d = HouseDialog(self.m_frame, p_key, "Editing House")

    def main_screen(self):
        self.frame_delete(self.m_frame)
        m = gui.MainWindow()



class HouseDialog(gui_tools.GuiTools):
    """
    Add / edit / delete dialog window for a house.
    """

    def __init__(self, p_parent, p_key, p_title = None):
        self.m_top = Toplevel(p_parent)
        if p_title:
            self.m_top.title(p_title)
        self.m_parent = p_parent
        self.l_result = None
        self.create_vars()
        self.load_vars(p_key)
        self.m_frame = Frame(self.m_top)
        #self.initial_focus = self.body(self.m_frame)
        self.m_frame.grid(padx = 5, pady = 5)
        Label(self.m_frame, text = "Name").grid(row = 1, column = 0, sticky = E)
        self.m_name = Entry(self.m_frame, textvar = self.Name)
        self.m_name.grid(row = 1, column = 1)
        Label(self.m_frame, text = "Street").grid(row = 3, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Street).grid(row = 3, column = 1)
        Label(self.m_frame, text = "City").grid(row = 5, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.City).grid(row = 5, column = 1)
        Label(self.m_frame, text = "State").grid(row = 7, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.State).grid(row = 7, column = 1)
        Label(self.m_frame, text = "Zip Code").grid(row = 9, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Zip).grid(row = 9, column = 1)
        Label(self.m_frame, text = "Time Zone").grid(row = 11, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Timezone).grid(row = 11, column = 1)
        Label(self.m_frame, text = "Savings Time").grid(row = 13, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.SavingTime).grid(row = 13, column = 1)
        Label(self.m_frame, text = "Phone").grid(row = 15, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Phone).grid(row = 15, column = 1)
        Label(self.m_frame, text = "Latitude").grid(row = 17, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Latitude).grid(row = 17, column = 1)
        Label(self.m_frame, text = "Longitude").grid(row = 19, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Longitude).grid(row = 19, column = 1)
        Label(self.m_frame, text = "Active").grid(row = 21, column = 0, sticky = E)
        self.yes_no_radio(self.m_frame, self.Active).grid(row = 21, column = 1, sticky = W)
        Label(self.m_frame, text = "Key").grid(row = 23, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Key, state = DISABLED).grid(row = 23, column = 1)
        l_text = "Add"
        if p_title.startswith("Edit"):
            l_text = "Save"
            Button(self.m_frame, text = 'Delete', command = self.delete_house).grid(row = 91, column = 1)
        Button(self.m_frame, text = l_text, fg = "blue", command = self.add_house).grid(row = 91, column = 0)
        Button(self.m_frame, text = "Cancel", fg = "red", command = self.quit_dialog).grid(row = 91, column = 2)

    def delete_house(self):
        l_key = self.Key.get()
        del Location_Data[l_key]
        config_xml.WriteConfig().write_houses()
        self.quit_dialog()
    
    def quit_dialog(self):
        self.m_top.destroy()

    def create_vars(self):
        self.Active = IntVar()
        print "Created House Active in var {0:}".format(self.Active)
        self.Name = StringVar()
        self.Street = StringVar()
        self.City = StringVar()
        self.State = StringVar()
        self.Zip = StringVar()
        self.Timezone = StringVar()
        self.SavingTime = StringVar()
        self.Phone = StringVar()
        self.Latitude = DoubleVar()
        self.Longitude = DoubleVar()
        self.Key = IntVar()

    def add_house(self):
        l_obj = house.LocationData()
        l_obj.Name = self.Name.get()
        l_obj.Street = self.Street.get()
        l_obj.City = self.City.get()
        l_obj.State = self.State.get()
        l_obj.ZipCode = self.Zip.get()
        l_obj.TimeZone = self.Timezone.get()
        l_obj.SavingTime = self.SavingTime.get()
        l_obj.Phone = self.Phone.get()
        l_obj.Latitude = self.Latitude.get()
        l_obj.Longitude = self.Longitude.get()
        l_obj.Active = self.Active.get()
        print "Add House - Active={0:}".format(l_obj.Active)
        l_obj.Key = self.Key.get()
        Location_Data[l_obj.Key] = l_obj
        config_xml.WriteConfig().write_houses()
        self.quit_dialog()


    def load_vars(self, p_key):
        try:
            l_obj = Location_Data[p_key]
        except:
            l_obj = house.LocationData()
            l_obj.Key = p_key
        self.Name.set(l_obj.Name)
        print "Setting Active to {0:}".format(l_obj.Active)
        self.Active.set(self.get_bool(l_obj.Active))
        self.Street.set(l_obj.Street)
        self.City.set(l_obj.City)
        self.State.set(l_obj.State)
        self.Zip.set(l_obj.ZipCode)
        self.Timezone.set(l_obj.TimeZone)
        self.SavingTime.set(l_obj.SavingTime)
        self.Phone.set(l_obj.Phone)
        self.Latitude.set(l_obj.Latitude)
        self.Longitude.set(l_obj.Longitude)
        self.Key.set(l_obj.Key)



### END
