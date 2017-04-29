"""
-*- test-case-name: PyHouse.src.Modules.Core.Utilities.test.test_tools -*-

@name:      PyHouse/src/Modules.Core.Utilities.tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@note:      Created on Apr 11, 2013
@license:   MIT License
@summary:   Various functions and utility methods.

Various tools that can be imported.  Named differently for recognition.

"""

__updated__ = '2017-04-26'


# Import system type stuff
from xml.etree import ElementTree as ET
from xml.dom import minidom

# Import PyMh files


def truncstring(s, maxlen=2000):
    if len(s) > maxlen:
        return s[0:maxlen] + ' ...(%d more chars)...' % (len(s) - maxlen)
    else:
        return s


# ======================================================================

def PrettyPrintCols(strings, widths, split=' '):
    """
    Pretty prints text in columns, with each string breaking at split according to _format_line.
    Margins gives the corresponding right breaking point.

    The first string is the title which is usually ''.

    The number of strings must match the number of widths.
    Each width is the width of a column with the last number is the total width.
    """
    assert len(strings) == len(widths)
    strings = map(_nukenewlines, strings)
    # pretty Print each column
    cols = [''] * len(strings)
    for i in range(len(strings)):
        cols[i] = _format_line(strings[i], widths[i], split)
    # prepare a format line
    l_format = ''.join(["%%-%ds" % width for width in widths[0:-1]]) + "%s"
    def formatline(*cols):
        return l_format % tuple(map(lambda s: (s or ''), cols))
    # generate the formatted text
    return '\n'.join(map(formatline, *cols))


#######################################

def PrettyPrint(p_title, p_str, maxlen=150):
    print('Title: {}\n'.format(p_title), '\n'.join(_format_line(str(p_str), maxlen, ' ')))

def PrintObject(p_title, p_obj, suppressdoc=True, maxlen=180, lindent=24, maxspew=2000):
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
    intro = "\nInstance of class '{}' as defined in module {} with id {}".format(objclass, objmodule, id(p_obj))
    print('\nTitle:  ', p_title, '\n'.join(_format_line(intro, maxlen)))
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
        bi_str = _delchars(str(builtins), "[']") or str(None)
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

def _format_line(string, maxlen=175, split=' '):
    """Pretty prints the given string to break at an occurrence of
    split where necessary to avoid lines longer than maxlen.

    This will overflow the line if no convenient occurrence of split is found.
    """
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

# def _split_long_lines(string, maxlen = 175):
#    l_lines = _format_line(string, maxlen)
#    return l_lines
#    return '--'.join(l_line for l_line in l_lines)

def _nukenewlines(string):
    """
    Strip newlines and any trailing/following whitespace;
    rejoin with a single space where the newlines were.

    Bug: This routine will completely butcher any whitespace-formatted text.
    """
    if not string: return ''
    lines = string.splitlines()
    return ' '.join([line.strip() for line in lines])

def _delchars(p_str, chars):
    """Returns a string for which all occurrences of characters in
    chars have been removed."""
    # Translate demands a mapping string of 256 characters;
    # whip up a string that will leave all characters unmolested.
    identity = ''.join([chr(x) for x in range(256)])
    return p_str.translate(identity, chars)


class Lister():

    def __repr__(self):
        return ("Lister:: <Instance of {}, Address {}:\n{}>\n".format(self.__class__.__name__, id(self), self.attrnames()))

    def attrnames(self):
        l_ret = ''
        for attr in self.__dict__.keys():
            if attr[:2] == '__':
                l_ret = l_ret + "\tName: {}=<built-in>\n".format(attr)
            else:
                l_ret = l_ret + "\tName: {}={}\n".format(attr, self.__dict__ [attr])
        return l_ret


__all__ = [
           'PrettyPrintCols',
           'PrettyPrintObject',
           'PrettyPrintXML'
           ]


# ## END DBK
