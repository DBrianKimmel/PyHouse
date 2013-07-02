=======
PyHouse
=======

PyHouse is a home automation tool.

It is written to become a daemon on a Linux computer.

It is now (2013-06-06) running in a raspberry pi model B.  It has been turning
lights on and off reliably for several weeks on this new platform.

See __init__ module for developer documentation.


Lighting
--------
One of the first of the components is a Lighting system.
The goal of this component is to automate the daily lighting system.
There is a schedule associated with the lighting system and its purpose
is to turn lights on and off at various times of the day and night.

The system was developed around the Insteon lighting controls.  There is also
the beginnings of a UPB system included along with X-10 beginnings.  Some of
the controllers used for development are serial connections with the computer
while the newer controllers are USB connections.


HVAC
----
The HVAC system is being added to allow the schedule of the lighting system
to control the house's heating and air conditioning.


UPnP
----
UPnP is being developed and added as a separate control mechanism for the
lighting system as well as entertainment


Entertainment
-------------
The entertainment component is to allow the control of the house TV, Radio
and other similar devices via UPnP.


Communication
-------------
The communication component will include telephone, cell phone, fax, email etc.



### END
