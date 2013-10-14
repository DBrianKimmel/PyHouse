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
        }
        //Divmod.debug('---', 'controllers.ready() was called. ' + self);
        var uris = collectIMG_src(self.node, null);
        var l_defer = loadImages(uris);
        l_defer.addCallback(cb_widgetready);
        return l_defer;
    },
    
    function showWidget(self) {
        Divmod.debug('---', 'controllers.showWidget() was called.');
        self.node.style.display = 'block';
        self.showButtons(self);
        self.hideEntry(self);
        self.fetchControllerData(self, globals.House.HouseIx);
    },
    function hideButtons(self) {
        Divmod.debug('---', 'controllers.hideButtons() was called. ');
        self.nodeById('ControllerButtonsDiv').style.display = 'none';        
    },
    function showButtons(self) {
        Divmod.debug('---', 'controllers.showButtons() was called. ');
        self.nodeById('ControllerButtonsDiv').style.display = 'block';    
    },
    function hideEntry(self) {
        //Divmod.debug('---', 'controllers.hideEntry() was called. ');
        self.nodeById('ControllerEntryDiv').style.display = 'none';        
    },
    function showEntry(self) {
        //Divmod.debug('---', 'controllers.showEntry() was called. ');
        self.nodeById('ControllerEntryDiv').style.display = 'block';        
    },

    // ============================================================================
    /**
     * This triggers getting the controller data from the server.
     * The server calls displayControllerButtons with the controllers info.
     * 
     * @param p_houseIndex is the house index that was selected
     */
    function fetchControllerData(self, p_houseIndex) {
        function cb_fetchControllerData(self, p_json, p2) {
            Divmod.debug('---', 'controllers.cb_fetchControllerData() was called.');
        }
        function eb_fetchControllerData(self, p1, p2) {
            Divmod.debug('---', 'controllers.eb_fetchControllerData() was called. ' + p1 + ' ' + p2);
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
    function fillEntry(self, p_entry) {
        Divmod.debug('---', 'controllers.fillEntry() was called. ' + self + ' ' + p_entry);
        self.nodeById('Name').value = selectedControllerObj.Name;
        self.nodeById('Key').value = selectedControllerObj.Key;
        self.nodeById('Active').value = selectedControllerObj.Active;
        self.nodeById('Type').value = selectedControllerObj.Type;
        self.nodeById('Time').value = selectedControllerObj.Time;
        self.nodeById('Level').value = selectedControllerObj.Level;
        self.nodeById('Rate').value = selectedControllerObj.Rate;
        self.nodeById('RoomName').value = selectedControllerObj.RoomName;
        self.nodeById('LightName').value = selectedControllerObj.LightName;
    },
    
    function fetchEntry(self) {
        var l_controllerData = {
            Name : self.nodeById('Name').value,
            Key : self.nodeById('Key').value,
            Active : self.nodeById('Active').value,
            Type : self.nodeById('Type').value,
            Time : self.nodeById('Time').value,
            Level : self.nodeById('Level').value,
            Rate : self.nodeById('Rate').value,
            RoomName : self.nodeById('RoomName').value,
            LightName : self.nodeById('LightName').value
            }
        return l_controllerData;
    },

    /**
     * Event handler for controller selection buttons.
     * 
     * @param self is    <"Instance" of undefined.controllers.ControllersWidget>
     * @param p_node is  the node of the button that was clicked.
     */
    function doHandleOnClick(self, p_node) {
        var l_ix = p_node.name;
        var l_name = p_node.value;
        if (l_ix <= 1000) {
            selectedControllerIx = p_node.name;
            selectedControllerObj = controllersObj[selectedControllerIx];
            Divmod.debug('---', 'controllers.doHandleOnClick(1) was called. ' + selectedControllerIx + ' ' + l_name);
            console.log("controllers.doHandleOnClick() - controllers %O", controllersObj);
            self.showEntry(self);
            self.hideButtons(self);
            self.fillEntry(self, selectedControllerObj);
        } else if (l_ix == 10001) {
            // add key
            self.showEntry(self);
            self.hideButtons(self);
        } else if (l_ix == 10002) {
            // back key
            self.hideWidget();
            var l_node = findWidgetByClass('HouseMenu');
            l_node.showWidget(self);
        }
    },
    
    /**
     * Event handler for submit buttons at bottom of entry portion of this widget.
     * Get the possibly changed data and send it to the server.
     */
    function doHandleSubmit(self, p_node) {
        Divmod.debug('---', 'controllers.doHandleSubmit() was called. ');
        console.log("controllers.doHandleSubmit() - self %O", self);
        console.log("controllers.doHandleSubmit() - node %O", p_node);
        
        function cb_doHandleSubmit(p_json) {
            Divmod.debug('---', 'controller.cb_doHandleSubmit() was called.');
            self.showWidget(self);
        }
        function eb_doHandleSubmit(res){
            Divmod.debug('---', 'login.eb_doHandleSubmit() was called. res=' + res);
        }
        var l_json = JSON.stringify(self.fetchEntry(self));
        Divmod.debug('---', 'login.doHandleSubmit(1) was called. json:' + l_json);
        var l_defer = self.callRemote("doControllerSubmit", l_json);  // @ web_controller
        l_defer.addCallback(cb_doHandleSubmit);
        l_defer.addErrback(eb_doHandleSubmit);
        // return false stops the resetting of the server.
        return false;
    },

    // ============================================================================
    /**
     * Pushed from the server. fill in the table and wait for an event to happen (doHandleOnClick).
     */
    function displayControllerButtons(self, p_json) {
        Divmod.debug('---', 'controllers.displayControllerButtons() was called. ');
        controllersObj = JSON.parse(p_json);
        var l_tab = buildTable(self, controllersObj, '');
        self.nodeById('ControllerTableDiv').innerHTML = l_tab;
    }
);

//### END DBK
