/**
 * 
 */

// import Nevow.Athena

//    rootMenu.MyWidget = Nevow.Athena.Widget.subclass('rootMenu.MyWidget');

Nevow.Athena.Widget.subclass(pyhousePackage, 'LoginClass').methods(

    function __init__(self, node) {
        ChatThing.ChatterWidget.upcall(self, "__init__", node);
        self.loginForm = self.nodeByAttribute('name', 'loginForm');
        self.loginNameField = self.nodeByAttribute('name', 'loginName');
    },

    function doLogin(self) {
        self.callRemote("say", self.loginNameField.value);
        //self.nodeByAttribute('name', 'userMessage').value = "";
        return false;
    }
    );

//### END DBK
