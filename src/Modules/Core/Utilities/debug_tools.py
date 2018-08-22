"""
@name:      PyHouse/src/Modules.Core.Utilities.debug_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 8, 2015
@Summary:

"""

__updated__ = '2018-08-13'

#  Import system type stuff
from xml.etree import ElementTree as ET
from xml.dom import minidom
# import pprint

#  Import PyMh files


def _trunc_string(s, maxlen=2000):
    if len(s) > maxlen:
        return s[0:maxlen]  # + ' ...(%d more chars)...' % (len(s) - maxlen)
    else:
        return s


def _nuke_newlines(p_string):
    """
    Strip newlines and any trailing/following whitespace;
    rejoin with a single space where the newlines were.

    Bug: This routine will completely butcher any whitespace-formatted text.
    """
    if not p_string:
        return ''
    l_lines = p_string.splitlines()
    return ' '.join([line.strip() for line in l_lines])


def _format_line(string, maxlen=175, split=' '):
    """
    Pretty prints the given string to break at an occurrence of
    split where necessary to avoid lines longer than maxlen.

    This will overflow the line if no convenient occurrence of split is found.
    @param string: is a string that will be broken up into several strings if needed.
    @param maxlen: is the maximum length of a string segment
    @param split: is the character around which the split will occur.
    @return: a list of string segments
    """
    #  Tack on the splitting character to guarantee a final match
    string += split
    linelist = []
    oldeol = 0
    eol = 0
    while not (eol == -1 or eol == len(string) - 1):
        eol = string.rfind(split, oldeol, oldeol + maxlen + len(split))
        linelist.append(string[oldeol:eol])
        oldeol = eol + len(split)
    return linelist


def _format_cols(strings, widths, split=' '):
    """
    Pretty prints text in columns, with each string breaking at split according to _format_line.
    Margins gives the corresponding right breaking point.

    The first string is the title which is usually ''.

    The number of strings must match the number of widths.
    Each width is the width of a column with the last number is the total width.
    @param strings: is a tuple of strings
    @param widths: is a tuple of integer column widths.  There must be the same number of widths as strings
    @return: the line of output with the strings left justified in the column width specified
    """
    assert len(strings) == len(widths)
    stringlist = list(map(_nuke_newlines, strings))
    #  pretty Print each column
    cols = [''] * len(stringlist)
    for i in range(len(stringlist)):
        cols[i] = _format_line(stringlist[i], widths[i], split)
    #  prepare a format line
    l_format = ''.join(["%%-%ds" % width for width in widths[0:-1]]) + "%s"

    def formatline(*cols):
        return l_format % tuple(map(lambda s: (s or ''), cols))

    #  generate the formatted text
    return '\n'.join(map(formatline, *cols))


def _formatObject(p_title, p_obj, suppressdoc=True, maxlen=180, lindent=24, maxspew=2000):
    """Print a nicely formatted overview of an object.

    The output lines will be wrapped at maxlen, with lindent of space
    for names of attributes.  A maximum of maxspew characters will be
    printed for each attribute value.

    You can hand formatObj any data type -- a module, class, instance,
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
    l_output = ''
    #  Formatting parameters.
    ltab = 2  #  initial tab in front of level 2 text
    #  There seem to be a couple of other types; gather templates of them
    MethodWrapperType = type(object().__hash__)
    #
    #  Gather all the attributes of the object
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
#        elif isinstance(attr, types.TypeType):
#            classes.append((slot, attr))
        else:
            attrs.append((slot, attr))
    #  Organize them
    methods.sort()
    builtins.sort()
    classes.sort()
    attrs.sort()
    #  Print a readable summary of those attributes
    normalwidths = [lindent, maxlen - lindent]
    tabbedwidths = [ltab, lindent - ltab, maxlen - lindent - ltab]

    #  def truncstring(s, maxlen):
    #    if len(s) > maxlen:
    #        return s[0:maxlen] + ' ...(%d more chars)...' % (len(s) - maxlen)
    #    else:
    #        return s

    #  Summary of introspection attributes
    if objclass == '':
        objclass = type(p_obj).__name__
    intro = "\nInstance of class '{}' as defined in module '{}' with id '{}'".format(objclass, objmodule, id(p_obj))
    l_output += '\nTitle:  {} {}'.format(p_title, '\n'.join(_format_line(intro, maxlen)))
    #  Object's Docstring
    if not suppressdoc:
        if objdoc is None:
            objdoc = str(objdoc)
        else:
            objdoc = ('"""' + objdoc.strip() + '"""')
        l_output += '\n'
        l_output += _format_cols(('Documentation string: ', _trunc_string(objdoc, maxspew)), normalwidths, ' ')
    #  Built-in methods
    if builtins:
        bi_str = _delchars(str(builtins), "[']") or str(None)
        l_output += '\n'
        l_output += _format_cols(('Built-in Methods: ', _trunc_string(bi_str, maxspew)), normalwidths, ', ')
    #  Classes
    if classes:
        l_output += '\nClasses'
    for (classname, classtype) in classes:
        classdoc = getattr(classtype, '__doc__', None) or '<No documentation>'
        if suppressdoc:
            classdoc = '<No documentation>'
        l_output += _format_cols(('Class: ', classname, _trunc_string(classdoc, maxspew)), tabbedwidths, ' ')
    #  User methods
    if methods:
        l_output += '\nMethods'
    for (methodname, method) in methods:
        methoddoc = getattr(method, '__doc__', None) or '<No documentation>'
        if suppressdoc:
            methoddoc = '<No documentation>'
        l_output += _format_cols(('Method: ', methodname, _trunc_string(methoddoc, maxspew)), tabbedwidths, ' ')
    #  Attributes
    if attrs:
        l_output += '\nAttributes'
    for (attr, val) in attrs:
        l_output += _format_cols(('Attr: ', attr, _trunc_string(str(val), maxspew)), tabbedwidths, ' ')
        l_output += '\n'
    l_output += '\n====================\n'
    return l_output


def PrettyFormatObject(p_obj, p_title, suppressdoc=True, maxlen=180, lindent=24, maxspew=2000):
    _formatObject(p_title, p_obj, suppressdoc, maxlen, lindent, maxspew)


class PrettyFormatAny(object):
    """
    """

    @staticmethod
    def form(p_any, title='No Title Given', maxlen=120):
        """ Top level call PrettyFormatAmy(form(obj, Title, MaxLineLen)
        """
        l_indent = 0
        l_type = type(p_any)
        l_ret = '\n===== {} ===== {}\n'.format(title, l_type)
        l_ret += PrettyFormatAny._type_dispatcher(p_any, maxlen, l_indent) + '\n'
        return l_ret

    @staticmethod
    def _type_dispatcher(p_any, maxlen, indent):
        """ We have the following dispatch to pretty up the things we want to see.

        The default is to print a generic object of some sort.
        """
        if isinstance(p_any, dict):
            l_ret = PrettyFormatAny._format_dict(p_any, maxlen=maxlen, indent=indent)
        elif isinstance(p_any, ET.Element):
            l_ret = PrettyFormatAny._format_XML(p_any, maxlen=maxlen, indent=indent)
        elif isinstance(p_any, str):
            l_ret = PrettyFormatAny._format_string(p_any, maxlen=maxlen, indent=indent)
        elif isinstance(p_any, type(str)):
            l_ret = PrettyFormatAny._format_unicode(p_any, maxlen=maxlen, indent=indent)
        elif isinstance(p_any, bytearray):
            l_ret = PrettyFormatAny._format_bytearray(p_any, maxlen=maxlen, indent=indent)
        elif isinstance(p_any, list):
            l_ret = PrettyFormatAny._format_list(p_any, maxlen=maxlen, indent=indent + 4)
        elif isinstance(p_any, tuple):
            l_ret = PrettyFormatAny._format_tuple(p_any, maxlen=maxlen, indent=indent + 4)
        elif isinstance(p_any, type(None)):
            l_ret = PrettyFormatAny._format_none(p_any)
        else:  #  Default to an object
            l_ret = PrettyFormatAny._format_object(p_any, maxlen=maxlen, indent=indent)
        l_ret += '---------------------------------'
        return l_ret

    @staticmethod
    def _format_string(p_obj, maxlen, indent):
        l_ret = _format_cols(('String: ', p_obj), [indent, maxlen - indent], ' ') + '\n'
        return l_ret

    @staticmethod
    def _format_unicode(p_obj, maxlen, indent):
        l_ret = _format_cols(('Unicode: ', p_obj), [indent, maxlen - indent], ' ') + '\n'
        return l_ret

    @staticmethod
    def _format_bytearray(p_obj, maxlen, indent):

        l_str = FormatBytes(p_obj)
        l_ret = _format_cols(('Bytearray: ', l_str), [indent, maxlen - indent], ' ') + '\n'
        return l_ret

    @staticmethod
    def _format_dict(p_dict, maxlen, indent):
        l_ret = ''
        l_tabbedwidths = [indent, 30, maxlen - 30]
        # l_tabbedwidths = [indent, maxlen - 30]
        for l_key, l_val in p_dict.items():
            if isinstance(l_val, dict):
                # l_ret += '_d_' + _format_cols(('\t', str(l_key), PrettyFormatAny._type_dispatcher(l_val, maxlen, indent + 4)), l_tabbedwidths, ' ') + '\n'
                l_ret += ' ' + _format_cols(('> ', str(l_key), PrettyFormatAny._type_dispatcher(l_val, maxlen, indent + 4)), l_tabbedwidths, ' ') + '\n'
            else:
                # l_ret += '_ _' + _format_cols(('\t', str(l_key), str(l_val)), l_tabbedwidths, ' ') + '\n'
                # l_ret += '_'   + _format_cols((str(l_key), str(l_val)), l_tabbedwidths, ' ') + '\n'
                l_ret += ' ' + _format_cols(('. ', str(l_key), str(l_val)), l_tabbedwidths, ' ') + '\n'
        return l_ret

    @staticmethod
    def _format_XML(p_element, maxlen, indent):
        """Return a pretty-printed XML string for the Element.

        @param p_element: an element to format as a readable XML tree.
        @return: a string formatted with indentation and newlines.
        """
        l_ret = ''
        _l_tabbedwidths = [indent, 30, maxlen - 30]
        l_rough_string = ET.tostring(p_element, 'utf-8')
        try:
            l_reparsed = minidom.parseString(l_rough_string)
        except Exception as e_err:
            l_ret = 'Error {}\n{}'.format(e_err, l_rough_string)
            return l_ret
        l_doc = l_reparsed.toprettyxml()
        l_lines = l_doc.splitlines()
        for l_line in l_lines:
            if not l_line.isspace():
                l_list = _format_line(l_line, maxlen=maxlen)
                for l_line in l_list:
                    l_ret += l_line + '\n'
        return l_ret

    @staticmethod
    def _format_list(p_obj, maxlen, indent):
        maxlen = maxlen
        _l_tabbedwidths = [indent, 30, maxlen - 30]
        l_ix = 0
        l_ret = 'Ix\tValue\n--\t-----\n'
        for l_line in p_obj:
            l_ret += '{}\t"{}";\n'.format(l_ix, l_line)
            l_ix += 1
        return l_ret

    @staticmethod
    def _format_tuple(p_obj, maxlen, indent):
        maxlen = maxlen
        _l_tabbedwidths = [indent, 30, maxlen - 30]
        l_ix = 0
        l_ret = '{:<8} {:<}\n'.format('Ix', 'Value')
        for l_line in p_obj:
            l_ret += '{:<8}"{:}";\n'.format(l_ix, l_line)
            l_ix += 1
        return l_ret

    @staticmethod
    def _format_object(p_obj, maxlen, indent=24, maxspew=2000):
        l_col_1_width = 28
        l_tab = 4
        l_attrs = []
        l_tabbedwidths = [indent, l_col_1_width - l_tab, maxlen - l_col_1_width - l_tab]
        l_filtered = filter(lambda aname: not aname.startswith('__'), dir(p_obj))
        l_ret = ''
        for l_slot in l_filtered:
            l_attr = getattr(p_obj, l_slot)
            l_attrs.append((l_slot, l_attr))
        l_attrs.sort()
        for (attr, l_val) in l_attrs:
            l_ret += _format_cols(('Obj: ', attr, _trunc_string(str(l_val), maxspew)), l_tabbedwidths, ' ') + '\n'
        return l_ret

    @staticmethod
    def _format_none(p_obj):
        l_ret = 'Object is "None" {}\n'.format(p_obj)
        return l_ret

# ======================================================================


def FormatBytes(p_message):
    """Print all the bytes of a message as hex bytes.
    """
    l_len = len(p_message)
    l_message = ''
    if l_len == 0:
        l_message = "<NONE>"
    else:
        for l_x in range(l_len):
            try:
                l_message += " {:#04x}".format(int(p_message[l_x]))
            except ValueError:
                try:
                    l_message += " {:#04X}".format(ord(p_message[l_x]))
                except TypeError:  #  Must be a string
                    l_message += " {} ".format(p_message[l_x])
    l_message += " <END>"
    return l_message

#######################################


def PrettyPrint(p_title, p_str, maxlen=150):
    print('Title: {}\n'.format(p_title), '\n'.join(_format_line(str(p_str), maxlen, ' ')))


def _delchars(p_str, p_chars):
    """ Returns a string for which all occurrences of characters in chars have been removed.
    """
    #  Translate demands a mapping string of 256 characters;
    #  whip up a string that will leave all characters unmolested.
    l_table = dict.fromkeys(map(ord, p_chars), None)
    return p_str.translate(l_table)


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

#  ## END DBK
