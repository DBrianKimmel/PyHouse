/**
 * @name: PyHouse/src/Modules/Web/js/lcars.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2014 by D. Brian Kimmel
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
function build_lcars_top(p_title, /* optional* */ p_color){
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
	l_html += "      </div>\n";  // column_1-2
	l_html += "    </div>\n";  // row 2
	l_html += "  </div>\n";  // column_6-8
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
function build_lcars_middle_menu(p_rows, p_html){
	var l_html = '';
	var l_half = (p_rows + 1) / 2;
	l_html += "<div class='lcars-row spaced'>\n";  // row 1

	l_html += "  <div class='lcars-column u-1-8'>\n";  // Column 1
	l_html += "    <ul class='lcars-menu left'>\n";  // filler bar left
	for (var l_row = 0; l_row < l_half; l_row++)
		l_html += "      <li class='lcars-blue-bg'></li>\n";
	for (l_row = 0; l_row < l_half; l_row++)
		l_html += "      <li class='lcars-tan-bg'></li>\n";
	l_html += "    </ul>\n";
	l_html += "  </div>\n";  // column 1

	l_html += "  <div class='lcars-column u-6-8'>\n";  // Middle columns
	l_html += p_html;
	l_html += "  </div>\n";

	l_html += "  <div class='lcars-column u-1-8'>\n";  // Right columns
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
function build_lcars_bottom(){
	var l_html = '';
	l_html += "<div class='lcars-row spaced'>\n";
	l_html += "  <div class='lcars-column u-1-8 lcars-elbow left top lcars-tan-bg'></div>";
	l_html += "  <div class='lcars-column u-6-8 lcars-divider bottom lcars-tan-blue-divide'></div>";
	l_html += "  <div class='lcars-column u-1-8 lcars-elbow right top lcars-blue-bg'></div>\n";
	l_html += "</div>\n";
	return l_html;
}


// Base entry data routines

function buildBaseEntry(self, p_obj) {
	var l_html = '';
	l_html += buildLcarTextWidget(self, 'Name', 'Light Name', p_obj.Name);
	l_html += buildLcarTextWidget(self, 'Key', 'Light Index', p_obj.Key, 'size=10 disabled');
	l_html += buildLcarTrueFalseWidget(self, 'Active', 'Active ?', p_obj.Active);
	l_html += buildLcarTextWidget(self, 'UUID', 'UUID', p_obj.UUID, 'disabled');
	return l_html;
}
function fetchBaseEntry(self, p_data) {
	p_data.Name = fetchTextWidget(self, 'Name');
	p_data.Key = fetchTextWidget(self, 'Key');
	p_data.Active = fetchTrueFalseWidget(self, 'Active');
	p_data.UUID = fetchTextWidget(self, 'UUID');
	return p_data;
}
function createBaseEntry(self, p_key) {
    var l_data = {
		Delete : false
    };
	l_data.Name = 'ChangeMe';
	l_data.Key = p_key;
	l_data.Active = true;
	l_data.UUID = '123';
	return l_data;
}


// Lighting Core entry data routines

function buildLightingCoreEntry(self, p_obj, p_html, p_onchange) {
	p_html += buildLcarTextWidget(self, 'Comment', 'Comment', p_obj.Comment);
	p_html += buildLcarTextWidget(self, 'Coords', 'Coords', p_obj.Coords);
	p_html += buildLcarTrueFalseWidget(self, 'Dimmable', 'Light Dimmable ?', p_obj.IsDimmable);
	p_html += buildLcarFamilySelectWidget(self, 'ControllerFamily', 'Family', p_obj.ControllerFamily, p_onchange);
	p_html += buildLcarRoomSelectWidget(self, 'RoomName', 'Room', p_obj.RoomName);
	p_html += buildLcarLightTypeSelectWidget(self, 'LightingType', 'Type', p_obj.LightingType);
	return p_html;
}
function fetchLightingCoreEntry(self, p_data) {
    p_data.ControllerFamily = fetchSelectWidget(self, 'ControllerFamily');
    p_data.Comment = fetchTextWidget(self, 'Comment');
    p_data.Coords = fetchTextWidget(self, 'Coords');
    p_data.IsDimmable = fetchTrueFalseWidget(self, 'Dimmable');
    p_data.RoomName = fetchTextWidget(self, 'RoomName');
    p_data.LightingType = fetchSelectWidget(self, 'LightingType');
	return p_data;
}
function createLightingCoreEntry(self, p_data) {
    p_data.ControllerFamily = 'Insteon';
    p_data.Comment = '';
    p_data.Coords = "['0', '0']";
    p_data.IsDimmable = true;
    p_data.RoomName = 'XXX Room';
    p_data.LightingType = 'Light';
	return p_data;
}


// Divmod.debug('---', 'lcars.build_lcars_top() was called.');
// console.log("lcars.build_lcars_middle() - %O", l_html);
// END DBK
