/* controllers.js
 * 
 * Browser side code.
 * 
 * Display the controllers 
 */

// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(controllers, 'ControllersWidget').methods(

    function __init__(self, node) {
        controllers.ControllersWidget.upcall(self, "__init__", node);
    },

	function ready(self) {  // override helpers.Widget.ready()

		function cb_widgetready(res) {
			// do whatever init needs here, 'show' for the widget is handled in superclass
			self.hideControllers();
		};
	
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	function hideControllers(self) {
		//Divmod.debug('---', 'controllers.hideController was called.');
		self.node.style.display = 'none';
	},
	
	/**
	 * 
	 * @param self
	 * @returns {Boolean}
	 */
	function doControlerEdit(self) {  // from html handler onSubmit
		
		function cb_doEdit(p_json) {
			Divmod.debug('---', 'login.cb_doLogin(1) was called.');
		}
		function eb_doEdit(res){
			Divmod.debug('---', 'login.eb_doLogin(1) was called. res=' + res);
		}

		l_defer.addCallback(cb_doEdit);
		l_defer.addErrback(eb_doEdit);
	},
	
	function doControllerAdd(self) {
		//Divmod.debug('---', 'login.eb_doControllerAdd was called. self=' + self);
	},
	
	function doControllerDelete(self) {
		//Divmod.debug('---', 'login.eb_doControllerDelete was called. self=' + self);
	},
	
	function XXXdisplayXLoggedIn(self) {
		var formNode = self.nodeById('LoginForm');
		var loggedInDiv = self.nodeById('LoggedInDiv');
		formNode.style.display = "none";
		loggedInDiv.style.display = "visible";
	}
);

//### END DBK
