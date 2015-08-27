"""
@name:      PyHouse/src/Modules/Families/Insteon/test/xml_insteon.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 9, 2014
@summary:   Insteon specific information.

This information will be present in a device's XML for Insteon type devices.

"""

TESTING_INSTEON_ADDRESS = '16.62.2D'
TESTING_INSTEON_DEVCAT = '02.1C'
TESTING_INSTEON_PRODUCT_KEY = '20.1A.35'
TESTING_INSTEON_GROUP_NUM = '0'
TESTING_INSTEON_GROUP_LIST = 'All_Lights|Outside|Foyer(0;0)'
TESTING_INSTEON_VERSION = '1'

L_INSTEON_ADDRESS = '    <Address>' + TESTING_INSTEON_ADDRESS + '</Address>'
L_INSTEON_DEVCAT = '    <DevCat>' + TESTING_INSTEON_DEVCAT + '</DevCat>'
L_INSTEON_GROUP_NUM = '    <GroupNumber>' + TESTING_INSTEON_GROUP_NUM + '</GroupNumber>'
L_INSTEON_GROUP_LIST = '    <GroupList>' + TESTING_INSTEON_GROUP_LIST + '</GroupList>'
L_INSTEON_PRODUCT_KEY = '    <ProductKey>' + TESTING_INSTEON_PRODUCT_KEY + '</ProductKey>'
L_INSTEON_VERSION = '    <Version>' + TESTING_INSTEON_VERSION + '</Version>'

XML_INSTEON = '\n'.join([
    L_INSTEON_ADDRESS,
    L_INSTEON_DEVCAT,
    L_INSTEON_GROUP_NUM,
    L_INSTEON_GROUP_LIST,
    L_INSTEON_PRODUCT_KEY,
    L_INSTEON_VERSION
    ])


INSTEON_XSD = """
<xs:element type="xs:string" name="InsteonAddress"/>
<xs:element type="xs:string" name="DevCat"/>
<xs:element type="xs:string" name="GroupList"/>
<xs:element type="xs:byte" name="GroupNumber"/>
<xs:element type="xs:string" name="ProductKey"/>

<xs:element type="xs:byte" name="UPBNetworkID" minOccurs="0"/>
<xs:element type="xs:short" name="UPBPassword" minOccurs="0"/>
<xs:element type="xs:short" name="UPBAddress" minOccurs="0"/>

<xs:element type="xs:string" name="InterfaceType"/>
<xs:element type="xs:string" name="Port"/>
"""

# ## END DBK
