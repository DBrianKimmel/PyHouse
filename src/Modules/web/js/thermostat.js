/**
 * thermostat.js
 * 
 * The Thermostat widget.
 */

// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(thermostat, 'ThermostatWidget').methods(

    function __init__(self, node) {
        thermostat.ThermostatWidget.upcall(self, "__init__", node);
    },

	/**
     * Place the widget in the workspace.
	 * 
	 * @param self is    <"Instance" of undefined.thermostat.ThermostatWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		function cb_widgetready(res) {
			self.hideWidget();
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	/**
	 * routines for showing and hiding parts of the screen.
	 */
	function showWidget(self) {
		self.node.style.display = 'block';
		self.showButtons();
		self.hideEntry();
		self.fetchHouseData();
	},
	function hideButtons(self) {
		self.nodeById('ThermostatButtonsDiv').style.display = 'none';
	},
	function showButtons(self) {
		self.nodeById('ThermostatButtonsDiv').style.display = 'block';
	},
	function hideEntry(self) {
		self.nodeById('ThermostatEntryDiv').style.display = 'none';
	},
	function showEntry(self) {
		self.nodeById('ThermostatEntryDiv').style.display = 'block';
	},

	// ============================================================================
	/**
	 * This triggers getting the Thermostat data from the server.
	 * The server calls displayThermostatButtons with the Thermostat info.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			//Divmod.debug('---', 'thermostat.cb_fetchHouseData() was called. ' + p_json);
			//globals.Computer = JSON.parse(p_json);
			// this is the external IP address finding URL and its value
	        self.nodeById('UrlDiv').innerHTML = buildTextWidget('ThermostatUrl', globals.Computer.ThermostatConnection.ExternalUrl);
	        self.nodeById('ExtDelayDiv').innerHTML = buildTextWidget('ThermostatExtDelay', globals.Computer.ThermostatConnection.ExternalDelay);
	        self.nodeById('ExtIpDiv').innerHTML = buildTextWidget('ThermostatExtIp', globals.Computer.ThermostatConnection.ExternalIP, 'disabled');
			var l_tab = buildTable(globals.Computer.ThermostatConnection.DynDns, 'handleMenuOnClick');
			self.nodeById('ThermostatTableDiv').innerHTML = l_tab;

		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'thermostat.eb_fetchHouseData() was called. ERROR: ' + res);
		}
		//Divmod.debug('---', 'thermostat.fetchHouseData() was called. ');
        var l_defer = self.callRemote("getHouseData", 0);  // call server @ web_thermostat.py
		l_defer.addCallback(cb_fetchHouseData);
		l_defer.addErrback(eb_fetchHouseData);
        return false;
	},

	/**
	 * Fill in the dynamic dns part of the compound entry screen with all of the data for this schedule.
	 * 
	 */
	function fillEntry(self, p_obj, p_ix) {
		Divmod.debug('---', 'thermostat.fillEntry(1) was called.  Ix:' + p_ix);
		//console.log("thermostat.fillEntry() - Obj = %O", p_obj);
        self.nodeById('DynDnsNameDiv').innerHTML = buildTextWidget('DynDnsName', p_obj.DynDns[p_ix].Name);
        self.nodeById('DynDnsKeyDiv').innerHTML = buildTextWidget('DynDnsKey', p_obj.DynDns[p_ix].Key, 'disabled');
        self.nodeById('DynDnsActiveDiv').innerHTML = buildTrueFalseWidget('DynDnsActive', p_obj.DynDns[p_ix].Active);
        self.nodeById('DynDnsUrlDiv').innerHTML = buildTextWidget('DynDnsUrl', p_obj.DynDns[p_ix].Url);
        self.nodeById('DynDnsIntervalDiv').innerHTML = buildTextWidget('DynDnsInterval', p_obj.DynDns[p_ix].Interval);
		self.nodeById('ThermostatEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick');
	},
	function fetchEntry(self) {
		Divmod.debug('---', 'thermostat.fetchEntry() was called. ');
        var l_data = {
        	ExternalDelay : fetchTextWidget('ThermostatExtDelay'),
        	ExternalUrl : fetchTextWidget('ThermostatUrl'),
            Name : fetchTextWidget('DynDnsName'),
            Key : fetchTextWidget('DynDnsKey'),
			Active : fetchTrueFalseWidget('DynDnsActive'),
            Url : fetchTextWidget('DynDnsUrl'),
            Interval : fetchTextWidget('DynDnsInterval'),
			Delete : false
            }
		return l_data;
	},
	function createEntry(self, p_ix) {
		Divmod.debug('---', 'thermostat.createEntry() was called.  Ix: ' + p_ix);
        var l_Data = {
    			Name : 'Change Me',
    			Key : Object.keys(globals.House.HouseObj.Thermostat).length,
    			Active : false,
    			Url : '',
    			Interval : 0,
    			Delete : false
                }
		return l_Data;
	},

	// ============================================================================
	/**
	 * Event handler for thermostat selection buttons.
	 * 
	 * The user can click on a thermostat button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.thermostat.ThermostatWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.ThermostatIx = l_ix;
		globals.House.ThermostatName = l_name;
		if (l_ix <= 1000) {
			// One of the Thermostat buttons.
			var l_obj = globals.House.HouseObj.Thermostat;
			Divmod.debug('---', 'thermostat.handleMenuOnClick("Thermostat" Button) was called. ' + l_ix + ' ' + l_name);
			//console.log("thermostat.handleMenuOnClick() - l_obj = %O", l_obj);
			self.showEntry();
			//self.hideButtons();
			self.fillEntry(l_obj, l_ix);
		} else if (l_ix == 10001) {
			// The "Add" button
			Divmod.debug('---', 'thermostat.handleMenuOnClick(Add Button) was called. ' + l_ix + ' ' + l_name);
			self.showEntry();
			self.hideButtons();
			var l_ent = self.createEntry(globals.House.ThermostatIx);
			self.fillEntry(l_ent);
		} else if (l_ix == 10002) {
			// The "Back" button
			Divmod.debug('---', 'thermostat.handleMenuOnClick(Back Button) was called. ' + l_ix + ' ' + l_name);
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		}
	},

	// ============================================================================
	/**
	 * Event handler for buttons at bottom of the data entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataOnClick(self, p_node) {
		function cb_handleDataOnClick(p_json) {
			//Divmod.debug('---', 'thermostat.cb_handleDataOnClick() was called.');
			self.showWidget();
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'thermostat.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		//Divmod.debug('---', 'thermostat.handleDataOnClick() was called. Node:' + l_ix);
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
	        var l_defer = self.callRemote("saveThermostatData", l_json);  // @ web_thermostat
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			self.hideEntry();
			self.showButtons();
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry();
			l_obj['Delete'] = true;
	    	var l_json = JSON.stringify(l_obj);
	        var l_defer = self.callRemote("saveThermostatData", l_json);  // @ web_rooms
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
