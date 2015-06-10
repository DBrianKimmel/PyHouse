"""
This package is used for MQTT communications.

A section of the PyHouse Object (Mqtt) is reserverd for holding the information.

broker.py is the main interface to the MQTT system.

Multilpe Brokers.
-----------------

While nultiple brokers may be defined and used, There is no mechanism to be sure the
information is the same for all brokers.

As a first implementation, all that will be used is the first broker.
Further development may use the other brokers that may be defined.

Passing broker information via Mqtt itself may allow for synchronization of the broker tree.

XML routines will read/write all brokers in the XML configuration file.
Only Broker[0] will be used at the moment.

"""