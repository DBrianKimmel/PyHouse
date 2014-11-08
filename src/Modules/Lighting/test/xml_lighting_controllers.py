"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Lighting/test/xml_lighting_controllers.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 7, 2014
@Summary:

"""

CONTROLLER_XML = """
        <ControllerSection>
            <Controller Active="False" Key="0" Name="PLM_1">
                <Comment>Dongle using serial converter 067B:2303</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Office</RoomName>
                <LightingType>Controller</LightingType>
                <Address>AA.AA.AA</Address>
                <IsController>True</IsController>
                <DevCat>12.34</DevCat><GroupList />
                <GroupNumber>0</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>23.45.67</ProductKey>
                <IsResponder>True</IsResponder>
                <InterfaceType>Serial</InterfaceType>
                <Port>/dev/ttyUSB0</Port>
                <BaudRate>19200</BaudRate>
                <ByteSize>8</ByteSize>
                <Parity>N</Parity>
                <StopBits>1.0</StopBits>
                <Timeout>1.0</Timeout>
                <DsrDtr>False</DsrDtr>
                <RtsCts>False</RtsCts>
                <XonXoff>False</XonXoff>
            </Controller>
            <Controller Active="True" Key="1" Name="PowerLink">
                <Comment>2413UH Powerlink Controller</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Office</RoomName>
                <LightingType>Controller</LightingType>
                <Address>17.03.B2</Address>
                <IsController>True</IsController>
                <DevCat>0x0</DevCat>
                <GroupList />
                <GroupNumber>0</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
                <InterfaceType>Serial</InterfaceType>
                <Port>/dev/ttyUSB0</Port>
                <BaudRate>19200</BaudRate>
                <ByteSize>8</ByteSize>
                <Parity>N</Parity>
                <StopBits>1.0</StopBits>
                <Timeout>1.0</Timeout>
                <DsrDtr>False</DsrDtr>
                <RtsCts>False</RtsCts>
                <XonXoff>False</XonXoff>
            </Controller>
            <Controller Active="False" Key="2" Name="UPB_PIM">
                <Comment>UPB PIM  using USB connection</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>UPB</ControllerFamily>
                <RoomName>Master Bath</RoomName>
                <LightingType>Controller</LightingType>
                <UPBNetworkID>6</UPBNetworkID>
                <UPBPassword>1253</UPBPassword>
                <UPBAddress>255</UPBAddress>
                <InterfaceType>USB</InterfaceType>
                <Port>None</Port>
                <Vendor>6109</Vendor>
                <Product>21760</Product>
            </Controller>
        </ControllerSection>
"""

CONTROLLER_XSD = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="ControllerSection">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="Controller" maxOccurs="unbounded" minOccurs="0">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:string" name="Comment"/>
              <xs:element type="xs:string" name="Coords"/>
              <xs:element type="xs:string" name="IsDimmable"/>
              <xs:element type="xs:string" name="ControllerFamily"/>
              <xs:element type="xs:string" name="RoomName"/>
              <xs:element type="xs:string" name="LightingType"/>
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
            </xs:sequence>
            <xs:attribute type="xs:string" name="Active" use="optional"/>
            <xs:attribute type="xs:byte" name="Key" use="optional"/>
            <xs:attribute type="xs:string" name="Name" use="optional"/>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
"""
# ## END DBK
