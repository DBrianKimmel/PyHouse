/**
 * @name:      PyHouse/src/Modules/Web/js/family.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2017 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Dec 09, 2014
 * @summary:   Lcars components to handle all the various device families.
 * Currently:
 * 				Insteon
 * 				UPB
 * 				X10
 * 
 * This MUST be imported in workspace.js
 */

// ============================================================================
/**
 * Build family parts Special - has onchange
 */
function buildFamilySelectWidget(self, p_id, p_caption, p_obj, p_change) {
	// Divmod.debug('---', 'family.buildFamilySelectWidget() was called.');
	return buildSelectWidget(self, p_id, p_caption, globals.Valid.Families, p_obj.DeviceFamily, p_change);
}

// ============================================================================
/**
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
/**
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

// ============================================================================

function buildInsteonPart(self, p_obj, p_html) {
	// Divmod.debug('---', 'family.buildInsteonPart() was called.');
	// console.log("family.buildInsteonPart() - self = %O", self);
	p_html += buildTextWidget(self, 'InsteonAddress', 'Insteon Address', int2hex(p_obj.InsteonAddress, 3));
	p_html += buildTextWidget(self, 'DevCat', 'Dev Cat', int2hex(p_obj.DevCat, 2), 'disable');
	p_html += buildTextWidget(self, 'GroupNumber', 'Group Number', p_obj.GroupNumber);
	p_html += buildTextWidget(self, 'GroupList', 'Group List', p_obj.GroupList);
	p_html += buildTextWidget(self, 'ProductKey', 'Product Key', int2hex(p_obj.ProductKey, 3), 'disable');
	p_html += buildTextWidget(self, 'EngineVersion', 'EngineVersion', p_obj.EngineVersion, 'disable');
	return p_html;
}

function fetchInsteonEntry(self, p_obj) {
	// Divmod.debug('---', 'family.fetchInsteonEntry() was called.');
	try {
		p_obj.InsteonAddress = hex2int(fetchTextWidget(self, 'InsteonAddress'), 3);
	} catch (err) {
		p_obj.InsteonAddress = hex2int('01.02.03', 3);
		Divmod.debug('---', 'family.fetchInsteonEntry() was called. InsteonAddress ERROR ' + err);
	}
	try {
		p_obj.DevCat = hex2int(fetchTextWidget(self, 'DevCat'), 2);
	} catch (err) {
		p_obj.DevCat = hex2int('01.01', 2);
	}
	try {
		p_obj.GroupNumber = fetchTextWidget(self, 'GroupNumber');
	} catch (err) {
		p_obj.GroupNumber = 0;
	}
	try {
		p_obj.GroupList = fetchTextWidget(self, 'GroupList');
	} catch (err) {
		p_obj.GroupList = '';
}
	try {
		p_obj.ProductKey = hex2int(fetchTextWidget(self, 'ProductKey'), 3);
	} catch (err) {
		p_obj.ProductKey = hex2int('01.01.01', 3);
	}
	try {
		p_obj.EngineVersion = fetchTextWidget(self, 'EngineVersion');
	} catch (err) {
		p_obj.EngineVersion = 2;
	}
	console.log("family.fetchInsteonEntry() - Obj = %O", p_obj);
}

function createInsteonEntry(p_obj) {
	// Divmod.debug('---', 'family.createInsteonEntry() was called.');
	p_obj.InsteonAddress = hex2int('11.22.33', 3);
	p_obj.DevCat = 0;
	p_obj.GroupNumber = 0;
	p_obj.GroupList = '';
	p_obj.ProductKey = 0;
	p_obj.EngineVersion = 2;
	p_obj.FirmwareVersion = 0;
	// console.log("family.createInsteonEntry() - Obj = %O", p_obj);
}

//============================================================================

function buildUpbPart(self, p_obj, p_html) {
	// Divmod.debug('---', 'family.buildUpbPart() was called.');
	p_html += buildTextWidget(self, 'UpbAddress', 'UPB Address', p_obj.UPBAddress);
	p_html += buildTextWidget(self, 'UpbPassword', 'UPB Password', p_obj.UPBPassword);
	p_html += buildTextWidget(self, 'UpbNetworkID', 'UPB Network', p_obj.UPBNetworkID);
	return p_html;
}

function fetchUpbEntry(self, p_obj) {
	// Divmod.debug('---', 'family.fetchUpbEntry() was called.');
	p_obj.UPBAddress = fetchTextWidget(self, 'UpbAddress');
	p_obj.UPBPassword = fetchTextWidget(self, 'UpbPassword');
	p_obj.UPBNetworkID = fetchTextWidget(self, 'UpbNetworkID');
}

function createUpbEntry(p_obj) {
	p_obj.UPBAddress = '123';
	p_obj.UPBPassword = 1234;
	p_obj.UPBNetworkID = 1;
}

// ============================================================================

function buildFamilyPart(self, p_obj, p_html, p_change) {
	// Divmod.debug('---', 'family.buildFamilyPart() called.');
	// console.log("family.buildFamilyPart() - self = %O", self);
	// console.log("family.buildFamilyPart() - p_obj = %O", p_obj);

	p_html += buildFamilySelectWidget(self, 'DeviceFamily', 'Family', p_obj, p_change);
	if (p_obj.DeviceFamily === 'Insteon')
		p_html = buildInsteonPart(self, p_obj, p_html);
	else if (p_obj.DeviceFamily === 'UPB')
		p_html = buildUpbPart(self, p_obj, p_html);
	else
		Divmod.debug('---', 'ERROR - family.buildFamilyPart()  Invalid Family = ' + p_obj.DeviceFamily);
	return p_html;
}

function fetchFamilyPart(self, p_obj) {
	// Divmod.debug('---', 'family.fetchFamilyPart() called.');
	p_obj.DeviceFamily = fetchSelectWidget(self, 'DeviceFamily');
	if (p_obj.DeviceFamily === 'Insteon')
		fetchInsteonEntry(self, p_obj);
	else if (p_obj.DeviceFamily === 'UPB')
		fetchUpbEntry(self, p_obj);
	else
		Divmod.debug('---', 'ERROR - family.fetchFamilyPart()  Invalid Family = ' + p_obj.DeviceFamily);
}

function createFamilyPart(self, p_data) {
	// Divmod.debug('---', 'family.createFamilyPart() called.');
	
	if (p_data.DeviceFamily === 'Insteon')
		createInsteonEntry(p_data);
	else if (p_data.DeviceFamily === 'UPB')
		createUpbEntry(p_data);
	else
		Divmod.debug('---', 'ERROR - family.createFamilyPart()  Invalid Family = ' + p_obj.DeviceFamily);
}

// Divmod.debug('---', 'family.buildSerialPart() called.');
// console.log("family.handleMenuOnClick() - l_obj = %O", l_obj);

// ### END DBK
