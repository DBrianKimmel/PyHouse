"""
@name:      PyHouse/src/Modules/Computer/Nodes/xml_nodes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 7, 2014
@Summary:

"""

#  Import system type stuff

#  Import PyMh files

L_NODE_SECTION_START = '  <NodeSection>'
L_NODE_SECTION_END = '  </NodeSection>'
L_NODE_INTERFACE_SECTION_START = '  <InterfaceSection>'
L_NODE_INTERFACE_SECTION_END = '  </InterfaceSection>'
L_NODE_END = '    </Node>'
L_NODE_INTERFACE_END = '    </Interface>'

TESTING_NODES_NODE_NAME_0 = "pi-01"
TESTING_NODES_NODE_ACTIVE_0 = "True"
TESTING_NODES_NODE_KEY_0 = "0"
TESTING_NODES_NODE_UUID_0 = '87654321-1001-11e3-b583-082e5f899999'
TESTING_NODES_CONNECTION_ADDRESS_V4_0 = '192.168.1.123'
TESTING_NODES_CONNECTION_ADDRESS_V6_0 = '2001:db8::dead:beef'
TESTING_NODES_NODE_ROLL_0 = '123'

TESTING_NODES_INTERFACE_NAME_0_0 = "eth0"
TESTING_NODES_INTERFACE_KEY_0_0 = '0'
TESTING_NODES_INTERFACE_ACTIVE_0_0 = 'True'
TESTING_NODES_INTERFACE_UUID_0_0 = '87654321-1001-11e3-b583-012300001111'
TESTING_NODES_INTERFACE_MAC_ADDRESS_0_0 = '01:02:03:04:05:06'
TESTING_NODES_INTERFACE_ADDRESS_V4_0_0 = '192.168.1.11'
TESTING_NODES_INTERFACE_ADDRESS_V6_0_0 = '2001:db8::dead:beef:100'

TESTING_NODES_INTERFACE_NAME_0_1 = "wlan0"
TESTING_NODES_INTERFACE_KEY_0_1 = '1'
TESTING_NODES_INTERFACE_ACTIVE_0_1 = 'True'
TESTING_NODES_INTERFACE_UUID_0_1 = '87654321-1001-11e3-b583-012300002222'
TESTING_NODES_INTERFACE_MAC_ADDRESS_0_1 = '01:02:03:14:15:16'
TESTING_NODES_INTERFACE_ADDRESS_V4_0_1 = '192.168.1.22'
TESTING_NODES_INTERFACE_ADDRESS_V6_0_1 = '2001:db8::dead:beef:2 2001.db8::222'

TESTING_NODES_INTERFACE_NAME_0_2 = "lo"
TESTING_NODES_INTERFACE_KEY_0_2 = '2'
TESTING_NODES_INTERFACE_ACTIVE_0_2 = 'True'
TESTING_NODES_INTERFACE_UUID_0_2 = '87654321-1001-11e3-b583-012300002222'
TESTING_NODES_INTERFACE_MAC_ADDRESS_0_2 = '01:02:03:24:25:26'
TESTING_NODES_INTERFACE_ADDRESS_V4_0_2 = '192.168.1.33'
TESTING_NODES_INTERFACE_ADDRESS_V6_0_2 = '2001:db8::dead:beef:3 2001.db8::333'

TESTING_NODES_NODE_NAME_1 = "pi-02"
TESTING_NODES_NODE_ACTIVE_1 = 'True'
TESTING_NODES_NODE_KEY_1 = '0'
TESTING_NODES_NODE_UUID_1 = '87654321-1001-11e3-b583-082e5f892222'
TESTING_NODES_CONNECTION_ADDRESS_V4_1 = '192.168.1.124'
TESTING_NODES_CONNECTION_ADDRESS_V6_1 = '2001:db8::2:dead:beef'
TESTING_NODES_NODE_ROLL_1 = '123'

L_NODE_START_0 = '    <Node Name="' + TESTING_NODES_NODE_NAME_0 + \
                    '" Key="' + TESTING_NODES_NODE_KEY_0 + \
                    '" Active="' + TESTING_NODES_NODE_ACTIVE_0 + '">'
L_NODE_UUID_0 = '        <UUID>' + TESTING_NODES_NODE_UUID_0 + '</UUID>'
L_NODE_CONNECTION_ADDRESS_V4_0 = '        <ConnectionAddressV4>' + TESTING_NODES_CONNECTION_ADDRESS_V4_0 + '</ConnectionAddressV4>'
L_NODE_CONNECTION_ADDRESS_V6_0 = '        <ConnectionAddressV6>' + TESTING_NODES_CONNECTION_ADDRESS_V6_0 + '</ConnectionAddressV6>'
L_NODE_ROLE_0 = '        <NodeRoll>' + TESTING_NODES_NODE_ROLL_0 + '</NodeRoll>'

L_NODE_INTERFACE_START_0_0 = '    <Interface Name="' + TESTING_NODES_INTERFACE_NAME_0_0 + \
                                '" Key="' + TESTING_NODES_INTERFACE_KEY_0_0 + \
                                '" Active="' + TESTING_NODES_INTERFACE_ACTIVE_0_0 + '">'
L_NODE_INTERFACE_UUID_0_0 = '        <UUID>' + TESTING_NODES_INTERFACE_UUID_0_0 + '</UUID>'
L_NODE_INTERFACE_MAC_ADDRESS_0_0 = '        <MacAddress>' + TESTING_NODES_INTERFACE_MAC_ADDRESS_0_0 + '</MacAddress>'
L_NODE_INTERFACE_IPV4_ADDRESS_0_0 = '        <IPv4Address>' + TESTING_NODES_INTERFACE_ADDRESS_V4_0_0 + '</IPv4Address>'
L_NODE_INTERFACE_IPV6_ADDRESS_0_0 = '        <IPv6Address>' + TESTING_NODES_INTERFACE_ADDRESS_V6_0_0 + '</IPv6Address>'
XML_NODE_INTERFACE_0_0 = '\n    '.join([
        L_NODE_INTERFACE_START_0_0,
        L_NODE_INTERFACE_UUID_0_0,
        L_NODE_INTERFACE_MAC_ADDRESS_0_0,
        L_NODE_INTERFACE_IPV4_ADDRESS_0_0,
        L_NODE_INTERFACE_IPV6_ADDRESS_0_0,
        L_NODE_INTERFACE_END
])

L_NODE_INTERFACE_START_0_1 = '    <Interface Name="' + TESTING_NODES_INTERFACE_NAME_0_1 + \
                                '" Key="' + TESTING_NODES_INTERFACE_KEY_0_1 + \
                                '" Active="' + TESTING_NODES_INTERFACE_ACTIVE_0_1 + '">'
L_NODE_INTERFACE_UUID_0_1 = '        <UUID>' + TESTING_NODES_INTERFACE_UUID_0_1 + '</UUID>'
L_NODE_INTERFACE_MAC_ADDRESS_0_1 = '        <MacAddress>' + TESTING_NODES_INTERFACE_MAC_ADDRESS_0_1 + '</MacAddress>'
L_NODE_INTERFACE_IPV4_ADDRESS_0_1 = '        <IPv4Address>' + TESTING_NODES_INTERFACE_ADDRESS_V4_0_1 + '</IPv4Address>'
L_NODE_INTERFACE_IPV6_ADDRESS_0_1 = '        <IPv6Address>' + TESTING_NODES_INTERFACE_MAC_ADDRESS_0_1 + '</IPv6Address>'
XML_NODE_INTERFACE_0_1 = '\n    '.join([
        L_NODE_INTERFACE_START_0_1,
        L_NODE_INTERFACE_UUID_0_1,
        L_NODE_INTERFACE_MAC_ADDRESS_0_1,
        L_NODE_INTERFACE_IPV4_ADDRESS_0_1,
        L_NODE_INTERFACE_IPV6_ADDRESS_0_1,
        L_NODE_INTERFACE_END
])

L_NODE_INTERFACE_START_0_2 = '    <Interface Name="' + TESTING_NODES_INTERFACE_NAME_0_2 + \
                                '" Key="' + TESTING_NODES_INTERFACE_KEY_0_2 + \
                                '" Active="' + TESTING_NODES_INTERFACE_ACTIVE_0_2 + '">'
L_NODE_INTERFACE_UUID_0_2 = '        <UUID>' + TESTING_NODES_INTERFACE_UUID_0_2 + '</UUID>'
L_NODE_INTERFACE_MAC_ADDRESS_0_2 = '        <MacAddress>' + TESTING_NODES_INTERFACE_MAC_ADDRESS_0_2 + '</MacAddress>'
L_NODE_INTERFACE_IPV4_ADDRESS_0_2 = '        <IPv4Address>' + TESTING_NODES_INTERFACE_ADDRESS_V4_0_2 + '</IPv4Address>'
L_NODE_INTERFACE_IPV6_ADDRESS_0_2 = '        <IPv6Address>' + TESTING_NODES_INTERFACE_MAC_ADDRESS_0_2 + '</IPv6Address>'
XML_NODE_INTERFACE_0_2 = '\n    '.join([
        L_NODE_INTERFACE_START_0_2,
        L_NODE_INTERFACE_UUID_0_2,
        L_NODE_INTERFACE_MAC_ADDRESS_0_2,
        L_NODE_INTERFACE_IPV4_ADDRESS_0_2,
        L_NODE_INTERFACE_IPV6_ADDRESS_0_2,
        L_NODE_INTERFACE_END
])

L_NODE_0 = '\n'.join([
    L_NODE_START_0,
    L_NODE_UUID_0,
    L_NODE_CONNECTION_ADDRESS_V4_0,
    L_NODE_CONNECTION_ADDRESS_V6_0,
    L_NODE_ROLE_0,
        L_NODE_INTERFACE_SECTION_START,
        XML_NODE_INTERFACE_0_0,
        XML_NODE_INTERFACE_0_1,
        XML_NODE_INTERFACE_0_2,
        L_NODE_INTERFACE_SECTION_END,
    L_NODE_END
])

L_NODE_START_1 = '    <Node Name="' + TESTING_NODES_NODE_NAME_1 + \
                    '" Key="' + TESTING_NODES_NODE_KEY_1 + \
                    '" Active="' + TESTING_NODES_NODE_ACTIVE_1 + '">'
L_NODE_UUID_1 = '    <UUID>' + TESTING_NODES_NODE_UUID_1 + '</UUID>'
L_NODE_CONNECTION_ADDRESS_V4_1 = '    <ConnectionAddressV4>' + TESTING_NODES_CONNECTION_ADDRESS_V4_1 + '</ConnectionAddressV4>'
L_NODE_CONNECTION_ADDRESS_V6_1 = '    <ConnectionAddressV6>' + TESTING_NODES_CONNECTION_ADDRESS_V6_1 + '</ConnectionAddressV6>'
L_NODE_ROLE_1 = '    <NodeRoll>' + TESTING_NODES_NODE_ROLL_1 + '</NodeRoll>'
L_NODE_1 = '\n'.join([
    L_NODE_START_1,
    L_NODE_UUID_1,
    L_NODE_CONNECTION_ADDRESS_V4_1,
    L_NODE_CONNECTION_ADDRESS_V6_1,
    L_NODE_ROLE_1,
    L_NODE_INTERFACE_SECTION_START,
    L_NODE_INTERFACE_SECTION_END,
    L_NODE_END
])

XML_NODES = '\n'.join([
    L_NODE_SECTION_START,
        L_NODE_0,
        L_NODE_1,
    L_NODE_SECTION_END
])


NODES_XSD = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="NodeSection">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="Node" maxOccurs="unbounded" minOccurs="0">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:string" name="UUID"/>
              <xs:element type="xs:string" name="ConnectionAddressV4"/>
              <xs:element name="InterfaceSection" minOccurs="0">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element name="Interface" maxOccurs="unbounded" minOccurs="0">
                      <xs:complexType>
                        <xs:sequence>
                          <xs:element type="xs:string" name="UUID" minOccurs="0"/>
                          <xs:element type="xs:string" name="MacAddress"/>
                          <xs:element type="xs:string" name="IPv4Address"/>
                          <xs:element type="xs:string" name="IPv6Address"/>
                        </xs:sequence>
                        <xs:attribute type="xs:string" name="Name" use="optional"/>
                        <xs:attribute type="xs:byte" name="Key" use="optional"/>
                        <xs:attribute type="xs:string" name="Active" use="optional"/>
                      </xs:complexType>
                    </xs:element>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
            </xs:sequence>
            <xs:attribute type="xs:string" name="Name" use="optional"/>
            <xs:attribute type="xs:byte" name="Key" use="optional"/>
            <xs:attribute type="xs:string" name="Active" use="optional"/>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
"""
#  ## END DBK
