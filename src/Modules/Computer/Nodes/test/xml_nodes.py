"""
@name:      PyHouse/src/Modules/Computer/Nodes/xml_nodes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 7, 2014
@Summary:

"""

# Import system type stuff

# Import PyMh files

TESTING_NODES_NODE_NAME_1 = "pi-01"
TESTING_NODES_INTERFACE_NAME_1 = "eth0"
TESTING_NODES_INTERFACE_NAME_2 = "wlan0"


NODES_XML = """\
        <NodeSection>
            <Node Name='""" + TESTING_NODES_NODE_NAME_1 + """' Key='0' Active='True'>
                <UUID>87654321-1001-11e3-b583-082e5f899999</UUID>
                <ConnectionAddressV4>192.168.1.123</ConnectionAddressV4>
                <ConnectionAddressV6>1234:5678::dead.beef</ConnectionAddressV6>
                <NodeRoll>123</NodeRoll>
                <InterfaceSection>
                    <Interface Name='""" + TESTING_NODES_INTERFACE_NAME_1 + """' Key="0" Active="True">
                        <UUID>87654321-1001-11e3-b583-012300001111</UUID>
                        <MacAddress>01:02:03:04:05:06</MacAddress>
                        <IPv4Address>192.168.1.11</IPv4Address>
                        <IPv6Address>2000:1D::1, 2000:1D::101</IPv6Address>
                    </Interface>
                    <Interface Name='""" + TESTING_NODES_INTERFACE_NAME_2 + """' Key="1" Active="True">
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
                <NodeRoll>6</NodeRoll>
            </Node>
        </NodeSection>
"""



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
# ## END DBK
