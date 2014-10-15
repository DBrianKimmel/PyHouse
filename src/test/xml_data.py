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
from Modules.Computer.Internet.internet_xml import INTERNET_XML
from Modules.Communication.send_email import EMAIL_XML
from Modules.Web.web_server import WEB_SERVER_XML
from Modules.Housing.location import LOCATION_XML
from Modules.Housing.rooms import ROOMS_XML
from Modules.Scheduling.schedule_xml import SCHEDULE_XML
from Modules.Lighting.lighting_lights import LIGHTS_XML
from Modules.Lighting.lighting_buttons import BUTTONS_XML
from Modules.Lighting.lighting_controllers import CONTROLLER_XML
from Modules.Hvac.thermostats import THERMOSTAT_XML


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
NODES_XML = """\
        <NodeSection>
            <Node Name='pi-01' Key='0' Active='True'>
                <UUID>87654321-1001-11e3-b583-082e5f899999</UUID>
                <ConnectionAddressV4>192.168.1.123</ConnectionAddressV4>
                <InterfaceSection>
                    <Interface Name='eth0' Key="0" Active="True">
                        <UUID>87654321-1001-11e3-b583-012300001111</UUID>
                        <MacAddress>01:02:03:04:05:06</MacAddress>
                        <IPv4Address>192.168.1.11</IPv4Address>
                        <IPv6Address>2000:1D::1, 2000:1D::101</IPv6Address>
                    </Interface>
                    <Interface Name='wlan0' Key="1" Active="True">
                        <UUID>87654321-1001-11e3-b583-012300002222</UUID>
                        <MacAddress>01:02:03:04:05:06</MacAddress>
                        <IPv4Address>192.168.1.22</IPv4Address>
                        <IPv6Address>2000:1D::2, 2000:1D::202</IPv6Address>
                    </Interface>
                    <Interface Name='lo' Key="2" Active="True">
                        <MacAddress>01:02:03:04:05:06</MacAddress>
                        <IPv4Address>192.168.1.33</IPv4Address>
                        <IPv6Address>2000:1D::3, 2000:1D::303</IPv6Address>
                    </Interface>
                </InterfaceSection>
            </Node>
            <Node Name='pi-02' Key='0' Active='True'>
                <UUID>87654321-1001-11e3-b583-082e5f899999</UUID>
                <ConnectionAddressV4>192.168.1.124</ConnectionAddressV4>
            </Node>
        </NodeSection>
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


PYHOUSE_HEADER_XML = """\
<PyHouse Version='2'>
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
