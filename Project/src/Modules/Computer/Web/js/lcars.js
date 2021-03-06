/**
 * @name: PyHouse/src/Modules/Web/js/lcars.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2017 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Sep 12, 2014
 * @summary: Lcars components.
 */

lcarsDefs = {
	test : 123
};

/**
 * Build the top part of the display.
 * 
 * @param: p_title(str) is the title to display near the center of the display
 */
function build_lcars_top(p_title, /* optional* */p_color) {
	// Divmod.debug('---', 'lcars.build_lcars_top() was called.');
	var l_color = p_color;
	if (l_color === undefined)
		l_color = 'lcars-salmon-color';
	var l_html = '';
	l_html += "<div class='lcars-row spaced'>\n";
	l_html += "  <div class='lcars-column u-1-8 lcars-elbow left bottom lcars-blue-bg'></div>\n";
	l_html += "  <div class='lcars-column u-6-8 lcars-divider lcars-blue-tan-divide'>\n";
	l_html += "    <div class='lcars-row'>\n";
	l_html += "      <div class='lcars-column u-1-2'>\n";
	l_html += "        <h1 class='right " + l_color + "'>" + p_title + "</h1>\n";
	l_html += "      </div>\n"; // column_1-2
	l_html += "    </div>\n"; // row 2
	l_html += "  </div>\n"; // column_6-8
	l_html += "  <div class='lcars-column u-1-8 lcars-elbow right bottom lcars-tan-bg'></div>\n";
	l_html += "</div>\n";
	return l_html;
}
/**
 * Build the middle part of the display.
 * 
 * @param: p_rows is the number of rows to allow space for.
 * @param: p_html is the (big) html for the entire body.
 */
function build_lcars_middle_menu(p_rows, p_html) {
	var l_html = '';
	var l_half = (p_rows + 1) / 2;
	l_html += "<div class='lcars-row spaced'>\n"; // row 1

	l_html += "  <div class='lcars-column u-1-8'>\n"; // Column 1
	l_html += "    <ul class='lcars-menu left'>\n"; // filler bar left
	for (var l_row = 0; l_row < l_half; l_row++)
		l_html += "      <li class='lcars-blue-bg'></li>\n";
	for (l_row = 0; l_row < l_half; l_row++)
		l_html += "      <li class='lcars-tan-bg'></li>\n";
	l_html += "    </ul>\n";
	l_html += "  </div>\n"; // column 1

	l_html += "  <div class='lcars-column u-6-8'>\n"; // Middle columns
	l_html += p_html;
	l_html += "  </div>\n";

	l_html += "  <div class='lcars-column u-1-8'>\n"; // Right columns
	l_html += "    <ul class='lcars-menu right'>\n";
	for (l_row = 0; l_row < l_half; l_row++)
		l_html += "      <li class='lcars-tan-bg'></li>\n";
	for (l_row = 0; l_row < l_half; l_row++)
		l_html += "      <li class='lcars-blue-bg'></li>\n";
	l_html += "    </ul>\n";
	l_html += "  </div>\n";

	l_html += "</div>\n";
	return l_html;
}
/**
 * Build the bottom part of the display.
 */
function build_lcars_bottom() {
	var l_html = '';
	l_html += "<div class='lcars-row spaced'>\n";
	l_html += "  <div class='lcars-column u-1-8 lcars-elbow left top lcars-tan-bg'></div>";
	l_html += "  <div class='lcars-column u-6-8 lcars-divider bottom lcars-tan-blue-divide'></div>";
	l_html += "  <div class='lcars-column u-1-8 lcars-elbow right top lcars-blue-bg'></div>\n";
	l_html += "</div>\n";
	return l_html;
}

// Menu
/**
 * Build a LCAR style Menu button
 */
function buildLcarMenuButton(p_button, p_background_color, p_handler) {
	// console.log("lcars.buildLcarMenuButton() Button %O", p_button);
	var l_html = '';
	l_html += "<button type='button' ";
	l_html += setValueAttribute(p_button[1]);
	l_html += "class='lcars-button radius " + p_background_color + "' ";
	l_html += setNameAttribute(p_button[0]);
	l_html += "onclick='return Nevow.Athena.Widget.handleEvent(this, \"onclick\", \"" + p_handler + "\" ";
	l_html += ");' >\n";
	l_html += p_button[1];
	return l_html;
}
function buildLcarMenuButtons(p_list, p_handler) {
	// console.log("lcars.buildLcarMenuButtons() - list: %O", p_list);
	var l_button = [];
	var l_cols = 5;
	var l_count = 0;
	var l_html = "<div class='lcars-row spaced'>\n";
	for (var l_ix = 0; l_ix < p_list.length; l_ix++) {
		l_button = p_list[l_ix];
		var l_background = 'lcars-orange-bg';
		l_html += "<div class='lcars-column u-1-6'>\n";
		l_html += buildLcarMenuButton(l_button, l_background, p_handler);
		l_count++;
		l_html += "</div>\n"; // column
		if ((l_count > 0) & (l_count % l_cols === 0)) {
			l_html += "</div>\n"; // Row
			l_html += "<div class='lcars-row spaced'>\n";
		}
	}
	l_html += "</div>\n"; // Row
	return l_html;
}
/**
 * Build a LCAR style selection button
 * 
 * <button
 *     type='button'
 *     value='obj_name'
 *     class='lcars-button radius background_color'
 *     name='obj_key'
 *     onclick='return Nevow.Athena.Widget.handleEvent(this, "onclick", "p_handler" );'
 *     >
 *     NameCreatedByNameFunction
 * </button>
 * 
 */
function buildLcarButton(p_obj, p_handler, p_background_color, /* optional */nameFunction) {
	var l_html = '';
	l_html += "<button type='button' ";
	l_html += setValueAttribute(p_obj.Name);
	l_html += "class='lcars-button radius " + p_background_color + "' ";
	l_html += setNameAttribute(p_obj.Key);
	l_html += "onclick='return Nevow.Athena.Widget.handleEvent(this, \"onclick\", \"" + p_handler + "\" ";
	l_html += ");' >\n";
	if (typeof nameFunction === 'function')
		l_html += nameFunction(p_obj);
	else
		l_html += p_obj.Name;
	l_html += "</button>\n";
	return l_html;
}

// ============================================================================
// Base entry data routines

function buildBaseEntry(self, p_obj, p_html, /* optional */noUuid) {
	/*
	 * Build a base entry - Name, Key, Active, UUID If called with 'nouuid' then
	 * the UUID field will not be displayed. If the UUID field is displayed, It
	 * will be unchangeable.
	 */
	var l_uuid = noUuid;
	// Divmod.debug('---', 'lcars.build_lcars_top() was called. ' + noUuid);
	p_html += buildTextWidget(self, 'Name', 'Device Name', p_obj.Name);
	p_html += buildTextWidget(self, 'Key', 'Index', p_obj.Key, 'size=10 disabled');
	p_html += buildTrueFalseWidget(self, 'Active', 'Active ?', p_obj.Active);
	if (l_uuid === undefined)
		p_html += buildTextWidget(self, 'UUID', 'UUID', p_obj.UUID, 'disabled');
	return p_html;
}

function fetchBaseEntry(self) {
	var l_data = {
		Add : false,
		Delete : false
	};
	l_data.Name = fetchTextWidget(self, 'Name');
	l_data.Key = fetchTextWidget(self, 'Key');
	l_data.Active = fetchTrueFalseWidget(self, 'Active');
	try {
		l_data.UUID = fetchTextWidget(self, 'UUID');
	} catch (err) {
		;
	}
	return l_data;
}

function createBaseEntry(self, p_key) {
	var l_data = {
		Delete : false,
		Add : false
	};
	l_data.Name = 'ChangeMe';
	if (p_key === undefined)
		p_key = 0;
	l_data.Key = p_key;
	l_data.Active = true;
	l_data.UUID = generateUUID();
	return l_data;
}

//============================================================================
// Lighting Core entry data routines

function buildDeviceEntry(self, p_obj, p_handleChange) {
	// Divmod.debug('---', 'lcars.buildDeviceEntry() was called.');
	// console.log("lcars.buildDeviceEntry() Device = %O", p_obj);
	var l_html = '';
	l_html += buildTextWidget(self, 'Comment', 'Comment', p_obj.Comment);
	l_html += buildRoomSelectEntry(self, p_obj, p_handleChange);  // in handle_rooms.js
	return l_html;
}

function fetchDeviceEntry(self, p_data) {
	p_data.Comment = fetchTextWidget(self, 'Comment');
	fetchRoomSelectEntry(self, p_data);  // in handle_rooms.js
}

function createDeviceEntry(self, p_data) {
	p_data.Comment = '';
	p_data.DeviceFamily = 'Insteon';
	createRoomSelectEntry(self, p_data);
}

// Divmod.debug('---', 'lcars.build_lcars_top() was called.');
// console.log("lcars.build_lcars_middle() - %O", l_html);

// END DBK
