* Name:      PyHouse/Project/Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-10-11
* Updated:   2018-10-11
* License:   MIT License
* Summary:   This is the design documentation of PyHouse.


# PyHouse

## Installation

### Add user

We need a pyhouse user to run the PyHouse software.

* Add the user pyhouse to the computer.
* Add pyhouse to the proper groups.
* Add the user to sudo authoriation.
   Be sure the following line exists in the file '/etc/sudoers.d/pyhouse'
```bash
pyhouse ALL=(ALL) NOPASSWD: ALL
```
* Become the user pyhouse

### Create Virtual environment


### Install the software


## Configuration


### Autologin

Set up the computer to automatically login the pyhouse user after booting.

* edit /etc/systemd/system/autologin.@service
   under [service] change the line beginning with ExecStart to have '--autologin=pyhouse'
* sudo systemctl enable autologin@.service


### Autostart

Set up the pyhouse to automatically start the PyHouse software when autologin is setup   

* Be sure the following code is at or near the bottom of the .bashrc file.
```bash
#
# Start pyhouse if we autologin this user
#
if [ $(tty) == /dev/tty1 ]; then
    bin/start_pyhouse
fi
### END DBK
```
* Be sure the pyhouse user has a bin directory
* Place the following file in 'bin/start_pyhouse' and be sure it is executable.
```bash
#!/bin/bash
# Name:      start_pyhouse
# Author:    D. Brian Kimmel
# Contact:   D.BrianKimmel@gmail.com
# Copyright: (c) 2010-2018 by D. Brian Kimmel
# License:   MIT License
# Created:   Created on Oct 11, 2018
# Updated:   2018-10-11
# Summary:   This starts PyHouse
HOME=/home/pyhouse/
VENV=${HOME}venv/
WORK=${VENV}PyHouse/
MAIN=${WORK}Project/src/PyHouse.py
echo "Starting the PyHouse system"
cd ${HOME}
> nohup.out
source ${VENV}bin/activate
nohup python ${MAIN}  1>/dev/null 2>&1 </dev/null &
### END DBK
```

* Place the following file in 'bin/stop_pyhouse' and be sure it is executable.
```bash
#!/bin/bash
# Name:      stop_pyhouse
# Author:    D. Brian Kimmel
# Contact:   D.BrianKimmel@gmail.com
# Copyright: (c) 2010-2018 by D. Brian Kimmel
# License:   MIT License
# Created:   Created on Oct 19, 2015
# Updated:   2018-10-11
# Summary:   This stops PyHouse
WORK=/home/pyhouse/workspace/PyHouse
echo "Stopping the PyHouse system"
PID=$(ps -ef | grep PyHouse | grep -v grep | awk '{ print $2 }')
kill -TERM $PID
### END DBK
```


### END DBK
