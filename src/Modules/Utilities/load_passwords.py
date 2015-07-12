"""
-*- test-case-name: PyHouse.src.Modules.utils.test.test_load_password -*-

@name:      PyHouse/src/Modules/utils/load_passwords.py
@author:    briank
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by briank
@license:   MIT License
@note:      Created on Jul 5, 2014
@Summary:


See the documentation for PassLib here:

passlib - password hashing library for python - Google Project Hosting
https://code.google.com/p/passlib/

Passlib 1.6.2 documentation � Passlib v1.6.2 Documentation
http://pythonhosted.org/passlib/

passlib-users - Google Groups
https://groups.google.com/forum/#!forum/passlib-users

New Application Quickstart Guide � Passlib v1.6.2 Documentation
http://pythonhosted.org/passlib/new_app_quickstart.html#sha512-crypt

passlib.hash.sha512_crypt - SHA-512 Crypt � Passlib v1.6.2 Documentation
http://pythonhosted.org/passlib/lib/passlib.hash.sha512_crypt.html#passlib.hash.sha512_crypt
"""

import passlib.hash

# Crypt is unix only so this will error out on windows.
import crypt

ctype = "6"  # for sha512 (see man crypt)
salt = "qwerty"
insalt = '${}${}$'.format(ctype, salt)
password = "AMOROSO8282"

value1 = sha512_crypt.encrypt(password, salt = salt, rounds = 5000)
value2 = crypt.crypt(password, insalt)
if not value1 == value2:
    print("algorithms do not match")
print("{}\n{}\n\n".format(value1, value2))

# ## END DBK
