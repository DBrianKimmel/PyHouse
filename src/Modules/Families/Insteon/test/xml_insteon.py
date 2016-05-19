"""
@name:      PyHouse/src/Modules/Families/Insteon/test/xml_insteon.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 9, 2014
@summary:   Insteon specific information.

This information will be present in a device's XML for Insteon type devices.

"""

TESTING_INSTEON_ADDRESS_0 = '16.62.2D'
TESTING_INSTEON_DEVCAT_0 = '02.1C'
TESTING_INSTEON_ENGINE_VERSION_0 = '1'
TESTING_INSTEON_GROUP_NUM_0 = '0'
TESTING_INSTEON_GROUP_LIST_0 = 'All_Lights|Outside|Foyer(0;0)'
TESTING_INSTEON_PRODUCT_KEY_0 = '20.1A.35'
TESTING_INSTEON_LINKS_0 = {}

TESTING_INSTEON_VERSION = '2'

L_INSTEON_ADDRESS_0 = '    <InsteonAddress>' + TESTING_INSTEON_ADDRESS_0 + '</InsteonAddress>'
L_INSTEON_DEVCAT_0 = '    <DevCat>' + TESTING_INSTEON_DEVCAT_0 + '</DevCat>'
L_INSTEON_ENGINE_VERSION_0 = '    <EngineVersion>' + TESTING_INSTEON_ENGINE_VERSION_0 + '</EngineVersion>'
L_INSTEON_GROUP_NUM_0 = '    <GroupNumber>' + TESTING_INSTEON_GROUP_NUM_0 + '</GroupNumber>'
L_INSTEON_GROUP_LIST_0 = '    <GroupList>' + TESTING_INSTEON_GROUP_LIST_0 + '</GroupList>'
L_INSTEON_PRODUCT_KEY_0 = '    <ProductKey>' + TESTING_INSTEON_PRODUCT_KEY_0 + '</ProductKey>'
L_INSTEON_VERSION = '    <Version>' + TESTING_INSTEON_VERSION + '</Version>'

XML_INSTEON = '\n'.join([
    L_INSTEON_ADDRESS_0,
    L_INSTEON_DEVCAT_0,
    L_INSTEON_ENGINE_VERSION_0,
    L_INSTEON_GROUP_NUM_0,
    L_INSTEON_GROUP_LIST_0,
    L_INSTEON_PRODUCT_KEY_0,
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

#  ## END DBK
