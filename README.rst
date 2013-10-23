=======
PyHouse
=======

PyHouse is a home automation tool.

See __init__ module for developer documentation.


What is PyHouse?
----------------
PyHouse is one or more nodes, running PyHouse software, and co-operating with
other nodes either in the same domain or in in affiliated domains.

Nodes
-----
Each node is a separate computer that will self boot, start the PyHouse software
and begin the operations configured for that node.  Nodes can communicate with
each other using IP-v6 over some common media such as Ethernet or Wi-Fi.

It is now (2013-06-06) running in a raspberry pi model B.  It has been turning
lights on and off reliably for several weeks on this new platform.

Domains
-------
Domains are a group of nodes that are able to communicate with each other and
have been given authentication tokens to allow them to share information.
This will allow two condominiums to be independent of each other and two houses
separated by many miles to cooperate with each other.

Configuration
-------------
Each node is initially self configured via its own web server.  The configuration
is stored as xml in a file somewhere in the file system of the node.  This
configuration also has current status stored in the file.  This allows the
node to have a reboot and continue operations.  Some status information may be
lost as there is no attempt to be a real-time node.


=======
Modules
=======

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
