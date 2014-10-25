/**
 * @name: PyHouse/src/Modules/Web/js/globals.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Mar 11, 2014
 * @summary: the global hook where we hang our coat and everything else
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
var BUTTON_INACTIVE = '#d0f0c0';
var BUTTON_ACTIVE   = '#d0d0ff';
var BUTTON_ADD      = 10001;
var BUTTON_BACK     = 10002;
var BUTTON_CHANGE   = 10003;
var BUTTON_DELETE   = 10004;
var COLOR_LIGHT_RED      = '#ffa0a0';
var COLOR_LIGHT_YELLOW   = '#f7ffa0';
var COLOR_LIGHT_GREEN    = '#b0ffa0';
var COLOR_LIGHT_BLUE     = '#d0d0ff';
var COLOR_LCARS_RED      = '#ff3300';
var COLOR_LCARS_L_BLUE   = '#ccccff';

globals = {
	XXXfonts : [ 'Verdana', 'Arial', 'Helvetica', 'sans-serif' ],
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
		if (!img.complete) {
			return false;
		}
		if (typeof img.naturalWidth != "undefined" && img.naturalWidth === 0) {
			return false;
		}
		return true;
	}  // isImageOK

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
		if ((stepcount > 120)) {
			self.timer = null;
			l_ready_deferred.errback(new globals.ImageLoadingError(
					'could not load all images: ' + imgsNotloaded()));
		} else if (imgsloaded()) {
			l_ready_deferred.callback();
		} else {
			stepcount++;
			self.timer = setTimeout(checkStep, 1000 / steprate);
		}
	};  // checkStep

	self.timer = setTimeout(checkStep, 1000 / steprate);
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
	Divmod.debug('---', 'ERROR - findWidgetByClass failed for ' + p_name);
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



// ============================================================================
/**
 * A series of routines to build HTML for insertion into widgets.
 */

/**
 * Build an athena qualified ID
 */
function buildAthenaId(self, p_id) {
	l_id = self.node.id + '-' + p_id;
	var l_ret = l_id.substring(0, 6) + 'id' + l_id.substring(6, l_id.length);
	return l_ret;
}

/**
 * Build a button
 */
function buildButton(p_obj, p_handler, p_background_color, /* optional */ nameFunction) {
	var l_html = '<td>';
	l_html += "<button type='button' ";
	l_html += "value='" + p_obj.Name + "' ";
	l_html += "name ='" + p_obj.Key + "' ";
	l_html += "style = 'background-color: " + p_background_color + "' ";
	l_html += "onclick = 'return Nevow.Athena.Widget.handleEvent(this, \"onclick\", \""  + p_handler + "\" ";
	l_html += ");' >\n";
	if (typeof nameFunction === 'function')
		l_html += nameFunction(p_obj);
	else
		l_html += p_obj.Name;
	l_html += "</button></td>\n";
	return l_html;
}
/**
 * <button type='button' class='lcars-button radius *bg_color*' name='*name*' onclick='return Nevow.Athena.Widget.handleEvent(this, "onclick", *p_handler*')>
 * *buttonName*
 * </button>
 */
function buildAddButton(p_handler) {
	return buildButton({'Name' : 'Add', 'Key' : BUTTON_ADD}, p_handler, COLOR_LIGHT_BLUE);
}
function buildBackButton(p_handler) {
	return buildButton({'Name' : 'Back', 'Key' : BUTTON_BACK}, p_handler, COLOR_LIGHT_BLUE);
}
function buildChangeButton(p_handler) {
	return buildButton({'Name' : 'Change', 'Key' : BUTTON_CHANGE}, p_handler, COLOR_LIGHT_BLUE);
}
function buildDeleteButton(p_handler) {
	return buildButton({'Name' : 'Delete', 'Key' : BUTTON_DELETE}, p_handler, COLOR_LIGHT_BLUE);
}


/**
 * Build a LCAR style button
 */
function buildLcarButton(p_obj, p_handler, p_background_color, /* optional */ nameFunction) {
	var l_html = '';
	l_html += "<button type='button' ";
	l_html += "value='" + p_obj.Name + "' ";
	l_html += "class='lcars-button radius " + p_background_color + "' ";
	l_html += "name='" + p_obj.Key + "' ";
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
 * @param nameFunction (optional) is the name of a function used to build a more complex caption for the buttons.
 * 			Omit this parameter if it is not used - no need for a placeholder
 * @param noOptions (optional) is the things to skip ('NoAdd' will omit the add button).
 * @returns = innerHTML of a table filled in with buttons
 */
function buildTable(p_obj, p_handler, /* optional */ nameFunction, noOptions) {
	var l_function = nameFunction;
	var l_options = noOptions;
	if (typeof nameFunction !== 'function') {
		l_options = l_function;
		l_function = null;
	}
	if (l_options === undefined)
		l_options = '';
	var l_cols = 5;
	var l_count = 0;
	var l_html = "<table><tr>\n";

	for (var l_item in p_obj) {
		var l_background = COLOR_LIGHT_GREEN;
		if (p_obj[l_item].Active !== true)
			l_background = COLOR_LIGHT_RED;
		l_html += buildButton(p_obj[l_item], p_handler, l_background, l_function);
		l_count++;
		if ((l_count > 0) & (l_count % l_cols === 0))
			l_html += '</tr><tr>\n';
	}
	l_html += "</tr><tr>\n";
	if (l_options.toLowerCase().indexOf('add') === -1)
		l_html += buildAddButton(p_handler);
	if (l_options.toLowerCase().indexOf('back') === -1)
		l_html += buildBackButton(p_handler);
	l_html += "</tr></table>\n";
	return l_html;
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
	// Divmod.debug('---', 'globals.buildLcarSelectionButtonsTable() called.  Handler=' + p_handler + '  ' + p_noOptions);
	var l_nameFunction = p_nameFunction;
	var l_noOptions = p_noOptions;
	// See if function was passed
	if (typeof p_nameFunction !== 'function') {
		l_noOptions = p_nameFunction;
		l_nameFunction = null;
	}
	if (l_noOptions === undefined)
		l_noOptions = '';
	var l_cols = 6;
	var l_count = 0;
	var l_html = "<div class='lcars-row spaced'>\n";
	for (var l_item in p_obj) {
		var l_background = 'lcars-purple-bg';
		if (p_obj[l_item].Active !== true)
			l_background = 'lcars-pink-bg';
	    l_html += "<div class='lcars-column u-1-7'>\n";
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
 */
function buildEntryButtons(p_handler, /* optional */ noOptions) {
	//Divmod.debug('---', 'globals.buildEntryButtons() called.  Handler=' + p_handler + '  ' + noOptions);
	var l_options = noOptions;
	if (l_options === undefined)
		l_options = '';
	var l_html = '';
	if (l_options.toLowerCase().indexOf('change') === -1)
		l_html = buildChangeButton(p_handler);
	if (l_options.toLowerCase().indexOf('delete') === -1)
		l_html += buildDeleteButton(p_handler);
	if (l_options.toLowerCase().indexOf('back') === -1)
		l_html += buildBackButton(p_handler);
	return l_html;
}
function buildLcarEntryButtons(p_handler, /* optional */ noOptions) {
	// Divmod.debug('---', 'globals.buildEntryButtons() called.  Handler=' + p_handler + '  ' + noOptions);
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


/**
 * Radio button set widget.
 * 
 * @param p_name   is the name of the radio button set ('SchedActive' e.g.) also used as a label.
 *   suggested values are like 'SchedActive', 'RoomActive'
 * @param p_value  is bool showing the current value .
 */
function buildRadioButtonWidget(p_name, p_label, p_value, p_checkVal) {
	var l_html = "&nbsp;<input type='radio' name='" + p_name + "' value='" + p_value + "' ";
	if (p_value == p_checkVal)
		l_html += "checked='checked'";
	l_html += "/>" + p_label + '&nbsp;\n';
	return l_html;
}
function buildLcarRadioButtonWidget(p_name, p_label, p_value, p_checkVal) {
	var l_html = "&nbsp;<input type='radio' name='" + p_name + "' value='" + p_value + "' ";
	if (p_value == p_checkVal)
		l_html += "checked='checked'";
	l_html += "/>" + p_label + '&nbsp;\n';
	return l_html;
}
function buildTrueFalseWidget(p_name, p_value) {
	var l_html = "<span id='" + p_name + "Buttons'>";
	var l_value = p_value !== false;  // force to be a bool
	l_html += buildRadioButtonWidget(p_name, 'True',  true, l_value);
	l_html += buildRadioButtonWidget(p_name, 'False', false, l_value);
	l_html += '</span>\n';
	return l_html;
}
function buildLcarTrueFalseWidget(self, p_id, p_caption, p_value) {

	var l_html = '';
	var l_value = p_value !== false;  // force to be a bool
	l_html += "<div class='lcars-row spaced'>\n";
	l_html += "<div class=lcars-column u-3-4'>\n";
	l_html += "<div class='lcars-button radius'>\n";
	l_html += p_caption;

	l_html += "<span class='lcars-button-addition' id='" + buildAthenaId(self, p_id) + "Buttons'>";
	l_html += buildLcarRadioButtonWidget(p_id, 'True',  true, l_value);
	l_html += buildLcarRadioButtonWidget(p_id, 'False', false, l_value);
	l_html += '</span>\n';

	l_html += "</div>\n";  // Button
	l_html += "</div>\n";  // Column
	l_html += "</div>\n";  // row 1
	return l_html;
}
function fetchTrueFalseWidget(p_name) {
	var l_active = document.getElementsByName(p_name);
	var l_ret = false;
	//Divmod.debug('---', 'globals.fetchTrueFalse() called.  Name=' + p_name + '  Len:' + l_active.length);
	for (var ix = 0; ix < l_active.length; ix++) {
		//Divmod.debug('---', 'globals.fetchTrueFalse() called.  Name=' + p_name + '  Checked:' + l_active[ix].checked + '  Val:' + l_active[ix].value);
		if (l_active[ix].checked && l_active[ix].value === 'true') {
			l_ret = true;
			break;
		}
	}
	return l_ret;
}


/**
 * Build a select widget
 */
function buildSelectWidget(p_id, p_list, p_checked) {
	//Divmod.debug('---', 'globals.buildSelectWidget() called.  p_list=' + p_list + '  p_checked=' + p_checked);
	var l_html = "<select id='" + p_id + "' >\n";
	for (var ix = 0; ix < p_list.length; ix++) {
		var l_name = p_list[ix];
		l_html += "<option value='" + ix + "' ";
		if (l_name == p_checked)
			l_html += 'selected ';
		l_html += ">" + l_name + "</option>\n";
	}
	l_html += "</select>\n";
	return l_html;
}
function buildLcarSelectWidget(self, p_id, p_caption, p_list, p_checked) {
	//Divmod.debug('---', 'globals.buildSelectWidget() called.  p_list=' + p_list + '  p_checked=' + p_checked);
	var l_html = "";
	l_html += "<div class='lcars-row spaced'>\n";
	l_html += "<div class=lcars-column u-3-4'>\n";
	l_html += "<div class='lcars-button radius'>\n";
	l_html += p_caption;
	l_html += "<select class='lcars-button-addition' id='" + p_id + "' >\n";
	for (var ix = 0; ix < p_list.length; ix++) {
		var l_name = p_list[ix];
		l_html += "<option value='" + ix + "' ";
		if (l_name == p_checked)
			l_html += 'selected ';
		l_html += ">" + l_name + "</option>\n";
	}
	l_html += "</select>\n";
	l_html += "</div>\n";
	l_html += "</div>\n";
	l_html += "</div>\n";
	return l_html;
}
function fetchSelectWidget(p_id) {
	var l_field = document.getElementById(p_id);
	var l_ix = l_field.value;
	var l_name = l_field.options[l_field.selectedIndex].text;
	//Divmod.debug('---', 'globals.fetchSelectWidget(1) was called. Id=' + p_id);
	//console.log("    %O", l_field);
	return l_name;
}
function buildRoomSelectWidget(p_id, p_checked) {
	var l_obj = globals.House.HouseObj.Rooms;
	var l_list = [];
	for (var ix = 0; ix < Object.keys(l_obj).length; ix++)
		l_list[ix] = l_obj[ix].Name;
	return buildSelectWidget(p_id, l_list, p_checked);
}
function buildLcarRoomSelectWidget(self, p_id, p_caption, p_checked) {
	//Divmod.debug('---', 'globals.buildRoomSelectWidget() was called. Id=' + p_id + '  Checked=' + p_checked);
	var l_obj = globals.House.HouseObj.Rooms;
	var l_list = [];
	for (var ix = 0; ix < Object.keys(l_obj).length; ix++)
		l_list[ix] = l_obj[ix].Name;
	return buildLcarSelectWidget(self, p_id, p_caption, l_list, p_checked);
}
function buildLightNameSelectWidget(p_id, p_checked) {
	//Divmod.debug('---', 'globals.buildLightNameSelectWidget() was called. Id=' + p_id + '  Checked=' + p_checked);
	var l_obj = globals.House.HouseObj.Lights;
	var l_list = [];
	for (var ix = 0; ix < Object.keys(l_obj).length; ix++)
		l_list[ix] = l_obj[ix].Name;
	return buildSelectWidget(p_id, l_list, p_checked);
}
function buildLcarLightNameSelectWidget(self, p_id, p_caption, p_checked) {
	//Divmod.debug('---', 'globals.buildLightNameSelectWidget() was called. Id=' + p_id + '  Checked=' + p_checked);
	var l_obj = globals.House.HouseObj.Lights;
	var l_list = [];
	for (var ix = 0; ix < Object.keys(l_obj).length; ix++)
		l_list[ix] = l_obj[ix].Name;
	return buildLcarSelectWidget(self, p_id, p_caption, l_list, p_checked);
}
function buildFamilySelectWidget(self, p_id, p_caption, p_checked) {
	Divmod.debug('---', 'globals.buildFamilySelectWidget() was called. Id=' + p_id + '  Checked=' + p_checked);
	return buildSelectWidget(self, p_id, p_caption, globals.Valid.Families, p_checked);
}
function buildLcarFamilySelectWidget(self, p_id, p_caption, p_checked) {
	Divmod.debug('---', 'globals.buildLcaeFamilySelectWidget() was called. Id=' + p_id + '  Checked=' + p_checked);
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.Families, p_checked);
}
function buildFloorSelectWidget(p_id, p_checked) {
	return buildSelectWidget(p_id, globals.Valid.Floors, p_checked);
}
function buildLcarFloorSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.Floors, p_checked);
}
function buildInterfaceTypeSelectWidget(p_id, p_checked) {
	return buildSelectWidget(p_id, globals.Valid.InterfaceType, p_checked);
}
function buildLcarInterfaceTypeSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.InterfaceType, p_checked);
}
function buildLightTypeSelectWidget(p_id, p_checked) {
	return buildSelectWidget(p_id, globals.Valid.LightType, p_checked);
}
function buildLcarLightTypeSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.LightType, p_checked);
}
function buildProtocolTypeSelectWidget(p_id, p_checked) {
	return buildSelectWidget(p_id, globals.Valid.ProtocolType, p_checked);
}
function buildLcarProtocolTypeSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.ProtocolType, p_checked);
}
function buildScheduleModeSelectWidget(p_id, p_checked) {
	return buildSelectWidget(p_id, globals.Valid.ScheduleMode, p_checked);
}
function buildLcarScheduleModeSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.ScheduleMode, p_checked);
}
function buildScheduleTypeSelectWidget(p_id, p_checked) {
	return buildSelectWidget(p_id, globals.Valid.ScheduleType, p_checked);
}
function buildLcarScheduleTypeSelectWidget(self, p_id, p_caption, p_checked) {
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.ScheduleType, p_checked);
}
/**
 * Build a valid select widget
 */
function buildValidSelectWidget(p_id, p_list, p_checked) {
	l_list = globals.Valid[p_list];
	var l_html = '';
	l_html += buildSelectWidget(p_id, l_list, p_checked);
	return l_html;
}



/**
 * Build a slider widget
 */
function buildSliderWidget(p_id, p_value) {
	var l_html = "<input type='range' min='0' max='100' id='" + p_id + "' name='slider' ";
	l_html += "value='" + p_value + "' ";
	l_html += ">\n";
	l_html += '&nbsp';  // add a box to display the slider value and find a way to update it when the slider is moved.
	l_html += "<input type='text' id='" + p_id;
	l_html += "' size='4' value='" + p_value;
	l_html += "' >\n";
	return l_html;
}
function buildLcarSliderWidget(self, p_id, p_caption, p_value) {
	var l_html = "";
	l_html += "<div class='lcars-row spaced'>\n";
	l_html += "<div class=lcars-column u-3-4'>\n";
	l_html += "<div class='lcars-button radius'>\n";
	l_html += p_caption;
	l_html += "<input class='lcars-button-addition' type='range' min='0' max='100' id='" + p_id + "' name='slider' ";
	l_html += "value='" + p_value + "' ";
	l_html += ">\n";
	l_html += '&nbsp';  // add a box to display the slider value and find a way to update it when the slider is moved.
	l_html += "<input type='text' id='" + p_id;
	l_html += "' size='4' value='" + p_value;
	l_html += "' >\n";
	l_html += "</div>\n";
	l_html += "</div>\n";
	l_html += "</div>\n";
	return l_html;
}
function buildLevelSliderWidget(p_name, p_level) {
	var l_html = buildSliderWidget(p_name, p_level);
	return l_html;
}
function buildLcarLevelSliderWidget(self, p_name, p_caption, p_level) {
	var l_html = buildLcarSliderWidget(self, p_name, p_caption, p_level);
	return l_html;
}
function fetchLevelWidget(p_id) {
	//Divmod.debug('---', 'globals.fetchLevelWidget() called.  Name=' + p_name);
	return document.getElementById(p_id).value;
}



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
	var l_html = '';
	var l_size = 40;
	var l_options = p_options;
	if (p_options === undefined)
		l_options = '';
	l_html += "<div class='lcars-row spaced'>\n";
	l_html += "<div class=lcars-column u-3-4'>\n";
	l_html += "<div class='lcars-button radius'>\n";
	l_html += p_caption;
	l_html += "<input type='text' class='lcars-button-addition' id='" + buildAthenaId(self, p_id);
	var l_ix = l_options.toLowerCase().indexOf('size=');
	if (l_ix > -1)
		l_size = l_options.substring(l_ix, l_ix+2);
	l_html += "' size='" + l_size + "' value='" + p_value;
	l_html += "' ";
	if (l_options.toLowerCase().indexOf('disable') > -1)
		l_html += "disabled='disabled' ";
	l_html += " />\n";
	l_html += "</div>\n";  // Button
	l_html += "</div>\n";  // Column
	l_html += "</div>\n";  // row 1
	// console.log("globals.buildLcarTextWidget() - %O", l_html)
	return l_html;
}
function fetchTextWidget(p_id) {
	var l_data = document.getElementById(p_id).value;
	return l_data;
}
function buildTextWidget(p_id, p_value, /* optional */ p_options) {
	var l_html = '';
	var l_options = p_options;
	if (p_options === undefined)
		l_options = '';
	l_html += "<input type='text' id='" + p_id;
	l_html += "' size='40' value='" + p_value;
	l_html += "' ";
	if (l_options.toLowerCase().indexOf('disable') > -1)
		l_html += "disabled='disabled' ";
	l_html += " />\n";
	return l_html;
}


/**
 * Build a DOW widget (mon = 0)
 */
function buildDowWidget(p_id, p_value, /* optional */ p_options) {
	var l_html = '';
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

	return l_html;
}
function fetchDowWidget(p_id) {
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


/**
 * Build an entire row to put in the table
 */
function buildTextRowWidget(p_id, p_name, p_value, /* optional */ hidden) {
	var l_html = '';
	l_html += "<tr><td>" + p_name;
	l_html += "</td><td><input type='text' id='" + p_name;
	l_html += "' value='" + p_value;
	l_html += "' /></td></tr>\n";
	return l_html;
}


/**
 * Build the top part of the display.
 *
 * @param: p_title(str) is the title to display near the center of the display
 */
function build_lcars_top(p_title, /* optional* */ p_color){
	// Divmod.debug('---', 'globals.build_lcars_top() was called.');
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
 * Bild the middle part of the display
 *
 * @param: p_rows is the number of rows to allow space for.
 * @param: p_html is the (big) html for the entire menu.
 */
function build_lcars_middle_menu(p_rows, p_html){
	// Divmod.debug('---', 'globals.build_lcars_middle() was called.');
	var l_html = '';
	var l_half = (p_rows + 1) / 2;
	l_html += "<div class='lcars-row spaced'>\n";  // row 1
	l_html += "  <div class='lcars-column u-1-8'>\n";  // Column 1
	l_html += "    <ul class='lcars-menu'>\n";
	for (var l_row = 0; l_row < l_half; l_row++) {
		l_html += "      <li class='lcars-blue-bg'></li>\n";
	}
	for (l_row = 0; l_row < l_half; l_row++) {
		l_html += "      <li class='lcars-tan-bg'></li>\n";
	}
	l_html += "    </ul>\n";
	l_html += "  </div>\n";  // column 1
	l_html += "  <div class='lcars-column u-6-8'>\n";
	l_html += p_html;

	l_html += "  </div>\n";
	l_html += "  <div class='lcars-column u-1-8'>\n";
	l_html += "    <ul class='lcars-menu'>\n";  // RIGHT
	for (l_row = 0; l_row < l_half; l_row++) {
		l_html += "      <li class='lcars-tan-bg'></li>\n";
	}
	for (l_row = 0; l_row < l_half; l_row++) {
		l_html += "      <li class='lcars-blue-bg'></li>\n";
	}
	l_html += "    </ul>\n";
	l_html += "  </div>\n";
	l_html += "</div>\n";
	// console.log("globals.build_lcars_middle() - %O", l_html)
	return l_html;
}
/**
 * Build the top part of the display.
 */
function build_lcars_bottom(){
	// Divmod.debug('---', 'globals.build_lcars_bottom() was called.');
	var l_html = '';
	l_html += "<div class='lcars-row spaced'>\n";
	l_html += "  <div class='lcars-column u-1-8 lcars-elbow left top lcars-tan-bg'></div>";
	l_html += "  <div class='lcars-column u-6-8 lcars-divider bottom lcars-tan-blue-divide'></div>";
	l_html += "  <div class='lcars-column u-1-8 lcars-elbow right top lcars-blue-bg'></div>\n";
	l_html += "</div>\n";
	return l_html;
}



/**
 * Startup
 */
Divmod.Runtime.theRuntime.addLoadEvent(
	function appStartup() {
		globals.workspace.appStartup();
	}
);
// Divmod.debug('---', 'globals.buildLcarTextWidget() was called.');
// console.log("globals.build_lcars_middle() - %O", l_html)
// END DBK