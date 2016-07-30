/*
 * @name:      PyHouse/src/Modules/Computer/Web/js/entertainMenu.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2016-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created 07-29-2016
 * @summary:   The entertainment menu
 *
 */

/**
 * The entertainment menu widget.
 *
 */
helpers.Widget.subclass(entertainMenu, 'EntertainmentMenuWidget').methods(

    function __init__(self, node) {
        entertainMenu.EntertainmentMenuWidget.upcall(self, "__init__", node);
    },


	// ============================================================================
    /**
     * Startup - Place the widget in the workspace and hide it.
     * 
     * Override the ready function in C{ helpers.Widget.ready() }
     */
	function ready(self) {
		function cb_widgetready(res) {
			self.hideWidget();
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function startWidget(self) {
		showSelectionButtons(self);
		self.buildLcarSelectScreen();
	}


// END DBK
