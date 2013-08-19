/* login.js
 * 
 * Browser side code.
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
			//self.getAndShowLogin();
		}  // cb_widgetready
	
		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(cb_widgetready);
		return d;
	},  // ready

	function getAndShowLogin(self) {

		function cb_showLogin(p_user) {
			self.node.innerHTML = 'Show Login';
		}  // cb_showLogin
	
        var l_logData = {
        		name : 'silly',
        		passwd : '123'
        };
    	var l_json = JSON.stringify(l_logData);
		Divmod.debug('---', 'login.getAndShowLogin() was called.');
    	var d = self.callRemote("login", l_json);  // @ web_mainpage
		d.addCallback(cb_showLogin);
        return false;
	},  // getAndShowLogin
	
	function doLogin(self) {  // from html handler onSubmit
		
		function cb_doLogin(p_json) {
			Divmod.debug('---', 'login.cb_doLogin() was called.');
		}
		
		var loginNameField = self.nodeById('LoginName');
		var loginPasswordField = self.nodeById('LoginPassword');
    	var l_name = loginNameField.value;
    	var l_pass = loginPasswordField.value;
        var l_logData = {
        		name : l_name,
        		passwd : l_pass
        };
    	var l_json = JSON.stringify(l_logData);
		Divmod.debug('---', ' doLogin was called. json:' + l_json);
        var d = self.callRemote("doLogin", l_json);
		d.addCallback(cb_doLogin);
        return false;
	}
);

//### END DBK
