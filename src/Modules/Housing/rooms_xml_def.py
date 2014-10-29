"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Housing/rooms_xml_def.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Oct 26, 2014
@Summary:

"""

ROOMS_XML = """
<RoomSection>
    <Room Active="True" Key="0" Name="Master Bath">
        <Comment>Test Comment</Comment>
        <Corner>0.50, 10.50</Corner>
        <Size>14.00, 13.50</Size>
    </Room>
    <Room Active="True" Key="1" Name="Master Bed Closet 1">
        <Comment />
        <Corner>0.83, 24.58</Corner>
        <Size>6.91, 8.91</Size>
    </Room>
    <Room Active="False" Key="2" Name="Master Bedroom">
        <Comment />
        <Corner>0.83, 25.08</Corner>
        <Size>14.00, 18.00</Size>
    </Room>
    <Room Active="False" Key="3" Name="Master Sitting Room">
        <Comment />
        <Corner>0.83, 54.16</Corner>
        <Size>14.00, 8.00</Size>
    </Room>
</RoomSection>
"""

ROOMS_XSD = """

<xs:element name='RoomSection >
    <xs:complexType>
    </xs:complexType>
</xs:element name='RoomSection >


    <xs:sequence>
        <xs:element name='Comment' type='xs:string' />
        <xs:element name='Corner' type='xs:string' />
        <xs:element name='Size' type='xs:string' />
    </xs:sequence>





<xs:complexType name="RoomSection">
    <xs:simpleContent>
    </xs:simpleContent>
    <xs:sequence>
        <xs:element name="Comment" type="xs:string"/>
        <xs:element name="Corner" type="xs:string"/>
        <xs:element name="Size" type="xs:string"/>
    </xs:sequence>
</xs:complexType>
"""

# ## END DBK
