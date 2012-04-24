#!/usr/bin/python

"""Driver_USB.py - USB Driver module. 

This will interface various PyHouse modules to a USB device.

This may be instanced as many times as there are USB devices to control.

This should also allow control of many different houses.
"""

# Import system type stuff
import logging
import usb.core
import usb.util
from tools import PrintBytes
from twisted.internet.task import LoopingCall

# Import PyHouse modules
#from tools import PrintBytes

ENDPOINT = 0x81
REQUEST_TYPE = 0x21


class UsbDeviceData(object):

    def __init__(self):
        self.Device = None
        self.Interface = None
        self.Name = None
        self.Port = None
        self.Product = None
        self.Vendor = None

    def get_device(self):
        return self.__Device
    def set_device(self, value):
        self.__Device = value
    def get_interface(self):
        return self.__Interface
    def set_interface(self, value):
        self.__Interface = value
    def get_name(self):
        return self.__Name
    def set_name(self, value):
        self.__Name = value
    def get_port(self):
        return self.__Port
    def set_port(self, value):
        self.__Port = value
    def get_product(self):
        return self.__Product
    def set_product(self, value):
        self.__Product = value
    def get_vendor(self):
        return self.__Vendor
    def set_vendor(self, value):
        self.__Vendor = value

    Device = property(get_device, set_device, None, None)
    Interface = property(get_interface, set_interface, None, None)
    Name = property(get_name, set_name, None, None)
    Port = property(get_port, set_port, None, None)
    Product = property(get_product, set_product, None, None)
    Vendor = property(get_vendor, set_vendor, None, None)


class UsbUtility(UsbDeviceData):
    """
    """

    def _serialLoop(self):
        """This is invoked every 1 second.
        """
        self.read_device(self.get_device())

    def extract_usb(self, p_obj):
        self.m_device_data = UsbDeviceData()
        self.set_name(p_obj.Name)
        self.set_port(p_obj.Port)
        self.set_product(p_obj.Product)
        self.set_vendor(p_obj.Vendor)

    def dump_usb_info_for_debugging(self):
        Vend = self.get_vendor()
        Prod = self.m_device_data.Device.idProduct
        Cfgs = self.m_device_data.Device.bNumConfigurations
        print "! !Driver_USB.usb_open"
        print "  !Vendor:{0:X}:{1:X}, Configs:{2:}".format(Vend, Prod, Cfgs)
        for attr in self.m_device_data.Device.__dict__.keys():
            if attr[:2] == '__':
                print "\tName: {0:}=<built-in>".format(attr)
            else:
                print "\tName: {0:}={1:}".format(attr, self.m_device_data.Device.__dict__ [attr])
        print


class UsbDriverAPI(UsbUtility):
    """
    """

    def open_device(self):
        l_vendor = self.get_vendor()
        l_product = self.get_product()
        l_dev = usb.core.find(idVendor = l_vendor, idProduct = l_product)
        self.set_device(l_dev)
        self.m_message = ''
        if l_dev is None:
            self.m_logger.error('USB device not found  {0:X}:{1:X}, {2:}'.format(l_vendor, l_product, self.get_name()))
            return False
        try:
            l_dev.set_configuration(1)
        except:
            pass
        self.m_device_data.m_endpoint_cfg = l_dev.get_active_configuration()
        try:
            l_dev.detach_kernel_driver(0)
        except:
            pass
        return l_dev

    def close_device(self, p_dev):
        pass

    def read_device(self, p_dev):
        try:
            l_msg = usb.core.Device.read(p_dev, ENDPOINT, REQUEST_TYPE)
            self.m_message += l_msg
        except:
            pass
        #print " !!UsbDriver.read_device() >>{0:}<<".format(PrintBytes(self.m_message))

    def fetch_read_data(self):
        l_ret = self.m_message
        self.m_message = ''
        return l_ret

    def write_device(self, p_dev, p_message):
        """Send message to the USB device.
        
        @return: the number of bytes written
        """
        print " !!UsbDriver.write_device() - {0:}".format(PrintBytes(p_message))
        l_len = len(p_message)
        usb.core.Device.write(p_dev, 2, p_message)
        return l_len


class USBDriverMain(UsbDriverAPI):
    """
    """

    def __init__(self, p_obj):
        """
        @param p_obj:is the Controller_Data object for a USB device to open. 
        """
        self.m_logger = logging.getLogger('PyHouse.USBDriver')
        self.extract_usb(p_obj)
        self.m_logger.info(" Initializing USB port - {0:} on port {1:}".format(self.get_name(), self.get_port()))
        _l_dev = self.open_device()
        LoopingCall(self._serialLoop).start(1)

    """
/**
Copyright 2007 by D. Brian Kimmel.  All rights reserved.
 */

#include <QtDebug>

#include "usbhidserial.h"
#include "macros.h"

//#include "libusb.h"

const int HID_GET_REPORT    = 0x01;
const int HID_GET_IDLE      = 0x02;
const int HID_GET_PROTOCOL  = 0x03;
const int HID_SET_REPORT    = 0x09;
const int HID_SET_IDLE      = 0x0A;
const int HID_SET_PROTOCOL  = 0x0B;

// EPERM            1      /* Operation not permitted */
// ENOENT           2      /* No such file or directory */
// ESRCH            3      /* No such process */
// EINTR            4      /* Interrupted system call */
#define  EIO              5      /* I/O error */
// ENXIO            6      /* No such device or address */
// E2BIG            7      /* Argument list too long */
// ENOEXEC          8      /* Exec format error */
// EBADF            9      /* Bad file number */
// ECHILD          10      /* No child processes */
// EAGAIN          11      /* Try again */
// ENOMEM          12      /* Out of memory */
// EACCES          13      /* Permission denied */
// EFAULT          14      /* Bad address */
// ENOTBLK         15      /* Block device required */
// EBUSY           16      /* Device or resource busy */
// EEXIST          17      /* File exists */
// EXDEV           18      /* Cross-device link */
// ENODEV          19      /* No such device */
// ENOTDIR         20      /* Not a directory */
// EISDIR          21      /* Is a directory */
// EINVAL          22      /* Invalid argument */
// ENFILE          23      /* File table overflow */
// EMFILE          24      /* Too many open files */
// ENOTTY          25      /* Not a typewriter */
// ETXTBSY         26      /* Text file busy */
// EFBIG           27      /* File too large */
// ENOSPC          28      /* No space left on device */
// ESPIPE          29      /* Illegal seek */
// EROFS           30      /* Read-only file system */
// EMLINK          31      /* Too many links */
// EPIPE           32      /* Broken pipe */
// EDOM            33      /* Math argument out of domain of func */
// ERANGE          34      /* Math result not representable */
// ENODATA         61      /* No data available */

// Public routines

UsbHidSerial::UsbHidSerial( int k_vendor, int k_product, int k_debug ) :
            m_idVendor( k_vendor ),
            m_idProduct( k_product ),
            m_debugLevel( k_debug ),
            m_interface( 0 ),
            m_configuration( 0 )
            {
    DEBUG( -1, "UsbHidSerial::Constructor - Entry" );
    mp_Device        = 0;
    mp_deviceHandle        = 0;
    m_timeout            = 5 * 1000;
    //m_idVendor  = 0x06f7;
    //m_idProduct = 0x0003;
    m_idProduct  = 0x5500;
    m_idVendor = 0x17dd;
    m_interface_claimed = FALSE;
    // Initialize the libraries we are using.
    DEBUG( 1, "UsbHidSerial::Constructor - lib init" );
    libusb_init(NULL);
    libusb_set_debug( NULL, 3 );
    AcquireDevice();
    DEBUG( -1, "UsbHidSerial::Constructor - Exit" );
}

UsbHidSerial::~UsbHidSerial() {
    DEBUG( -1, "UsbHidSerial::Destructor - Entry" );
    if ( mp_Device == NULL ) {
        DEBUG( 0, "UsbHidSerial::Destructor - Invalid Device - FAIL!!!\n" );
        return;
    }
    libusb_release_interface(mp_deviceHandle, m_interface );
    libusb_exit( NULL );
    DEBUG( -2, "UsbHidSerial::Destructor - Exit" );
}

void UsbHidSerial::AcquireDevice() {
    bool l_ok = FALSE;
    mp_Device    = NULL;
       DEBUG( -1, "UsbHidSerial::AcquireDevice - Entry" );
    int cnt = libusb_get_device_list(NULL, &mpp_list);
       DEBUG( -1, "UsbHidSerial::AcquireDevice - found" << cnt << " USB devices." );
    if (cnt < 0) {
        DEBUG( 0, "UsbHidSerial::AcquireDevice - Exit - ERROR" );
        return;
    }
    for (int i = 0; i < cnt; i++) {
        libusb_device* l_device = mpp_list[i];
        if (is_interesting(mpp_list[i])) {
            mp_Device = l_device;
            break;
        }
    }
    // Our find of the proper device
    if (mp_Device != NULL) {
        l_ok = TRUE;
    }
    if ( l_ok ) { l_ok = OpenDevice();  }
    if ( l_ok ) { l_ok = ClaimInterface(); }
    if ( l_ok ) { l_ok = SetConfig(); }
    if ( l_ok ) { l_ok = InitializeHID(); }
    libusb_free_device_list(mpp_list,1);
    DEBUG( -2, "UsbHidSerial::AcquireDevice - Exit " );
}

bool UsbHidSerial::is_interesting(libusb_device* p_dev) {
    DEBUG( 1, "UsbHidSerial::is_interesting - Entry  " << (&p_dev) );
    int l_err = libusb_get_device_descriptor(p_dev, &m_deviceDescriptor);
    if (l_err != 0) {
        DEBUG( 0, "UsbHidSerial::is_interesting - cannot get device descriptor" );
        return FALSE;
    }
    DEBUG( 1, "UsbHidSerial::is_interesting - getting data from device." );
    //m_usbBus      = (int)libusb_get_bus_number(p_dev);
    //m_usbDevice   = (int)libusb_get_device_address( p_dev);
    int l_vendor  = m_deviceDescriptor.idVendor;
    int l_product = m_deviceDescriptor.idProduct;
    DEBUG( 1, "UsbHidSerial::is_interesting -  Vendor:" << l_vendor << ", Product:" << l_product);
    if (l_vendor != m_idVendor) {
        DEBUG( 3, "UsbHidSerial::is_interesting - wrong vendor ID" );
        return FALSE;
    }
    if (l_product != m_idProduct) {
        DEBUG( 3, "UsbHidSerial::is_interesting - wrong product ID" );
        return FALSE;
    }
    DEBUG( -2, "UsbHidSerial::is_interesting - Exit - Found it." );
    return TRUE;
}

void UsbHidSerial::DropDevice() {
    DEBUG( -1, "UsbHidSerial::DropDevice" );
/*
    int l_result = libusb_release_interface( mp_handle, m_interface );
    if ( l_result != 0 ) {
        DEBUG( 0, "UsbHidSerial::DropDevice - error releasing interface=" << l_result );
    }
    sleep(2);
    libusb_exit(NULL);
    DEBUG( 2, "UsbHidSerial::usbDropDevice - Exit" );
*/
}

int UsbHidSerial::usbReadBytes( QByteArray& kr_buffer ) {
    int     l_ret;
    int     l_endPoint = 0x81; // Interrupt IN End Point
    char    l_buff[128];
    int     l_size          = 8;
    int     l_transferred;

    memset( l_buff, 0, 100 );
    if ( mp_Device == 0 ) {
        DEBUG( 0, "UsbHidSerial::usbReadBytes - Invalid Device - FAIL!!! " );
        return -1;
    }
    l_ret = libusb_interrupt_transfer( mp_deviceHandle,
                                l_endPoint,
                                (unsigned char*)l_buff,
                                l_size,
                                &l_transferred,
                                m_timeout );
    kr_buffer = l_buff;
    QString l_str = ToString( l_buff );
    l_size = strlen( l_buff );
    DEBUG( 7, "UsbHidSerial::usbReadBytes - Returned " << l_size << " " << l_str.toAscii() );
    return l_ret;
}

int UsbHidSerial::Write1Byte(char k_byte) {
    int     l_transferred;
    int l_ret = 0;
    QByteArray l_buf;
    l_buf[0] = 0x31;    // Ascii length byte.
    l_buf[1] = k_byte;    // Data byte
    l_ret = libusb_interrupt_transfer( mp_deviceHandle,
                                 2, // Interrupt OUT End Point
                                 (unsigned char*)l_buf.data(),
                                 l_buf.size(),
                                 &l_transferred,
                                 m_timeout );
    DEBUG( 3, "UsbHidSerial::Write1Byte - Erc:" << l_ret << ", Sent:" << l_transferred );
    return l_ret;
}

int UsbHidSerial::usbWriteBytes( const QByteArray& k_buffer ) {
    int         l_ret = 0;
    QString l_str = ToString( k_buffer );
    DEBUG( 6, "UsbHidSerial::usbWriteBytes - Entry Len=" << k_buffer.size() << " " << l_str.toAscii() );
    if ( mp_Device == 0 ) {
        DEBUG( 0, "UsbHidSerial::usbWriteBytes - Invalid Device - FAIL!!! " );
        return -1;
    }

    for ( int l_ix = 0; l_ix < k_buffer.size(); l_ix++ ) {
        l_ret = Write1Byte(k_buffer[l_ix]);
        // if the device re-enumerated we will get an error of -19 here.
        if ( l_ret < 0 ) {
            DEBUG( 0, "UsbHidSerial::usbWriteBytes - got error " << l_ret << " attempting to re-acquiire the PIM" );
            //DropDevice();
            //AcquireDevice();
            //l_ret = Write1Byte(k_buffer[l_ix]);
        }
        if ( l_ret < 0 ) {
            DEBUG( 0, "UsbHidSerial::usbWriteBytes = ERROR Wrote=" << l_ret );
            return -1;
        }
    }
    DEBUG( 7, "UsbHidSerial::usbWriteBytes - Exit" );
    return l_ret;
}

// Protected routines

bool UsbHidSerial::OpenDevice() {
    DEBUG( -1, "UsbHidSerial::OpenDevice - Entry" );
    // Open the device that we found for the given vendor/product.
    int l_int = libusb_open( mp_Device, &mp_deviceHandle );
    if ( l_int != 0) {
        DEBUG( 0, "UsbHidSerial::OpenDevice - Exit FAILED to open device ! - Err:" << l_int );
        return FALSE;
    }
    DEBUG( -2, "UsbHidSerial::OpenDevice - Exit OK");
    return TRUE;
}

bool UsbHidSerial::SetConfig() {
    DEBUG( 1, "UsbHidSerial::SetConfig - Entry" );
    m_configuration = 1;
    int l_ret = libusb_set_configuration( mp_deviceHandle,  m_configuration );
    if ( l_ret != 0 ) {
        DEBUG( 0, "UsbHidSerial::SetConfig - FAILED returned " << l_ret );
        return TRUE;
    }
    DEBUG( 2, "UsbHidSerial::SetConfig - Exit OK" );
    return TRUE;
}

bool UsbHidSerial::InitializeHID() {
    int l_ret;
    DEBUG( 1, "UsbHidSerial::InitializeHID - Entry" );
    QByteArray l_report = "12345";
    l_report[0] = 0xc0;
    l_report[1] = 0x12;
    l_report[2] = 0x00;
    l_report[3] = 0x00;
    l_report[4] = 0x03;
    int l_requestType = LIBUSB_ENDPOINT_OUT | LIBUSB_REQUEST_TYPE_CLASS | LIBUSB_RECIPIENT_DEVICE; // 0x21
    l_requestType = 0x21;
    int l_request = HID_SET_REPORT; // 0x09
    int l_value   = 0x0003; // Report type & Report ID
    int l_index   = 0;
    l_ret = libusb_control_transfer( mp_deviceHandle,
                             l_requestType,
                             l_request,
                             l_value,
                             l_index,
                             (unsigned char*)l_report.data(),
                             l_report.size(),
                             m_timeout );
    if ( l_ret < 0 ) {
        DEBUG( 0, "UsbHidSerial::InitializeHID = ERROR returned=" << l_ret );
        return -1;
    }
    DEBUG( 2, "UsbHidSerial::InitializeHID - Exit OK - Bytes=" << l_ret );
    return TRUE;
}

bool UsbHidSerial::ClaimInterface() {
    m_interface = 0;
    DEBUG( 1, "UsbHidSerial::ClaimInterface - Entry - Interface=" << m_interface );
    // zero if no kernel driver is active.
    int l_activ = libusb_kernel_driver_active(mp_deviceHandle, m_interface);
    DEBUG( 1, "UsbHidSerial::ClaimInterface - libusb_kernel_driver_active=" << l_activ );
    if ( l_activ == 0) {
        return TRUE;  // we have the interface?
    }
    int l_detach = libusb_detach_kernel_driver(mp_deviceHandle, m_interface);
    DEBUG( 1, "UsbHidSerial::ClaimInterface - libusb_detach_kernel_driver=" << l_detach );
    m_interface_claimed = TRUE;
    DEBUG(  2, "UsbHidSerial::ClaimInterface - Exit OK Interface=" << m_interface );
    return TRUE;
}

QString UsbHidSerial::GetString( int k_index ) {
    QString     l_str;
    unsigned char        l_chr[1024];
    int l_ret = libusb_get_string_descriptor( mp_deviceHandle, k_index, 0, l_chr , 1024 );
    if ( l_ret < 0 ) {
        return QString();
    }
    l_chr[l_ret] = 0x00;
    l_str.append( (char*)l_chr );
    return l_str;
}

QString UsbHidSerial::ToString( const QByteArray& k_ba ) {
    QString l_str( " " );
    char    l_char[128];
    int     l_size = k_ba.size();
    for ( int l_ix = 0; l_ix < l_size; l_ix++ ) {
        int l_byte = (unsigned int)k_ba[l_ix]&0xFF;
        if ( ( l_byte > 0x1F ) && ( l_byte < 0x7F ) ) {
            sprintf( l_char, "%c ", l_byte );
        } else {
            sprintf( l_char, "0x%2.2X ", l_byte );
        }
        l_str.append( l_char );
    }
    return l_str;
}
    """
### END
