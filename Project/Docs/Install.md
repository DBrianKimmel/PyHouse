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
sudo apt install python3-venv
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




### END DBK
