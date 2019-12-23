* Name:      PyHouse/Project/src/Modules/Housing/Entertainment/samsung/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-10-16
* Updated:   2018-10-16
* License:   MIT License
* Summary:   This is the design documentation for the Samsung Module of PyHouse.


# Samsung

```xml
<?xml version="1.0" ?>
<SamsungSection Active="True">
	<Device Active="True" Key="0" Name="ct - L/R - TV 48abc1234">
		<UUID>Samsung.-0000-0000-0000-0123456789ab</UUID>
		<Comment>48in Smart-Tv  </Comment>
		<Installed>2016-07-29</Installed>
		<IPv4>192.168.9.118</IPv4>
		<Model>UN48J5201AFXZA</Model>
		<Port>55000</Port>
		<RoomName>Living Room</RoomName>
		<RoomUUID>Room....-0000-0000-0000-0123456789ab</RoomUUID>
		<Type>TV</Type>
		<Volume>53</Volume>
	</Device>
</SamsungSection>
```

```python
src     = '192.168.100.25'      # ip of remote (Indigo Server)
mac     = '00-15-17-F3-C0-B8'   # mac of remote
remote  = 'Indigo'              # remote name
dst     = '192.168.100.51'      # ip of tv
app     = 'python'              # iphone..iapp.samsung
tv      = 'UE32ES6800'          # iphone.UE32ES6800.iapp.samsung
 
def push(key):
  new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  new.connect((dst, 55000))
  msg = chr(0x64) + chr(0x00) +\
        chr(len(base64.b64encode(src)))    + chr(0x00) + base64.b64encode(src) +\
        chr(len(base64.b64encode(mac)))    + chr(0x00) + base64.b64encode(mac) +\
        chr(len(base64.b64encode(remote))) + chr(0x00) + base64.b64encode(remote)
  pkt = chr(0x00) +\
        chr(len(app)) + chr(0x00) + app +\
        chr(len(msg)) + chr(0x00) + msg
  new.send(pkt)
  msg = chr(0x00) + chr(0x00) + chr(0x00) +\
        chr(len(base64.b64encode(key))) + chr(0x00) + base64.b64encode(key)
  pkt = chr(0x00) +\
        chr(len(tv))  + chr(0x00) + tv +\
        chr(len(msg)) + chr(0x00) + msg
  new.send(pkt)
  new.close()
  time.sleep(0.1)
  
while True:
  push("KEY_POWEROFF")
  break 
```


### END DBK
