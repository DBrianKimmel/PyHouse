""" drivers/__init__.py

Copyright (C) 2012-2015 by D. Brian Kimmel

The following terms apply to all files associated
 with the software unless explicitly disclaimed in individual files.

The authors hereby grant permission to use, copy, modify, distribute,
 and license this software and its documentation for any purpose, provided
 that existing copyright notices are retained in all copies and that this
 notice is included verbatim in any distributions. No written agreement,
 license, or royalty fee is required for any of the authorized uses.
 Modifications to this software may be copyrighted by their authors
 and need not follow the licensing terms described here, provided that
 the new terms are clearly indicated on the first page of each file where
 they apply.

IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
 FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
 ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
 DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.

THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
 INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
 IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
 NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
 MODIFICATIONS.

----------------------------------------------------------------------------

These are the drivers for various interfaces with the computer.

Serial - going away but it still exists.  Serial commands thru a USB dongle work here.

USB - the new standard.

HID - Human Interface Device class of USB devices.

Ethernet - not too much of this is used yet.

"""

__version_info__ = (1, 1, 0)
__version__ = '.' . join(map(str, __version_info__))

VALID_INTERFACES = ['Null', 'Serial', 'USB', 'Ethernet']
VALID_PROTOCOLS = ['TCP', 'UDP', 'Both']

# ## END DBK
