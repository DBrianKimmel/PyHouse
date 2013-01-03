'''
Created on Dec 13, 2012

@author: briank

Created to handle the UPB PIM:

Bus xxx Device yyy: ID 17dd:5500
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               1.00
  bDeviceClass            0 (Defined at Interface level)
  bDeviceSubClass         0
  bDeviceProtocol         0
  bMaxPacketSize0         8
  idVendor           0x17dd
  idProduct          0x5500
  bcdDevice            0.00
  iManufacturer           1 Simply Automated Inc.
  iProduct                2 USB to Serial
  iSerial                 0
  bNumConfigurations      1

'''
import array
import sys
import time
from twisted.internet import reactor
# Use USB package that was written by Wander Lairson Costa
# PYUSB_DEBUG_LEVEL=debug
# export PYUSB_DEBUG_LEVEL
import usb.core
import usb.util

import Driver_USB


callLater = reactor.callLater

g_debug = Driver_USB.g_debug

# Timeouts for send/receive delays
SEND_TIMEOUT = 0.8
RECEIVE_TIMEOUT = 0.3
READ_TIMER = 0.100  # Every 100 miliseconds

class UsbDriverAPI(Driver_USB.UsbDriverAPI):

    def setup_hid_device(self):
        """Use the control endpoint to set up report descriptors for HID devices.

        Much of this was determined empirically for a smarthome UPB PIM
        """
        if g_debug > 0:
            print "Driver_USB_17DD_5500._setup_hid_device() 2 "
        l_report = array.array('B', "12345")
        l_report[0] = 0xc0
        l_report[1] = 0x12
        l_report[2] = 0x00
        l_report[3] = 0x00
        l_report[4] = 0x03
        l_requestType = 0x21  # LIBUSB_ENDPOINT_OUT (0x00) | LIBUSB_REQUEST_TYPE_CLASS (0x20) | LIBUSB_RECIPIENT_DEVICE (0x00)
        l_request = Driver_USB.HID_SET_REPORT  # 0x09
        l_value = 0x0003  # Report type & Report ID
        l_index = 0
        l_ret = (l_requestType,
                l_request,
                l_value,
                l_index,
                l_report)
        return l_ret

    def read_device(self, p_usb):
        l_len = -1
        while l_len != 0:
            try:
                l_msg = p_usb.Device.read(0x81, 8, timeout = 100)
                # we seem to have actual length + 240 as 1st char
                l_len = l_msg[0] - 240
                if l_len > 0:
                    if g_debug > 0:
                        print "Driver_USB.read_device() {0:} - {1:}".format(l_len, l_msg)
                    p_usb.msg_len += l_len
                    for l_x in range(l_len):
                        p_usb.message.append(l_msg[l_x + 1])
            except usb.USBError, e:
                print "Driver_USB.read_device() got USBError", e
            except Exception, e:
                print " -- Error in Driver_USB.read_device() ", sys.exc_info(), e
            # time.sleep(0.1)


def Init(p_obj):
    """
    """
    if g_debug > 0:
        print "\nDriver_USB_17DD_5500.Init()"
    l_ret = Driver_USB.Init(p_obj, READ_TIMER, UsbDriverAPI())
    return l_ret






"""
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
    """
""" UsbHidSerial::UsbHidSerial( int k_vendor, int k_product, int k_debug ) :
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
    """
""" UsbHidSerial::~UsbHidSerial() {
    if ( mp_Device == NULL ) {
        DEBUG( 0, "UsbHidSerial::Destructor - Invalid Device - FAIL!!!\n" );
        return;
    }
    libusb_release_interface(mp_deviceHandle, m_interface );
    libusb_exit( NULL );
}
    """
""" void UsbHidSerial::AcquireDevice() {
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
}
    """
""" bool UsbHidSerial::is_interesting(libusb_device* p_dev) {
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
    """
""" void UsbHidSerial::DropDevice() {
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
    """
""" int UsbHidSerial::usbReadBytes( QByteArray& kr_buffer ) {
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
    """
""" int UsbHidSerial::Write1Byte(char k_byte) {
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
    """
""" int UsbHidSerial::usbWriteBytes( const QByteArray& k_buffer ) {
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
    """
""" bool UsbHidSerial::OpenDevice() {
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
    """
""" bool UsbHidSerial::SetConfig() {
    m_configuration = 1;
    int l_ret = libusb_set_configuration( mp_deviceHandle,  m_configuration );
    if ( l_ret != 0 ) {
        DEBUG( 0, "UsbHidSerial::SetConfig - FAILED returned " << l_ret );
        return TRUE;
    }
    return TRUE;
}
    """
""" bool UsbHidSerial::InitializeHID() {
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
    """
""" bool UsbHidSerial::ClaimInterface() {
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
    """
""" QString UsbHidSerial::GetString( int k_index ) {
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
    """

# ## END
