/**
 * @name: PyHouse/src/Modules/Web/js/internet.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2012-2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created about 2012
 * @summary: Displays the Internet element
 *
 */
// import Nevow.Athena
// import globals
// import helpers



helpers.Widget.subclass(internet, 'InternetWidget').methods(

    function __init__(self, node) {
        internet.InternetWidget.upcall(self, "__init__", node);
		// Divmod.debug('---', 'internet.__init__() was called.');
    },

	// ============================================================================
	/**
     * Place the widget in the workspace.
	 * 
	 * @param self is    <"Instance" of undefined.internet.InternetWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		function cb_widgetready(res) {
			// Divmod.debug('---', 'internet.cb_widgready was called.');
			self.hideWidget();
		}
		// Divmod.debug('---', 'internet.ready() was called.');
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	/**
	 * routines for showing and hiding parts of the screen.
	 */
	function startWidget(self) {
		// Divmod.debug('---', 'internet.showWidget() was called.');
		self.node.style.display = 'block';
		self.showSelectionButtons();
		self.hideDataEntry();
		self.fetchHouseData();
	},
	function hideSelectionButtons(self) {
		self.nodeById('InternetButtonsDiv').style.display = 'none';
	},
	function showSelectionButtons(self) {
		self.nodeById('InternetButtonsDiv').style.display = 'block';
	},
	function hideDataEntry(self) {
		self.nodeById('InternetEntryDiv').style.display = 'none';
	},
	function showDataEntry(self) {
		self.nodeById('InternetEntryDiv').style.display = 'block';
	},

	// ============================================================================
	/**
	 * This triggers getting the Internet data from the server.
	 * The server calls displayInternetButtons with the Internet info.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			globals.Computer = JSON.parse(p_json);
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'internet.eb_fetchHouseData() was called. ERROR: ' + res);
		}
        var l_defer = self.callRemote("getHouseData");  // call server @ web_internet.py
		l_defer.addCallback(cb_fetchHouseData);
		l_defer.addErrback(eb_fetchHouseData);
        return false;
	},

	/**
	 * Fill in the dynamic dns part of the compound entry screen with all of the data for this schedule.
	 * 
	 */
	function fillEntry(self, p_obj, p_ix) {
		// Divmod.debug('---', 'internet.fillEntry(1) was called.  Ix:' + p_ix);
		// console.log("internet.fillEntry() - Obj = %O", p_obj);
	},

	function fetchEntry(self) {
		// Divmod.debug('---', 'internet.fetchEntry() was called. ');
        var l_data = {
        	// ExternalDelay : fetchTextWidget(self, 'InternetExtDelay')
            // Interval : fetchTextWidget(self, 'DynDnsInterval')
 			Delete : false
            };
		return l_data;
	},

	function createEntry(self) {
		// Divmod.debug('---', 'internet.createEntry() was called.');
        var l_Data = {
    			Name : 'Change Me',
    			Key : Object.keys(globals.House.HouseObj.Internet).length,
    			Active : false,
    			Url : '',
    			Interval : 0,
    			Delete : false
                };
		return l_Data;
	},

	// ============================================================================
	/**
	 * Event handler for internet selection buttons.
	 * 
	 * The user can click on a internet button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.internet.InternetWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.InternetIx = l_ix;
		globals.House.InternetName = l_name;
		if (l_ix <= 1000) {
			// One of the Internet buttons.
			var l_obj = globals.House.HouseObj.Internet;
			// Divmod.debug('---', 'internet.handleMenuOnClick("Internet" Button) was called. ' + l_ix + ' ' + l_name);
			// console.log("internet.handleMenuOnClick() - l_obj = %O", l_obj);
			self.showDataEntry();
			//self.hideSelectionButtons();
			self.fillEntry(l_obj, l_ix);
		} else if (l_ix == 10001) {
			// The "Add" button
			// Divmod.debug('---', 'internet.handleMenuOnClick(Add Button) was called. ' + l_ix + ' ' + l_name);
			self.showDataEntry();
			self.hideSelectionButtons();
			var l_ent = self.createEntry(globals.House.InternetIx);
			self.fillEntry(l_ent);
		} else if (l_ix == 10002) {
			// The "Back" button
			// Divmod.debug('---', 'internet.handleMenuOnClick(Back Button) was called. ' + l_ix + ' ' + l_name);
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget2('HouseMenu');
		}
	},

	// ============================================================================
	/**
	 * Event handler for buttons at bottom of the data entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataOnClick(self, p_node) {
		function cb_handleDataOnClick(p_json) {
			// Divmod.debug('---', 'internet.cb_handleDataOnClick() was called.');
			self.showWidget();
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'internet.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		var l_defer;
		var l_json;
		// Divmod.debug('---', 'internet.handleDataOnClick() was called. Node:' + l_ix);
		switch(l_ix) {
		case '10003':  // Change Button
	    	l_json = JSON.stringify(self.fetchEntry());
	        l_defer = self.callRemote("saveInternetData", l_json);  // @ web_internet
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			self.hideDataEntry();
			self.showSelectionButtons();
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry();
			l_obj.Delete = true;
	    	l_json = JSON.stringify(l_obj);
	        l_defer = self.callRemote("saveInternetData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		default:
			break;
		}
        return false;  // false stops the chain.
	}
);
//### END DBK
