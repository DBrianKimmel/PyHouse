/** login.js
 * 
 */
// import Nevow.Athena

login.LoginElement = Nevow.Athena.Widget.subclass('login.LoginElement');
login.LoginElement.methods(

    function __init__(self, node) {
    	//alert('LoginElement.__init__() ' + node)
        login.LoginElement.upcall(self, "__init__", node);
        self.loginElement = self.nodeByAttribute('name', 'LoginElement');
        self.loginForm = self.nodeByAttribute('name', 'LoginForm');
        self.loginNameField = self.nodeByAttribute('name', 'LoginName');
        self.loginPassword = self.nodeByAttribute('name', 'LoginPassword')
    },

    function doLogin(self, node) {
    	//DivMod.debug('doLogin', "Startup")
    	var symbol = node.value
    	var l_name = self.loginNameField.value
    	var l_pass = self.loginPassword.value
        var l_logData = {
        		name : l_name,
        		passwd : l_pass
        }
    	var l_json = JSON.stringify(l_logData)
        self.callRemote("login", l_json);
    	//DivMod.debug('login', "Finished")
    	//alert('doLogin ' + l_json)
        return false;
    }
    );

//### END DBK
