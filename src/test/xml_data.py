"""
@name:      PyHouse/src/test/xml_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jan 20, 2010
@summary:   Handle all of the information for all houses.

XML to define the PyHouse.xml file

used for testing
"""

#  Import system type stuff

#  Import PyMh files
from Modules.Computer.test.xml_computer import XML_COMPUTER_DIVISION
from Modules.Housing.test.xml_housing import HOUSE_DIVISION_XML


TESTING_VERSION = '1.4.0'
TESTING_XMLNS_COMP = 'http://PyHouse.Org/ComputerDiv'
TESTING_XMLNS_XSI = 'http://www.w3.org/2001/XMLSchema-instance'
TESTING_XSI_SCHEMA = 'http://PyHouse.org schemas/PyHouse.xsd'
TESTING_UPDATE_COMMENT = '<!-- Updated by PyHouse 2015-07-19 11:22:33.996000 -->'

L_VERSION = '   Version="' + TESTING_VERSION + '"'
L_XMLNS_COMP = '    xmlns:comp="' + TESTING_XMLNS_COMP + '"'
L_XMLNS_XSI = '    xmlns:xsi="' + TESTING_XMLNS_XSI + '"'
L_XSI_SCHEMA = '    xsi:schemaLocation="' + TESTING_XSI_SCHEMA + '"'

L_PYHOUSE_START = '\n'.join([
    '<PyHouse',
    L_VERSION,
    L_XMLNS_COMP,
    L_XMLNS_XSI,
    L_XSI_SCHEMA,
    '>',
    TESTING_UPDATE_COMMENT
])
L_PYHOUSE_END = '</PyHouse>'


XML_EMPTY = '\n'.join([
    L_PYHOUSE_START,
    L_PYHOUSE_END
])

XML_LONG = '\n'.join([
    L_PYHOUSE_START,
    XML_COMPUTER_DIVISION,
    HOUSE_DIVISION_XML,
    L_PYHOUSE_END
])


XSD_HEADER = """
"""

XSD_LONG = XSD_HEADER

#  ## END DBK
