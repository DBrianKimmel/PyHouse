=======
PyHouse
=======

PyHouse is a home automation tool.

See src.__init__ module for developer documentation.
Also see the Docs directories throught the code.


This Git repository (PyHouse) is for the software that runs PyHouse,
There is a companion repository (SysAdmin) that is for the rather complex task of
setting up Raspberry Pis to run PyHouse.

Both of these repositories are on GitHub under the user DBrianKimmel.


What is PyHouse?
----------------
PyHouse is one or more nodes, running PyHouse software, and co-operating with
other nodes either in the same domain or in in affiliated domains.

PyHouse attempts to avoid 'Islands of Automation' by integrating all the modules
under one "Roof".

The "Official" language of PyHouse is English.  All documents will be in this language
but there may be translations to any other language.

There is a hierarchy here.  At it's current level the Internet is the top level for
control and logging of things in which PyHouse is interested.  The information scheme
used by PyHouse is MQTT.

The first level of MQTT topic is "pyhouse".  This will us to keep all the information
in one virtual tree.  

The second level is used by each person or group using PyHouse and is known as the
"Domain" level.  Therefore the topic so far is "pyhouse/domain/".  The domain name
should probably be a UUID in order to keep from choosing a name and finding out that
the name is already in use.  Each domain should have a scheme of encrypting the
information within that domain to keep things private.

The Third level is used by a person or group to designate a house or equivalent
within the domain.  Now the MQTT topic is "pyhouse/domain UUID/House UUID/".
A UUID looks like "c15f7d76-092e-11e4-bffa-b827eb189eb4".


Domains
-------
Domains are a group of nodes that are able to communicate with each other and
have been given authentication tokens to allow them to share information.
This will allow two adjacent Town Houses to be independent of each other and two houses
separated by many miles to cooperate with each other.


Nodes
-----
Each node is a separate computer that will self boot, start the PyHouse software
and begin the operations configured for that node.  Nodes can communicate with
each other using IP-V6 over some common media such as Ethernet or Wi-Fi.

It is now (2013-06-06) running in a raspberry pi model B.  It has been turning
lights on and off reliably for several weeks on this new platform.


Configuration
-------------
Each node is initially self configured via its own web server.  The configuration
is stored as XML in a file somewhere in the file system of the node.  This
configuration also has current status stored in the file.  This allows the
node to have a reboot and continue operations.  Some status information may be
lost as there is no attempt to be a real-time node.

Configuration files are being split out of the master file and into "Module" files.
Each module is about equivalent to a python package.


Organization
------------

PyHouse is a twisted application.  That is it uses the Twisted-Python framework
to implement its basic structure.  This allows an event loop to control the various
services in a totally asynchronous manner, the lighting system is independent of
the entertainment system and so on.

As we move from a Desktop/Server to small (Raspberry Pi) computers, we are moving
toward having each node load only the parts of the software that it needs.  There is
no real need to hve each node load the entire PyHouse software.


Requirements
------------

Python 2.7 (awaiting twisted to work with version 3.x)
Twisted 13.2.0



=======
Systems
=======


Lighting
--------
One of the first of the components to be programmed is a Lighting system.
The goal of this component is to automate the daily lighting system.
There is a schedule associated with the lighting system and its purpose
is to turn lights on and off at various times of the day and night.

The system was developed around the Insteon lighting controls.  There is also
the beginnings of a UPB system included along with X-10 beginnings.  Some of
the controllers used for development are serial connections with the computer
while the newer controllers are USB connections.

There are currently four pieces of the lighting system.  The first of these is
the Controller.

The controller is the computer interface into the lighting system,  It talks to
the computer via one of the drivers.  Most seem to use a serial interface.  The
controllers then communicate with the rest of the lighting system.

The second component is the light itself.  These are either a replacement switch
that is installed in the wall and replaces the standard light switch, or a 
module that plugs into an electrical outlet and controls a device plugged into
the module.

The third component is a switch.  This is a module with one or more buttons that
is not directly connected to a light.  The buttons send signals to the controller
and other lights to turn lights off and on.

The fourth component is a scene.  Scenes are logical rather than physical.  A
scene can control several lights at once and are usually associated with an
action.  A scene could be 'All lights On' for an emergency or 'In Bed' for
night time sleeping.


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

Also there is a Pandora node.  It uses a Pi with a PiFaceCad card.  The node
plugs into a receiver/amplifier and plays Pandora radio streams through the
houses speaker system.  The IR receiver picks up remote signals and starts and
stops the PianoBar process to stream music.


Communication
-------------
The communication component will include telephone, cell phone, fax, email etc.



2015-04-22 UPDATE.
I am tired of some people and companies releasing individual modules of something
to do with Home Automation.

We do NOT need more "Islands of Automation".

I am, therefore, creating a bunch of small projects based on Arduino type microcontrollers to
be interfaced easily into PyHouse.  It is my hope that a complete Home Automation system will
be the result.


### END DBK
