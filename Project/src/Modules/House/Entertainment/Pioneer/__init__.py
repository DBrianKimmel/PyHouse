r"""
http://www.mikepoulson.com/2011/06/programmatically-controlling-pioneer.html
https://dl.dropboxusercontent.com/u/3275573/2010%20USA%20AVR%20RS-232C%20%26%20IP%20Commands%20for%20CI.pdf

Telnet Protocol
PORT = 8102
IP = '192.168.9.121'


Basic Commands (more commands to come in another post):
----------
?P    Is Device powered ON?
PWR0    Device is ON
PWR1    Device is OFF

PF    Power Device OFF
PO    Power Device ON

----------

?M     Is Zone MAIN muted
MUT1    Zone is NOT Muted
MUT0    Zone is Muted

MO     Mute MAIN zone
MF     unMute MAIN zone

----------

?V    Get Current Volume level
VOLxxx    Current volume level, xxx is 000-200
VOL121    -20.0db
VOL081    -40.0db
XXXVL    Set Volume Level to XXX (000 - 200)
001VL    Set Volume Level to -80.0db
081VL    Set Volume Level to -40.0db

VU        Set volume Up (822)Open a terminal
VD        Set volume Down (822)

----------

?RGC    Get inputs on device (i think)
RGC111001002    *Unknown*

?RGBxx    Get inputs Name (related to above command), available inputs will change based on model
?RGB01    RGB010CD
?RGB02    RGB020TUNER
?RGB03    RGB030CD-R/TAPE

?F    Get current input (use ?RGB to get name)
FN19    Input 19
FN15    Input 15

XXFN    Set current input (XX = Input number)
19FN    Set to input 19
15FN    Set to input 15

?BP    *UNKNOWN*
BPR1

?AP    *UNKNOWN*
APR1





Volume:
VD = VOLUME DOWN
MZ = MUTE ON/OFF
VU = VOLUME UP
?V = QUERY VOLUME

Power control:
PF = POWER OFF
PO = POWER ON
?P = QUERY POWER STATUS

Input selection:
05FN = TV/SAT
01FN = CD
03FN = CD-R/TAPE
04FN = DVD
19FN = HDMI1
05FN = TV/SAT
00FN = PHONO
03FN = CD-R/TAPE
26FN = HOME MEDIA GALLERY(Internet Radio)
15FN = DVR/BDR
05FN = TV/SAT
10FN = VIDEO 1(VIDEO)
14FN = VIDEO 2
19FN = HDMI1
20FN = HDMI2
21FN = HDMI3
22FN = HDMI4
23FN = HDMI5
24FN = HDMI6
25FN = BD
17FN = iPod/USB
FU = INPUT CHANGE (cyclic)
?F = QUERY INPUT

"""
