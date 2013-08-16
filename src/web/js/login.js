/* login.js
 * 
 * Displays the login 
 */

// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(login, 'LoginWidget').methods(

    function __init__(self, node) {
        login.LoginWidget.upcall(self, "__init__", node);
    },

	function ready(self) {

		function cb_widgetready(res) {
			// do whatever init needs here, show for the widget is handled in superclass
			self.getAndShowLogin();
		}
	
		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(cb_widgetready);
		return d;
	},  // ready

	function getAndShowLogin(self) {

		function cb_showLogin(p_user) {
			self.node.innerHTML = p_user;
			//self.callLater(1.0, function() {
			//	self.getAndShowLogin();
			//});
			}
	
		//alert("DBK - Login ");
    	var l_name = self.loginNameField.value;
    	var l_pass = '123'; // self.loginPassword.value;
        var l_logData = {
        		name : l_name,
        		passwd : l_pass
        };
    	var l_json = JSON.stringify(l_logData);
        var d = self.callRemote("login", l_json);
		d.addCallback(cb_showLogin);
        return false;
	},  // getAndShowLogin
	
	function doLogin(self) {
		//alert("login.js doLogin()");
		var loginNameField = self.nodeById('LoginName');
    	var l_name = loginNameField.value;
    	var l_pass = '123'; // self.loginPassword.value;
        var l_logData = {
        		name : l_name,
        		passwd : l_pass
        };
    	var l_json = JSON.stringify(l_logData);
		Divmod.debug('---', ' doLogin was called. json:' + l_json);
        var d = self.callRemote("login", l_json);
		d.addCallback(cb_showLogin);
        return false;
	}

);

//### END DBK
