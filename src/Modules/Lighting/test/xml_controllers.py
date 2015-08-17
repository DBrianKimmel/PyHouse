"""
@name:      PyHouse/src/Modules/Lighting/test/xml_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

"""

# Import system type stuff

# Import PyMh files
from Modules.Core.test.xml_device import \
        XML_DEVICE_INSTEON, \
        XML_DEVICE_INSTEON_1_3, \
        XML_DEVICE_UPB
from Modules.Drivers.test.xml_interface import \
        INTERFACE_SERIAL_XML
from Modules.Families.Insteon.test.xml_insteon import \
        XML_INSTEON
from Modules.Families.UPB.test.xml_upb import \
        XML_UPB
from Modules.Drivers.Serial.test.xml_serial import \
        SERIAL_XML
from Modules.Drivers.USB.test.xml_usb import \
        USB_XML


TESTING_CONTROLLER_TYPE = 'Controller'
TESTING_CONTROLLER_NAME_1 = 'Insteon Serial Controller'
TESTING_CONTROLLER_KEY_1 = '0'
TESTING_CONTROLLER_ACTIVE_1 = 'True'
TESTING_CONTROLLER_NAME_2 = 'UPB USB Controller'
TESTING_CONTROLLER_KEY_2 = '1'
TESTING_CONTROLLER_ACTIVE_2 = 'True'

L_CONTROLLER_LINE_1 = '  <Controller Name="' + TESTING_CONTROLLER_NAME_1 + '" Key="' + TESTING_CONTROLLER_KEY_1 + '" Active="' + TESTING_CONTROLLER_ACTIVE_1 + '">'
L_CONTROLLER_LINE_2 = '  <Controller Name="' + TESTING_CONTROLLER_NAME_2 + '" Key="' + TESTING_CONTROLLER_KEY_2 + '" Active="' + TESTING_CONTROLLER_ACTIVE_2 + '">'

L_CONTROLLER_TYPE = '    <LightingType>' + TESTING_CONTROLLER_TYPE + '</LightingType>'

L_CONTROLLER_BODY_INSTEON = '\n'.join([
    XML_DEVICE_INSTEON,
    L_CONTROLLER_TYPE
    ])

L_CONTROLLER_BODY_UPB = '\n'.join([
    XML_DEVICE_UPB,
    L_CONTROLLER_TYPE
    ])

L_CONTROLLER_BODY_1_3 = '\n'.join([
    XML_DEVICE_INSTEON_1_3,
    L_CONTROLLER_TYPE
    ])

INSTEON_CONTROLLER_XML = '\n'.join([
    L_CONTROLLER_LINE_1,
    L_CONTROLLER_BODY_INSTEON,
    XML_INSTEON,
    INTERFACE_SERIAL_XML,
    SERIAL_XML,
    "</Controller>"
    ])

INSTEON_CONTROLLER_XML_1_3 = '\n'.join([
    L_CONTROLLER_LINE_1,
    L_CONTROLLER_BODY_1_3,
    XML_INSTEON,
    INTERFACE_SERIAL_XML,
    SERIAL_XML,
    "</Controller>"])

UPB_CONTROLLER_XML = '\n'.join([
    L_CONTROLLER_LINE_2,
    L_CONTROLLER_BODY_UPB,
    XML_UPB,
    USB_XML,
    "</Controller>"])

UPB_CONTROLLER_XML_1_3 = '\n'.join([
    L_CONTROLLER_LINE_2,
    L_CONTROLLER_BODY_1_3,
    XML_UPB,
    USB_XML,
    "</Controller>"])

XML_CONTROLLER_SECTION = '\n'.join([
    "<ControllerSection>",
    INSTEON_CONTROLLER_XML,
    UPB_CONTROLLER_XML,
    "</ControllerSection>"])

XML_CONTROLLER_SECTION_1_3 = '\n'.join([
    "<ControllerSection>",
    INSTEON_CONTROLLER_XML_1_3,
    UPB_CONTROLLER_XML_1_3,
    "</ControllerSection>"])

# ## END DBK
