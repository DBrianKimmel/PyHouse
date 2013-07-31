/** login.js
 * 
 */

// import Nevow.Athena

login.LoginElement = Nevow.Athena.Widget.subclass('login.LoginElement');
login.LoginElement.methods(

    function __init__(self, node) {
    	//alert('LoginElement.__init__()')
        login.LoginElement.upcall(self, "__init__", node);
        self.loginElement = self.nodeByAttribute('name', 'LoginElement');
        self.loginForm = self.nodeByAttribute('name', 'LoginForm');
        self.loginNameField = self.nodeByAttribute('name', 'LoginName');
    },

    function doLogin(self, node) {
    	//DivMod.debug('doLogin', "Startup")
    	alert('doLogin')
    	var symbol = node.value
        self.callRemote("login", self.loginNameField.value);
    	//DivMod.debug('login', "Finished")
        return false;
    }
    );

Nevow.Athena.Widget.subclass(login, 'LoginPage').methods(

	    function __init__(self, node) {
	    	alert('LoginPage')
	        login.LoginPage.upcall(self, "__init__", node);
	        self.loginForm = self.nodeByAttribute('name', 'loginForm');
	        self.loginNameField = self.nodeByAttribute('name', 'loginName');
	    },

	    function do_LoginPage(self) {
	        self.callRemote("say", self.loginNameField.value);
	        //self.nodeByAttribute('name', 'userMessage').value = "";
	        return false;
	    }
	    );

//### END DBK
