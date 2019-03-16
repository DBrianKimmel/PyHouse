"""
-*- test-case-name: PyHouse/src/Modules/Families/Hue/Hue_data.py -*-

@name:      PyHouse/src/Modules/Families/Hue/Hue_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2019-03-15'

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import DeviceData
from Modules.Housing.Lighting.lighting_lights import LightData

"""
{
    '1': {
        'action': {
            'alert': 'none',
            'bri': 254,
            'on': False
        },
        'class': 'Living room',
        'lights': ['1'],
        'name': 'Living room',
        'recycle': False,
        'sensors': [],
        'state': {
            'all_on': False,
            'any_on': False
        },
        'type': 'Room'
    },
    '2': {
        'action': {
            'alert': 'none',
            'bri': 254,
            'on': False
        },
        'class': 'Office',
        'lights': ['2'],
        'name': 'Office',
        'recycle': False,
        'sensors': [],
        'state': {
            'all_on': False,
            'any_on': False
        },
        'type': 'Room'
    }
}
"""


class HueData(LightData):
    """
    This is known only within the Hue family package.

    {
        '1': {
            'capabilities': {
                'certified': True,
                'control': {
                    'maxlumen': 840,
                    'mindimlevel': 5000
                },
                'streaming': {
                    'proxy': False,
                    'renderer': False
                }
            },
            'config': {
                'archetype': 'classicbulb',
                'direction': 'omnidirectional',
                'function': 'functional',
                'startup': {
                    'configured': True,
                    'mode': 'safety'
                }
            },
            'manufacturername': 'Philips',
            'modelid': 'LWB014',
            'name': 'Living room floor lamp',
            'productid': 'Philips-LWB014-1-A19DLv3',
            'productname': 'Hue white lamp',
            'state': {
                'alert': 'none',
                'bri': 254,
                'mode': 'homeautomation',
                'on': False,
                'reachable': True
            },
            'swconfigid': 'E790821B',
            'swupdate': {
                'lastinstall': '2018-12-08T08:29:20',
                'state': 'noupdates'
            },
            'swversion': '1.46.13_r26312',
            'type': 'Dimmable light',
            'uniqueid': '00:17:88:01:02:83:69:39-0b'
        },
        '2': {
            'capabilities': {
                'certified': True,
                'control': {
                    'maxlumen': 840,
                    'mindimlevel': 5000
                },
                'streaming': {
                    'proxy': False,
                    'renderer': False
                }
            },
            'config': {
                'archetype': 'classicbulb',
                'direction': 'omnidirectional',
                'function': 'functional',
                'startup': {
                    'configured': True,
                    'mode': 'safety'
                }
            },
            'manufacturername': 'Philips',
            'modelid': 'LWB014',
            'name': 'Office lamp',
            'productid': 'Philips-LWB014-1-A19DLv3',
            'productname': 'Hue white lamp',
            'state': {
                'alert': 'none',
                'bri': 254,
                'mode': 'homeautomation',
                'on': False,
                'reachable': True
            },
            'swconfigid': 'E790821B',
            'swupdate': {
                'lastinstall': '2018-12-08T08:28:14',
                'state': 'noupdates'
            },
            'swversion': '1.46.13_r26312',
            'type': 'Dimmable light',
            'uniqueid': '00:17:88:01:02:80:90:96-0b'
        }
    }

    """

    def __init__(self):
        super(HueData, self).__init__()
        self.DeviceFamily = 'Hue'
        self.HueLightIndex = 0


class HueHubData(DeviceData):
    """
    {
        'UTC': '2019-02-26T18:51:09',
        'apiversion': '1.29.0',
        'backup': {
            'errorcode': 0,
            'status': 'idle'
        },
        'bridgeid': '001788FFFE68688F',
        'datastoreversion': '76',
        'dhcp': True,
        'factorynew': False,
        'gateway': '192.168.1.1',
        'internetservices': {
            'internet': 'connected',
            'remoteaccess': 'connected',
            'swupdate': 'connected',
            'time': 'connected'
        },
        'ipaddress': '192.168.1.131',
        'linkbutton': False,
        'localtime': '2019-02-26T13:51:09',
        'mac': '00:17:88:68:68:8f',
        'modelid': 'BSB002',
        'name': 'Philips hue',
        'netmask': '255.255.255.0',
        'portalconnection': 'connected',
        'portalservices': True,
        'portalstate': {
            'communication': 'disconnected',
            'incoming': False,
            'outgoing': True,
            'signedon': True
        },
        'proxyaddress': 'none',
        'proxyport': 0,
        'replacesbridgeid': None,
        'starterkitid': '',
        'swupdate': {
            'checkforupdate': False,
            'devicetypes': {
                'bridge': False,
                'lights': [],
                'sensors': []
            },
            'notify': True,
            'text': '',
            'updatestate': 0,
            'url': ''
        },
        'swupdate2': {
            'autoinstall': {
                'on': True,
                'updatetime': 'T03:00:00'
            }, 'bridge': {
                'lastinstall': '2019-02-16T08:38:09',
                'state': 'noupdates'
            },
            'checkforupdate': False,
            'lastchange': '2019-02-16T08:40:27',
            'state': 'noupdates'
        },
        'swversion': '1901181309',
        'timezone': 'America/New_York',
        'whitelist': {
            'MBFBC-agf6rq5bsWcxLngYZoClGr2pw2oKEMLZgs': {
                'create date': '2017-12-19T14:57:47',
                'last use date': '2019-02-26T18:51:09'
                'name': 'my_hue_app#iphone peter'
            },
            'OJpVv10mFcBWKEF8niBOZik2YXMhhGeSMOfg5Rww': {
                'create date': '2017-12-16T20:28:13',
                'last use date': '2019-02-26T08:23:07',
                'name': 'Echo'
            },
            'Q4IeJmi312IYLKeOdK8zgTxY9iRwSFjGpXWs52f9': {
                'create date': '2017-12-16T20:28:14',
                'last use date': '2019-02-13T06:21:34',
                'name': 'hue-alexa-smarthome-skill-v1'
            },
            'XpfmU-zBwUyGrDq7VW-5muXVmTkn1aZpe4x2Ef-j': {
                'create date': '2017-12-16T18:47:10',
                'last use date': '2018-02-25T02:47:54',
                'name': 'Hue 2#Samsung SM-G930P'
            }
        },
        'zigbeechannel': 25
    }

    """

    def __init__(self):
        super(HueHubData, self).__init__()
        self.DeviceType = 4
        self.ApiKey = 'None defined'


class HueAddInData(object):
    """ This is the Hue specific data.
    It will be added into device objects that are Hue.
    """

    def __init__(self):
        self.ApiKey = None


class HueueQueue(object):
    """ This is the contents of a Queue Entry
    """

    def __init__(self):
        self.Uri = None
        self.Command = None  # for convenience
        self.Headers = None
        self.Payload = None

# ## END DBK
