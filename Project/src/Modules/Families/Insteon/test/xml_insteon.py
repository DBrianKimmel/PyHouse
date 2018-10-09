"""
@name:      PyHouse/src/Modules/Families/Insteon/test/xml_insteon.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 9, 2014
@summary:   Insteon specific information.

This information will be present in a device's XML for Insteon type devices.

"""

__updated__ = '2016-11-07'

# Insteon Light

TESTING_INSTEON_ADDRESS_0 = '16.62.2D'
TESTING_INSTEON_DEVCAT_0 = '02.1C'
TESTING_INSTEON_ENGINE_VERSION_0 = '1'
TESTING_INSTEON_FIRMWARE_VERSION_0 = '32'
TESTING_INSTEON_GROUP_NUM_0 = '0'
TESTING_INSTEON_GROUP_LIST_0 = 'Insteon Group List 0'
TESTING_INSTEON_PRODUCT_KEY_0 = '20.69.35'
TESTING_INSTEON_LINKS_0 = {}

L_INSTEON_ADDRESS_0 = '    <InsteonAddress>' + TESTING_INSTEON_ADDRESS_0 + '</InsteonAddress>'
L_INSTEON_DEVCAT_0 = '    <DevCat>' + TESTING_INSTEON_DEVCAT_0 + '</DevCat>'
L_INSTEON_ENGINE_VERSION_0 = '    <EngineVersion>' + TESTING_INSTEON_ENGINE_VERSION_0 + '</EngineVersion>'
L_INSTEON_FIRMWARE_VERSION_0 = '    <FirmwareVersion>' + TESTING_INSTEON_FIRMWARE_VERSION_0 + '</FirmwareVersion>'
L_INSTEON_GROUP_NUM_0 = '    <GroupNumber>' + TESTING_INSTEON_GROUP_NUM_0 + '</GroupNumber>'
L_INSTEON_GROUP_LIST_0 = '    <GroupList>' + TESTING_INSTEON_GROUP_LIST_0 + '</GroupList>'
L_INSTEON_PRODUCT_KEY_0 = '    <ProductKey>' + TESTING_INSTEON_PRODUCT_KEY_0 + '</ProductKey>'

XML_INSTEON_0 = '\n'.join([
    L_INSTEON_ADDRESS_0,
    L_INSTEON_DEVCAT_0,
    L_INSTEON_ENGINE_VERSION_0,
    L_INSTEON_FIRMWARE_VERSION_0,
    L_INSTEON_GROUP_NUM_0,
    L_INSTEON_GROUP_LIST_0,
    L_INSTEON_PRODUCT_KEY_0,
    ])

# Controller

TESTING_INSTEON_ADDRESS_1 = '21.34.1F'
TESTING_INSTEON_DEVCAT_1 = '01.1C'
TESTING_INSTEON_ENGINE_VERSION_1 = '1'
TESTING_INSTEON_FIRMWARE_VERSION_1 = '32'
TESTING_INSTEON_GROUP_NUM_1 = '5'
TESTING_INSTEON_GROUP_LIST_1 = 'Insteon Group list 1'
TESTING_INSTEON_PRODUCT_KEY_1 = '11.1A.DD'
TESTING_INSTEON_LINKS_1 = {}

L_INSTEON_ADDRESS_1 = '    <InsteonAddress>' + TESTING_INSTEON_ADDRESS_1 + '</InsteonAddress>'
L_INSTEON_DEVCAT_1 = '    <DevCat>' + TESTING_INSTEON_DEVCAT_1 + '</DevCat>'
L_INSTEON_ENGINE_VERSION_1 = '    <EngineVersion>' + TESTING_INSTEON_ENGINE_VERSION_1 + '</EngineVersion>'
L_INSTEON_FIRMWARE_VERSION_1 = '    <FirmwareVersion>' + TESTING_INSTEON_FIRMWARE_VERSION_1 + '</FirmwareVersion>'
L_INSTEON_GROUP_NUM_1 = '    <GroupNumber>' + TESTING_INSTEON_GROUP_NUM_1 + '</GroupNumber>'
L_INSTEON_GROUP_LIST_1 = '    <GroupList>' + TESTING_INSTEON_GROUP_LIST_1 + '</GroupList>'
L_INSTEON_PRODUCT_KEY_1 = '    <ProductKey>' + TESTING_INSTEON_PRODUCT_KEY_1 + '</ProductKey>'

XML_INSTEON_1 = '\n'.join([
    L_INSTEON_ADDRESS_1,
    L_INSTEON_DEVCAT_1,
    L_INSTEON_ENGINE_VERSION_1,
    L_INSTEON_FIRMWARE_VERSION_1,
    L_INSTEON_GROUP_NUM_1,
    L_INSTEON_GROUP_LIST_1,
    L_INSTEON_PRODUCT_KEY_1,
    ])

# Insteon Button

TESTING_INSTEON_ADDRESS_2 = '53.22.56'

L_INSTEON_ADDRESS_2 = '    <InsteonAddress>' + TESTING_INSTEON_ADDRESS_2 + '</InsteonAddress>'

XML_INSTEON_2 = '\n'.join([
    L_INSTEON_ADDRESS_2,
    L_INSTEON_DEVCAT_1,
    L_INSTEON_ENGINE_VERSION_1,
    L_INSTEON_FIRMWARE_VERSION_1,
    L_INSTEON_GROUP_NUM_1,
    L_INSTEON_GROUP_LIST_1,
    L_INSTEON_PRODUCT_KEY_1,
    ])

# Insteon Button

TESTING_INSTEON_ADDRESS_3 = '53.33.33'

L_INSTEON_ADDRESS_3 = '    <InsteonAddress>' + TESTING_INSTEON_ADDRESS_3 + '</InsteonAddress>'

XML_INSTEON_3 = '\n'.join([
    L_INSTEON_ADDRESS_3,
    L_INSTEON_DEVCAT_1,
    L_INSTEON_ENGINE_VERSION_1,
    L_INSTEON_FIRMWARE_VERSION_1,
    L_INSTEON_GROUP_NUM_1,
    L_INSTEON_GROUP_LIST_1,
    L_INSTEON_PRODUCT_KEY_1,
    ])

# Insteon Button

TESTING_INSTEON_ADDRESS_4 = '54.44.44'

L_INSTEON_ADDRESS_4 = '    <InsteonAddress>' + TESTING_INSTEON_ADDRESS_4 + '</InsteonAddress>'

XML_INSTEON_4 = '\n'.join([
    L_INSTEON_ADDRESS_4,
    L_INSTEON_DEVCAT_1,
    L_INSTEON_ENGINE_VERSION_1,
    L_INSTEON_FIRMWARE_VERSION_1,
    L_INSTEON_GROUP_NUM_1,
    L_INSTEON_GROUP_LIST_1,
    L_INSTEON_PRODUCT_KEY_1,
    ])

XML_INSTEON = '\n'.join([
    XML_INSTEON_0,  # Light
    XML_INSTEON_1,  # Controller
    XML_INSTEON_2,  # Button
    XML_INSTEON_3,  # Button
    XML_INSTEON_4  # Button
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