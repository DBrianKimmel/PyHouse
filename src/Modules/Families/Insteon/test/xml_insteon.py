"""
@name: PyHouse/src/Modules/Families/Insteon/test/xml_insteon.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 9, 2014
@Summary:

"""


TESTING_INSTEON_ADDRESS = "16.62.2D"
TESTING_INSTEON_DEVCAT = "02.1C"
TESTING_INSTEON_PRODUCT_KEY = "20.1A.35"


INSTEON_XML = """
    <ControllerFamily>Insteon</ControllerFamily>
    <Address>""" + TESTING_INSTEON_ADDRESS + """</Address>
    <DevCat>""" + TESTING_INSTEON_DEVCAT + """</DevCat>
    <GroupList>All_Lights|Outside|Foyer(0;0)</GroupList>
    <GroupNumber>0</GroupNumber>
    <IsController>False</IsController>
    <IsMaster>False</IsMaster>
    <IsResponder>False</IsResponder>
    <ProductKey>30.1A.35</ProductKey>
"""


INSTEON_XSD = """
<xs:element type="xs:string" name="InsteonAddress"/>
<xs:element type="xs:string" name="IsController"/>
<xs:element type="xs:string" name="DevCat"/>
<xs:element type="xs:string" name="GroupList"/>
<xs:element type="xs:byte" name="GroupNumber"/>
<xs:element type="xs:string" name="IsMaster"/>
<xs:element type="xs:string" name="ProductKey"/>
<xs:element type="xs:string" name="IsResponder"/>

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
