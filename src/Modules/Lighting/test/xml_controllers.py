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
from Modules.Lighting.test.xml_core import *
from Modules.Drivers.test.xml_interface import INTERFACE_SERIAL_XML
from Modules.Families.Insteon.test.xml_insteon import *
from Modules.Families.UPB.test.xml_upb import UPB_XML
from Modules.Drivers.Serial.test.xml_serial import SERIAL_XML
from Modules.Drivers.USB.test.xml_usb import USB_XML


CONTROLLER_TYPE = "    <LightingType>Controller</LightingType>"

CONTROLLER_BODY = '\n'.join([
    CORE_DEVICE,
    CONTROLLER_TYPE
    ])

INSTEON_CONTROLLER_XML = '\n'.join([
    '<Controller Active="True" Key="0" Name="Insteon Serial Controller">',
    CONTROLLER_BODY,
    INSTEON_XML,
    INTERFACE_SERIAL_XML,
    SERIAL_XML,
    "</Controller>"])

UPB_CONTROLLER_XML = '\n'.join([
    '<Controller Active="True" Key="1" Name="UPB USB Controller">',
    CONTROLLER_BODY,
    UPB_XML,
    USB_XML,
    "</Controller>"])

CONTROLLER_SECTION_XML = '\n'.join([
    "<ControllerSection>",
    INSTEON_CONTROLLER_XML,
    UPB_CONTROLLER_XML,
    "</ControllerSection>"])

# ## END DBK
