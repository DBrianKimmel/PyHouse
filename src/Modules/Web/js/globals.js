/**
 * globals.js - the global hook where we hang our coat and everything else
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
var BUTTON_ADD      = '#ffd0d0';
var BUTTON_BACK     = '#ffd0d0';
var BUTTON_CHANGE   = '#ffd0d0';
var BUTTON_DELETE   = '#ffd0d0';

globals = {
	fonts : [ 'Verdana', 'Arial', 'Helvetica', 'sans-serif' ],
	workspace : null,

	Computer : {},
	House : {},
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
	}  // __init__
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
}  // getCardSizefromCSS


function collectClasses(node) {
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
	var imgs = [];
	for ( var i = 0; i < uris.length; i++) {
		var img = new Image();
		img.src = uris[i];
		imgs.push(img);
	}  // for loop

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
	var readyDeferred = Divmod.Defer.Deferred();

	var checkStep = function() {
		if ((stepcount > 120)) {
			self.timer = null;
			// readyDeferred.errback(new minimal.common.globals.ImageLoadingError(
			readyDeferred.errback(new globals.ImageLoadingError(
					'could not load all images: ' + imgsNotloaded()));
		} else if (imgsloaded()) {
			readyDeferred.callback();
		} else {
			stepcount++;
			self.timer = setTimeout(checkStep, 1000 / steprate);
		}
	};  // checkStep

	self.timer = setTimeout(checkStep, 1000 / steprate);
	return readyDeferred;
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
	//Divmod.debug('---', 'globals.serverState was called. state:' + p_state);
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
	//Divmod.debug('---', 'globals.findWidgetByClass(1) - Name:' + p_name);
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
	//Divmod.debug('---', 'globals.getPyHouseData() was called. ');
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


/**
 * A series of routines to build HTML for insertion into widgets.
 */
function buildButton(p_obj, p_handler, p_background_color, /* optional */ nameFunction) {
	var l_html = '<td>';
	l_html += "<button type='button' ";
	l_html += "value='" + p_obj['Name'] + "' ";
	l_html += "name ='" + p_obj['Key'] + "' ";
	l_html += "style = 'background-color: " + p_background_color + "' ";
	l_html += "onclick = 'return Nevow.Athena.Widget.handleEvent(this, \"onclick\", \""  + p_handler + "\" ";
	l_html += ");' >\n";
	if (typeof nameFunction === 'function')
		l_html += nameFunction(p_obj);
	else
		l_html += p_obj['Name'];
	l_html += "</button></td>\n";
	return l_html;
}
function buildAddButton(p_handler) {
	return buildButton({'Name' : 'Add', 'Key' : 10001}, p_handler, BUTTON_ADD);
}
function buildBackButton(p_handler) {
	return buildButton({'Name' : 'Back', 'Key' : 10002}, p_handler, BUTTON_BACK);
}
function buildChangeButton(p_handler) {
	return buildButton({'Name' : 'Change', 'Key' : 10003}, p_handler, BUTTON_CHANGE);
}
function buildDeleteButton(p_handler) {
	return buildButton({'Name' : 'Delete', 'Key' : 10004}, p_handler, BUTTON_DELETE);
}

/**
 * Build a table of buttons in the current widget space.
 * Use the names to build callbacks for the buttons being clicked on
 * Used for things like selecting a light or house to work on.
 * 
 * @param p_obj = a dict of item dicts to build from
 * @param p_handler = is a literal name of a handler function { 'handleMenuOnClick' )
 * @param nameFunction (optional) is the name of a function used to build a more complex caption for the buttons.
 * 			Omit this parameter if it is not used - no need for a placeholder
 * @param noOptions (optional) is the things to skip ('NoAdd' will omit the add button).
 * @returns = innerHTML of a table filled in with buttons
 */
function buildTable(p_obj, p_handler, /* optional */ nameFunction, noOptions) {
	//Divmod.debug('---', 'globals.buildTable(1) called. ' + p_obj + ' ' + p_handler + ' ' + nameFunction + ' ' + noOptions);
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

	//Divmod.debug('---', 'globals.buildTable(2) called. Building a table of ' + Object.keys(p_obj).length);
	var l_html = "<table><tr>\n";

	for (var l_item in p_obj) {
		//Divmod.debug('---', 'globals.buildTable(3) called. ' + l_item + ' ' + p_obj);
		var l_background = BUTTON_ACTIVE;
		if (p_obj[l_item]['Active'] != true)
			l_background = BUTTON_INACTIVE;
		l_html += buildButton(p_obj[l_item], p_handler, l_background, l_function);
		l_count++;
		if ((l_count > 0) & (l_count % l_cols == 0))
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
function buildTrueFalseWidget(p_name, p_value) {
	var l_html = "<span id='" + p_name + "Buttons'>";
	var l_value = p_value != false;  // force to be a bool
	l_html += buildRadioButtonWidget(p_name, 'True',  true, l_value);
	l_html += buildRadioButtonWidget(p_name, 'False', false, l_value);
	l_html += '</span>\n';
	return l_html;
}
function fetchTrueFalseWidget(p_name) {
	var l_active = document.getElementsByName(p_name);
	var l_ret = false;
	//Divmod.debug('---', 'globals.fetchTrueFalse() called.  Name=' + p_name + '  Len:' + l_active.length);
	for (var ix = 0; ix < l_active.length; ix++) {
		//Divmod.debug('---', 'globals.fetchTrueFalse() called.  Name=' + p_name + '  Checked:' + l_active[ix].checked + '  Val:' + l_active[ix].value);
		if (l_active[ix].checked && l_active[ix].value === 'true') {
			l_ret = true
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
function fetchSelectWidget(p_id) {
	var l_field = document.getElementById(p_id);
	var l_ix = l_field.value;
	var l_name = l_field.options[l_field.selectedIndex].text;
	//Divmod.debug('---', 'globals.fetchSelectWidget(1) was called. Id=' + p_id);
	//console.log("    %O", l_field);
	return l_name;
}
function buildRoomSelectWidget(p_id, p_checked) {
	//Divmod.debug('---', 'globals.buildRoomSelectWidget() was called. Id=' + p_id + '  Checked=' + p_checked);
	var l_obj = globals.House.HouseObj.Rooms;
	var l_list = [];
	for (var ix = 0; ix < Object.keys(l_obj).length; ix++)
		l_list[ix] = l_obj[ix].Name;
	return buildSelectWidget(p_id, l_list, p_checked);
}
function buildLightSelectWidget(p_id, p_checked) {
	//Divmod.debug('---', 'globals.buildLightSelectWidget() was called. Id=' + p_id + '  Checked=' + p_checked);
	var l_obj = globals.House.HouseObj.Lights;
	var l_list = [];
	for (var ix = 0; ix < Object.keys(l_obj).length; ix++)
		l_list[ix] = l_obj[ix].Name;
	return buildSelectWidget(p_id, l_list, p_checked);
}
function buildFamilySelectWidget(p_id, p_checked) {
	//Divmod.debug('---', 'globals.buildFamilySelectWidget() was called. Id=' + p_id + '  Checked=' + p_checked);
	return buildSelectWidget(p_id, globals.Valid.Families, p_checked);
}
function buildInterfaceSelectWidget(p_id, p_checked) {
	return buildSelectWidget(p_id, globals.Valid.Interfaces, p_checked);
}
/**
 * Build a valid select widget
 */
function buildValidSelectWidget(p_id, p_list, p_checked) {
	l_list = globals.Valid[p_list];
	//Divmod.debug('---', 'globals.buildValidSelectWidget() was called. Id=' + p_id + '  Checked=' + p_checked + '  List=' + l_list);
	var l_html = '';
	l_html += buildSelectWidget(p_id, l_list, p_checked)
	return l_html;
}

/**
 * Build a slider widget
 */
function buildSliderWidget(p_id, p_value) {
	//Divmod.debug('---', 'globals.buildSliderWidget() called.  Value=' + p_value);
	var l_html = "<input type='range' min='0' max='100' id='" + p_id + "' name='slider' ";
	l_html += "value='" + p_value + "' ";
	l_html += ">\n";
	return l_html;
}
function buildLevelSliderWidget(p_name, p_level) {
	//.debug('---', 'globals.buildLevelSliderWidget() called.  Level=' + p_level);
	var l_html = buildSliderWidget(p_name, p_level);
	return l_html;
}
function fetchLevelWidget(p_id) {
	//Divmod.debug('---', 'globals.fetchLevelWidget() called.  Name=' + p_name);
	return document.getElementById(p_id).value;
}

/**
 * Build a text widget
 */
function buildTextWidget(p_id, p_value, /* optional */ p_options) {
	var l_html = '';
	var l_options = p_options;
	if (p_options === undefined)
		l_options = '';
	l_html += "<input type='text' id='" + p_id + "' size='40' value='" + p_value + "' ";
	if (l_options.toLowerCase().indexOf('disable') > -1)
		l_html += "disabled='disabled' ";
	l_html += " >\n"
	return l_html;
}
function fetchTextWidget(p_id) {
	var l_data = document.getElementById(p_id).value;
	return l_data;
}

/**
 * Build an entire row to put in the table
 */
function buildTextRowWidget(p_id, p_name, p_value, /* optional */ hidden) {
	//Divmod.debug('---', 'globals.buildTextRowWidget() was called.  Name' + p_name + '  Value=' + p_value);
	var l_html = '';
	l_html += "<tr><td>" + p_name + "</td><td><input type='text' id='" + p_name + "' value='" + p_value + "' /></td></tr>\n";
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
// END DBK