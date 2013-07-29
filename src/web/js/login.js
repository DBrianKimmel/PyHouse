/** login.js
 * 
 */

// import Nevow.Athena

Nevow.Athena.Widget.subclass(login, 'LoginElement').methods(

    function __init__(self, node) {
        login.LoginElement.upcall(self, "__init__", node);
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
