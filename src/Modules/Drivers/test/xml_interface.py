"""
@name:      PyHouse/src/Modules/Drivers/test/xml_interface.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 7, 2014
@Summary:

"""

TESTING_INTERFACE_TYPE_SERIAL = 'Serial'
TESTING_INTERFACE_TYPE_USB = 'USB'
TESTING_INTERFACE_PORT_SERIAL = '/dev/ttyS0'
TESTING_INTERFACE_PORT_USB = '/dev/ttyUSB0'
TESTING_INTERFACE_PORT_WINDOWS = 'COMM15'

L_TYPE_SERIAL = '    <InterfaceType>' + TESTING_INTERFACE_TYPE_SERIAL + '</InterfaceType>'
L_TYPE_USB = '    <InterfaceType>' + TESTING_INTERFACE_TYPE_USB + '</InterfaceType>'
L_PORT_SERIAL = '    <Port>' + TESTING_INTERFACE_PORT_SERIAL + '</Port>'
L_PORT_USB = '    <Port>' + TESTING_INTERFACE_PORT_USB + '</Port>'
L_PORT_WINDOWS = '    <Port>' + TESTING_INTERFACE_PORT_WINDOWS + '</Port>'

XML_SERIAL_LINUX_INTERFACE = '\n'.join([
    L_TYPE_SERIAL,
    L_PORT_SERIAL
])

XML_SERIAL_WINDOWS_INTERFACE = '\n'.join([
    L_TYPE_SERIAL,
    L_PORT_WINDOWS
])

XML_USB_INTERFACE = '\n'.join([
    L_TYPE_USB,
    L_PORT_USB
])

# ## END DBK
