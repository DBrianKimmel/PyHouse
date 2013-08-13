/* login.js
 * 
 */

// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(login, 'LoginElement').methods(


    function __init__(self, node) {
    	//alert('LoginElement.__init__() ' + node)
        login.LoginElement.upcall(self, "__init__", node);

        self.loginElement = self.nodeByAttribute('name', 'LoginElement');
        self.loginForm = self.nodeByAttribute('name', 'LoginForm');
        self.loginNameField = self.nodeByAttribute('name', 'LoginName');
        self.loginPassword = self.nodeByAttribute('name', 'LoginPassword')
    },

	function ready(self) {

		function widgetready(res) {
			// do whatever init needs here, show for the widget is handled in superclass
			self.doLogin();
		}
	
		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(widgetready);
		return d;
	},

	function getAndShowTime(self) {

		function cb_showTime(time) {
			self.node.innerHTML = time;
			self.callLater(1.0, function() {
				self.getAndShowTime();
			});
		}
	
		var d = self.callRemote('getTimeOfDay');
		d.addCallback(cb_showTime);
	},

    function doLogin(self, node) {
		
		function cb_showLogin() {
			self.node.innerHTML = l_name
		}
    	var symbol = node.value
    	var l_name = self.loginNameField.value
    	var l_pass = self.loginPassword.value
        var l_logData = {
        		name : l_name,
        		passwd : l_pass
        }
    	var l_json = JSON.stringify(l_logData)
        var d = self.callRemote("loginUser", l_json);
		d.addCallback(cb_showLogin);
        return false;
    }

);

//### END DBK
