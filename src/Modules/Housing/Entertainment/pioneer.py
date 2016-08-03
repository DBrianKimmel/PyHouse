"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Entertainment/pioneer.py -*-

@name:      src.Modules.Entertainment.pioneer
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@note:      Created on Jul 10, 2016
@license:      MIT License
@summary:

http://www.mikepoulson.com/2011/06/programmatically-controlling-pioneer.html
https://dl.dropboxusercontent.com/u/3275573/2010%20USA%20AVR%20RS-232C%20%26%20IP%20Commands%20for%20CI.pdf



Basic Commands (more commands to come in another post):
?P
Is Device powered ON?
PWR0    Device is ON
PWR1    Device is OFF

PF    Power Device OFF
PO    Power Device ON

?M     Is Zone MAIN muted
MUT1    Zone is NOT Muted
MUT0    Zone is Muted

MO     Mute MAIN zone
MF     unMute MAIN zone

?V    Get Current Volume level
VOLxxx    Current volume level, xxx is 000-200
VOL121    -20.0db
VOL081    -40.0db
XXXVL    Set Volume Level to XXX (000 - 200)
001VL    Set Volume Level to -80.0db
081VL    Set Volume Level to -40.0db

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
XX    Input number
19FN    Set to input 19
15FN    Set to input 15

?BP    *UNKNOWN*
BPR1

?AP    *UNKNOWN*
APR1





Remote control your Pioneer VSX receiver over telnet
Posted by Raymond Julin on 15/07/2012



11
telnet <ip> VU<enter> #win!
I’m a hacker, developer and lazy guy. So when I found myself in the kitchen cooking, just realizing that my Pioneer VSX 921 receiver was turned down too low I didn’t walk over to turn it up or find the remote; I instead remembered that it has a bad app for iOS, meaning that it accepts being controlled remote over the network. A little bit of google searching and I found a plugin for an I-dont-know-what containing an XML with some Lua code (XML with code — yay), and also a very nice mapping table for commands the same code runs against a VSX 1021.

So a quick telnet session later I had yanked the volume up without ever leaving the kitchen! These commands probably work for most of the VSX  921/1021 series and later. Enjoy:

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

If you want to change input to the iPod port and turn up the volume, given you’re using OS X or some Unix derivative, you would do this:

Open a terminal
Run the command telnet <ip>
Select input by typing: 17FN<enter>
Nod volume up 1 time: VU<enter>
Repeat VU until you are happy.
There is a tone of other commands you can use, I believe this manual for the VSX 1120 is very much valid for other devices in the series.

"""

__updated__ = '2016-08-01'

PORT = 8102



# ## END DBK
