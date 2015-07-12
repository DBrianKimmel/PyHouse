/**
 * @name:      PyHouse/src/Modules/Web/js/family.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2015 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Dec 09, 2014
 * @summary:   Lcars components to handle all the various device families.
 * Currently:
 * 				Insteon
 * 				UPB
 * 				X10
 */


/**
 * Special - has onchange 
 */
function buildLcarFamilySelectWidget(self, p_id, p_caption, p_checked, p_change) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.Families, p_checked, p_change);
}
/*
 * get a user field (dotted hex) to an internal field (int string).
 */
function hex2int(p_hex, p_bytes) {
	var l_hex = '00';
	var l_int = 0;
	if (p_bytes === 2) {
		l_hex = p_hex.slice(0, 2) + p_hex.slice(3);
		l_int = parseInt(l_hex, 16).toString();
	}
	if (p_bytes === 3) {
		l_hex = p_hex.slice(0, 2) + p_hex.slice(3, 5) + p_hex.slice(6);
		l_int = parseInt(l_hex, 16).toString();
	}
	return l_int;
}
/*
 * convert the internal data (int string) to a user field (dotted hex).
 */
function int2hex(p_int, p_bytes) {
	var l_hex = Number(p_int).toString(16);
	var l_ret = 0;
	if (p_bytes === 2) {
		l_hex = ('0000' + l_hex).slice(-4);
		l_ret = l_hex.slice(0, 2) + '.' + l_hex.slice(2);
	}
	if (p_bytes === 3) {
		l_hex = ('000000' + l_hex).slice(-6);
		l_ret = l_hex.slice(0, 2) + '.' + l_hex.slice(2, 4) + '.' + l_hex.slice(4);
	}
	return l_ret;
}
function buildInsteonPart(self, p_obj, p_html) {
	// Divmod.debug('---', 'family.buildInsteonPart() was called.');
	// console.log("family.buildInsteonPart() - self = %O", self);
	p_html += buildLcarTextWidget(self, 'InsteonAddress', 'Insteon Address', int2hex(p_obj.InsteonAddress, 3));
	p_html += buildLcarTextWidget(self, 'DevCat', 'Dev Cat', int2hex(p_obj.DevCat, 2));
	p_html += buildLcarTextWidget(self, 'GroupNumber', 'Group Number', p_obj.GroupNumber);
	p_html += buildLcarTextWidget(self, 'GroupList', 'Group List', p_obj.GroupList);
	p_html += buildLcarTrueFalseWidget(self, 'Master', 'Light Master ?', p_obj.IsMaster);
	p_html += buildLcarTrueFalseWidget(self, 'Controller', 'Light Controller ?', p_obj.IsController);
	p_html += buildLcarTrueFalseWidget(self, 'Responder', 'Light Responder ?', p_obj.IsResponder);
	p_html += buildLcarTextWidget(self, 'ProductKey', 'Product Key', int2hex(p_obj.ProductKey, 3));
	return p_html;
}
function fetchInsteonEntry(self, p_data) {
	// Divmod.debug('---', 'family.fetchInsteonEntry() was called.');
	try {
	    p_data.InsteonAddress = hex2int(fetchTextWidget(self, 'InsteonAddress'), 3);
	    p_data.DevCat = hex2int(fetchTextWidget(self, 'DevCat'), 2);
	    p_data.GroupNumber = fetchTextWidget(self, 'GroupNumber');
	    p_data.GroupList = fetchTextWidget(self, 'GroupList');
	    p_data.IsMaster = fetchTrueFalseWidget(self, 'Master');
	    p_data.IsResponder = fetchTrueFalseWidget(self, 'Responder');
	    p_data.IsController = fetchTrueFalseWidget(self, 'Controller');
	    p_data.ProductKey = hex2int(fetchTextWidget(self, 'ProductKey'), 3);
	}
	catch(err) {
		p_data.InsteonAddress = hex2int('01.01.01', 3);
		p_data.DevCat = hex2int('01.01', 2);
		p_data.ProductKey = hex2int('01.01.01', 3);
	}
	return p_data;
}
function createInsteonEntry(self, p_data) {
	p_data.InsteonAddress = '11.22.33';
	p_data.DevCat = 0;
	p_data.GroupNumber = 0;
	p_data.GroupList = '';
	p_data.IsMaster = false;
	p_data.IsResponder = false;
	p_data.IsController = false;
	p_data.ProductKey = 0;
	return p_data;
}



function buildUpbPart(self, p_obj, p_html) {
	// Divmod.debug('---', 'family.buildUpbPart() was called.');
	p_html += buildLcarTextWidget(self, 'UpbAddress', 'UPB Address', p_obj.UPBAddress);
	p_html += buildLcarTextWidget(self, 'UpbPassword', 'UPB Password', p_obj.UPBPassword);
	p_html += buildLcarTextWidget(self, 'UpbNetworkID', 'UPB Network', p_obj.UPBNetworkID);
	return p_html;
}
function fetchUpbEntry(self, p_data) {
	// Divmod.debug('---', 'family.fetchUpbEntry() was called.');
    p_data.UPBAddress = fetchTextWidget(self, 'UpbAddress');
    p_data.UPBPassword = fetchTextWidget(self, 'UpbPassword');
    p_data.UPBNetworkID = fetchTextWidget(self, 'UpbNetworkID');
	return p_data;
}
function createUpbEntry(self, p_data) {
	p_data.UPBAddress = '123';
	p_data.UPBPassword = 1234;
	p_data.UPBNetworkID = 1;
	return p_data;
}

// Divmod.debug('---', 'family.buildSerialPart() called.');
// console.log("family.handleMenuOnClick() - l_obj = %O", l_obj);
// ### END DBK