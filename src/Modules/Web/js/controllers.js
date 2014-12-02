/**
 * @name: PyHouse/src/Modules/Web/js/controllers.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Mar 11, 2014
 * @summary: Displays the controller element
 *
 * Note that a controller contains common light info, controller info, family info and interface info.
 */


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
    function startWidget(self) {
        self.showSelectionButtons(self);
        self.hideDataEntry(self);
        self.fetchDataFromServer();
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
    	function eb_fetchInterfaceData(p_reason) {
            Divmod.debug('---', 'ERROR - controllers.cb_fetchInterfaceData() - ' + p_reason);
    	}
    	Divmod.debug('---', 'controllers.fetchInterfaceData() was called. ');
        var l_defer = self.callRemote("getInterfaceData");  // call server @ web_controllers.py
        l_defer.addCallback(cb_fetchInterfaceData);
        l_defer.addeRRback(eb_fetchInterfaceData);
		return false;
    },



// ============================================================================
	/**
	 * Build a screen full of buttons - One for each room and some actions.
	 */
	function buildLcarSelectScreen(self){
		var l_button_html = buildLcarSelectionButtonsTable(globals.House.HouseObj.Controllers, 'handleMenuOnClick');
		var l_html = build_lcars_top('Controllers', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, l_button_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
    /**
     * This triggers getting the data from the server.
     */
    function fetchDataFromServer(self) {
        function cb_fetchDataFromServer(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			self.buildLcarSelectScreen();
        }
        function eb_fetchDataFromServer(p_reason) {
            Divmod.debug('---', 'ERROR controllers.eb_fetchDataFromServer() - ' + p_reason);
        }
        var l_defer = self.callRemote("getHouseData");  // call server @ web_controllers.py
        l_defer.addCallback(cb_fetchDataFromServer);
        l_defer.addErrback(eb_fetchDataFromServer);
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
            self.buildLcarDataEntryScreen(l_obj, 'handleDataOnClick');
        } else if (l_ix == 10001) {  // The 'Add' button
            self.hideSelectionButtons();
            self.showDataEntry();
			var l_ent = self.createEntry();
			self.buildLcarDataEntryScreen(l_ent, 'handleDataOnClick');
        } else if (l_ix == 10002) {  // The 'Back' button
            self.showWidget2('HouseMenu');
        }
    },



// ============================================================================
	/**
	 * Build a screen full of data entry fields.
	 */
	function buildBasicPart(self, p_controller, p_html, p_onchange) {
		p_html += buildLcarTextWidget(self, 'Name', 'Light Name', p_controller.Name);
		p_html += buildLcarTextWidget(self, 'Key', 'Light Index', p_controller.Key, 'size=10');
		p_html += buildLcarTrueFalseWidget(self, 'Active', 'Active ?', p_controller.Active);
		p_html += buildLcarTextWidget(self, 'UUID', 'UUID', p_controller.UUID, 'disabled');
		p_html += buildLcarTextWidget(self, 'Comment', 'Comment', p_controller.Comment);
		p_html += buildLcarTextWidget(self, 'Coords', 'Coords', p_controller.Coords);
		p_html += buildLcarTrueFalseWidget(self, 'Dimmable', 'Light Dimmable ?', p_controller.IsDimmable);
		p_html += buildLcarFamilySelectWidget(self, 'ControllerFamily', 'Family', p_controller.ControllerFamily, p_onchange);
		p_html += buildLcarRoomSelectWidget(self, 'RoomName', 'Room', p_controller.RoomName);
		p_html += buildLcarLightTypeSelectWidget(self, 'LightingType', 'Type', p_controller.LightingType);
		p_html += buildLcarInterfaceTypeSelectWidget(self, 'InterfaceType', 'Interface Type', p_controller.InterfaceType);
		p_html += buildLcarTextWidget(self, 'Port', 'Port', p_controller.Port);
		return p_html;
	},
	function buildInsteonPart(self, p_controller, p_html) {
		p_html += buildLcarTextWidget(self, 'InsteonAddress', 'Insteon Address', p_controller.InsteonAddress);
		p_html += buildLcarTextWidget(self, 'DevCat', 'Dev Cat', p_controller.DevCat);
		p_html += buildLcarTextWidget(self, 'GroupNumber', 'Group Number', p_controller.GroupNumber);
		p_html += buildLcarTextWidget(self, 'GroupList', 'Group List', p_controller.GroupList);
		p_html += buildLcarTrueFalseWidget(self, 'Master', 'Light Master ?', p_controller.IsMaster);
		p_html += buildLcarTrueFalseWidget(self, 'Controller', 'Light Controller ?', p_controller.IsController);
		p_html += buildLcarTrueFalseWidget(self, 'Responder', 'Light Responder ?', p_controller.IsResponder);
		p_html += buildLcarTextWidget(self, 'ProductKey', 'Product Key', p_controller.ProductKey);
		return p_html;
	},
	function buildUpbPart(self, p_controller, p_html) {
		p_html += buildLcarTextWidget(self, 'UpbAddress', 'UPB Address', p_controller.UPBAddress);
		p_html += buildLcarTextWidget(self, 'UpbPassword', 'UPB Password', p_controller.UPBPassword);
		p_html += buildLcarTextWidget(self, 'UpbNetworkID', 'UPB Network', p_controller.UPBNetworkID);
		return p_html;
	},
	function buildAllParts(self, p_controller, p_html, p_handler, p_onchange) {
		p_html = self.buildBasicPart(p_controller, p_html, p_onchange) ;
		if (p_controller.ControllerFamily === 'Insteon')
			p_html = self.buildInsteonPart(p_controller, p_html);
		else if (p_controller.ControllerFamily === 'UPB')
        	p_html = self.buildUpbPart(p_controller, p_html);
		else
			Divmod.debug('---', 'ERROR - controllers.buildAllParts() Family = ' + p_controller.ControllerFamily);
		if (p_controller.InterfaceType === 'Serial')
			p_html = buildSerialPart(self, p_controller, p_html);
		p_html += buildLcarEntryButtons(p_handler);
		return p_html;
	},
	function buildLcarDataEntryScreen(self, p_entry, p_handler){
		var l_controller = arguments[1];
		var l_html = self.buildAllParts(l_controller, l_html, p_handler, 'familyChanged');
		var l_html_2 = "";
		l_html_2 += build_lcars_top('Controller Data', 'lcars-salmon-color');
		l_html_2 += build_lcars_middle_menu(40, l_html);
		l_html_2 += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html_2;
	},
	function familyChanged() {
		var l_obj = globals.House.LightObj;
		var l_self = globals.House.Self;
		l_obj.ControllerFamily = fetchSelectWidget(l_self, 'ControllerFamily');
		l_self.buildLcarDataEntryScreen(l_obj, 'handleDataOnClick');
	},
    function fetchEntry(self) {
    	var l_data = {
    		Delete :		false
        };
		l_data = self.fetchBaseEntry(l_data);
		l_data = self.fetchLightingCoreEntry(l_data);
		l_data = self.fetchControllerEntry(l_data);
        if (l_data.ControllerFamily === 'Insteon')
        	l_data = self.fetchInsteonEntry(l_data);
        if (l_data.ControllerFamily === 'UPB')
        	l_data = self.fetchUpbEntry(l_data);
        if (l_data.InterfaceType === 'Serial')
        	l_data = fetchSerialEntry(self, l_data);
     	console.log("controllers.fetchEntry() - Data = %O", l_data);
        return l_data;
    },
    function fetchBaseEntry(self, p_data) {
    	p_data.Name = fetchTextWidget(self, 'Name');
    	p_data.Key = fetchTextWidget(self, 'Key');
    	p_data.Active = fetchTrueFalseWidget(self, 'Active');
    	p_data.UUID = fetchTextWidget(self, 'UUID');
    	return p_data;
    },
    function fetchLightingCoreEntry(self, p_data) {
        p_data.ControllerFamily = fetchSelectWidget(self, 'ControllerFamily');
        p_data.Comment = fetchTextWidget(self, 'Comment');
        p_data.Coords = fetchTextWidget(self, 'Coords');
        p_data.IsDimmable = fetchTrueFalseWidget(self, 'Dimmable');
        p_data.RoomName = fetchTextWidget(self, 'RoomName');
        p_data.LightingType = fetchSelectWidget(self, 'LightingType');
    	return p_data;
    },
    function fetchControllerEntry(self, p_data) {
        p_data.InterfaceType = fetchSelectWidget(self, 'InterfaceType');
        p_data.Port = fetchTextWidget(self, 'Port');
    	return p_data;
    },
	function fetchInsteonEntry(self, p_data) {
        p_data.InsteonAddress = fetchTextWidget(self, 'InsteonAddress');
        p_data.DevCat = fetchTextWidget(self, 'DevCat');
        p_data.GroupNumber = fetchTextWidget(self, 'GroupNumber');
        p_data.GroupList = fetchTextWidget(self, 'GroupList');
        p_data.IsMaster = fetchTrueFalseWidget(self, 'Master');
        p_data.IsResponder = fetchTrueFalseWidget(self, 'Responder');
        p_data.IsController = fetchTrueFalseWidget(self, 'Controller');
        p_data.ProductKey = fetchTextWidget(self, 'ProductKey');
		return p_data;
	},
	function fetchUpbEntry(self, p_data) {
		Divmod.debug('---', 'controllers.fetchUpbEntry() was called.');
        p_data.UPBAddress = fetchTextWidget(self, 'UpbAddress');
        p_data.UPBPassword = fetchTextWidget(self, 'UpbPassword');
        p_data.UPBNetworkID = fetchTextWidget(self, 'UpbNetworkID');
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
			ControllerFamily : 'Insteon',
			RoomName : '',
            LightingType : 'Controller',
			UUID : '',
			InsteonAddress  : '11.22.33',
			DevCat			: 0,
			GroupNumber		: 0,
			GroupList		: '',
			IsMaster		: false,
			IsResponder		: false,
			IsController	: false,
			ProductKey		: 0,
			InterfaceType	: 'Serial',
			Port			: '/dev/ttyS0',
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
        	self.startWidget()
        }
        function eb_handleDataOnClick(p_reason){
            Divmod.debug('---', 'ERROR controllers.eb_handleDataOnClick() - ' + p_reason);
        }
		var l_ix = p_node.name;
		var l_obj = self.fetchEntry();
		var l_json = '';
		var l_defer = '';
		switch(l_ix) {
		case '10003':  // The 'Change' Button
			l_json = JSON.stringify(l_obj);
	        l_defer = self.callRemote("saveControllerData", l_json);  // @ web_controller
	        l_defer.addCallback(cb_handleDataOnClick);
	        l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // The 'Back' button
			self.hideDataEntry();
			self.showSelectionButtons();
			break;
		case '10004':  // The 'Delete' button
			l_obj.Delete = true;
	    	l_json = JSON.stringify(l_obj);
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
// Divmod.debug('---', 'controllers.handleMenuOnClick(1) was called. ' + l_ix + ' ' + l_name);
// console.log("controllers.handleMenuOnClick() - l_obj = %O", l_obj);
//### END DBK
