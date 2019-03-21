* Name:      PyHouse/Project/src/Modules/Families/Hue/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-03-19
* Updated:   2019-03-19
* License:   MIT License
* Summary:   This is the design for Hue Hub.

#Hue

##Config

```json
{
	"name":"Philips hue",
	"zigbeechannel"25,
	"bridgeid":"001788FFFE68688F",
	"mac":"00:17:88:68:68:8f",
	"dhcp":true,
	"ipaddress":"192.168.1.131",
	"netmask":"255.255.255.0",
	"gateway":"192.168.1.1",
	"proxyaddress":"none",
	"proxyport":0,
	"UTC":"2019-03-20T00:18:19",
	"localtime":"2019-03-19T20:18:19",
	"timezone":"America/New_York",
	"modelid":"BSB002",
	"datastoreversion":"76",
	"swversion":"1901181309",
	"apiversion":"1.29.0",
	"swupdate":{
		"updatestate":0,
		"checkforupdate":false,
		"devicetypes":{
			"bridge":false,
			"lights":[],
			"sensors":[]
		},
		"url":"",
		"text":"",
		"notify":true
	},
	"swupdate2":{
		"checkforupdate":false,
		"lastchange":"2019-02-16T08:40:27",
		"bridge":{
			"state":"noupdates",
			"lastinstall":"2019-02-16T08:38:09"
		},
		"state":"noupdates",
		"autoinstall":{
			"updatetime":"T03:00:00",
			"on":true
		}
	},
	"linkbutton":false,
	"portalservices":true,
	"portalconnection":"connected",
	"portalstate":{
		"signedon":true,
		"incoming":false,
		"outgoing":true,
		"communication":"disconnected"
	},
	"internetservices":{
		"internet":"connected",
		"remoteaccess":"connected",
		"time":"connected",
		"swupdate":"connected"
	},
	"factorynew":false,
	"replacesbridgeid":null,
	"backup":{
		"status":"idle",
		"errorcode":0
	},
	"starterkitid":"",
	"whitelist":{
		"XpfmU-zBwUyGrDq7VW-5muXVmTkn1aZpe4x2Ef-j":{
			"last use date":"2018-02-25T02:47:54",
			"create date":"2017-12-16T18:47:10",
			"name":"Hue 2#Samsung SM-G930P"
		},
		"OJpVv10mFcBWKEF8niBOZik2YXMhhGeSMOfg5Rww":{
			"last use date":"2019-03-19T23:00:10",
			"create date":"2017-12-16T20:28:13",
			"name":"Echo"
		},
		"Q4IeJmi312IYLKeOdK8zgTxY9iRwSFjGpXWs52f9":{
			"last use date":"2019-02-13T06:21:34",
			"create date":"2017-12-16T20:28:14",
			"name":"hue-alexa-smarthome-skill-v1"
		},
		"MBFBC-agf6rq5bsWcxLngYZoClGr2pw2oKEMLZgs":{
			"last use date":"2019-03-20T00:18:19",
			"create date":"2017-12-19T14:57:47",
			"name":"my_hue_app#iphone peter"
		}
	}
}
```

## Lights

```json
{
    "1":{
        "name":"Living room floor lamp",
        "manufacturername":"Philips",
        "productname":"Hue white lamp",
        "type":"Dimmable light",
        "modelid":"LWB014",
        "uniqueid":"00:17:88:01:02:83:69:39-0b",
        "swversion":"1.46.13_r26312",
        "swconfigid":"E790821B",
        "productid":"Philips-LWB014-1-A19DLv3"
        "state":{
            "on":false,
            "bri":254,
            "alert":"none",
            "mode":"homeautomation",
            "reachable":true
        },
        "swupdate":{
            "state":"noupdates",
            "lastinstall":"2018-12-08T08:29:20"
        },
        "capabilities":{
            "certified":true,
            "control":{
                "mindimlevel":5000,
                "maxlumen":840
            },
            "streaming":{
                "renderer":false,
                "proxy":false
            }
        },
        "config":{
            "archetype":"classicbulb",
            "function":"functional",
            "direction":"omnidirectional",
            "startup":{
                "mode":"safety",
                "configured":true
            }
        },
    },
    "2":{
        "state":{
            "on":false,
            "bri":254,
            "alert":"none",
            "mode":"homeautomation",
            "reachable":true
        },
        "swupdate":{
            "state":"noupdates",
            "lastinstall":"2018-12-08T08:28:14"
        },
        "type":"Dimmable light",
        "name":"Office lamp",
        "modelid":"LWB014",
        "manufacturername":"Philips",
        "productname":"Hue white lamp",
        "capabilities":{
            "certified":true,
            "control":{
                "mindimlevel":5000,
                "maxlumen":840
            },
            "streaming":{
                "renderer":false,
                "proxy":false
            }
        },
        "config":{
            "archetype":"classicbulb",
            "function":"functional",
            "direction":"omnidirectional",
            "startup":{
                "mode":"safety",
                "configured":true
            }
        },
        "uniqueid":"00:17:88:01:02:80:90:96-0b",
        "swversion":"1.46.13_r26312",
        "swconfigid":"E790821B",
        "productid":"Philips-LWB014-1-A19DLv3"
    }
}
```

## Groups

```json
{
	"1":{
		"name":"Living room",
		"lights":["1"],
		"sensors":[],
		"type":"Room",
		"state":{
			"all_on":true,
			"any_on":true
		},
		"recycle":false,
		"class":"Living room",
		"action":{
			"on":true,
			"bri":254,
			"alert":"none"
		}
	},
	"2":{
		"name":"Office",
		"lights":["2"],
		"sensors":[],
		"type":"Room",
		"state":{
			"all_on":false,
			"any_on":false
		},
		"recycle":false,
		"class":"Office",
		"action":{
			"on":false,
			"bri":254,
			"alert":"none"
		}
	}
}
```

## Schedules

```json
none
```

## Scenes

```json
{
	"ReanQJmt8t8kpQf":{
		"name":"Nightlight",
		"type":"GroupScene",
		"group":"1",
		"lights":["1"],
		"owner":"XpfmU-zBwUyGrDq7VW-5muXVmTkn1aZpe4x2Ef-j",
		"recycle":false,
		"locked":false,
		"appdata":{
			"version":1,
			"data":"0Vunz_r01_d07"
		},
		"picture":"",
		"lastupdated":"2017-12-16T19:34:03",
		"version":2
	},
	"5JHIXGY3qOO2eKj":{
		"name":"Dimmed",
		"type":"GroupScene",
		"group":"1",
		"lights":["1"],
		"owner":"XpfmU-zBwUyGrDq7VW-5muXVmTkn1aZpe4x2Ef-j",
		"recycle":false,
		"locked":false,
		"appdata":{
			"version":1,
			"data":"9TVyd_r01_d06"
		},
		"picture":"",
		"lastupdated":"2017-12-16T19:34:04",
		"version":2
	},
	"ICYiBJAufd4tYAp":{
		"name":"Bright",
		"type":"GroupScene",
		"group":"1",
		"lights":["1"],
		"owner":"XpfmU-zBwUyGrDq7VW-5muXVmTkn1aZpe4x2Ef-j",
		"recycle":false,
		"locked":false,
		"appdata":{
			"version":1,
			"data":"01zpa_r01_d05"
		},
		"picture":"",
		"lastupdated":"2017-12-16T19:34:04",
		"version":2
	},
	"St03AsHCLBt8huT":{
		"name":"Dimmed",
		"type":"GroupScene",
		"group":"2",
		"lights":["2"],
		"owner":"XpfmU-zBwUyGrDq7VW-5muXVmTkn1aZpe4x2Ef-j",
		"recycle":false,
		"locked":false,
		"appdata":{
			"version":1,
			"data":"AEuGk_r02_d06"
		},
		"picture":"",
		"lastupdated":"2017-12-16T19:34:23",
		"version":2
	},
	"nroDcBieCO5VSR0":{
		"name":"Nightlight",
		"type":"GroupScene",
		"group":"2",
		"lights":["2"],
		"owner":"XpfmU-zBwUyGrDq7VW-5muXVmTkn1aZpe4x2Ef-j",
		"recycle":false,
		"locked":false,
		"appdata":{
			"version":1,
			"data":"tTsaF_r02_d07"
		},
		"picture":"",
		"lastupdated":"2017-12-16T19:34:23",
		"version":2
	},
	"AcZbU258QfgMT7d":{
		"name":"Bright",
		"type":"GroupScene",
		"group":"2",
		"lights":["2"],
		"owner":"XpfmU-zBwUyGrDq7VW-5muXVmTkn1aZpe4x2Ef-j",
		"recycle":false,
		"locked":false,
		"appdata":{
			"version":1,
			"data":"1YA4C_r02_d05"
		},
		"picture":"",
		"lastupdated":"2017-12-16T19:34:23",
		"version":2
	}
}
```

## Sensors

```json
{
	"1":{
		"state":{
			"daylight":false,
			"lastupdated":"2019-03-19T23:11:00"
		},
		"config":{
			"on":true,
			"configured":true,
			"sunriseoffset":30,
			"sunsetoffset":-30
		},
		"name":"Daylight",
		"type":"Daylight",
		"modelid":"PHDL00",
		"manufacturername":"Philips",
		"swversion":"1.0"
	}
}
'''

## Rules

```json
none
```

### END DBK
