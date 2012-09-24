#!/usr/bin/env python

from Tkinter import *
import Pmw


class ActiveBox(object):
    """An active radiobutton box that supplies 0/1.
    """
    def __init__(self, p_parent, p_var):
        l_frame = Frame(p_parent)
        Radiobutton(l_frame, text = "Yes", variable = p_var, value = 1).grid(row = 0, column = 0)
        Radiobutton(l_frame, text = "No", variable = p_var, value = 0).grid(row = 0, column = 1)
        #return l_frame

    
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

    def yes_no_radio(self, p_frame, p_var):
        _l_entry = int(p_var.get())
        #print "Creating Y/N buttons with value {0:} <{1:}>".format(p_var, l_entry)
        l_frame = Frame(p_frame)
        Radiobutton(l_frame, text = "Yes", variable = p_var, value = True).grid(row = 0, column = 0)
        Radiobutton(l_frame, text = "No", variable = p_var, value = False).grid(row = 0, column = 1)
        return l_frame

    def frame_delete(self, p_frame):
        try:
            p_frame.grid_forget()
        except:
            pass

    def get_bool(self, p_arg):
        l_ret = False
        if p_arg == 'True': l_ret = True
        return l_ret

    def pulldown_box(self, p_parent, p_list, p_sel):
        """Create a Pmw combo pulldown box.

        @param p_parent: the parent container / frame
        @param p_list: a list of the items for the box
        @param p_sel: the selection to be used
        @return: widget to be positioned in container.
        """
        l_entry = str(p_sel.get())
        #print "debug pulldown_box ", p_list, l_entry
        l_box = Pmw.ComboBox(p_parent,
                    scrolledlist_items = p_list,
                    )
        try:
            l_sel = p_list.index(l_entry)
            print "index = ", l_sel
        except ValueError:
            l_sel = p_list[0]
        l_box.selectitem(l_sel)
        return l_box


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
        l_id = self._id
        self._id = None
        if l_id:
            self.master.after_cancel(l_id)

    def _show(self):
        if self._opts['state'] == 'disabled':
            self._unschedule()
            return
        if not self._tipwindow:
            self._tipwindow = tw = Toplevel(self.master)
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
        label = Label(self._tipwindow, **opts)
        label.pack()

##---------demo code-----------------------------------##

def demo():
    root = Tk(className='ToolTip-demo')
    l = Listbox(root)
    l.insert('end', "I'm a listbox")
    l.pack(side='top')
    _t1 = ToolTip(l, follow_mouse=1, text="I'm a tooltip with follow_mouse set to 1, so I won't be placed outside my parent")
    b = Button(root, text='Quit', command=root.quit)
    b.pack(side='bottom')
    _t2 = ToolTip(b, text='Enough of this')
    root.mainloop()

if __name__ == '__main__':
    demo()    

### END
