/* controllers.js
 * 
 * Displays the controllers.
 * Browser side code.
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

    /**
     * Place the widget in the workspace.
     * 
     * @param self is    <"Instance" of undefined.controllers.ControllersWidget>
     * @returns a deferred
     */
    function ready(self) {
        
        function cb_widgetready(res) {
            // do whatever initialization needs here, 'show' for the widget is handled in superclass
            //Divmod.debug('---', 'controllers.cb_widgready() was called.');
            self.hideWidget();
            self.fetchInterfaceData();
        }
        //Divmod.debug('---', 'controllers.ready() was called. ' + self);
        var uris = collectIMG_src(self.node, null);
        var l_defer = loadImages(uris);
        l_defer.addCallback(cb_widgetready);
        return l_defer;
    },
    function showWidget(self) {
        self.node.style.display = 'block';
        self.showButtons(self);
        self.hideEntry(self);
        self.fetchControllerData();
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
     * This triggers getting the controller data from the server.
     * The server calls displayControllerButtons with the controllers info.
     */
    function fetchControllerData(self) {
        function cb_fetchControllerData(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			var l_tab = buildTable(globals.House.HouseObj.Controllers, 'handleMenuOnClick');
			self.nodeById('ControllerTableDiv').innerHTML = l_tab;
        }
        function eb_fetchControllerData(res) {
            Divmod.debug('---', 'controllers.eb_fetchControllerData() was called.  ERROR - ' + res);
        }
        var l_defer = self.callRemote("getControllerData", globals.House.HouseIx);  // call server @ web_controllers.py
        l_defer.addCallback(cb_fetchControllerData);
        l_defer.addErrback(eb_fetchControllerData);
        return false;
    },

    
    /**
     * Fill in the controller entry screen with all of the data for this controller.
     * 
     *  self.Name = ''
     *  self.Key = 0
     *  self.Active = False
     *  self.Comment = ''
     *  self.Coords = ''
     -  self.CurLevel = 0
     *  self.Dimmable = False
     *  self.Family = ''
     *  self.RoomName = ''
     *  self.Type = ''
        
     -  self.Command = None
     -  self.Data = None  # Interface specific data
     -  self.DriverAPI = None
     -  self.HandlerAPI = None  # PLM, PIM, etc (family controller device handler) API() address
     *  self.Interface = ''
     -  self.Message = ''
     -  self.Queue = None
     *  self.Port = ''
        
        self.DevCat = 0  # DevCat and SubCat (2 bytes)
     =  self.Family = 'Insteon'
     -  self.GroupList = ''
     -  self.GroupNumber = 0
        self.Master = False  # False is Slave
        self.ProductKey = ''
        self.Responder = False
     -  self.Command1 = 0
     -  self.Command2 = 0

     =  self.Family = 'UPB'
        self.NetworkID = None
        self.Password = None
        self.UnitID = None
     -  self.Command1 = 0

     */
    function fillEntry(self, p_obj) {
        //Divmod.debug('---', 'controllers.fillEntry() was called. ' + p_obj);
        self.nodeById('NameDiv').innerHTML = buildTextWidget('ControllerName', p_obj.Name);
        self.nodeById('KeyDiv').innerHTML = buildTextWidget('ControllerKey', p_obj.Key, 'disabled');
		self.nodeById('ActiveDiv').innerHTML = buildTrueFalseWidget('ControllerActive', p_obj.Active);
		self.nodeById('CommentDiv').innerHTML = buildTextWidget('ControllerComment', p_obj.Comment);
		self.nodeById('CoordsDiv').innerHTML = buildTextWidget('ControllerCoords', p_obj.Coords);
		self.nodeById('DimmableDiv').innerHTML = buildTrueFalseWidget('ControllerDimmable', p_obj.Dimmable);
		self.nodeById('FamilyDiv').innerHTML = buildTextWidget('ControllerFamily', p_obj.Family);
		self.nodeById('RoomNameDiv').innerHTML = buildRoomSelectWidget('ControllerRoomName', p_obj.RoomName);
		self.nodeById('TypeDiv').innerHTML = buildTextWidget('ControllerType', p_obj.Type, 'disabled');
		self.nodeById('UUIDDiv').innerHTML = buildTextWidget('ControllerUUID', p_obj.UUID, 'disabled');
		self.nodeById('ControllerEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick');
    },
    function fetchEntry(self) {
        var l_data = {
            Name : fetchTextWidget('ControllerName'),
            Key : fetchTextWidget('ControllerKey'),
			Active : fetchTrueFalse('ControllerActive'),
			Comment : fetchTextWidget('ControllerComment'),
			Coords : fetchTextWidget('ControllerCoords'),
			Dimmable : fetchTrueFalse('ControllerDimmable'),
			Family : fetchTextWidget('ControllerFamily'),
			RoomName : fetchSelectWidget('ControllerRoomName'),
			Type : fetchTextWidget('ControllerType'),
			UUID : fetchTextWidget('ControllerUUID'),
			HouseIx : globals.House.HouseIx,
			Delete : false
            }
        return l_data;
    },
    function createEntry(self, p_ix) {
        var l_data = {
            Name : 'Change Me',
            Key : Object.keys(globals.House.HouseObj.Controllers).length,
            Active : false,
			Comment : '',
			Coords : '',
			Dimmable : false,
			Family : '',
			RoomName : '',
            Type : 'Controller',
			UUID : '',
			HouseIx : p_ix,
			Delete : false
            }
        return l_data;
    },

    /**
     * Event handler for controller selection buttons.
     * 
     * @param self is    <"Instance" of undefined.controllers.ControllersWidget>
     * @param p_node is  the node of the button that was clicked.
     */
    function handleMenuOnClick(self, p_node) {
        var l_ix = p_node.name;
        var l_name = p_node.value;
		globals.House.ControllerIx = l_ix;
		globals.House.ControllerName = l_name;
        if (l_ix <= 1000) {
        	// One of the controller buttons
			var l_obj = globals.House.HouseObj.Controllers[l_ix];
            //Divmod.debug('---', 'controllers.handleMenuOnClick(1) was called. ' + l_ix + ' ' + l_name);
            self.showEntry();
            self.hideButtons();
            self.fillEntry(l_obj);
        } else if (l_ix == 10001) {
            // add key
            self.showEntry();
            self.hideButtons();
        } else if (l_ix == 10002) {
            // back key
            self.hideWidget();
            var l_node = findWidgetByClass('HouseMenu');
            l_node.showWidget();
        }
    },
    
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
		case '10003':  // Change Button
			var l_json = JSON.stringify(self.fetchEntry(self));
	        //Divmod.debug('---', 'controllers.handleDataOnClick(1) was called. json:' + l_json);
	        var l_defer = self.callRemote("saveControllerData", l_json);  // @ web_controller
	        l_defer.addCallback(cb_handleDataOnClick);
	        l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			//Divmod.debug('---', 'controllers.handleDataOnClick(Back) was called.  ');
			self.hideEntry();
			self.showButtons();
			break;
		case '10004':  // Delete button
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
