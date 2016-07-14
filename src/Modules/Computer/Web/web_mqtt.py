"""
@name:      PyHouse/src/Modules/Web/web_mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 18, 2015
@Summary:

"""

__updated__ = '2016-07-14'

# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.Core.data_objects import MqttBrokerData
from Modules.Computer.Web.web_utils import JsonUnicode, GetJSONComputerInfo
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.uuid_tools import Uuid

LOG = Logger.getLogger('PyHouse.webMqtt     ')

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')


class MqttElement(athena.LiveElement):
    """ a 'live' thermostat element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'mqttElement.html'))
    jsClass = u'mqtt.MqttWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getServerData(self):
        l_json = GetJSONComputerInfo(self.m_pyhouse_obj)
        return l_json

    @athena.expose
    def saveMqttData(self, p_json):
        """Mqtt data is returned, so update the info.
        """
        l_json = JsonUnicode().decode_json(p_json)
        l_delete = l_json['Delete']
        l_ix = int(l_json['Key'])
        if l_delete:
            try:
                del self.m_pyhouse_obj.Computer.Mqtt.Brokers
            except AttributeError:
                LOG.error("web_mqtt - Failed to delete - JSON: {0:}".format(l_json))
            return
        try:
            l_obj = self.m_pyhouse_obj.Computer.Mqtt.Brokers[l_ix]
        except KeyError:
            LOG.warning('Creating a new Mqtt Broker Key: {}'.format(l_ix))
            l_obj = MqttBrokerData()
        #
        LOG.info('JSON {}'.format(l_json))
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_ix
        l_obj.UUID = Uuid.make_valid(l_json['UUID'])
        l_obj.BrokerAddress = l_json['BrokerAddress']
        l_obj.BrokerPort = l_json['BrokerPort']
        self.m_pyhouse_obj.Computer.Mqtt.Brokers[l_obj.Key] = l_obj

# ## END DBK
