/**
 * @name:      PyHouse/src/Modules/Web/js/globals.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2015 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Mar 11, 2014
 * @summary:   This is the global hook where we hang our coat and everything else
 *
 * A not so impressive way to get dynamic modules loading properly when inserting fragments at some later time into the webapp.
 * The most promising way is to preload although this could lead to quite some code clutter,
 *  but knowing that the clients do not unload JS means at least preloading does no harm.
 *
 *  modulesWaiting = {};
 *
 *  function moduleLoaded(module) {
 *      modulesWaiting[module] = null;
 *      //Divmod.debug("moduleLoaded", "loaded module: " + module);
 *  }
 *
 *  function waitForModules(module, f) {
 *      modulesWaiting[module] = f;
 *      for (var m in modulesWaiting) {
 *          if (modulesWaiting[m])
 *              modulesWaiting[m]();
 *      }
 *  }
 *
 */
// import Divmod.Runtime
// import helpers


var REQ_404 = -1;
var REQ_ROOT = 0;
var REQ_WITHID = 2;
var BUTTON_ADD      = 10001;
var BUTTON_BACK     = 10002;
var BUTTON_CHANGE   = 10003;
var BUTTON_DELETE   = 10004;
var COLOR_LIGHT_RED      = '#ffa0a0';
var COLOR_LIGHT_GREEN    = '#b0ffa0';

globals = {
	XXXfonts : [ 'Arial', 'Helvetica', 'sans-serif' ],
	workspace : null,

	Computer : {},
	House : {},
	List : {},  // List of houses to select from
	Interface : {},
	User : {},
	Valid : {},

	__init__ : function() {
		globals.appLoaded = false;
		globals.center = {
			x : 400,
			y : 280
		};
		globals.tsize = {
			w : 800,
			h : 655
		};
	}
};


function int2str(i) {
	if (i < 10)
		return '0' + String(i);
	else
		return String(i);
}


function getCardSizefromCSS() {
	var s;
	var size;
	var w = 0;
	var h = 0;
	var n = 0;
	var done = false;
	Divmod.debug('---', 'globals.getCardSizefromCSS was called.');
	while (!done) {
		var rules = getCSSrules(n);
		if (rules === null)
			break;
		for ( var i = 0; i < rules.length; i++) {
			if (/\.cardsize/.test(rules[i].selectorText)) {
				size = rules[i].style.width;
				if ((size != 'none') && (size.length > 0)) {
					s = /^(\d*)(px)/.exec(size);
					if (s)
						w = parseInt(s[1], 10);
					else
						w = 0;
				}
				size = rules[i].style.maxHeight;
				if ((size != 'none') && (size.length > 0)) {
					s = /^(\d*)(px)/.exec(size);
					if (s)
						h = parseInt(s[1], 10);
					else
						h = 0;
				}
				done = true;
				break;
			}
		}
		n++;
	}
	return {
		w : w,
		h : h
	};
}



function collectClasses(node) {
	Divmod.debug('---', 'globals.collectClasses was called.');
	var classnames = [];
	var nodes = getElementsByTagAndClassName('div', null, node);  // (tagname, classname, parent)
	for ( var i = 0; i < nodes.length; i++) {
		if (nodes[i].className !== null) {
			classnames.push('.' + nodes[i].className);
		}
	}
	return classnames;
}



/**
 * Collects all the URIs present in img tags in within this node.
 * If the imgs array is passed into the function all found URIs are appended to the array, which can
 *  be passed later on to the loadImages function, which preloads all those images.
 */
function collectIMG_src(node, imgs) {
	// Divmod.debug('---', 'globals.collectIMG_src was called.  Node:' + node.className);
	// console.log("  collectIMG_src    %O", node);
	if (imgs != typeof ([])) {
		imgs = [];
	}
	var nodes = Divmod.Runtime.theRuntime.getElementsByTagNameShallow(node, 'img');
	for ( var i = 0; i < nodes.length; i++) {
		var src = nodes[i].src;
		imgs.push(src);
	}
	return imgs;
}



function getCSSrules(n) {
	Divmod.debug('---', 'globals.getCSSrules was called.');
	if (n < document.styleSheets.length) {
		if (document.styleSheets[0].rules) {
			return document.styleSheets[n].rules; // IE
		} else {
			return document.styleSheets[n].cssRules; // Mozilla
		}
	}
	return null;
}



/**
 * Collects all URIs in the present CSS which refer to images, thus allowing for the loadImages
 *  function to check for all images present in a browser neutral way.
 * 
 * If passed null the function creates an empty array of URIs and starts collecting them.
 * This allows for having an images array beforehand and adding other images (from offsite URIs) to the array manually.
 */
function collectCSS_backgroundImages(imgs, selectors) {
	Divmod.debug('---', 'globals.collectCSS_backgroundImages was called.');
	if (imgs === null) {
		imgs = [];
	}

	function addURI(uri) {
		for ( var j = 0; j < imgs.length; j++) {
			if (uri == imgs[j]) 
				return;
		}
		imgs.push(uri);
	}  // addURI

	function matchSelectors(sel, sels) {
		if (sels === null)
			return true;

		for ( var i = 0; i < sels.length; i++) {
			if (sels[i] == sel)
				return true;
		}
		return false;
	}  // matchSelectors

	var n = 0;
	while (true) {
		var rules = getCSSrules(n);
		if (rules === null)
			break;
		for ( var i = 0; i < rules.length; i++) {
			if (matchSelectors(rules[i].selectorText, selectors)) {
				var uri = rules[i].style.backgroundImage;
				if ((uri != 'none') && (uri.length > 0)) {
					var u = /^url\((.*)\)$/.exec(uri);
					if (u) {
						addURI(u[1]); // Safari has rather strange ideas of URIs in CSS
					}
				}
			}
		}
		n++;
	}
	return imgs;
}  // collectCSS_backgroundImages


/** DBK - unused so far.
 * 
 * Given a bunch of flags this function will sit and wait until all flags go to true.
 * If this happens callback is called, if not after some time the errback will be triggered.
 */
globals.TimeoutError = Divmod.Error.subclass('globals.TimeoutError');

function waitfor(flags, timeout) {
	function flagstrue() {
		for ( var i = 0; i < flags.length; i++) {
			if (!flags[i])
				return false;
		}
		return true;
	}

	var stepcount = 0;
	var steprate = 2; // checks per second
	var waitDeferred = Divmod.Defer.Deferred();
	var checkStep = function() {
		if (stepcount > (timeout * steprate)) {
			self.timer = null;
			// waitDeferred.errback(minimal.common.globals.TimeoutError('timeout...'));
			waitDeferred.errback(globals.TimeoutError('timeout...'));
		} else if (flagstrue()) {
			waitDeferred.callback();
		} else {
			stepcount++;
			self.timer = setTimeout(checkStep, 1000 / steprate);
		}
	};  // checkStep

	self.timer = setTimeout(checkStep, 1000 / steprate);
	return waitDeferred;
}  // waitfor



/**
 * Load image URIs
 */
globals.ImageLoadingError = Divmod.Error.subclass('globals.ImageLoadingError');

/**
 * Load Images deferred.
 * 
 * allow 60 seconds for all images to load.
 * trigger callback if all loaded in time
 * trigger errback if time expired before they all were loaded.
 */
function loadImages(uris) {
	// Divmod.debug('---', 'globals.loadImages was called.');
	var imgs = [];
	for ( var i = 0; i < uris.length; i++) {
		var img = new Image();
		img.src = uris[i];
		imgs.push(img);
	}

	/**
	 * Test to see if image is read into DOM yet.
	 * Will be false if default placeholder has not been filled (I think).
	 * 
	 * @param img
	 * @returns {Boolean}
	 */
	function isImageOk(img) {
		if (!img.complete)
			return false;
		if (typeof img.naturalWidth != "undefined" && img.naturalWidth === 0)
			return false;
		return true;
	}

	/**
	 * Test if *ALL* images have been loaded yet.
	 * 
	 * @returns {Boolean} true if all images are loaded
	 */
	function imgsloaded() {
		for ( var i = 0; i < imgs.length; i++) {
			if (!isImageOk(imgs[i]))
				return false;
		}
		return true;
	}  // imgsloaded

	/**
	 * List the images that have not loaded.
	 * 
	 * @returns {String}
	 */
	function imgsNotloaded() {
		var estr = '';
		for ( var i = 0; i < imgs.length; i++) {
			if (!isImageOk(imgs[i])) {
				if (estr.length > 0)
					estr += '; ';
				estr = estr + imgs[i].src;
			}
		}
		return estr;
	}  // imgsNotloaded

	var stepcount = 0;
	var steprate = 2; // checks per second
	var l_ready_deferred = Divmod.Defer.Deferred();

	var checkStep = function() {
		var timer = null;
		if ((stepcount > 120)) {
			//self.timer = null;
			timer = null;
			l_ready_deferred.errback(new globals.ImageLoadingError(
					'could not load all images: ' + imgsNotloaded()));
		} else if (imgsloaded()) {
			l_ready_deferred.callback();
		} else {
			stepcount++;
			//self.timer = setTimeout(checkStep, 1000 / steprate);
			timer = setTimeout(checkStep, 1000 / steprate);
		}
	};  // checkStep

	//self.timer = setTimeout(checkStep, 1000 / steprate);
	timer = setTimeout(checkStep, 1000 / steprate);
	return l_ready_deferred;
}  // loadImages



/**
 * Create a server state class that returns a deferred.
 * 
 * The deferred id triggered whenever the server state changes.
 * 
 * The main purpose is to control the display of the various sections of the PyHouse web page.
 */
globals.ServerStateError = Divmod.Error.subclass('globals.ServerStateError');

function serverState(p_state) {
	// Divmod.debug('---', 'globals.serverState was called. state:' + p_state);
	var m_state = p_state;
	var steprate = 2; // checks per second
	var maxsteps = steprate * 60 * 60 * 24;
	var stepcount = 0;
	var stateDeferred = Divmod.Defer.Deferred();
	var checkStep = function() {
		if ((stepcount > maxsteps)) {
			self.timer = null;
			stateDeferred.errback(new globals.ServerStateError('Invalid Server State: ' + m_state));
		} else if ((m_state < 999)) {
			stateDeferred.callback();
		} else {
			stepcount++;
			self.timer = setTimeout(checkStep, 1000 / steprate);
		}
	};
	self.timer = setTimeout(checkStep, 1000 / steprate);
	return stateDeferred;
}



/**
 * Find a widget in the workspace using 'class' of the widget.
 */
function findWidgetByClass(p_name) {
	for (var ix=0; ix < globals.workspace.childWidgets.length; ix++) {
		var l_widget = globals.workspace.childWidgets[ix];
		if (l_widget.node.className.toLowerCase() == p_name.toLowerCase())
			return l_widget;
	}
	Divmod.debug('---', 'ERROR - globals.findWidgetByClass failed for ' + p_name);
	console.log("globals.findWidgetByClass() - %O", globals.workspace.childWidgets);
	return undefined;
}



/**
 * Get PyHouse data from server.
 */
function getPyHouseData() {
	var steprate = 2; // checks per second
	var maxsteps = steprate * 60 * 60 * 24;
	var stepcount = 0;
	var stateDeferred = Divmod.Defer.Deferred();
	var checkStep = function() {
		if ((stepcount > maxsteps)) {
			self.timer = null;
			stateDeferred.errback(new globals.ServerStateError('Invalid Server State: ' + m_state));
		} else if ((m_state < 999)) {
			stateDeferred.callback();
		} else {
			stepcount++;
			self.timer = setTimeout(checkStep, 1000 / steprate);
		}
	};
	self.timer = setTimeout(checkStep, 1000 / steprate);
	return stateDeferred;
}
/**
 * Update PyHouse data back to server.
 */
function updatePyHouseData() {
	Divmod.debug('---', 'globals.updatePyHouseData() was called. ');
}



//============================================================================

function showSelectionButtons(self) {
	// Divmod.debug('---', 'globals.showSelectionButtons() was called.');
	// console.log("globals.showSelectionButtons() - %O", self);
	self.nodeById('DataEntryDiv').style.display = 'none';
	self.nodeById('SelectionButtonsDiv').style.display = 'block';
}
function showDataEntryFields(self) {
	// Divmod.debug('---', 'globals.showDataEntryFields() was called.');
	// console.log("globals.showDataEntryFields() - %O", self);
	self.nodeById('SelectionButtonsDiv').style.display = 'none';
	self.nodeById('DataEntryDiv').style.display = 'block';
}

// ============================================================================
/**
 * A series of routines to build HTML for insertion into widgets.
 */

/**
 * Build an athena qualified ID
 * 
 * Changes the supplied p_id from "LoginName" to "athenaid:11-LoginName" for example.
 */
function buildAthenaId(self, p_id) {
	l_id = self.node.id + '-' + p_id;
	var l_ret = l_id.substring(0, 6) + 'id' + l_id.substring(6, l_id.length);
	return l_ret;
}

function setCheckedAttribute(p_checked) {
	var l_html = "";
	if (p_checked)
		l_html += " checked='checked'";
	return l_html;
}
function setIdAttribute(p_id) {
	var l_html = "";
	l_html += " id='" + p_id + "'";
	return l_html;
}
function setNameAttribute(p_name) {
	var l_html = "";
	l_html += " name='" + p_name + "'";
	return l_html;
}
function setSizeOption(p_options) {
	var l_size = 40;
	if (p_options !== undefined) {
		var l_ix = p_options.toLowerCase().indexOf('size=');
		if (l_ix > -1)
			l_size = p_options.substring(l_ix+5, l_ix+7);
	}
	return setSizeAttribute(l_size);
}
function setSizeAttribute(p_size) {
	var l_html = '';
	l_html += " size='" + p_size + "'";
	return l_html;
}
function setValueAttribute(p_value) {
	var l_html = " value='" + p_value + "'";
	return l_html;
}
function buildTopDivs(p_caption) {
	var l_html = '';
	l_html += "<div class='lcars-row spaced'>\n";
	l_html += "<div class=lcars-column u-3-4'>\n";
	l_html += "<div class='lcars-button radius'>\n";
	if (p_caption !== 'undefined') {
		l_html += p_caption + "&nbsp";
	}
	return l_html;
}
function buildBottomDivs() {
	var l_html = '';
	l_html += "</div>\n";  // Button
	l_html += "</div>\n";  // Column
	l_html += "</div>\n";  // row 1
	return l_html;
}



/**
 * Build a LCAR style button
 */
function XXXbuildLcarButton(p_obj, p_handler, p_background_color, /* optional */ nameFunction) {
	var l_html = '';
	//l_html += "<div class='lcars-button radius " + p_background_color + "'>";
	l_html += "<button type='button' ";
	l_html += setValueAttribute(p_obj.Name);
	l_html += "class='lcars-button radius " + p_background_color + "' ";
	l_html += setNameAttribute(p_obj.Key);
	l_html += "onclick='return Nevow.Athena.Widget.handleEvent(this, \"onclick\", \""  + p_handler + "\" ";
	l_html += ");' >\n";
	if (typeof nameFunction === 'function')
		l_html += nameFunction(p_obj);
	else
		l_html += p_obj.Name;
	l_html += "</button>\n";
	// console.log("globals.buildLcarButton() - %O", l_html)
	return l_html;
}
function buildLcarAddButton(p_handler) {
	return buildLcarButton({'Name' : 'Add', 'Key' : BUTTON_ADD}, p_handler, 'lcars-salmon-bg');
}
function buildLcarBackButton(p_handler) {
	return buildLcarButton({'Name' : 'Back', 'Key' : BUTTON_BACK}, p_handler, 'lcars-salmon-bg');
}
function buildLcarChangeButton(p_handler) {
	return buildLcarButton({'Name' : 'Change', 'Key' : BUTTON_CHANGE}, p_handler, 'lcars-salmon-bg');
}
function buildLcarDeleteButton(p_handler) {
	return buildLcarButton({'Name' : 'Delete', 'Key' : BUTTON_DELETE}, p_handler, 'lcars-salmon-bg');
}



/**
 * Build a table of buttons in the current widget space.
 * Use the names to build callbacks for the buttons being clicked on
 * Used for things like selecting a light or schedule to work on.
 *
 * @param p_obj = a dict of item dicts to build from
 * @param p_handler = is a literal name of a handler function { 'handleMenuOnClick' )
 * @param p_nameFunction (optional) is the name of a function used to build a more complex caption for the buttons.
 * 			Omit this parameter if it is not used - no need for a placeholder
 * @param p_noOptions (optional) is the things to skip ('NoAdd' will omit the add button).
 *
 * @returns = innerHTML of a table filled in with buttons
 */
function buildLcarSelectionButtonsTable(p_obj, p_handler, p_nameFunction, p_noOptions) {
	var l_nameFunction = p_nameFunction;
	var l_noOptions = p_noOptions;
	if (typeof p_nameFunction !== 'function') {  // See if function was passed
		l_noOptions = p_nameFunction;
		l_nameFunction = null;
	}
	if (l_noOptions === undefined)
		l_noOptions = '';
	var l_cols = 5;
	var l_count = 0;
	var l_html = "<div class='lcars-row spaced'>\n";
	for (var l_item in p_obj) {
		var l_background = 'lcars-purple-bg';
		if (p_obj[l_item].Active !== true)
			l_background = 'lcars-pink-bg';
	    l_html += "<div class='lcars-column u-1-6'>\n";
		l_html += buildLcarButton(p_obj[l_item], p_handler, l_background, l_nameFunction);
		l_count++;
	    l_html += "</div>\n";  // column
		if ((l_count > 0) & (l_count % l_cols === 0)) {
			l_html += "</div>\n";  // Row
			l_html += "<div class='lcars-row spaced'>\n";
		}
	}
	l_html += "</div>\n";  // Row
	l_html += "<div class='lcars-row spaced'>\n";
	if (l_noOptions.toLowerCase().indexOf('add') === -1)
		l_html += buildLcarAddButton(p_handler);
	if (l_noOptions.toLowerCase().indexOf('back') === -1)
		l_html += buildLcarBackButton(p_handler);
	l_html += "</div>\n";  // Row
	return l_html;
}


/**
 * Entry buttons are for the bottom of data entry screens.
 * 
 * @param: p_handler is the onclick event handler for the data entry buttons
 * @param: noOptions is the string that tells us not to build a button - 'NoDelete' means not to build a delete button
 */
function buildLcarEntryButtons(p_handler, /* optional */ noOptions) {
	// Divmod.debug('---', 'globals.buildLcarEntryButtons() called.  Handler=' + p_handler + '  ' + noOptions);
	var l_options = noOptions;
	if (l_options === undefined)
		l_options = '';
	var l_html = '';
	if (l_options.toLowerCase().indexOf('change') === -1)
		l_html = buildLcarChangeButton(p_handler);
	if (l_options.toLowerCase().indexOf('delete') === -1)
		l_html += buildLcarDeleteButton(p_handler);
	if (l_options.toLowerCase().indexOf('back') === -1)
		l_html += buildLcarBackButton(p_handler);
	return l_html;
}


//========== Radio Button Widgets ==================================================================
/**
 * Radio button set widget.
 * 
 * @param p_name   is the name of the radio button set ('SchedActive' e.g.) also used as a label.
 *   suggested values are like 'SchedActive', 'RoomActive'
 * @param p_value  is bool showing the current value .
 */
function _buildLcarRadioButtonWidget(p_name, p_label, p_value, p_checkVal) {
	var l_html = "&nbsp;<input type='radio'";
	l_html += setNameAttribute(p_name);
	l_html += setValueAttribute(p_value);
	l_html += setCheckedAttribute(p_value === p_checkVal);
	l_html += "/>" + p_label + '&nbsp;\n';
	return l_html;
}
/**
 * Note the name is athenaid:xx-Name
 */
function buildLcarTrueFalseWidget(self, p_id, p_caption, p_value) {
	var l_html = '';
	var l_name = buildAthenaId(self, p_id);
	var l_value = p_value !== false;  // force to be a bool
	l_html += buildTopDivs(p_caption);
	l_html += "<span class='lcars-button-addition'>\n";
	l_html += _buildLcarRadioButtonWidget(l_name, 'True',  true, l_value);
	l_html += _buildLcarRadioButtonWidget(l_name, 'False', false, l_value);
	l_html += "</span>";
	l_html += buildBottomDivs();
	return l_html;
}
function fetchTrueFalseWidget(self, p_name) {
	var l_name = buildAthenaId(self, p_name);
	var l_buttons = document.getElementsByName(l_name);
	var l_ret = false;
	for (var ix = 0; ix < l_buttons.length; ix++) {
		if (l_buttons[ix].checked && l_buttons[ix].value === 'true') {
			l_ret = true;
			break;
		}
	}
	return l_ret;
}


//========== Select Widgets ==================================================================
/**
 * Build a select widget
 * 
 * @param: p_id is the ID of the select field.
 * @param: p_list is the list of valid options to be added to the select box.
 * @param: p_checked is the text of the option list that is selected.
 * @param: p_optionChange is the optional onchange function name.
 */
function buildLcarSelectWidget(self, p_id, p_caption, p_list, p_checked, /* optional */ p_optionChange) {
	var l_option = p_optionChange;
	var l_html = "";
	l_html += buildTopDivs(p_caption);
	l_html += "<select class='lcars-button-addition'";
	l_html += setIdAttribute(buildAthenaId(self, p_id));
	if (l_option !== 'undefined') 
		l_html += "onchange='return Nevow.Athena.Widget.handleEvent(this, \"onchange\", \"" + l_option + "\");' ";
	l_html += ">\n";
	for (var ix = 0; ix < p_list.length; ix++) {
		var l_name = p_list[ix];
		l_html += "<option";
		l_html += setValueAttribute(ix);
		if (l_name == p_checked)
			l_html += 'selected ';
		l_html += ">" + l_name + "</option>\n";
	}
	l_html += "</select>";
	l_html += buildBottomDivs();
	return l_html;
}
function fetchSelectWidget(self, p_id) {
	var l_field = self.nodeById(p_id);
	var l_ix = l_field.value;
	var l_name = l_field.options[l_field.selectedIndex].text;
	return l_name;
}
function _makeNamesList(p_obj) {
	var l_list = [];
	for (var ix = 0; ix < Object.keys(p_obj).length; ix++)
		l_list[ix] = p_obj[ix].Name;
	return l_list;
}
function buildLcarRoomSelectWidget(self, p_id, p_caption, p_checked) {
	var l_obj = globals.House.HouseObj.Rooms;
	var l_list = [];
	for (var ix = 0; ix < Object.keys(l_obj).length; ix++)
		l_list[ix] = l_obj[ix].Name;
	return buildLcarSelectWidget(self, p_id, p_caption, l_list, p_checked);
}
function buildLcarLightNameSelectWidget(self, p_id, p_caption, p_checked) {
	var l_obj = globals.House.HouseObj.Lights;
	var l_list = [];
	for (var ix = 0; ix < Object.keys(l_obj).length; ix++)
		l_list[ix] = l_obj[ix].Name;
	return buildLcarSelectWidget(self, p_id, p_caption, l_list, p_checked);
}
function buildLcarFloorSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.Floors, p_checked);
}
function buildLcarLightTypeSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.LightType, p_checked);
}
function buildLcarProtocolTypeSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.ProtocolType, p_checked);
}
function buildLcarScheduleModeSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.ScheduleMode, p_checked);
}
function buildLcarScheduleTypeSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.ScheduleType, p_checked);
}

function buildLcarThermostatTypeSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.LightType, p_checked);
}



//========== Slider Widgets ==================================================================
/**
 * Build a slider widget'
 *
 * The widget must handle the slider change event.
 */
function buildLcarSliderWidget(self, p_id, p_caption, p_value, p_min, p_max, p_step, p_handler) {
	var l_html = "";
	var l_id = buildAthenaId(self, p_id);
	var l_out = buildTopDivs(p_caption);
	l_out += "<span class='lcars-button-addition'";
	l_out += setIdAttribute(l_id);
	l_out += ">";
	l_html += "<input class='lcars-button-addition' ";
	l_html += "type='range'";
	l_html += setNameAttribute('slider');
	l_html += setIdAttribute(l_id + "-Slider");
	l_html += "min='" + p_min + "' ";
	l_html += "max='" + p_max + "' ";
	l_html += "step='" + p_step + "' ";
	l_html += "onchange='return Nevow.Athena.Widget.handleEvent(this, \"onchange\", \"" + p_handler + "\");' ";
	l_html += setValueAttribute(p_value);
	l_html += " >\n";
	l_html += '&nbsp';
	l_html += "<input type='text'";
	l_html += setIdAttribute(l_id + "-Box");
	l_html += setSizeAttribute(4);
	l_html += setValueAttribute(p_value);
	l_html += " >\n";
	l_out += l_html;
	l_out += "</span>\n";
	l_out += buildBottomDivs();
	return l_out;
}
function fetchSliderWidget(self, p_id) {
	// Divmod.debug('---', 'globals.fetchSliderWidget(1) Id=' + p_id);
	var l_id = p_id + "-Slider";
	// Divmod.debug('---', 'globals.fetchSliderWidget(2) Id=' + l_id);
	var l_val = self.nodeById(l_id).value;
	return l_val;
}
function updateSliderBoxValue(self, p_id, p_value){
	var l_id = p_id + "-Box";
	var l_node = self.nodeById(l_id);
	l_node.value = p_value;
}
function buildLcarLevelSliderWidget(self, p_name, p_caption, p_level, p_handler) {
	var l_html = buildLcarSliderWidget(self, p_name, p_caption, p_level, 0, 100, 1, p_handler);
	return l_html;
}
function buildLcarHvacSliderWidget(self, p_name, p_caption, p_level, p_handler) {
	var l_html = buildLcarSliderWidget(self, p_name, p_caption, p_level, 60, 90, 0.5, p_handler);
	return l_html;
}



//========== Text Widgets ==================================================================
/**
 * Build a text widget
 * 
 * @param: p_id is the ID of the imput widget.
 * @param: p_value is the value to be displyed when the widget appears.
 * @param: p_options contains 'disable' if the field is unchangeable.
 * 			contains size=xx to change the size of the entry field
 */
function buildLcarTextWidget(self, p_id, p_caption, p_value, p_options) {
	// Divmod.debug('---', 'globals.buildLcarTextWidget() was called.');
	var l_size = 40;
	var l_options = p_options;
	var l_id = buildAthenaId(self, p_id);
	if (p_options === undefined)
		l_options = '';
	var l_html = buildTopDivs(p_caption);
	l_html += "<input type='text' class='lcars-button-addition'";
	l_html += setIdAttribute(l_id);
	l_html += setSizeOption(p_options);
	l_html += setValueAttribute(p_value);
	l_html += " ";
	if (l_options.toLowerCase().indexOf('disable') > -1)
		l_html += "disabled='disabled' ";
	l_html += " />\n";
	// Add some code to set the focus to this field.
	if (l_options.toLowerCase().indexOf('focus') > -1)
		l_html += " ";
	l_html += buildBottomDivs();
	return l_html;
}
function buildLcarPasswordWidget(self, p_id, p_caption) {
	var l_html = buildTopDivs(p_caption);
	l_html += "<input type='password' class='lcars-button-addition'";
	l_html += setIdAttribute(buildAthenaId(self, p_id));
	l_html += setSizeAttribute(20);
	l_html += setValueAttribute('');
	l_html += " />\n";
	l_html += buildBottomDivs();
	return l_html;
}
function fetchTextWidget(self, p_id) {
	var l_data = self.nodeById(p_id).value;
	return l_data;
}



//========== DOW Widgets ==================================================================
/**
 * Day of Week Widget
 */
function buildLcarDowWidget(self, p_id, p_caption, p_value, /* optional */ p_options) {
	var l_html = buildTopDivs(p_caption);
	l_html += "<span class='lcars-button-addition'";
	l_html += setIdAttribute(buildAthenaId(self, p_id) + "Buttons");
	l_html += ">";
	l_html += "<input type='checkbox' name='" + p_id + "' value='1'";
	if (p_value & 1)
		l_html += " checked ";
	l_html += ">Mon&nbsp\n";
	l_html += "<input type='checkbox' name='" + p_id + "' value='2'";
	if (p_value & 2)
		l_html += " checked ";
	l_html += ">Tue&nbsp\n";
	l_html += "<input type='checkbox' name='" + p_id + "' value='4'";
	if (p_value & 4)
		l_html += " checked ";
	l_html += ">Wed&nbsp\n";
	l_html += "<input type='checkbox' name='" + p_id + "' value='8'";
	if (p_value & 8)
		l_html += " checked ";
	l_html += ">Thu&nbsp\n";
	l_html += "<input type='checkbox' name='" + p_id + "' value='16'";
	if (p_value & 16)
		l_html += " checked ";
	l_html += ">Fri&nbsp\n";
	l_html += "<input type='checkbox' name='" + p_id + "' value='32'";
	if (p_value & 32)
		l_html += " checked ";
	l_html += ">Sat&nbsp\n";
	l_html += "<input type='checkbox' name='" + p_id + "' value='64'";
	if (p_value & 64)
		l_html += " checked ";
	l_html += ">Sun&nbsp\n";
	l_html += "</span>\n";
	l_html += buildBottomDivs();
	return l_html;
}
function fetchDowWidget(self, p_id) {
	var l_dow = document.getElementsByName(p_id);
	var l_ret = 0;
	for (var ix = 0; ix < l_dow.length; ix++) {
		// Divmod.debug('---', 'globals.fetchDowWidget() called.  Name=' + p_id + '  Checked:' + l_dow[ix].checked + '  Val:' + l_dow[ix].value);
		if (l_dow[ix].checked) {
			l_ret += parseInt(l_dow[ix].value);
		}
	}
	// Divmod.debug('---', 'globals.fetchDowWidget() called.  FinalValue=' + l_ret);
	return l_ret;
}



//============================================================================
/**
 * Startup
 */
Divmod.Runtime.theRuntime.addLoadEvent(
	function appStartup() {
		globals.workspace.appStartup();
	}
);
// Divmod.debug('---', 'globals.buildLcarTextWidget() was called.');
// console.log("globals.build_lcars_middle() - %O", l_html);
// END DBK