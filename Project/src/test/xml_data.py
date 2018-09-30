"""
@name:      PyHouse/src/test/xml_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jan 20, 2010
@summary:   Handle all of the information for all houses.

XML to define the PyHouse.xml file

used for testing
"""

__updated__ = '2018-03-23'

#  Import system type stuff

#  Import PyMh files
from Modules.Core.data_objects import __version__ as dataVersion
from Modules.Computer.test.xml_computer import XML_COMPUTER_DIVISION
from Modules.Housing.test.xml_housing import XML_HOUSE_DIVISION

TESTING_PYHOUSE = 'PyHouse'

TESTING_VERSION = dataVersion
TESTING_XMLNS_COMP = 'http://PyHouse.Org/ComputerDiv'
TESTING_XMLNS_XSI = 'http://www.w3.org/2001/XMLSchema-instance'
TESTING_XSI_SCHEMA = 'http://PyHouse.org schemas/PyHouse.xsd'
TESTING_UPDATE_COMMENT = '<!-- Updated by PyHouse 2015-07-19 11:22:33.996000 -->'

L_VERSION = '   Version="' + TESTING_VERSION + '"\n'
L_XMLNS_COMP = '    xmlns:comp="' + TESTING_XMLNS_COMP + '"'
L_XMLNS_XSI = '    xmlns:xsi="' + TESTING_XMLNS_XSI + '"'
L_XSI_SCHEMA = '    xsi:schemaLocation="' + TESTING_XSI_SCHEMA + '"'

L_PYHOUSE_START = '\n'.join([
    '<' + TESTING_PYHOUSE + '\n',
    L_VERSION,
    L_XMLNS_COMP,
    L_XMLNS_XSI,
    L_XSI_SCHEMA,
    '>\n',
    TESTING_UPDATE_COMMENT
])
L_PYHOUSE_END = '</' + TESTING_PYHOUSE + '>'

XML_EMPTY = '\n'.join([
    L_PYHOUSE_START,
    L_PYHOUSE_END
])

XML_LONG = '\n'.join([
    L_PYHOUSE_START,
    XML_COMPUTER_DIVISION,
    XML_HOUSE_DIVISION,
    L_PYHOUSE_END
])

#  ## END DBK
