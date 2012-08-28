#!/usr/bin/env python

from Tkinter import *
from twisted.internet import tksupport

import house
import lighting


Location_Data = house.Location_Data
Light_Data = lighting.Light_Data
Button_Data = lighting.Button_Data
Controller_Data = lighting.Controller_Data


class MainWindow(object):
    """
    A dispatch window with status bar.
    """
    def __init__(self):
        self.m_frame = Frame(g_root)
        self.m_frame.grid()
        self.house_button = Button(self.m_frame, text = "House", command = self.house_screen)
        self.house_button.grid(row = 1, column = 2)
        self.lighting_button = Button(self.m_frame, text = "Lighting", command = self.lighting_screen)
        self.lighting_button.grid(row = 1, column = 4)
        self.button = Button(self.m_frame, text = "QUIT", fg = "red", command = self.main_quit)
        self.button.grid()
        status = StatusBar(g_root)
        status.grid()

    def house_screen(self):
        self.m_frame.grid_forget() # Main Window
        h = HouseWindow()

    def lighting_screen(self):
        self.m_frame.grid_forget() # Main Window
        h = LightingWindow()

    def main_quit(self):
        self.m_frame.grid_forget() # Main Window
        self.m_frame.destroy()


class HouseWindow(object):
    """
    Displays all defined houses and handles house add/change/delete.
    """

    def __init__(self):
        self.m_frame = Frame(g_root)
        self.m_ix = 0
        self.m_frame.grid()
        self.show_all_houses()
        self.house_button = Button(self.m_frame, text = "ADD New House", command = self.add_house)
        self.house_button.grid(row = self.m_ix, column = 0)
        self.button = Button(self.m_frame, text = "Back", fg = "red", command = self.main_screen)
        self.button.grid(row = self.m_ix, column = 1)
        status = StatusBar(g_root)
        status.grid()

    def main_screen(self):
        self.m_frame.grid_forget()
        self.m_frame.destroy()
        m = MainWindow()

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

    def edit_house(self, p_arg):
        print "Edit House", p_arg
        d = HouseDialog(self.m_frame, p_arg, "Editing House")



class HouseDialog(Toplevel):
    """
    Add / edit dialog window for a house.
    """

    def __init__(self, p_parent, p_key, p_title = None):
        Toplevel.__init__(self, p_parent)
        self.transient(p_parent)
        if p_title:
            self.title(p_title)
        self.m_parent = p_parent
        self.l_result = None

        self.create_vars()
        self.load_vars(p_key)

        self.m_frame = Frame(self)
        #self.initial_focus = self.body(self.m_frame)
        self.m_frame.grid(padx = 5, pady = 5)
        l_1 = Label(self.m_frame, text = "Name")
        l_1.grid(row = 1, column = 0)
        self.m_name = Entry(self.m_frame, textvar = self.Name)
        self.m_name.grid(row = 1, column = 1)
        l_2 = Label(self.m_frame, text = "Street")
        l_2.grid(row = 2, column = 0)
        l_street = Entry(self.m_frame, textvar = self.Street)
        l_street.grid(row = 2, column = 1)
        l_3 = Label(self.m_frame, text = "City")
        l_3.grid(row = 3, column = 0)
        l_city = Entry(self.m_frame, textvar = self.City)
        l_city.grid(row = 3, column = 1)
        l_4 = Label(self.m_frame, text = "State")
        l_4.grid(row = 4, column = 0)
        l_state = Entry(self.m_frame, textvar = self.State)
        l_state.grid(row = 4, column = 1)
        l_5 = Label(self.m_frame, text = "Zip Code")
        l_5.grid(row = 5, column = 0)
        l_zip = Entry(self.m_frame, textvar = self.Zip)
        l_zip.grid(row = 5, column = 1)
        l_6 = Label(self.m_frame, text = "Time Zone")
        l_6.grid(row = 6, column = 0)
        l_timezone = Entry(self.m_frame, textvar = self.Timezone)
        l_timezone.grid(row = 6, column = 1)
        l_7 = Label(self.m_frame, text = "Savings Time")
        l_7.grid(row = 7, column = 0)
        l_savings = self.yes_no_radio(self.m_frame, self.Savingstime)
        l_savings.grid(row = 7, column = 1)
        l_8 = Label(self.m_frame, text = "Phone")
        l_8.grid(row = 8, column = 0)
        l_phone = Entry(self.m_frame, textvar = self.Phone)
        l_phone.grid(row = 8, column = 1)
        l_9 = Label(self.m_frame, text = "Latitude")
        l_9.grid(row = 9, column = 0)
        l_latitude = Entry(self.m_frame, textvar = self.Latitude)
        l_latitude.grid(row = 9, column = 1)
        l_10 = Label(self.m_frame, text = "Longitude")
        l_10.grid(row = 10, column = 0)
        l_longitude = Entry(self.m_frame, textvar = self.Longitude)
        l_longitude.grid(row = 10, column = 1)
        l_11 = Label(self.m_frame, text = "Active")
        l_11.grid(row = 11, column = 0)
        l_active = self.yes_no_radio(self.m_frame, self.Active)
        l_active.grid(row = 11, column = 1)
        l_12 = Label(self.m_frame, text = "Key")
        l_12.grid(row = 12, column = 0)
        l_active = Entry(self.m_frame, textvar = self.Key, state = DISABLED)
        l_active.grid(row = 12, column = 1)

        #self.buttonbox()
        self.grab_set()

        self.add = Button(self.m_frame, text = "Add", fg = "blue", command = self.add_house)
        self.add.grid(row = 22, column = 0)
        self.quit = Button(self.m_frame, text = "Cancel", fg = "red", command = self.quit_dialog)
        self.quit.grid(row = 22, column = 1)
        status = StatusBar(g_root)
        status.grid()

    def quit_dialog(self):
        self.m_frame.grid_forget()
        self.m_frame.quit()

    def yes_no_radio(self, p_frame, p_var):
        l_frame = Frame(self.m_frame)
        l_yes = Radiobutton(l_frame, text = "Yes", variable = p_var, value = 'Y')
        l_yes.grid(row = 0, column = 0)
        l_no = Radiobutton(l_frame, text = "No", variable = p_var, value = 'N')
        l_no.grid(row = 0, column = 1)
        return l_frame

    def add_house(self):
        house.HouseAPI().dump_location()
        l_obj = house.LocationData()
        l_obj.Name = self.Name.get()
        l_obj.Street = self.Street.get()
        l_obj.City = self.City.get()
        l_obj.State = self.State.get()
        l_obj.ZipCode = self.Zip.get()
        l_obj.TimeZone = self.Timezone.get()
        l_obj.SavingTime = self.Savingstime.get()
        l_obj.Phone = self.Phone.get()
        l_obj.Latitude = self.Latitude.get()
        l_obj.Longitude = self.Longitude.get()
        l_obj.Active - self.Active.get()
        l_obj.Key = self.Key.get()
        Location_Data[l_obj.Key] = l_obj
        house.HouseAPI().dump_location()

    def create_vars(self):
        self.Name = StringVar()
        self.Street = StringVar()
        self.City = StringVar()
        self.State = StringVar()
        self.Zip = StringVar()
        self.Timezone = StringVar()
        self.Savingstime = StringVar()
        self.Phone = StringVar()
        self.Latitude = DoubleVar()
        self.Longitude = DoubleVar()
        self.Active = StringVar()
        self.Key = IntVar()

    def load_vars(self, p_key):
        try:
            l_obj = Location_Data[p_key]
        except:
            l_obj = house.LocationData()
            l_obj.Key = p_key

        self.Name.set(l_obj.Name)
        self.Street.set(l_obj.Street)
        self.City.set(l_obj.City)
        self.State.set(l_obj.State)
        self.Zip.set(l_obj.ZipCode)
        self.Timezone.set(l_obj.TimeZone)
        self.Savingstime.set(l_obj.SavingTime)
        self.Phone.set(l_obj.Phone)
        self.Latitude.set(l_obj.Latitude)
        self.Longitude.set(l_obj.Longitude)
        self.Active.set(l_obj.Active)
        self.Key.set(l_obj.Key)



class StatusBar(Frame):
    """
    Status bar.
    """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd = 1, relief = SUNKEN, anchor = W)
        self.label.grid()

    def set(self, format, *args):
        self.label.config(text = format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text = "")
        self.label.update_idletasks()


class LightingWindow(object):
    """
    """

    def __init__(self):
        self.m_frame = Frame(g_root)
        self.m_ix = 0
        self.m_frame.grid()
        self.show_all_lights()
        self.light_button = Button(self.m_frame, text = "ADD New Device", command = self.add_lights)
        self.light_button.grid(row = self.m_ix, column = 0)
        self.button = Button(self.m_frame, text = "Back", fg = "red", command = self.main_screen)
        self.button.grid(row = self.m_ix, column = 1)
        status = StatusBar(g_root)
        status.grid()

    def main_screen(self):
        self.m_frame.grid_forget()
        m = MainWindow()

    def show_all_lights(self):
        l_light = []
        for l_obj in Light_Data.itervalues():
            print l_obj.Name, l_obj.Key
            l = Button(self.m_frame, text = l_obj.Name,
                       command = lambda x = l_obj.Key: self.edit_lights(x))
            l_light.append(l)
            l_row = self.m_ix // 4
            l_col = self.m_ix % 4
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        for l_obj in Controller_Data.itervalues():
            c = Button(self.m_frame, fg = "red", text = l_obj.Name,
                       command = lambda x = l_obj.Key: self.edit_controllers(x))
            l_light.append(c)
            l_row = self.m_ix // 4
            l_col = self.m_ix % 4
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        for l_obj in Button_Data.itervalues():
            c = Button(self.m_frame, fg = "blue", text = l_obj.Name,
                       command = lambda x = l_obj.Key: self.edit_buttons(x))
            l_light.append(c)
            l_row = self.m_ix // 4
            l_col = self.m_ix % 4
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        self.m_ix += 2

    def edit_lights(self, p_arg):
        print "Edit lights", p_arg

    def edit_controllers(self, p_arg):
        print "Edit Controllers", p_args

    def edit_buttons(self, p_arg):
        print "Edit Buttons", p_args

    def add_lights(self):
        print "Adding lights"
        d = HouseDialog(self.m_frame, "Adding Lights")



global g_root
g_root = Tk()
tksupport.install(g_root)

app = MainWindow()

### END
