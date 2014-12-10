/** helpers.js
 *
 * @name: PyHouse/src/Modules/Web/js/helpers.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2012-2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created about 2012
 * @summary: Displays the Internet element
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
		 * Pre action tasks needing time, getting things from the server like text should be done here.
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
	},


	function show(self) {
		self.node.style.visibility = 'visible';
	},


	function hide(self) {
		self.node.style.visibility = 'hidden';
	},


	/** Generic ErrorBack 
	 *
	 * @param self is an instance of workspace.Workspace
	 * @param res(string) is an error message.
	 */
	function eb_genericErrback(self, res) {
		var l_node = self.node;
		var l_nodeName = l_node.nodeName;
		var l_obj = l_node.attributes;
		Divmod.debug('---', 'helpers.js - ERROR - attachWidget failed - Node:' + l_nodeName + '  ERROR = ' + res);
		console.log("GenericErrBck - %O", l_node);
	},


	/**
	 * Do the things that a widget requests when it becomes ready.
	 * <This was originally embedded in attachWidget>
	 *
	 * @param p_widget is the widget being added/started.
	 * @param p_readyfunc is the optional function to be called when the widget is done loading (and initializing?)
	 */
	function widget_ready(self, p_widget, p_readyfunc) {
		// Default readyfunc that shows the widget.
		function isready() {
			p_widget.show();
		}
		// If we did not call with a readyfunc, add a dummy function that is ready
		if (!p_readyfunc)
			p_readyfunc = isready;
		function eb_widget_ready(p_reason) {  // widget.ready failed
			self.eb_genericErrback('widget.ready failed for: ' + p_widget.node.className + ' - ' + p_reason);
		}
		// console.log("helpers.widget_ready()  p_widget  %O", p_widget);
		var l_defer = p_widget.ready();
		l_defer.addCallback(p_readyfunc);
		l_defer.addErrback(eb_widget_ready);
	},

	function attachWidget(self, p_name, p_params, p_readyfunc) {
		// Divmod.debug('---', 'attachWidget - "' + p_name + '" is being attached to:' + self.node.className + ', with params:'+ p_params);

		function cb_call_remote(le) {
		}
		function eb_call_remote(p_reason) {
			self.eb_genericErrback('Error: ' + p_reason + ' in callRemote failed for Name: ' + p_name);
		}
		var l_defer_1 = self.callRemote(p_name, p_params);

		function liveElementReceived(le) {

			function cb_childAdded(widget) {
				self.node.appendChild(widget.node);
				self.widget_ready(widget, p_readyfunc);
			}

			function eb_add_child(p_reason) {  // addChildWidgetFromWidgetInfo failed
				self.eb_genericErrback('Error: ' + p_reason + ' in addChildWidgetFromWidgetInfo failed for Name: ' + p_name);
			}

			var l_defer_2 = self.addChildWidgetFromWidgetInfo(le);
			l_defer_2.addCallback(cb_childAdded);
			l_defer_2.addErrback(eb_add_child);
		}  // liveElementReceived
		l_defer_1.addCallback(liveElementReceived);
		l_defer_1.addErrback(eb_call_remote);
	},


	function WORKS_attachWidget(self, p_name, p_params, p_readyfunc) {
		Divmod.debug('---', 'attachWidget - "' + p_name + '" is being attached to:' + self.node.className + ', with params:'+ p_params + ', ready_function:' + p_readyfunc);

		function cb_call_remote(le) {
		}
		function eb_call_remote(p_reason) {
			self.eb_genericErrback('Error: ' + p_reason + ' in addChildWidgetFromWidgetInfo failed for Name: ' + p_name);
		}
		var l_defer_1 = self.callRemote(p_name, p_params);

		l_defer_1.addCallback(function liveElementReceived(le) {
			var l_defer_2 = self.addChildWidgetFromWidgetInfo(le);
			l_defer_2.addCallback(function childAdded(widget) {
				self.node.appendChild(widget.node);
				var l_defer_3 = widget.ready();

				// Default readyfunc that shows the widget.
				function isready() {
					widget.show();
				}

				// If we did not call with a readyfunc, add a dummy function that is ready
				if (!p_readyfunc)
					p_readyfunc = isready;

				l_defer_3.addCallback(p_readyfunc);
				l_defer_3.addErrback(function(p_reason) {  // widget.ready failed
					self.eb_genericErrback(p_reason + ' widget.ready failed for: ' + p_name );
					}
					);
				}  // childAdded
			); // add callback to d2
			function eb_add_child(p_reason) {  // addChildWidgetFromWidgetInfo failed
				self.eb_genericErrback('Error: ' + p_reason + ' in addChildWidgetFromWidgetInfo failed for Name: ' + p_name);
				}
			l_defer_2.addErrback(function(p_reason) {  // addChildWidgetFromWidgetInfo failed
				self.eb_genericErrback('Error: ' + p_reason + ' in addChildWidgetFromWidgetInfo failed for Name: ' + p_name);
				}
			);
		}  // liveElementReceived
		);
		l_defer_1.addErrback(function(p_reason) {  // callRemote failed
			self.eb_genericErrback('Error: ' + p_reason + ' in callRemote failed for Name: ' + p_name);
			}
		);
	},


	function detached(self) {
		Divmod.debug('---', self.node.className + ' object was detached cleanly.');
		self.node.parentNode.removeChild(self.node);
		helpers.Widget.upcall(self, 'detached');
	},


	// DBK Added all widget functions below this line ----------------

	function showWidget(self, p_className) {
		// Divmod.debug('---', 'helpers.showWidget(1) was called for ' + p_className);
		// console.log("helpers.showWidget(1)  Self:  %O", self);
		self.node.style.display = 'none';
		var l_widget = findWidgetByClass(p_className);
		// console.log("helpers.showWidget(2)  l_widget:  %O", l_widget);
		l_widget.node.style.display = 'block';
		// Divmod.debug('---', 'helpers.showWidget(5) was called for ' + p_className);
		showSelectionButtons(l_widget);
		// Divmod.debug('---', 'helpers.showWidget(6) was called for ' + p_className);
		l_widget.startWidget();
	},
	function hideWidget(self) {
		// Divmod.debug('---', 'helpers.hideWidget() was called.');
		// console.log("helpers.hideWidget()  Self:  %O", self);
		self.node.style.display = 'none';
	},
	function startWidget(self) {
		// Divmod.debug('---', 'helpers.startWidget() was called.');
		// console.log("helpers.startWidget()  Self:  %O", self);
		self.node.style.display = 'block';
		showSelectionButtons(self);
		self.fetchDataFromServer();
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
		//alert('this is a fourOfour Message');
	}
);
// console.log("helpers.handleDataOnClick()  json  %O", l_json);
// Divmod.debug('---', 'helpers.handleDataOnClick(Change) was called. JSON:' + l_json);
// END DBK
