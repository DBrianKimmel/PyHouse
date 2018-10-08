* Name:      PyHouse/Project/src/Modules/Housing/Entertainment/pioneer/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-09-30
* Updated:   2018-10-04
* License:   MIT License
* Summary:   This is the design documentation for the Entertainment Module of PyHouse.


# Pioneer


## Design

The pioneer module (so far) is kind of a passive module.
It gets set up when the XML defines one or more Pioneer devices.

Then it sends out a Mqtt status message declaring the status when first connected to.]
It then waits for a control message.
Control messages can come from services sch as Pandora, or from a Node-Red dashboard triggering something.

The pioneer device I have does not wake up from a TCP connection.

There is the possibility of having more than one pioneer devices in a house.
The name of the devide is used for the key.
Be sure to configure the name to be unique and reference the name in the services.


## XML / Config

<PioneerSection Active="True">
	<Type>Component</Type>
	<Device Active="True" Key="0" Name="822-k">
		<Comment>X-822-K Receiver</Comment>
		<UUID>dc575f69-85ee-11e8-8a4d-a08cfd2fc483</UUID>
		<CommandSet>2015</CommandSet>
		<IPv4>192.168.9.121</IPv4>
		<Port>8102</Port>
		<Room>Living Room</Room>
		<Type>Receiver</Type>
	</Device>
</PioneerSection>


### _Connector
===== _Connector ===== <class 'twisted.internet.tcp.Connector'>
Obj:_addressType            <class 'twisted.internet.address.IPv4Address'> .
Obj:_makeTransport          <bound method Connector._makeTransport of <twisted.internet.tcp.Connector object at 0x7f1963b4b3c8>> .
Obj:bindAddress             None .
Obj:buildProtocol           <bound method BaseConnector.buildProtocol of <twisted.internet.tcp.Connector object at 0x7f1963b4b3c8>> .
Obj:cancelTimeout           <bound method BaseConnector.cancelTimeout of <twisted.internet.tcp.Connector object at 0x7f1963b4b3c8>> .
Obj:connect                 <bound method BaseConnector.connect of <twisted.internet.tcp.Connector object at 0x7f1963b4b3c8>> .
Obj:connectionFailed        <bound method BaseConnector.connectionFailed of <twisted.internet.tcp.Connector object at 0x7f1963b4b3c8>> .
Obj:connectionLost          <bound method BaseConnector.connectionLost of <twisted.internet.tcp.Connector object at 0x7f1963b4b3c8>> .
Obj:disconnect              <bound method BaseConnector.disconnect of <twisted.internet.tcp.Connector object at 0x7f1963b4b3c8>> .
Obj:factory                 <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8> .
Obj:factoryStarted          1 .
Obj:getDestination          <bound method Connector.getDestination of <twisted.internet.tcp.Connector object at 0x7f1963b4b3c8>> .
Obj:host                    192.168.9.121 .
Obj:port                    8102 .
Obj:reactor                 <twisted.internet.epollreactor.EPollReactor object at 0x7f1967db00b8> .
Obj:state                   connecting .
Obj:stopConnecting          <bound method BaseConnector.stopConnecting of <twisted.internet.tcp.Connector object at 0x7f1963b4b3c8>> .
Obj:timeout                 30 .
Obj:timeoutID               <DelayedCall 0x7f1963b4b5c0 [29.998800039291382s] called=0 cancelled=0 _BaseBaseClient.failIfNotConnected(TimeoutError('',))> .
Obj:transport               <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470> .


### _Factory
===== _Factory ===== <class 'Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory'>
Obj:_callID                 None .
Obj:buildProtocol           <bound method PioneerFactory.buildProtocol of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:clientConnectionFailed  <bound method PioneerFactory.clientConnectionFailed of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:clientConnectionLost    <bound method PioneerFactory.clientConnectionLost of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:clock                   None .
Obj:connectionLost          <bound method PioneerFactory.connectionLost of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:connector               None .
Obj:continueTrying          1 .
Obj:delay                   1.0 .
Obj:doStart                 <bound method Factory.doStart of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:doStop                  <bound method Factory.doStop of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:factor                  2.718281828459045 .
Obj:forProtocol             <bound method Factory.forProtocol of <class 'Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory'>> .
Obj:initialDelay            1.0 .
Obj:jitter                  0.11962656472 .
Obj:logPrefix               <bound method Factory.logPrefix of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:m_pioneer_device_obj    <Modules.Housing.Entertainment.pioneer.pioneer.PioneerDeviceData object at 0x7f1963b444a8> .
Obj:m_pyhouse_obj           <Modules.Core.data_objects.PyHouseData object at 0x7f19639fd400> .
Obj:makeConnection          <bound method PioneerFactory.makeConnection of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:maxDelay                3600 .
Obj:maxRetries              None .
Obj:noisy                   True .
Obj:numPorts                1 .
Obj:protocol                None .
Obj:resetDelay              <bound method ReconnectingClientFactory.resetDelay of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:retries                 0 .
Obj:retry                   <bound method ReconnectingClientFactory.retry of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:startFactory            <bound method Factory.startFactory of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:startedConnecting       <bound method PioneerFactory.startedConnecting of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:stopFactory             <bound method Factory.stopFactory of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .
Obj:stopTrying              <bound method ReconnectingClientFactory.stopTrying of <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f19681056d8>> .


### Transport
===== _Transport ===== <class 'twisted.internet.tcp.Client'>
Obj:SEND_LIMIT              131072 .
Obj:TLS                     False .
Obj:_aborting               False .
Obj:_addressType            <class 'twisted.internet.address.IPv4Address'> .
Obj:_base                   <class 'twisted.internet.tcp.Connection'> .
Obj:_closeSocket            <bound method _SocketCloser._closeSocket of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:_closeWriteConnection   <bound method Connection._closeWriteConnection of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:_collectSocketDetails   <bound method BaseClient._collectSocketDetails of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:_commonConnection       <class 'twisted.internet.tcp.Connection'> .
Obj:_connectDone            <bound method BaseClient._connectDone of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:_dataReceived           <bound method Connection._dataReceived of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:_finishInit             <bound method _BaseBaseClient._finishInit of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:_getLogPrefix           <bound method _LogOwner._getLogPrefix of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:_isSendBufferFull       <bound method FileDescriptor._isSendBufferFull of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:_maybePauseProducer     <bound method FileDescriptor._maybePauseProducer of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:_postLoseConnection     <bound method FileDescriptor._postLoseConnection of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:_requiresResolution     False .
Obj:_setRealAddress         <bound method _BaseBaseClient._setRealAddress of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:_shouldShutdown         True .
Obj:_stopReadingAndWriting  <bound method BaseClient._stopReadingAndWriting of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:_tempDataBuffer         [] .
Obj:_tempDataLen            0 .
Obj:_tlsClientDefault       True .
Obj:_writeDisconnected      False .
Obj:_writeDisconnecting     False .
Obj:abortConnection         <bound method _AbortingMixin.abortConnection of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:addr                    ('192.168.9.121', 8102) .
Obj:addressFamily           AddressFamily.AF_INET .
Obj:bufferSize              65536 .
Obj:connected               1 .
Obj:connectionLost          <bound method _BaseBaseClient.connectionLost of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:connector               <twisted.internet.tcp.Connector object at 0x7f1963b4b3c8> .
Obj:createInternetSocket    <bound method BaseClient.createInternetSocket of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:dataBuffer              b'' .
Obj:disconnected            0 .
Obj:disconnecting           0 .
Obj:doConnect               <bound method BaseClient.doConnect of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:doRead                  <bound method Connection.doRead of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:doWrite                 <bound method FileDescriptor.doWrite of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:failIfNotConnected      <bound method _BaseBaseClient.failIfNotConnected of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:fileno                  <built-in method fileno of socket object at 0x7f19639bbfa8> .
Obj:getHandle               <bound method Connection.getHandle of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:getHost                 <bound method _BaseTCPClient.getHost of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:getPeer                 <bound method _BaseTCPClient.getPeer of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:getTcpKeepAlive         <bound method Connection.getTcpKeepAlive of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:getTcpNoDelay           <bound method Connection.getTcpNoDelay of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:logPrefix               <bound method Connection.logPrefix of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:logstr                  PioneerClient,client .
Obj:loseConnection          <bound method ConnectionMixin.loseConnection of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:loseWriteConnection     <bound method FileDescriptor.loseWriteConnection of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:offset                  0 .
Obj:pauseProducing          <bound method FileDescriptor.pauseProducing of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:producer                None .
Obj:producerPaused          False .
Obj:protocol                <Modules.Housing.Entertainment.pioneer.pioneer.PioneerClient object at 0x7f1963b4f358> .
Obj:reactor                 <twisted.internet.epollreactor.EPollReactor object at 0x7f1967db00b8> .
Obj:readConnectionLost      <bound method Connection.readConnectionLost of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:realAddress             ('192.168.9.121', 8102) .
Obj:registerProducer        <bound method ConnectionMixin.registerProducer of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:resolveAddress          <bound method _BaseBaseClient.resolveAddress of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:resumeProducing         <bound method FileDescriptor.resumeProducing of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:setTcpKeepAlive         <bound method Connection.setTcpKeepAlive of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:setTcpNoDelay           <bound method Connection.setTcpNoDelay of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:socket                  <socket.socket fd=13, family=AddressFamily.AF_INET, type=2049, proto=0, laddr=('192.168.9.50', 39308), raddr=('192.168.9.121', 8102)> .
Obj:socketType              SocketKind.SOCK_STREAM .
Obj:startReading            <bound method FileDescriptor.startReading of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:startTLS                <bound method ConnectionMixin.startTLS of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:startWriting            <bound method FileDescriptor.startWriting of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:stopConnecting          <bound method _BaseBaseClient.stopConnecting of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:stopConsuming           <bound method FileDescriptor.stopConsuming of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:stopProducing           <bound method FileDescriptor.stopProducing of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:stopReading             <bound method FileDescriptor.stopReading of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:stopWriting             <bound method FileDescriptor.stopWriting of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:streamingProducer       False .
Obj:unregisterProducer      <bound method ConnectionMixin.unregisterProducer of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:write                   <bound method ConnectionMixin.write of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:writeConnectionLost     <bound method FileDescriptor.writeConnectionLost of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:writeSequence           <bound method ConnectionMixin.writeSequence of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .
Obj:writeSomeData           <bound method Connection.writeSomeData of <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f1963b4b470>> .


### END DBK
