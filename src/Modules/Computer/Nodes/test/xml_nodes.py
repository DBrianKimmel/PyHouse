"""
@name: PyHouse/src/Modules/Computer/Nodes/xml_nodes.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 7, 2014
@Summary:

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
