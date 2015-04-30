"""
@name:      C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Computer/Nodes/node_mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 28, 2015
@Summary:


topic scheme:
    PyHouse/<Domain UUID>/<HouseIdentifier>/<Device Specific>
    Where <Device Specific> is:
        <Location>/<Function>/<Action>
            <Location> = Room Name or some other description
            <Function> = Temperature, LightLevel, HumanDetected, Rainfall, WindSpeed etc.
            <Action> = Reading, TurnOn, TurnOff to list a few.
    There are no spaces in any of the sections.


<mqtt>
    <BrokerIp4 />
    <BrokerIp6 />
</mqtt>

"""


# ## END DBK
