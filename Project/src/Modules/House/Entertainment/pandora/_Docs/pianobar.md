* Name:      PyHouse/Project/src/Modules/Housing/Entertainment/pandora/Docs/pianobar.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-05-17
* Updated:   2019-06-02
* License:   MIT License
* Summary:   This is the design documentation for the Pianobar host


# Pianobar

## Installation

Install PyHouse.

```
sudo apt install pianobar
```

### Config

```
user = "Pandora Username"
password = "Pandora Password"
autostart_station = 1608513919875785623
audio_quality = high
event_command = /home/briank/Patiobar/eventcmd.sh
fifo = /home/briank/Patiobar/ctl
tls_fingerprint = FC2E6AF49FC63AEDAD1078DC22D1185B809E7534
volume = 5
```

This indicates a bad ttls_fingerprint in the config file:

```
b'(i) Unrecognized key tls_fingerprint at /home/pyhouse//.config/pianobar/config:5'
```

```
b'Welcome to pianobar (2016.06.02)! Press ? for a list of commands.'
b'(i) Login... '
b'Ok.'
b'(i) Get stations... '
b'Ok.'
b'|>  Station "QuickMix" (1608513919875785623)'
b'  Station "QuickMix" (1608513919875785623)'
b'(i) Receiving new playlist... '
b'Ok.'
b'|>  "Go For It" by "Bernie Williams" on "Moving Forward" @ Smooth Jazz Radio'
b'  "Go For It" by "Bernie Williams" on "Moving Forward" @ Smooth Jazz Radio'
```

### END DBK
