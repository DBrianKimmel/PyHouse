"""
@name: PyHouse/src/test/xml_data.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2010-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jan 20, 2010
@summary: Handle all of the information for all houses.

XML to define the PyHouse.xml file

used for testing
"""

# Import system type stuff

# Import PyMh files
from Modules.Communication.send_email import EMAIL_XML
from Modules.Computer.Internet.test.xml_internet import INTERNET_XML
from Modules.Computer.Nodes.test.xml_nodes import NODES_XML
from Modules.Housing.test.xml_location import LOCATION_XML
from Modules.Housing.test.xml_rooms import ROOMS_XML
from Modules.Hvac.test.xml_thermostat import THERMOSTAT_XML
from Modules.Lighting.test.xml_lighting_core import LIGHT_CORE_XML
from Modules.Lighting.test.xml_lighting_buttons import BUTTONS_XML
from Modules.Lighting.test.xml_lighting_controllers import CONTROLLER_XML
from Modules.Lighting.test.xml_lighting_lights import LIGHTS_XML
from Modules.Scheduling.test.xml_schedule import SCHEDULE_XML
from Modules.Web.web_server import WEB_SERVER_XML


# Missing
XML_MISSING = ''


# No sections
XML_EMPTY = """
<PyHouse>
</PyHouse>
"""



COMPUTER_HEADER_XML = """
    <ComputerDivision>
"""
COMPUTER_TRAILER_XML = """
    </ComputerDivision>
"""

COMPUTER_BODY_XML = """\
        <LogSection>
            <Debug>/var/log/pyhouse/debug</Debug>
            <Error>/var/log/pyhouse/error</Error>
        </LogSection>
"""

COMPUTER_XML = '\n'.join([
        COMPUTER_HEADER_XML,
        WEB_SERVER_XML,
        INTERNET_XML,
        NODES_XML,
        EMAIL_XML,
        COMPUTER_TRAILER_XML
                          ])

HOUSE_BODY_XML = """
        <EntertainmentSection />
"""

HOUSE_HEADER_XML = """
    <HouseDivision>
        <UUID>12345678-1002-11e3-b583-333e5f8cdfd2</UUID>
"""
HOUSE_TRAILER_XML = """
    </HouseDivision>
"""
HOUSE_XML = '\n'.join([
       HOUSE_HEADER_XML,
       LOCATION_XML,
       ROOMS_XML,
       SCHEDULE_XML,
       LIGHTS_XML,
       BUTTONS_XML,
       CONTROLLER_XML,
       THERMOSTAT_XML,
       HOUSE_BODY_XML,
       HOUSE_TRAILER_XML
       ])


PYHOUSE_SCHEMA = """
"""

PYHOUSE_HEADER_XML = """
<PyHouse
    Version='2'
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://PyHouse.org schemas/PyHouse.xsd">
"""

PYHOUSE_TRAILER_XML = """
</PyHouse>
"""



# Everything as expected in a running system.
XML_LONG = '/n'.join([
    PYHOUSE_HEADER_XML,
    COMPUTER_XML,
    HOUSE_XML,
    PYHOUSE_TRAILER_XML])



XML_SHORT = """
<PyHouse Version='2'>
    <Web>
    </Web>
    <Nodes>
        <Node Name='PiNode-1' Key='0' Active='True'>
            <UUID>ec955bcf-89c9-11e3-b583-082e5f8cdfd2</UUID>
        </Node>
    </Nodes>
    <Houses>
        <House Name='House_1' Key='0' Active='True'>
            <Controllers>
                <Controller Name='Serial_1' Key='0' Active='True'>
                    <InterfaceType>Serial</InterfaceType>
                    <BaudRate>19200</BaudRate>
                    <ByteSize>8</ByteSize>
                    <DsrDtr>False</DsrDtr>
                    <Parity>N</Parity>
                    <RtsCts>False</RtsCts>
                    <StopBits>1.0</StopBits>
                    <Timeout>0</Timeout>
                    <XonXoff>False</XonXoff>
                </Controller>
                <Controller Name='USB_1' Key='1' Active='True'>
                    <InterfaceType>USB</InterfaceType>
                    <Vendor>12345</Vendor>
                    <Product>9876</Product>
                </Controller>
            </Controllers>
        </House>
    </Houses>
</PyHouse>
"""

# ## END DBK
