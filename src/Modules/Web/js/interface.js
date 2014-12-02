/**
 * @name: PyHouse/src/Modules/Web/js/interface.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Sep 12, 2014
 * @summary: Lcars components.
 */

var VALID_BAUD_RATE = ['4800', '9600', '19200', '38400'];
var VALID_BYTE_SIZE = ['8', '7', '6'];
var VALID_PARITY = ['E', 'O', 'N'];
var VALID_STOP_BITS = ['1.0', '1.5', '2.0'];

function buildLcarBaudRateSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, VALID_BAUD_RATE, p_checked);
}
function buildLcarByteSizeSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, VALID_BYTE_SIZE, p_checked);
}
function buildLcarParitySelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, VALID_PARITY, p_checked);
}
function buildLcarStopBitsSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, VALID_STOP_BITS, p_checked);
}

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

// ### END DBK