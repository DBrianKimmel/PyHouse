// helpers.js

// import Nevow.Athena

/* This basic widget can attach subwidgets and provides some other basic functionality.
 */

Nevow.Athena.Widget.subclass(helpers, 'Widget').methods(
		
	function __init__(self, node) {
		helpers.Widget.upcall(self, '__init__', node);
	},  // __init__

	/* Special attention should be paid to the function ready which should be overridden in almost every case,
	 *  working with the widgetready function in a closure.
	 *  
	 * widgetready could of call another method func in the class but practice shows, that the point of being informed that
	 *  we're setup properly for action is way to important to delegate it into superclass.
	 *  
	 * Think of ready as a stub, which is more like a template to start work on your own widgets implementation.
	 */
	function ready(self) {

		function cb_widgetready(res) {
			//do whatever init needs here
		}

		/* Pre action tasks needing time, getting things from the server like texts should be done here.
		 * There is nothing worse as a widget which has stuff percolating in at random.
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

	function eb_genericErrback(self, res) {
		alert('helpers.Widget() - widget injection failed - ' + res + '  ' + self.node.caller);
	},  // eb_genericErrback
	  
	function attachWidget(self, p_name, p_params, readyfunc) {
		//Divmod.debug('---', self.node.className + ' object is bring attached.  '+ p_name );
		Divmod.debug('---', 'Object:' + p_name + ' is being attached to ' + self.node.className + ' with params:'+ p_params + ' ' + readyfunc );
		var d1 = self.callRemote(p_name, p_params);
		d1.addCallback(function liveElementReceived(le) {
			Divmod.debug('---', 'Object d1:' + p_name + ' 2' );
			var d2 = self.addChildWidgetFromWidgetInfo(le);
			d2.addCallback(function childAdded(widget) {
				Divmod.debug('---', 'Object d2:' + p_name + ' 3' );
				self.node.appendChild(widget.node);
				var d3 = widget.ready();
				//Divmod.debug('---', 'Object d3:' + p_name + ' 4' );

				function isready() {
					widget.show();
					}  // isready

				if (!readyfunc)
					readyfunc = isready;
				d3.addCallback(readyfunc);
				d3.addErrback(function(res) {
					self.eb_genericErrback(res);
				}
				);
			}  // childAdded
			);
			d2.addErrback(function(res) {
				self.eb_genericErrback(res);
				}
			);
		}  // liveElementReceived
		);
		d1.addErrback(function(res) {
			self.eb_genericErrback(res);
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
