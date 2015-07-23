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
from Modules.Core.test.xml_device import XML_DEVICE, XML_DEVICE_1_3
from Modules.Drivers.test.xml_interface import INTERFACE_SERIAL_XML
from Modules.Families.Insteon.test.xml_insteon import XML_INSTEON
from Modules.Families.UPB.test.xml_upb import UPB_XML
from Modules.Drivers.Serial.test.xml_serial import SERIAL_XML
from Modules.Drivers.USB.test.xml_usb import USB_XML


TESTING_CONTROLLER_TYPE = 'Controller'

L_CONTROLLER_TYPE = '    <LightingType>' + TESTING_CONTROLLER_TYPE + '</LightingType>'

L_CONTROLLER_BODY = '\n'.join([
    XML_DEVICE,
    L_CONTROLLER_TYPE
    ])

L_CONTROLLER_BODY_1_3 = '\n'.join([
    XML_DEVICE_1_3,
    L_CONTROLLER_TYPE
    ])

INSTEON_CONTROLLER_XML = '\n'.join([
    '<Controller Active="True" Key="0" Name="Insteon Serial Controller">',
    L_CONTROLLER_BODY,
    XML_INSTEON,
    INTERFACE_SERIAL_XML,
    SERIAL_XML,
    "</Controller>"])

INSTEON_CONTROLLER_XML_1_3 = '\n'.join([
    '<Controller Active="True" Key="0" Name="Insteon Serial Controller">',
    L_CONTROLLER_BODY_1_3,
    XML_INSTEON,
    INTERFACE_SERIAL_XML,
    SERIAL_XML,
    "</Controller>"])

UPB_CONTROLLER_XML = '\n'.join([
    '<Controller Active="True" Key="1" Name="UPB USB Controller">',
    L_CONTROLLER_BODY,
    UPB_XML,
    USB_XML,
    "</Controller>"])

UPB_CONTROLLER_XML_1_3 = '\n'.join([
    '<Controller Active="True" Key="1" Name="UPB USB Controller">',
    L_CONTROLLER_BODY_1_3,
    UPB_XML,
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
