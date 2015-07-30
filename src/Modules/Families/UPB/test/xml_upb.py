"""
@name:      PyHouse/src/Modules/Families/UPB/test/xml_upb.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 9, 2014
@Summary:

"""

TESTING_UPB_ADDRESS = '255'
TESTING_UPB_NETWORK = '6'
TESTING_UPB_PASSWORD = '1253'

L_UPB_ADDRESS = '    <UPBAddress>' + TESTING_UPB_ADDRESS + '</UPBAddress>'
L_UPB_NETWORK = '    <UPBNetworkID>' + TESTING_UPB_NETWORK + '</UPBNetworkID>'
L_UPB_PASSWORD = '    <UPBPassword>' + TESTING_UPB_PASSWORD + '</UPBPassword>'

UPB_XML = L_UPB_ADDRESS + \
          L_UPB_NETWORK + \
          L_UPB_PASSWORD

UPB_XSD = """
              <xs:element type="xs:byte" name="UPBNetworkID" minOccurs="0"/>
              <xs:element type="xs:short" name="UPBPassword" minOccurs="0"/>
              <xs:element type="xs:short" name="UPBAddress" minOccurs="0"/>
"""

# ## END DBK
