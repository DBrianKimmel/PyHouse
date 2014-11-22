"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Families/UPB/test/xml_upb.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 9, 2014
@Summary:

"""


UPB_XML = """\
    <ControllerFamily>UPB</ControllerFamily>
    <UPBNetworkID>6</UPBNetworkID>
    <UPBPassword>1253</UPBPassword>
    <UPBAddress>255</UPBAddress>"""



UPB_XSD = """
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
