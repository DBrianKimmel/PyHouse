"""
-*- test-case-name: PyHouse.src.Modules.util.test.test_tools -*-

@name: PyHouse/src/Modules/utils/tools.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on Apr 11, 2013
@license: MIT License
@summary: Various functions and utility methods.

Various tools that can be imported.  Named differently for recognition.

"""

# Import system type stuff
from xml.etree import ElementTree as ET
from xml.dom import minidom


def PrettyPrintAny(p_any, p_title = ''):
    l_type = type(p_any)
    print('=== ', p_title, ' === ', l_type)
    if isinstance(p_any, dict):
        PrettyPrintDict(p_any)
    elif isinstance(p_any, ET.Element):
        PrettyPrintXML(p_any)
    else:
        print(' - - Type is - - {0:}'.format(l_type))
        PrettyPrintObject(p_any)
    print('---------------------------------')


def PrintBytes(p_message):
    """Print all the bytes of a message as hex bytes.
    """
    l_len = len(p_message)
    l_message = ''
    if l_len == 0:
        l_message = "<NONE>"
    else:
        for l_x in range(l_len):
            try:
                l_message += " {0:#04x}".format(int(p_message[l_x]))
            except ValueError:
                try:
                    l_message += " {0:#04X}".format(ord(p_message[l_x]))
                except TypeError:  # Must be a string
                    l_message += " {0:} ".format(p_message[l_x])
    l_message += " <END>"
    return l_message


def PrettyPrintCols(strings, widths, split = ' '):
    """Pretty prints text in colums, with each string breaking at
    split according to prettyPrint.  margins gives the corresponding
    right breaking point.
    """
    assert len(strings) == len(widths)
    strings = map(nukenewlines, strings)
    # pretty Print each column
    cols = [''] * len(strings)
    for i in range(len(strings)):
        cols[i] = prettyPrint(strings[i], widths[i], split)
    # prepare a format line
    l_format = ''.join(["%%-%ds" % width for width in widths[0:-1]]) + "%s"
    def formatline(*cols):
        return l_format % tuple(map(lambda s: (s or ''), cols))
    # generate the formatted text
    return '\n'.join(map(formatline, *cols))

def PrettyPrintDict(p_dict, p_format = "%-25s %s"):
    for (key, val) in p_dict.iteritems():
        print(p_format % (str(key) + ':', val))


def PrettyPrintObject(p_obj, maxlen = 180, lindent = 24, maxspew = 2000):
    def truncstring(s, maxlen):
        if len(s) > maxlen:
            return s[0:maxlen] + ' ...(%d more chars)...' % (len(s) - maxlen)
        else:
            return s
    l_tab = 2
    l_attrs = []
    l_tabbedwidths = [l_tab, lindent - l_tab, maxlen - lindent - l_tab]
    l_filtered = filter(lambda aname: not aname.startswith('__'), dir(p_obj))
    # for l_slot in dir(p_obj):
    for l_slot in l_filtered:
        l_attr = getattr(p_obj, l_slot)
        l_attrs.append((l_slot, l_attr))
    l_attrs.sort()
    for (attr, l_val) in l_attrs:
        print(PrettyPrintCols(('', attr, truncstring(str(l_val), maxspew)), l_tabbedwidths, ' '))


def PrettyPrintXML(p_element):
    """Return a pretty-printed XML string for the Element.

    @param p_element: an element to format as a readable XML tree.
    @return: a string formatted with indentation and newlines.
    """
    l_rough_string = ET.tostring(p_element, 'utf-8')
    l_reparsed = minidom.parseString(l_rough_string)
    l_doc = l_reparsed.toprettyxml(indent = "    ")
    l_lines = l_doc.splitlines()
    for l_line in l_lines:
        if not l_line.isspace():
            print l_line


#######################################

def PrettyPrint(p_title, p_str, maxlen = 150):
    print('Title: {0:}\n'.format(p_title), '\n'.join(prettyPrint(str(p_str), maxlen, ' ')))

def PrintObject(p_title, p_obj, suppressdoc = True, maxlen = 180, lindent = 24, maxspew = 2000):
    """Print a nicely formatted overview of an object.

    The output lines will be wrapped at maxlen, with lindent of space
    for names of attributes.  A maximum of maxspew characters will be
    printed for each attribute value.

    You can hand dumpObj any data type -- a module, class, instance,
    new class.

    Note that in reformatting for compactness the routine trashes any
    formatting in the docstrings it prints.

    Example:
       >>> class Foo(object):
               a = 30
               def bar(self, b):
                   "A silly method"
                   return a*b
       ... ... ... ...
       >>> foo = Foo()
       >>> dumpObj(foo)
       Instance of class 'Foo' as defined in module __main__ with id 136863308
       Documentation string:   None
       Built-in Methods:       __delattr__, __getattribute__, __hash__, __init__
                               __new__, __reduce__, __repr__, __setattr__,
                               __str__
       Methods:
         bar                   "A silly method"
       Attributes:
         __dict__              {}
         __weakref__           None
         a                     30
    """

    import types
    # Formatting parameters.
    ltab = 2  # initial tab in front of level 2 text
    # There seem to be a couple of other types; gather templates of them
    MethodWrapperType = type(object().__hash__)
    #
    # Gather all the attributes of the object
    objclass = None
    objdoc = None
    objmodule = '<None defined>'
    methods = []
    builtins = []
    classes = []
    attrs = []
    for slot in dir(p_obj):
        attr = getattr(p_obj, slot)
        if   slot == '__class__':
            objclass = attr.__name__
        elif slot == '__doc__':
            objdoc = attr
        elif slot == '__module__':
            objmodule = attr
        elif (isinstance(attr, types.BuiltinMethodType) or isinstance(attr, MethodWrapperType)):
            builtins.append(slot)
        elif (isinstance(attr, types.MethodType) or isinstance(attr, types.FunctionType)):
            methods.append((slot, attr))
        elif isinstance(attr, types.TypeType):
            classes.append((slot, attr))
        else:
            attrs.append((slot, attr))
    # Organize them
    methods.sort()
    builtins.sort()
    classes.sort()
    attrs.sort()
    # Print a readable summary of those attributes
    normalwidths = [lindent, maxlen - lindent]
    tabbedwidths = [ltab, lindent - ltab, maxlen - lindent - ltab]

    def truncstring(s, maxlen):
        if len(s) > maxlen:
            return s[0:maxlen] + ' ...(%d more chars)...' % (len(s) - maxlen)
        else:
            return s

    # Summary of introspection attributes
    if objclass == '':
        objclass = type(p_obj).__name__
    intro = "\nInstance of class '{0:}' as defined in module {1:} with id {2:}".format(objclass, objmodule, id(p_obj))
    print('\nTitle:  ', p_title, '\n'.join(prettyPrint(intro, maxlen)))
    # Object's Docstring
    if not suppressdoc:
        if objdoc is None:
            objdoc = str(objdoc)
        else:
            objdoc = ('"""' + objdoc.strip() + '"""')
        print
        print(PrettyPrintCols(('Documentation string:', truncstring(objdoc, maxspew)), normalwidths, ' '))
    # Built-in methods
    if builtins:
        bi_str = delchars(str(builtins), "[']") or str(None)
        print
        print(PrettyPrintCols(('Built-in Methods:', truncstring(bi_str, maxspew)), normalwidths, ', '))
    # Classes
    if classes:
        print
        print('Classes:')
    for (classname, classtype) in classes:
        classdoc = getattr(classtype, '__doc__', None) or '<No documentation>'
        if suppressdoc:
            classdoc = '<No documentation>'
        print(PrettyPrintCols(('', classname, truncstring(classdoc, maxspew)), tabbedwidths, ' '))
    # User methods
    if methods:
        print
        print('Methods:')
    for (methodname, method) in methods:
        methoddoc = getattr(method, '__doc__', None) or '<No documentation>'
        if suppressdoc:
            methoddoc = '<No documentation>'
        print(PrettyPrintCols(('', methodname, truncstring(methoddoc, maxspew)), tabbedwidths, ' '))
    # Attributes
    if attrs:
        print
        print('Attributes:')
    for (attr, val) in attrs:
        print(PrettyPrintCols(('', attr, truncstring(str(val), maxspew)), tabbedwidths, ' '))
    print('====================\n')

def prettyPrint(string, maxlen = 175, split = ' '):
    """Pretty prints the given string to break at an occurrence of
    split where necessary to avoid lines longer than maxlen.

    This will overflow the line if no convenient occurrence of split
    is found"""
    # Tack on the splitting character to guarantee a final match
    string += split
    lines = []
    oldeol = 0
    eol = 0
    while not (eol == -1 or eol == len(string) - 1):
        eol = string.rfind(split, oldeol, oldeol + maxlen + len(split))
        lines.append(string[oldeol:eol])
        oldeol = eol + len(split)
    return lines

def nukenewlines(string):
    """Strip newlines and any trailing/following whitespace; rejoin
    with a single space where the newlines were.

    Bug: This routine will completely butcher any whitespace-formatted
    text."""
    if not string: return ''
    lines = string.splitlines()
    return ' '.join([line.strip() for line in lines])

def delchars(p_str, chars):
    """Returns a string for which all occurrences of characters in
    chars have been removed."""
    # Translate demands a mapping string of 256 characters;
    # whip up a string that will leave all characters unmolested.
    identity = ''.join([chr(x) for x in range(256)])
    return p_str.translate(identity, chars)


class Lister():

    def __repr__(self):
        return ("Lister:: <Instance of {0:}, Address {1:}:\n{2:}>\n".format(self.__class__.__name__, id(self), self.attrnames()))

    def attrnames(self):
        l_ret = ''
        for attr in self.__dict__.keys():
            if attr[:2] == '__':
                l_ret = l_ret + "\tName: {0:}=<built-in>\n".format(attr)
            else:
                l_ret = l_ret + "\tName: {0:}={1:}\n".format(attr, self.__dict__ [attr])
        return l_ret

def get_light_object(p_house, name = None, key = None):
    """return the light object for a given house using the given value.

    @param p_house: is the house object that contains the lights
    @return: the Light object found or None.
    """
    l_lights = p_house.Lights
    if name != None:
        for l_obj in l_lights.itervalues():
            if l_obj.Name == name:
                return l_obj
    elif key != None:
        for l_obj in l_lights.itervalues():
            if l_obj.Key == key:
                return l_obj
        return None


__all__ = [
           'PrettyPrintAny',
           'PrettyPrintCols',
           'PrettyPrintObject',
           'PrettyPrintXML'
           ]


# ## END DBK
