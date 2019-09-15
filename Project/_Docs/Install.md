* Name:      PyHouse/Project/Docs/Install.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-05-17
* Updated:   2019-05-17
* License:   MIT License
* Summary:   This is the design documentation for the Pandora Module of PyHouse.

# Install

## Python Virtual Environment

Pyhouse runs in a virtual Python environment.
This keeps the Python needed for PyHouse separate from the system Python and helps avoid package contamination.

Install the necessary software.


```bash
sudo apt update
sudo apt install python3-venv git python3-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev
sudo cp /etc/sudoers.d/010_pi-nopasswd /etc/sudoers.d/010_pyhouse-nopasswd
sudo vi /etc/sudoers.d/010_pyhouse-nopasswd
		change "pi" to "pyhouse"
sudo su pyhouse -l
python3 -m venv venv
cd venv
source bin/activate
git clone https://github.com/DBrianKimmel/PyHouse.git
pip3  install wheel
pip3  install -r PyHouse/Project/requirements.txt

sudo mkdir /var/log/pyhouse /etc/pyhouse
sudo chown pyhouse /var/log/pyhouse /etc/pyhouse

```

Login as user pyhouse.

Create the virtual environment.  The version of Python in the python3x part of the command will be used for the environment.
At the time this was created, the installed version was 3.5 so python3x will be entered as 'python3.5'

```bash
python3x -m venv venv
source venv/bin/activate
cd venv
git clone https://github.com/DBrianKimmel/PyHouse.git
cd
pip install -r venv/PyHouse/Project/requirements.txt
sudo mkdir /etc/pyhouse /var/log/pyhouse
sudo chown pyhouse.pyhouse /etc/pyhouse /var/log/pyhouse
```

## Autologin

In order to run PyHouse automatically after a reboot, the user pyhouse must be automatically logged in.

```bash
cd /etc/systemd/system/

As root edit the file:  autologin@.service
Fix the exec start line so it looks like this:
ExecStart=-/sbin/agetty --autologin pyhouse --noclear %I $TERM

systemctl enable autologin@.service
cd
edit .bashrc and be sure the file ends like this:
### AutoLogin PyHouse ###
#
# Start pyhouse if we autologin this user
#
if [ $(tty) == /dev/tty1 ]; then
    bin/start-pyhouse
fi
### END DBK

```
# Installation

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
