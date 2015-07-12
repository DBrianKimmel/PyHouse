"""
@name:      PyHouse/src/Modules/Drivers/USB/test/xml_usb.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 9, 2014
@Summary:

"""


USB_XML = """
        <Vendor>6109</Vendor>
        <Product>21760</Product>
"""

USB_XSD = """
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    targetNamespace="http://PyHouse.org"
    xmlns="http://PyHouse.org"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified">

    <xs:element type="xs:short" name="BaudRate"/>
    <xs:element type="xs:byte" name="ByteSize"/>
        <xs:simpleType>
            <xs:restriction base="xs:integer">
                <xs:enumeration value="6"/>
                <xs:enumeration value="7"/>
                <xs:enumeration value="8"/>
            </xs:restriction>
        </xs:simpleType>
    <xs:element type="xs:string" name="Parity"/>
    <xs:element type="xs:float" name="StopBits"/>
    <xs:element type="xs:float" name="Timeout"/>
    <xs:element type="xs:boolean" name="DsrDtr"/>
    <xs:element type="xs:boolean" name="RtsCts">
    <xs:element type="xs:boolean" name="XonXoff"/>

</xs:schema>
"""

OTHER = """
    <xs:element type="xs:string" name="Address" minOccurs="0"/>
    <xs:element type="xs:string" name="IsController" minOccurs="0"/>
    <xs:element type="xs:string" name="DevCat" minOccurs="0"/>
    <xs:element type="xs:string" name="GroupList" minOccurs="0"/>
    <xs:element type="xs:byte" name="GroupNumber" minOccurs="0"/>
    <xs:element type="xs:string" name="IsMaster" minOccurs="0"/>
    <xs:element type="xs:string" name="ProductKey" minOccurs="0"/>
    <xs:element type="xs:string" name="IsResponder" minOccurs="0"/>
    <xs:element type="xs:byte" name="UPBNetworkID" minOccurs="0"/>
    <xs:element type="xs:short" name="UPBPassword" minOccurs="0"/>
    <xs:element type="xs:short" name="UPBAddress" minOccurs="0"/>
    <xs:element type="xs:string" name="InterfaceType"/>
    <xs:element type="xs:string" name="Port"/>
    <xs:element type="xs:short" name="BaudRate" minOccurs="0"/>
    <xs:element type="xs:byte" name="ByteSize" minOccurs="0"/>
    <xs:element type="xs:string" name="Parity" minOccurs="0"/>
    <xs:element type="xs:float" name="StopBits" minOccurs="0"/>
    <xs:element type="xs:float" name="Timeout" minOccurs="0"/>
    <xs:element type="xs:string" name="DsrDtr" minOccurs="0"/>
    <xs:element type="xs:string" name="RtsCts" minOccurs="0"/>
    <xs:element type="xs:string" name="XonXoff" minOccurs="0"/>
    <xs:element type="xs:short" name="Vendor" minOccurs="0"/>
    <xs:element type="xs:short" name="Product" minOccurs="0"/>
"""

# ## END DBK
