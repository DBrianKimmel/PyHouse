/** helpers.js
 * 
 * This script is the live element functionality.
 */

// import Nevow.Athena

/**
 * This basic widget can attach subwidgets and provides some other basic functionality.
 */

Nevow.Athena.Widget.subclass(helpers, 'Widget').methods(
		
	function __init__(self, node) {
		helpers.Widget.upcall(self, '__init__', node);
	},

	
	/**
	 *  Special attention should be paid to the function C{ready} which should be overridden in almost every case,
	 *  working with the C{widgetready} function in a closure.
	 *  
	 * C{widgetready} could of call another method C{func} in the class but practice shows, that the point of being informed that
	 *  we're setup properly for action is way too important to delegate it into superclass.
	 *  
	 * Think of C{ready} as a stub, which is more like a template to start work on your own widgets implementation.
	 * 
	 * @param self = 
	 * @returns a deferred that completes async
	 */
	function ready(self) {

		function cb_widgetready(res) {
			//do whatever init needs here
		}

		/**
		 *  Pre action tasks needing time, getting things from the server like text should be done here.
		 * There is nothing worse than a widget which has stuff percolating in at random.
		 */
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},  // ready

	
	function loaded(self) {
		// This function is called by the Athena setup.
		self.isloaded = true;
	},  // loaded

	function show(self) {
		self.node.style.visibility = 'visible';
	},  // show

	function hide(self) {
		self.node.style.visibility = 'hidden';
	},  // hide

	/** Generic ErrorBack 
	 * 
	 * @param self is an instance of workspace.Workspace
	 * @param res(string) is an error message.
	 */
	function eb_genericErrback(self, res) {
		var l_node = self.node;
		var l_nodeName = l_node.nodeName;
		var l_obj = l_node.attributes;
		Divmod.debug('---', 'helpers.js - ERROR - attachWidget failed - Node:' + l_nodeName + '  Err:' + res);
		console.log("GenericErrBck - %O", l_node);
	},
	  
	function attachWidget(self, p_name, p_params, p_readyfunc) {
		//Divmod.debug('---', 'attachWidget - ' + p_name + ' is being attached to:' + self.node.className + ', with params:'+ p_params + ', ready_function:' + p_readyfunc);
		var l_defer_1 = self.callRemote(p_name, p_params);
		l_defer_1.addCallback(function liveElementReceived(le) {
			//Divmod.debug('---', 'attachWidget - ' + p_name + ' callRemote' );
			var d2 = self.addChildWidgetFromWidgetInfo(le);
			d2.addCallback(function childAdded(widget) {
				//Divmod.debug('---', 'attachWidget - ' + p_name + ' addChildWidgetFromWidgetInfo');
				self.node.appendChild(widget.node);
				var d3 = widget.ready();
				//Divmod.debug('---', 'attachWidget - ' + p_name + ' widget.ready' );

				function isready() {
					widget.show();
					}  // isready

				if (!p_readyfunc)
					p_readyfunc = isready;
				d3.addCallback(p_readyfunc);
				d3.addErrback(function(res) {  // widget.ready failed
					self.eb_genericErrback(res + ' widget.reay failed for: ' + p_name );
				}
				);
			}  // childAdded
			);
			d2.addErrback(function(res) {  // addChildWidgetFromWidgetInfo failed
				self.eb_genericErrback(res + ' addChildWidgetFromWidgetInfo failed for: ' + p_name);
				}
			);
		}  // liveElementReceived
		);
		l_defer_1.addErrback(function(res) {  // callRemote failed
			self.eb_genericErrback(res + ' callRemote failed for: ' + p_name);
		}
		);
	},
	  
	function detached(self) {
		Divmod.debug('---', self.node.className + ' object was detached cleanly.');
		self.node.parentNode.removeChild(self.node);
		helpers.Widget.upcall(self, 'detached');
	},
	  
	  // DBK Added all widget functions below this line
	  
	function showWidget(self) {
		//Divmod.debug('---', 'helpers.js - Widget is now visible. ' + self.node.className);
		self.node.style.display = 'block';
	},
	  
	function hideWidget(self) {
		//Divmod.debug('---', 'helpers.js - Widget is now hidden. ' + self.node.className);
		self.node.style.display = 'none';
	}
);


/**
 * Page not found widget
 */

helpers.Widget.subclass(helpers, 'FourOfour').methods(

	function ready(self) {

		function widgetready(res) {
			//do whatever init needs here
		}

		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(widgetready);
		return d;
	},

	function show(self) {
		alert('this is a fourOfour Message');
	}
);

// END DBK
