"""
@name:      PyHouse/src/Modules/Lighting/test/xml_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

There is a matrix of controllers to create here

"""

# Import system type stuff
import platform

# Import PyMh files
from Modules.Core.test.xml_device import \
        XML_DEVICE_INSTEON, \
        XML_DEVICE_UPB
from Modules.Drivers.test.xml_interface import \
        XML_SERIAL_LINUX_INTERFACE, \
        XML_SERIAL_WINDOWS_INTERFACE, \
        XML_USB_INTERFACE
from Modules.Families.Insteon.test.xml_insteon import \
        XML_INSTEON
from Modules.Families.UPB.test.xml_upb import \
        XML_UPB
from Modules.Drivers.Serial.test.xml_serial import \
        XML_SERIAL
from Modules.Drivers.USB.test.xml_usb import \
        XML_USB


if platform.uname()[0] == 'Windows':
    L_SERIAL_INTERFACE = XML_SERIAL_WINDOWS_INTERFACE
else:
    L_SERIAL_INTERFACE = XML_SERIAL_LINUX_INTERFACE

L_CONTROLLER_SECTION_START = '<ControllerSection>'
L_CONTROLLER_SECTION_END = '</ControllerSection>'
L_CONTROLLER_END = '</Controller>'


TESTING_CONTROLLER_NAME_0 = 'Insteon Serial Controller'
TESTING_CONTROLLER_KEY_0 = '0'
TESTING_CONTROLLER_ACTIVE_0 = 'True'
TESTING_CONTROLLER_TYPE_0 = 'Controller'

L_CONTROLLER_START_0 = '  <Controller Name="' + TESTING_CONTROLLER_NAME_0 + '" Key="' + TESTING_CONTROLLER_KEY_0 + '" Active="' + TESTING_CONTROLLER_ACTIVE_0 + '">'
L_CONTROLLER_TYPE_0 = '    <LightingType>' + TESTING_CONTROLLER_TYPE_0 + '</LightingType>'

L_CONTROLLER_0 = '\n'.join([
    L_CONTROLLER_START_0,
    L_CONTROLLER_TYPE_0,
    XML_DEVICE_INSTEON,
    XML_INSTEON,
    L_SERIAL_INTERFACE,
    XML_SERIAL,
    L_CONTROLLER_END
    ])


TESTING_CONTROLLER_NAME_1 = 'UPB USB Controller'
TESTING_CONTROLLER_KEY_1 = '1'
TESTING_CONTROLLER_ACTIVE_1 = 'True'
TESTING_CONTROLLER_TYPE_1 = 'Controller'

L_CONTROLLER_START_1 = '  <Controller Name="' + TESTING_CONTROLLER_NAME_1 + '" Key="' + TESTING_CONTROLLER_KEY_1 + '" Active="' + TESTING_CONTROLLER_ACTIVE_1 + '">'
L_CONTROLLER_TYPE_1 = '    <LightingType>' + TESTING_CONTROLLER_TYPE_1 + '</LightingType>'

L_CONTROLLER_1 = '\n'.join([
    L_CONTROLLER_START_1,
    L_CONTROLLER_TYPE_1,
    XML_DEVICE_UPB,
    XML_UPB,
    XML_USB_INTERFACE,
    XML_USB,
    L_CONTROLLER_END
    ])


XML_CONTROLLER_SECTION = '\n'.join([
    L_CONTROLLER_SECTION_START,
    L_CONTROLLER_0,
    L_CONTROLLER_1,
    L_CONTROLLER_SECTION_END
    ])

# ## END DBK
