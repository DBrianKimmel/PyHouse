@name:      PyHouse/Project/src/Modules/Housing/Entertainment/Docs/Design
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Sep 30, 2018
@license:   MIT License
@summary:   This is the design documentation for the Entertainment Module of PyHouse.

Design
======

The entertainment is a load on demand module.
In a running instance of PyHouse only the sub-modules that are defined in the config file are loaded.
This makes it sort of a plugin system.
This lowers the memory footprint of the system.  Since there are a lot of different entertainment device modules,
this will be a big savings of memory.

This module is message driven.  A Mqtt message is sent to entertainment.py and it dispatches it to the appropriate module.
These messages have topics that begin with:
		pyhouse/house name/entertainment/...

The modules may return a status message, control other submodules or ...


===== _Connector ===== <class 'twisted.internet.tcp.Connector'>
Obj:_addressType            <class 'twisted.internet.address.IPv4Address'> .
Obj:_makeTransport          <bound method Connector._makeTransport of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:bindAddress             None .
Obj:buildProtocol           <bound method BaseConnector.buildProtocol of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:cancelTimeout           <bound method BaseConnector.cancelTimeout of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:connect                 <bound method BaseConnector.connect of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:connectionFailed        <bound method BaseConnector.connectionFailed of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:connectionLost          <bound method BaseConnector.connectionLost of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:disconnect              <bound method BaseConnector.disconnect of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:factory                 <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f226af526d8> .
Obj:factoryStarted          1 .
Obj:getDestination          <bound method Connector.getDestination of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:host                    192.168.9.121 .
Obj:port                    8102 .
Obj:reactor                 <twisted.internet.epollreactor.EPollReactor object at 0x7f226abfde80> .
Obj:state                   connecting .
Obj:stopConnecting          <bound method BaseConnector.stopConnecting of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:timeout                 30 .
Obj:timeoutID               <DelayedCall 0x7f22669d5160 [29.99857497215271s] called=0 cancelled=0 _BaseBaseClient.failIfNotConnected(TimeoutError('',))> .
Obj:transport               <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f22669d50f0> .


### END DBK
