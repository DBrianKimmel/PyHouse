#!/usr/bin/env python

from Tkinter import *
from twisted.internet import tksupport

import house
import lighting
import config_xml


Location_Data = house.Location_Data
Light_Data = lighting.Light_Data
Button_Data = lighting.Button_Data
Controller_Data = lighting.Controller_Data


class GuiTools(object):

    def columnize(self, p_count, p_cols = 4):
        l_row = p_count // p_cols
        l_col = p_count % p_cols
        return l_row, l_col

    def make_label(self, p_name):
        l_ret = Label(self.m_frame, text = p_name).grid(column = 0)
        return l_ret

    def make_entry_line(self, p_parent, p_label, p_field):
        l_1 = Label(p_parent, text = p_label)
        l_1.grid(row = 1, column = 0)
        self.m_name = Entry(p_parent, textvar = self.Name)
        self.m_name.grid(row = 1, column = 1)
        return 


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
        #house.HouseAPI().dump_location()
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
        #l_obj.Active - self.Active.get()
        l_obj.Key = self.Key.get()
        Location_Data[l_obj.Key] = l_obj
        house.HouseAPI().dump_location()
        config_xml.WriteConfig().write_houses()


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
            #print l_obj.Name, l_obj.Key
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
            b = Button(self.m_frame, fg = "blue", text = l_obj.Name,
                       command = lambda x = l_obj.Key: self.edit_buttons(x))
            l_light.append(b)
            l_row = self.m_ix // 4
            l_col = self.m_ix % 4
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        self.m_ix += 2

    def edit_lights(self, p_arg):
        print "Edit lights", p_arg
        d = LightingDialog(self.m_frame, "Editing Light")
        config_xml.WriteConfig().write_lights()

    def edit_controllers(self, p_arg):
        print "Edit Controllers", p_arg
        d = LightingDialog(self.m_frame, "Adding Controller")
        config_xml.WriteConfig().write_lights()

    def edit_buttons(self, p_arg):
        print "Edit Buttons", p_arg
        d = LightingDialog(self.m_frame, "Adding Button")
        config_xml.WriteConfig().write_lights()

    def add_lights(self):
        print "Adding lights"
        d = LightingDialog(self.m_frame, "Adding Lights")
        config_xml.WriteConfig().write_lights()


class LightingDialog(Toplevel, GuiTools):
    """
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

    def create_vars(self):
        self.Name = StringVar()
        self.Family = StringVar()
        self.Active = IntVar()
        self.Comment = StringVar()
        self.Key = IntVar()
        self.Type = StringVar()

    def load_vars(self, p_key):
        pass


global g_root
g_root = Tk()
tksupport.install(g_root)

app = MainWindow()

### END
'''Michael Lange <klappnase (at) freakmail (dot) de>
The ToolTip class provides a flexible tooltip widget for Tkinter; it is based on IDLE's ToolTip
module which unfortunately seems to be broken (at least the version I saw).
INITIALIZATION OPTIONS:
anchor :        where the text should be positioned inside the widget, must be on of "n", "s", "e", "w", "nw" and so on;
                default is "center"
bd :            borderwidth of the widget; default is 1 (NOTE: don't use "borderwidth" here)
bg :            background color to use for the widget; default is "lightyellow" (NOTE: don't use "background")
delay :         time in ms that it takes for the widget to appear on the screen when the mouse pointer has
                entered the parent widget; default is 1500
fg :            foreground (i.e. text) color to use; default is "black" (NOTE: don't use "foreground")
follow_mouse :  if set to 1 the tooltip will follow the mouse pointer instead of being displayed
                outside of the parent widget; this may be useful if you want to use tooltips for
                large widgets like listboxes or canvases; default is 0
font :          font to use for the widget; default is system specific
justify :       how multiple lines of text will be aligned, must be "left", "right" or "center"; default is "left"
padx :          extra space added to the left and right within the widget; default is 4
pady :          extra space above and below the text; default is 2
relief :        one of "flat", "ridge", "groove", "raised", "sunken" or "solid"; default is "solid"
state :         must be "normal" or "disabled"; if set to "disabled" the tooltip will not appear; default is "normal"
text :          the text that is displayed inside the widget
textvariable :  if set to an instance of Tkinter.StringVar() the variable's value will be used as text for the widget
width :         width of the widget; the default is 0, which means that "wraplength" will be used to limit the widgets width
wraplength :    limits the number of characters in each line; default is 150

WIDGET METHODS:
configure(**opts) : change one or more of the widget's options as described above; the changes will take effect the
                    next time the tooltip shows up; NOTE: follow_mouse cannot be changed after widget initialization

Other widget methods that might be useful if you want to subclass ToolTip:
enter() :           callback when the mouse pointer enters the parent widget
leave() :           called when the mouse pointer leaves the parent widget
motion() :          is called when the mouse pointer moves inside the parent widget if follow_mouse is set to 1 and the
                    tooltip has shown up to continually update the coordinates of the tooltip window
coords() :          calculates the screen coordinates of the tooltip window
create_contents() : creates the contents of the tooltip window (by default a Tkinter.Label)
'''
# Ideas gleaned from PySol

import Tkinter

class ToolTip:
    def __init__(self, master, text='Your text here', delay=1500, **opts):
        self.master = master
        self._opts = {'anchor':'center', 'bd':1, 'bg':'lightyellow', 'delay':delay, 'fg':'black',\
                      'follow_mouse':0, 'font':None, 'justify':'left', 'padx':4, 'pady':2,\
                      'relief':'solid', 'state':'normal', 'text':text, 'textvariable':None,\
                      'width':0, 'wraplength':150}
        self.configure(**opts)
        self._tipwindow = None
        self._id = None
        self._id1 = self.master.bind("<Enter>", self.enter, '+')
        self._id2 = self.master.bind("<Leave>", self.leave, '+')
        self._id3 = self.master.bind("<ButtonPress>", self.leave, '+')
        self._follow_mouse = 0
        if self._opts['follow_mouse']:
            self._id4 = self.master.bind("<Motion>", self.motion, '+')
            self._follow_mouse = 1
    
    def configure(self, **opts):
        for key in opts:
            if self._opts.has_key(key):
                self._opts[key] = opts[key]
            else:
                KeyError = 'KeyError: Unknown option: "%s"' %key
                raise KeyError
    
    ##----these methods handle the callbacks on "<Enter>", "<Leave>" and "<Motion>"---------------##
    ##----events on the parent widget; override them if you want to change the widget's behavior--##
    
    def enter(self, event=None):
        self._schedule()
        
    def leave(self, event=None):
        self._unschedule()
        self._hide()
    
    def motion(self, event=None):
        if self._tipwindow and self._follow_mouse:
            x, y = self.coords()
            self._tipwindow.wm_geometry("+%d+%d" % (x, y))
    
    ##------the methods that do the work:---------------------------------------------------------##
    
    def _schedule(self):
        self._unschedule()
        if self._opts['state'] == 'disabled':
            return
        self._id = self.master.after(self._opts['delay'], self._show)

    def _unschedule(self):
        id = self._id
        self._id = None
        if id:
            self.master.after_cancel(id)

    def _show(self):
        if self._opts['state'] == 'disabled':
            self._unschedule()
            return
        if not self._tipwindow:
            self._tipwindow = tw = Tkinter.Toplevel(self.master)
            # hide the window until we know the geometry
            tw.withdraw()
            tw.wm_overrideredirect(1)

            if tw.tk.call("tk", "windowingsystem") == 'aqua':
                tw.tk.call("::tk::unsupported::MacWindowStyle", "style", tw._w, "help", "none")

            self.create_contents()
            tw.update_idletasks()
            x, y = self.coords()
            tw.wm_geometry("+%d+%d" % (x, y))
            tw.deiconify()
    
    def _hide(self):
        tw = self._tipwindow
        self._tipwindow = None
        if tw:
            tw.destroy()
                
    ##----these methods might be overridden in derived classes:----------------------------------##
    
    def coords(self):
        # The tip window must be completely outside the master widget;
        # otherwise when the mouse enters the tip window we get
        # a leave event and it disappears, and then we get an enter
        # event and it reappears, and so on forever :-(
        # or we take care that the mouse pointer is always outside the tipwindow :-)
        tw = self._tipwindow
        twx, twy = tw.winfo_reqwidth(), tw.winfo_reqheight()
        w, h = tw.winfo_screenwidth(), tw.winfo_screenheight()
        # calculate the y coordinate:
        if self._follow_mouse:
            y = tw.winfo_pointery() + 20
            # make sure the tipwindow is never outside the screen:
            if y + twy > h:
                y = y - twy - 30
        else:
            y = self.master.winfo_rooty() + self.master.winfo_height() + 3
            if y + twy > h:
                y = self.master.winfo_rooty() - twy - 3
        # we can use the same x coord in both cases:
        x = tw.winfo_pointerx() - twx / 2
        if x < 0:
            x = 0
        elif x + twx > w:
            x = w - twx
        return x, y

    def create_contents(self):
        opts = self._opts.copy()
        for opt in ('delay', 'follow_mouse', 'state'):
            del opts[opt]
        label = Tkinter.Label(self._tipwindow, **opts)
        label.pack()

##---------demo code-----------------------------------##

def demo():
    root = Tkinter.Tk(className='ToolTip-demo')
    l = Tkinter.Listbox(root)
    l.insert('end', "I'm a listbox")
    l.pack(side='top')
    t1 = ToolTip(l, follow_mouse=1, text="I'm a tooltip with follow_mouse set to 1, so I won't be placed outside my parent")
    b = Tkinter.Button(root, text='Quit', command=root.quit)
    b.pack(side='bottom')
    t2 = ToolTip(b, text='Enough of this')
    root.mainloop()

if __name__ == '__main__':
    demo()    
