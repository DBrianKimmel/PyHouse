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



### END DBK