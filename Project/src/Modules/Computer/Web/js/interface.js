/**
 * @name: PyHouse/src/Modules/Web/js/interface.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2017 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Sep 12, 2014
 * @summary: Lcars components to handle all the controller interfaces. Currently: Serial USB Ethernet
 */

var VALID_BAUD_RATE = [ '4800', '9600', '19200', '38400' ];
var VALID_BYTE_SIZE = [ '8', '7', '6' ];
var VALID_PARITY = [ 'E', 'O', 'N' ];
var VALID_STOP_BITS = [ '1.0', '1.5', '2.0' ];

function buildLcarBaudRateSelectWidget(self, p_id, p_caption, p_checked) {
	return buildSelectWidget(self, p_id, p_caption, VALID_BAUD_RATE, p_checked);
}
function buildLcarByteSizeSelectWidget(self, p_id, p_caption, p_checked) {
	return buildSelectWidget(self, p_id, p_caption, VALID_BYTE_SIZE, p_checked);
}
function buildLcarParitySelectWidget(self, p_id, p_caption, p_checked) {
	return buildSelectWidget(self, p_id, p_caption, VALID_PARITY, p_checked);
}
function buildLcarStopBitsSelectWidget(self, p_id, p_caption, p_checked) {
	return buildSelectWidget(self, p_id, p_caption, VALID_STOP_BITS, p_checked);
}

//============================================================================
/**
 * Build interface parts Special - has onchange
 */
function buildInterfaceSelectWidget(self, p_id, p_caption, p_obj, p_change_function_name) {
	// Divmod.debug('---', 'interface.buildInterfaceSelectWidget() was called.');
	return buildSelectWidget(self, p_id, p_caption, globals.Valid.InterfaceTypes, p_obj.InterfaceType, p_change_function_name);
}


// ============================================================================
// Setial Interface

function buildSerialPart(self, p_controller, p_html) {
	// Divmod.debug('---', 'interface.buildSerialPart() called.');
	p_html += buildLcarBaudRateSelectWidget(self, 'BaudRate', 'Baud Rate', p_controller.BaudRate);
	p_html += buildLcarByteSizeSelectWidget(self, 'ByteSize', 'Byte Size', p_controller.ByteSize);
	p_html += buildLcarParitySelectWidget(self, 'Parity', 'Parity', p_controller.Parity);
	p_html += buildLcarStopBitsSelectWidget(self, 'StopBits', 'Stop Bits', p_controller.StopBits);
	return p_html;
}

function fetchSerialEntry(self, p_data) {
	// Divmod.debug('---', 'interface.fetchSerialEntry() was called.');
	p_data.BaudRate = fetchSelectWidget(self, 'BaudRate');
	p_data.ByteSize = fetchSelectWidget(self, 'ByteSize');
	p_data.Parity = fetchSelectWidget(self, 'Parity');
	p_data.StopBits = fetchSelectWidget(self, 'StopBits');
	p_data.DsrDtr = false;
	p_data.RtsCts = false;
	p_data.Timeout = 1.0;
	p_data.XonXoff = false;
	return p_data;
}

function createSerialEntry(self, p_data) {
	p_data.BaudRate = 9600;
	p_data.ByteSize = 8;
	p_data.Parity = 'N';
	p_data.StopBits = 1.0;
	p_data.DsrDtr = false;
	p_data.RtsCts = false;
	p_data.Timeout = 1.0;
	p_data.XonXoff = false;
	return p_data;
}

//============================================================================
// USB interface

function buildUsbPart(self, p_obj, p_html) {
	return p_html;
}

function fetchUsbEntry(self, p_data){
	return p_data;
}

function createUsbEntry(self, p_data){
	return p_data;
}

//============================================================================

function buildInterfacePart(self, p_obj, p_html, p_change_function_name) {
	// Divmod.debug('---', 'interface.buildInterfacePart() called.');
	// console.log("interface.buildInterfacePart() - self = %O", self);
	// console.log("interface.buildInterfacePart() - p_obj = %O", p_obj);
	p_html += buildInterfaceSelectWidget(self, 'InterfaceType', 'Interface', p_obj, p_change_function_name);
	if (p_obj.InterfaceType === 'Serial')
		p_html = buildSerialPart(self, p_obj, p_html);
	else if (p_obj.InterfaceType === 'USB')
		p_html = self.buildUsbPart(p_obj, p_html);
	else
		Divmod.debug('---', 'ERROR - interface.buildInterfacePart()  Invalid Interface = ' + p_obj.DeviceFamily);
	return p_html;
}

function fetchInterfacePart(self, p_data) {
	// Divmod.debug('---', 'interface.fetchInterfacePart() called.');
	if (p_data.InterfaceType === 'Serial')
		p_data = fetchSerialEntry(self, p_data);
	else if (p_data.InterfaceType === 'USB')
		p_data = fetchUsbEntry(self, p_data);
	return p_data;
}

function createInterfacePart(self, p_data) {
	// Divmod.debug('---', 'interface.createInterfacePart() called.');
	if (p_data.InterfaceType === 'Serial')
		p_data = createSerialEntry(self, p_data);
	else if (p_data.InterfaceType === 'USB')
		p_data = createUsbEntry(self, p_data);
	return p_data;
}

// Divmod.debug('---', 'interface.buildSerialPart() called.');
// ### END DBK
