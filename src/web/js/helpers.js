// helpers.js

// import Nevow.Athena

/**
 * This basic widget can attach subwidgets and provides some other basic functionality.
 */

Nevow.Athena.Widget.subclass(helpers, 'Widget').methods(
		
	function __init__(self, node) {
		helpers.Widget.upcall(self, '__init__', node);
	},  // __init__

	/**
	 *  Special attention should be paid to the function C{ready} which should be overridden in almost every case,
	 *  working with the C{widgetready} function in a closure.
	 *  
	 * C{widgetready} could of call another method C{func} in the class but practice shows, that the point of being informed that
	 *  we're setup properly for action is way too important to delegate it into superclass.
	 *  
	 * Think of C{ready} as a stub, which is more like a template to start work on your own widgets implementation.
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
		var d = loadImages(uris);
		d.addCallback(cb_widgetready);
		return d;
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

	/**
	 * 
	 * @param self is an istannce of workspace.Workspace
	 * @param res(string) is an error message.
	 */
	function eb_genericErrback(self, res) {
		var l_node = self.node;
		var l_nodeName = l_node.nodeName;
		var l_obj = l_node.attributes.item(0);
		var l_keys = self.node.attributes.item(0);
		var l_name = Object.keys(l_keys);
		var l_info = l_node;
		Divmod.debug('---', 'helpers.Widget() - widget injection failed - ' + res + '  ' + l_nodeName + '  ' + self);
	},  // eb_genericErrback
	  
	function attachWidget(self, p_name, p_params, p_readyfunc) {
		Divmod.debug('---', 'attachWidget - ' + p_name + ' is being attached to:' + self.node.className + ', with params:'+ p_params + ', ready_function:' + p_readyfunc );
		var d1 = self.callRemote(p_name, p_params);
		d1.addCallback(function liveElementReceived(le) {
			//Divmod.debug('---', 'attachWidget - Object d1 - callRemote ' + p_name + ' 2' );
			var d2 = self.addChildWidgetFromWidgetInfo(le);
			d2.addCallback(function childAdded(widget) {
				Divmod.debug('---', 'attachWidget - Object d2 - addChildWidgetFromWidgetInfo :' + p_name + ' 3 ' + widget);
				self.node.appendChild(widget.node);
				var d3 = widget.ready();
				Divmod.debug('---', 'attachWidget - Object d3 widget.ready :' + p_name + ' 4' );

				function isready() {
					widget.show();
					}  // isready

				if (!p_readyfunc)
					p_readyfunc = isready;
				d3.addCallback(p_readyfunc);
				d3.addErrback(function(res) {  // widget.ready failed
					self.eb_genericErrback(res + ' d3 ' + widget );
				}
				);
			}  // childAdded
			);
			d2.addErrback(function(res) {  // addChildWidgetFromWidgetInfo failed
				self.eb_genericErrback(res + ' d2 failed ');
				}
			);
		}  // liveElementReceived
		);
		d1.addErrback(function(res) {  // callRemote failed
			self.eb_genericErrback(res + ' d1 (callRemote failed ');
		}
		);
	  },  // attatchWidget
	  
	  function detached(self) {
		  Divmod.debug('---', self.node.className + ' object was detached cleanly.');
		  self.node.parentNode.removeChild(self.node);
		  helpers.Widget.upcall(self, 'detached');
	  }  // detached
);


helpers.Widget.subclass(helpers, 'FourOfour').methods(

	function ready(self) {

		function widgetready(res) {
			//do whatever init needs here
		}

		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(widgetready);
		return d;
	},  // ready

	function show(self) {
		alert('this is a fourOfour Message');
	}  // show
);

// END DBK
