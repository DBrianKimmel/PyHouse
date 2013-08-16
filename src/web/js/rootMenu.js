/** rootMenu.js
 * 
 */
// import Nevow.Athena

helpers.Widget.subclass(rootMenu, 'RootMenuWidget').methods(

    function __init__(self, node) {
        rootMenu.RootMenuWidget.upcall(self, "__init__", node);
        alert('rootMenu 1');
    },

	function ready(self) {
		
		function cb_widgetready(res) {
	        alert('rootMenu 2');
			self.showRoot();
			// do whatever init needs here, show for the widget is handled in superclass
	        alert('rootMenu 1\3');
		}
	
        alert('rootMenu 4');
		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(cb_widgetready);
		return d;
	},

	function showRoot(self) {

		function cb_showRoot() {
	        alert('rootMenu 5');
			self.node.innerHTML = 'abc';
			//self.callLater(1.0, function() {
			//	self.getAndShowTime();
			});
		}
	
    	alert('rootMenu 6');
		var d = self.callRemote('rootMenu');
		d.addCallback(cb_showRoot);
	}

    );

//### END DBK
