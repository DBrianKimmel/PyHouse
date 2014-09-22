/* controllers.js
 * 
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
 * 
 * This widget has 2 parts:
 *   1. The controller selection section whhich shows a button for each controller and allows one to add a new controller.
 *   2. The controller data section which allows entering/changing all the detail about the selected controller.
 *      It also allows the controller to be deleted.
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
            //Divmod.debug('---', 'controllers.cb_widgready() was called.');
            self.hideWidget();
            //self.fetchInterfaceData();
        }
        var uris = collectIMG_src(self.node, null);
        var l_defer = loadImages(uris);
        l_defer.addCallback(cb_widgetready);
        return l_defer;
    },
    function showWidget(self) {
        self.node.style.display = 'block';
        self.showButtons(self);
        self.hideEntry(self);
        self.fetchHouseData();
    },
    function hideButtons(self) {
        self.nodeById('ControllerButtonsDiv').style.display = 'none';        
    },
    function showButtons(self) {
        self.nodeById('ControllerButtonsDiv').style.display = 'block';    
    },
    function hideEntry(self) {
        self.nodeById('ControllerEntryDiv').style.display = 'none';        
    },
    function showEntry(self) {
        self.nodeById('ControllerEntryDiv').style.display = 'block';        
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
        var l_defer = self.callRemote("getInterfaceData");  // call server @ web_controllers.py
        l_defer.addCallback(cb_fetchInterfaceData);
		return false;
    },

    // ============================================================================
    /**
     * This triggers getting the data from the server.
     */
    function fetchHouseData(self) {
        function cb_fetchHouseData(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			var l_tab = buildTable(globals.House.HouseObj.Controllers, 'handleMenuOnClick');
			self.nodeById('ControllerTableDiv').innerHTML = l_tab;
        }
        function eb_fetchHouseData(res) {
            Divmod.debug('---', 'controllers.eb_fetchHouseData() was called.  ERROR - ' + res);
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
            //Divmod.debug('---', 'controllers.hndleMenuOnClick(Controller) was called. ');
            self.hideButtons();
            self.showEntry();
			var l_obj = globals.House.HouseObj.Controllers[l_ix];
            self.fillEntry(l_obj);
        } else if (l_ix == 10001) {  // The 'Add' button
            self.hideButtons();
            self.showEntry();
			var l_ent = self.createEntry();
			self.fillEntry(l_ent);
        } else if (l_ix == 10002) {  // The 'Back' button
            self.hideWidget();
            var l_node = findWidgetByClass('HouseMenu');
            l_node.showWidget();
        }
    },
    function fillEntry(self, p_obj) {
        self.nodeById('NameDiv').innerHTML           = buildTextWidget('ControllerName', p_obj.Name);
        self.nodeById('KeyDiv').innerHTML            = buildTextWidget('ControllerKey', p_obj.Key, 'disabled');
		self.nodeById('ActiveDiv').innerHTML         = buildTrueFalseWidget('ControllerActive', p_obj.Active);
		self.nodeById('CommentDiv').innerHTML        = buildTextWidget('ControllerComment', p_obj.Comment);
		self.nodeById('CoordsDiv').innerHTML         = buildTextWidget('ControllerCoords', p_obj.Coords);
		self.nodeById('DimmableDiv').innerHTML       = buildTrueFalseWidget('ControllerDimmable', p_obj.Dimmable);
		self.nodeById('FamilyDiv').innerHTML         = buildTextWidget('ControllerFamily', p_obj.ControllerFamily);
		self.nodeById('RoomNameDiv').innerHTML       = buildRoomSelectWidget('ControllerRoomName', p_obj.RoomName);
		self.nodeById('TypeDiv').innerHTML           = buildTextWidget('ControllerType', p_obj.LightingType, 'disabled');
		self.nodeById('UUIDDiv').innerHTML           = buildTextWidget('ControllerUUID', p_obj.UUID, 'disabled');
		self.nodeById('InterfaceDiv').innerHTML      = buildInterfaceTypeSelectWidget('InterfaceType', p_obj.InterfaceType);
		self.nodeById('PortDiv').innerHTML           = buildTextWidget('ControllerPort', p_obj.Port);
        if (p_obj['ControllerFamily'] == 'Insteon') {  // Insteon info
			self.fillInsteonEntry(p_obj);
        }
		self.nodeById('ControllerEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick');
    },
	function fillInsteonEntry(self, p_obj) {
		self.nodeById('i01Div').innerHTML  = buildTextWidget('LightAddress', p_obj.InsteonAddress);
		self.nodeById('i02Div').innerHTML  = buildTextWidget('LightDevCat', p_obj.DevCat);
		self.nodeById('i03Div').innerHTML  = buildTextWidget('LightGroupNumber', p_obj.GroupNumber);
		self.nodeById('i04Div').innerHTML  = buildTextWidget('LightGroupList', p_obj.GroupList);
		self.nodeById('i05Div').innerHTML  = buildTrueFalseWidget('LightMaster', p_obj.IsMaster);
		self.nodeById('i06Div').innerHTML  = buildTrueFalseWidget('LightResponder', p_obj.IsResponder);
		self.nodeById('i07Div').innerHTML  = buildTextWidget('LightProductKey', p_obj.ProductKey);
	},
    function fetchEntry(self) {
        var l_data = {
            Name :           fetchTextWidget('ControllerName'),
            Key :            fetchTextWidget('ControllerKey'),
			Active :         fetchTrueFalseWidget('ControllerActive'),
			Comment :        fetchTextWidget('ControllerComment'),
			Coords :         fetchTextWidget('ControllerCoords'),
			IsDimmable :     fetchTrueFalseWidget('ControllerDimmable'),
			ControllerFamily : fetchTextWidget('ControllerFamily'),
			RoomName :       fetchSelectWidget('ControllerRoomName'),
			LightingType :   fetchTextWidget('ControllerType'),
			UUID :           fetchTextWidget('ControllerUUID'),
			InterfaceType :      fetchSelectWidget('InterfaceType'),
			Port :           fetchTextWidget('ControllerPort'),
			Delete : false
            }
        if (l_data['ControllerFamily'] == 'Insteon') {
        	l_data = self.fetchInsteonEntry(l_data);
        }
        return l_data;
    },
	function fetchInsteonEntry(self, p_data) {
        p_data['InsteonAddress'] = fetchTextWidget('LightAddress');
        p_data['DevCat'] = fetchTextWidget('LightDevCat');
        p_data['GroupNumber'] = fetchTextWidget('LightGroupNumber');
        p_data['GroupList'] = fetchTextWidget('LightGroupList');
        p_data['IsMaster'] = fetchTrueFalseWidget('LightMaster');
        p_data['IsResponder'] = fetchTrueFalseWidget('LightResponder');
        p_data['ProductKey'] = fetchTextWidget('LightProductKey');
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
            }
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
		switch(l_ix) {
		case '10003':  // The 'Change' Button
			var l_json = JSON.stringify(self.fetchEntry(self));
	        //Divmod.debug('---', 'controllers.handleDataOnClick(1) was called. json:' + l_json);
	        var l_defer = self.callRemote("saveControllerData", l_json);  // @ web_controller
	        l_defer.addCallback(cb_handleDataOnClick);
	        l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // The 'Back' button
			//Divmod.debug('---', 'controllers.handleDataOnClick(Back) was called.  ');
			self.hideEntry();
			self.showButtons();
			break;
		case '10004':  // The 'Delete' button
			var l_obj = self.fetchEntry();
			l_obj['Delete'] = true;
	    	var l_json = JSON.stringify(l_obj);
			//Divmod.debug('---', 'controllers.handleDataOnClick(Delete) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveControllerData", l_json);  // @ web_rooms
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
//### END DBK
