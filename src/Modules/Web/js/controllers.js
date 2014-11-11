/**
 *
 * @name: PyHouse/src/Modules/Web/js/controllers.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Mar 11, 2014
 * @summary: Displays the controller element
 * Displays the controllers.
 * Browser side code.
 * 
 * Note that a controller contains common light info, controller info, family info and interface info.
 */
// import Nevow.Athena
// import globals
// import helpers



/**
 * The controller widget.
 */
helpers.Widget.subclass(controllers, 'ControllersWidget').methods(

    function __init__(self, node) {
        controllers.ControllersWidget.upcall(self, '__init__', node);
    },

// ============================================================================
    /**
     * Place the widget in the workspace.
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
    function showWidget(self) {
        self.node.style.display = 'block';
        self.showSelectionButtons(self);
        self.hideDataEntry(self);
        self.fetchHouseData();
    },
    function hideSelectionButtons(self) {
        self.nodeById('SelectionButtonsDiv').style.display = 'none';
    },
    function showSelectionButtons(self) {
        self.nodeById('SelectionButtonsDiv').style.display = 'block';
    },
    function hideDataEntry(self) {
        self.nodeById('DataEntryDiv').style.display = 'none';
    },
    function showDataEntry(self) {
        self.nodeById('DataEntryDiv').style.display = 'block';
    },

    // ============================================================================
    /**
     * Get interface info from the server.  This data can never change during a server run.
     */
    function fetchInterfaceData(self) {
    	function cb_fetchInterfaceData(p_json) {
    		globals.Interface.Obj = JSON.parse(p_json);
            //Divmod.debug('---', 'controllers.cb_fetchInterfaceData() was called.  JSON = ' + p_json);
    	}
    	Divmod.debug('---', 'controllers.fetchInterfaceData() was called. ');
        var l_defer = self.callRemote("getInterfaceData");  // call server @ web_controllers.py
        l_defer.addCallback(cb_fetchInterfaceData);
		return false;
    },

    // ============================================================================
	/**
	 * Build a screen full of buttons - One for each room and some actions.
	 */
	function buildLcarSelectScreen(self){
    	Divmod.debug('---', 'controllers.buildLcarSelectScreen() was called. ');
		var l_button_html = buildLcarSelectionButtonsTable(globals.House.HouseObj.Controllers, 'handleMenuOnClick');
		var l_html = build_lcars_top('Controllers', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, l_button_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
    /**
     * This triggers getting the data from the server.
     */
    function fetchHouseData(self) {
        function cb_fetchHouseData(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			self.buildLcarSelectScreen();
        }
        function eb_fetchHouseData(p_reason) {
            Divmod.debug('---', 'ERROR controllers.eb_fetchHouseData() - ' + p_reason);
        }
        var l_defer = self.callRemote("getHouseData");  // call server @ web_controllers.py
        l_defer.addCallback(cb_fetchHouseData);
        l_defer.addErrback(eb_fetchHouseData);
        return false;
    },


// ============================================================================
    /**
     * Event handler for controller selection buttons.
     */
    function handleMenuOnClick(self, p_node) {
        var l_ix = p_node.name;
        var l_name = p_node.value;
		globals.House.ControllerIx = l_ix;
		globals.House.ControllerName = l_name;
        if (l_ix <= 1000) {  // One of the controller buttons
            self.hideSelectionButtons();
            self.showDataEntry();
			var l_obj = globals.House.HouseObj.Controllers[l_ix];
            self.fillEntry(l_obj);
        } else if (l_ix == 10001) {  // The 'Add' button
            self.hideSelectionButtons();
            self.showDataEntry();
			var l_ent = self.createEntry();
			self.fillEntry(l_ent);
        } else if (l_ix == 10002) {  // The 'Back' button
            self.hideWidget();
            var l_node = findWidgetByClass('HouseMenu');
            l_node.showWidget();
        }
    },



// ============================================================================
	/**
	 * Build a screen full of data entry fields.
	 */
	function buildBasicPart(self, p_controller, p_html, p_onchange) {
		p_html += buildLcarTextWidget(self, 'Name', 'Light Name', p_controller.Name);
		p_html += buildLcarTextWidget(self, 'Key', 'Light Index', p_controller.Key, 'size=10');
		p_html += buildLcarTrueFalseWidget(self, 'ControllerActive', 'Active ?', p_controller.Active);
		p_html += buildLcarTextWidget(self, 'UUID', 'UUID', p_controller.UUID, 'disabled');
		p_html += buildLcarTextWidget(self, 'Comment', 'Comment', p_controller.Comment);
		p_html += buildLcarTextWidget(self, 'Coords', 'Coords', p_controller.Coords);
		p_html += buildLcarTrueFalseWidget(self, 'ControllerDimmable', 'Light Dimmable ?', p_controller.IsDimmable);
		p_html += buildLcarFamilySelectWidget(self, 'ControllerFamily', 'Family', p_controller.ControllerFamily, p_onchange);
		p_html += buildLcarRoomSelectWidget(self, 'RoomName', 'Room', p_controller.RoomName);
		p_html += buildLcarLightTypeSelectWidget(self, 'ControllerType', 'Type', p_controller.LightingType);
		return p_html;
	},
	function buildInsteonPart(self, p_controller, p_html) {
		p_html += buildLcarTextWidget(self, 'LightAddressI', 'Insteon Address', p_controller.InsteonAddress);
		p_html += buildLcarTextWidget(self, 'LightDevCat', 'Dev Cat', p_controller.DevCat);
		p_html += buildLcarTextWidget(self, 'LightGroupNumber', 'Group Number', p_controller.GroupNumber);
		p_html += buildLcarTextWidget(self, 'LightGroupList', 'Group List', p_controller.GroupList);
		p_html += buildLcarTrueFalseWidget(self, 'LightMaster', 'Light Master ?', p_controller.IsMaster);
		p_html += buildLcarTrueFalseWidget(self, 'LightController', 'Light Controller ?', p_controller.IsController);
		p_html += buildLcarTrueFalseWidget(self, 'LightResponder', 'Light Responder ?', p_controller.IsResponder);
		p_html += buildLcarTextWidget(self, 'LightProductKey', 'Product Key', p_controller.ProductKey);
		return p_html;
	},
	function buildUpbPart(self, p_controller, p_html) {
		p_html += buildLcarTextWidget(self, 'LightAddressU', 'UPB Address', p_controller.UPBAddress);
		p_html += buildLcarTextWidget(self, 'LightPassword', 'UPB Password', p_controller.UPBPassword);
		p_html += buildLcarTextWidget(self, 'LightNetworkID', 'UPB Network', p_controller.UPBNetworkID);
		return p_html;
	},
	function buildAllParts(self, p_controller, p_html, p_handler, p_onchange) {
		p_html = self.buildBasicPart(p_controller, p_html, p_onchange) ;
		if (p_controller.ControllerFamily == 'Insteon') {
			p_html = self.buildInsteonPart(p_controller, p_html);
		}
        if (p_controller.ControllerFamily == 'UPB') {
        	p_html = self.buildUpbPart(p_controller, p_html);
        }
		p_html += buildLcarEntryButtons(p_handler);
		return p_html;
	},
	function buildLcarDataEntryScreen(self, p_entry, p_handler){
		Divmod.debug('---', 'controllers.buildLcarDataEntryScreen() was called.');
		// console.log("controllers.buildLcarDataEntryScreen() - self = %O", self);
		var l_light = arguments[1];
		var l_html = self.buildAllParts(l_light, l_html, p_handler, 'familyChanged');
		var l_html_2 = "";
		l_html_2 += build_lcars_top('Enter Light Data', 'lcars-salmon-color');
		l_html_2 += build_lcars_middle_menu(26, l_html);
		l_html_2 += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html_2;
	},
	function familyChanged() {
		var l_obj = globals.House.LightObj;
		var l_self = globals.House.Self;
		Divmod.debug('---', 'controllers.familyChanged was called !!!');
		var l_family = fetchSelectWidget(l_self, 'ControllerFamily');
		l_obj.ControllerFamily = l_family;
		l_self.fillEntry(l_obj);
	},
    function fillEntry(self, p_obj) {
		self.buildLcarDataEntryScreen(p_obj, 'handleDataOnClick');
    },
    function fetchEntry(self) {
        var l_data = {
            Name :           fetchTextWidget(self, 'Name'),
            Key :            fetchTextWidget(self, 'Key'),
			Active :         fetchTrueFalseWidget(self, 'ControllerActive'),
			Comment :        fetchTextWidget(self, 'Comment'),
			Coords :         fetchTextWidget(self, 'Coords'),
			IsDimmable :     fetchTrueFalseWidget(self, 'ControllerDimmable'),
			ControllerFamily : fetchTextWidget(self, 'ControllerFamily'),
			RoomName :       fetchSelectWidget(self, 'RoomName'),
			LightingType :   fetchTextWidget(self, 'ControllerType'),
			UUID :           fetchTextWidget(self, 'UUID'),
			InterfaceType :      fetchSelectWidget(self, 'InterfaceType'),
			Port :           fetchTextWidget(self, 'ControllerPort'),
			Delete : false
            };
        if (l_data.ControllerFamily == 'Insteon') {
        	l_data = self.fetchInsteonEntry(l_data);
        }
        return l_data;
    },
	function fetchInsteonEntry(self, p_data) {
		// Divmod.debug('---', 'lights.fetchInsteonEntry() was called.');
        p_data.InsteonAddress = fetchTextWidget(self, 'LightAddressI');
        p_data.DevCat = fetchTextWidget(self, 'LightDevCat');
        p_data.GroupNumber = fetchTextWidget(self, 'LightGroupNumber');
        p_data.GroupList = fetchTextWidget(self, 'LightGroupList');
        p_data.IsMaster = fetchTrueFalseWidget(self, 'LightMaster');
        p_data.IsResponder = fetchTrueFalseWidget(self, 'LightResponder');
        p_data.IsController = fetchTrueFalseWidget(self, 'LightController');
        p_data.ProductKey = fetchTextWidget(self, 'LightProductKey');
		// Divmod.debug('---', 'lights.fetchInsteonEntry() finished.');
      	// console.log("lights.fetchInsteonEntry()  p_data  %O", p_data)
		return p_data;
	},
	function fetchUpbEntry(self, p_data) {
		Divmod.debug('---', 'lights.fetchUpbEntry() was called.');
        p_data.UPBAddress = fetchTextWidget(self, 'LightAddressU');
        p_data.UPBPassword = fetchTextWidget(self, 'LightPassword');
        p_data.UPBNetworkID = fetchTextWidget(self, 'LightNetworkID');
		return p_data;
	},
    function createEntry(self) {
        var l_data = {
            Name : 'Change Me',
            Key : Object.keys(globals.House.HouseObj.Controllers).length,
            Active : false,
			Comment : '',
			Coords : '',
			IsDimmable : false,
			ControllerFamily : '',
			RoomName : '',
            LightingType : 'Controller',
			UUID : '',
			Delete : false
            };
        return l_data;
    },

    // ============================================================================
    /**
     * Event handler for submit buttons at bottom of entry portion of this widget.
     * Get the possibly changed data and send it to the server.
     */
    function handleDataOnClick(self, p_node) {
        function cb_handleDataOnClick(p_json) {
            //Divmod.debug('---', 'controller.cb_handleDataOnClick() was called.');
            self.showWidget();
        }
        function eb_handleDataOnClick(res){
            Divmod.debug('---', 'login.eb_handleDataOnClick() was called.  ERROR = ' + res);
        }
		var l_ix = p_node.name;
		var l_obj = self.fetchEntry();
		var l_json = '';
		var l_defer = '';
		switch(l_ix) {
		case '10003':  // The 'Change' Button
			l_json = JSON.stringify(l_obj);
	        //Divmod.debug('---', 'controllers.handleDataOnClick(1) was called. json:' + l_json);
	        l_defer = self.callRemote("saveControllerData", l_json);  // @ web_controller
	        l_defer.addCallback(cb_handleDataOnClick);
	        l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // The 'Back' button
			//Divmod.debug('---', 'controllers.handleDataOnClick(Back) was called.  ');
			self.hideDataEntry();
			self.showSelectionButtons();
			break;
		case '10004':  // The 'Delete' button
			l_obj.Delete = true;
	    	l_json = JSON.stringify(l_obj);
			//Divmod.debug('---', 'controllers.handleDataOnClick(Delete) was called. JSON:' + l_json);
	        l_defer = self.callRemote("saveControllerData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		default:
			Divmod.debug('---', 'controllers.handleDataOnClick(Default) was called. l_ix:' + l_ix);
			break;			
		}
        return false;  // false stops the chain.
    }
);
//Divmod.debug('---', 'controllers.handleMenuOnClick(1) was called. ' + l_ix + ' ' + l_name);
//console.log("controllers.handleMenuOnClick() - l_obj = %O", l_obj);
//### END DBK
