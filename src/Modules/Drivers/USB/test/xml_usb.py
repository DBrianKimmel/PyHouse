"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Drivers/USB/test/xml_usb.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 9, 2014
@Summary:

"""



USB_XML = """
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

# ## END DBK
