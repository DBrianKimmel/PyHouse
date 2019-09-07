* Name:      PyHouse/Project/src/Modules/House/Controllers/_Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-08-04
* Updated:   2019-08-04
* License:   MIT License
* Summary:   This is the design documentation for Controllers


# Controllers

This is the modules for controllers.
Controllers are devices that PyHouse connects with in order to control things in the real world.

Controllers may be Hubs or Bridges created by manufacturers to control their products.
Controllers may be discrete devices such as an X-10, UPB, PLM made to communicate and control a class of responders

Controllers may be attached to a particular computer node by serial, parallel or USB port.
Controllers may also be remote and communicated with by the Internet or a private intranet.

Controllers may also be remote servers.
This is sorta OK if you own or exclusive control the server but it does put you at the
 risk of loosing control of your house if the connection is somehow broken.
It is one of the design goals of PyHouse to NOT rely on or even use the Internet for house control.

### END DBK
