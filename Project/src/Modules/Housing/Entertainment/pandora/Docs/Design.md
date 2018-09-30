@name:      PyHouse/Project/src/Modules/Housing/Entertainment/pandora/Docs/Design
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Sep 30, 2018
@license:   MIT License
@summary:   This is the design documentation for thePandora Module of PyHouse.

Design
======

The pandora module will recieve a control message and perform the action:
These messages have topics that begin with:
		pyhouse/house name/entertainment/pandora/<action>
	where <action> is control, status

.../control msg=on will have side effects of turning on and setting the "ConnectionName" device.

XML
===

<PandoraSection Active="True">
    <Type>Service</Type>
    <Device Active="True" Key="0" Name="Running on pi-06-ct ">
        <Comment>Living Room</Comment>
        <Host>192.168.9.16</Host>
        <Type>Service</Type>
        <ConnectionName>Pioneer</ConnectionName>
        <InputName>CD</InputName>
        <InputCode>01FN</InputCode>
        <Volume>47</Volume>
    </Device>
</PandoraSection>


### END DBK
