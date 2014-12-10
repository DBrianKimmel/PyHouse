/**
 * @name: PyHouse/src/Modules/Web/js/family.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Dec 09, 2014
 * @summary: Lcars components to handle all the various device families.
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



function buildInsteonPart(self, p_controller, p_html) {
	// Divmod.debug('---', 'family.buildInsteonPart() was called.');
	// console.log("family.buildInsteonPart() - self = %O", self);
	p_html += buildLcarTextWidget(self, 'InsteonAddress', 'Insteon Address', p_controller.InsteonAddress);
	p_html += buildLcarTextWidget(self, 'DevCat', 'Dev Cat', p_controller.DevCat);
	p_html += buildLcarTextWidget(self, 'GroupNumber', 'Group Number', p_controller.GroupNumber);
	p_html += buildLcarTextWidget(self, 'GroupList', 'Group List', p_controller.GroupList);
	p_html += buildLcarTrueFalseWidget(self, 'Master', 'Light Master ?', p_controller.IsMaster);
	p_html += buildLcarTrueFalseWidget(self, 'Controller', 'Light Controller ?', p_controller.IsController);
	p_html += buildLcarTrueFalseWidget(self, 'Responder', 'Light Responder ?', p_controller.IsResponder);
	p_html += buildLcarTextWidget(self, 'ProductKey', 'Product Key', p_controller.ProductKey);
	return p_html;
}
function fetchInsteonEntry(self, p_data) {
	// Divmod.debug('---', 'family.fetchInsteonEntry() was called.');
    p_data.InsteonAddress = fetchTextWidget(self, 'InsteonAddress');
    p_data.DevCat = fetchTextWidget(self, 'DevCat');
    p_data.GroupNumber = fetchTextWidget(self, 'GroupNumber');
    p_data.GroupList = fetchTextWidget(self, 'GroupList');
    p_data.IsMaster = fetchTrueFalseWidget(self, 'Master');
    p_data.IsResponder = fetchTrueFalseWidget(self, 'Responder');
    p_data.IsController = fetchTrueFalseWidget(self, 'Controller');
    p_data.ProductKey = fetchTextWidget(self, 'ProductKey');
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



function buildUpbPart(self, p_controller, p_html) {
	// Divmod.debug('---', 'family.buildUpbPart() was called.');
	p_html += buildLcarTextWidget(self, 'UpbAddress', 'UPB Address', p_controller.UPBAddress);
	p_html += buildLcarTextWidget(self, 'UpbPassword', 'UPB Password', p_controller.UPBPassword);
	p_html += buildLcarTextWidget(self, 'UpbNetworkID', 'UPB Network', p_controller.UPBNetworkID);
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