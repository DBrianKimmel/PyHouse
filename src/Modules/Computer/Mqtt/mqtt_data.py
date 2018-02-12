"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Computer/Mqtt/mqtt_data.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/Mqtt/mqtt_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@note:      Created on Feb 11, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2018-02-11'

#  Import system type stuff

#  Import PyMh files
from Modules.Core.data_objects import BaseObject


class MqttBrokerData(BaseObject):
    """ 0-N

    ==> PyHouse.Computer.Mqtt.Brokers.XXX as in the def below
    """

    def __init__(self):
        super(MqttBrokerData, self).__init__()
        self.BrokerName = None
        self.BrokerAddress = None
        self.BrokerPort = None
        self.UserName = ''
        self.Password = None
        self.Class = 'Local'
        self.ClientID = 'PyH-'
        self.Keepalive = 60
        self._ClientAPI = None
        self._ProtocolAPI = None
        self._isTLS = False

# ## END DBK
