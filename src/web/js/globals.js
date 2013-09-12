/**
 * globals.js - the global hook where we hang our coat and everything else
 * 
 * A not so impressive way to get dynamic modules loading properly when inserting fragments at some later time into the webapp.
 * The most promising way is to preload although this could lead to quite some code clutter,
 *  but knowing that the clients do not unload JS means at least preloading does no harm.
 *  
 *  modulesWaiting = {};
 *  
 *  function moduleLoaded(module) {
 *      modulesWaiting[module] = null;
 *      Divmod.debug("moduleLoaded", "loaded module: " + module);
 *  }
 *  
 *  function waitForModules(module, f) {
 *      modulesWaiting[module] = f;
 *      for (var m in modulesWaiting) {
 *          if (modulesWaiting[m])
 *              modulesWaiting[m]();
 *      }
 *  }
 *
 */


// import Divmod.Runtime

// import helpers


var REQ_404 = -1;
var REQ_ROOT = 0;
var REQ_WITHID = 2;

globals = {
	fonts : [ 'Verdana', 'Arial', 'Helvetica', 'sans-serif' ],
	workspace : null,

	__init__ : function() {
		globals.appLoaded = false;
		globals.center = {
			x : 400,
			y : 280
		};
		globals.tsize = {
			w : 800,
			h : 655
		};
	}  // __init__
};  // globals

function int2str(i) {
	if (i < 10)
		return '0' + String(i);
	else
		return String(i);
}  // int2str

function getCardSizefromCSS() {
	var s;
	var size;
	var w = 0;
	var h = 0;
	var n = 0;
	var done = false;
	while (!done) {
		var rules = getCSSrules(n);
		if (rules === null)
			break;
		for ( var i = 0; i < rules.length; i++) {
			if (/\.cardsize/.test(rules[i].selectorText)) {
				size = rules[i].style.width;
				if ((size != 'none') && (size.length > 0)) {
					s = /^(\d*)(px)/.exec(size);
					if (s)
						w = parseInt(s[1], 10);
					else
						w = 0;
				}
				size = rules[i].style.maxHeight;
				if ((size != 'none') && (size.length > 0)) {
					s = /^(\d*)(px)/.exec(size);
					if (s)
						h = parseInt(s[1], 10);
					else
						h = 0;
				}
				done = true;
				break;
			}
		}
		n++;
	}
	return {
		w : w,
		h : h
	};
}  // getCardSizefromCSS

function collectClasses(node) {
	var classnames = [];
	var nodes = getElementsByTagAndClassName('div', null, node);  // (tagname, classname, parent)

	for ( var i = 0; i < nodes.length; i++) {
		if (nodes[i].className !== null) {
			classnames.push('.' + nodes[i].className);
		}
	}
	return classnames;
}  // collectClasses


/**
 * Collects all the URIs present in img tags in within this node.
 * If the imgs array is passed into the function all found URIs are appended to the array, which can
 *  be passed later on to the loadImages function, which preloads all those images.
 */
function collectIMG_src(node, imgs) {
	if (imgs != typeof ([])) {
		imgs = [];
	}
	var nodes = Divmod.Runtime.theRuntime.getElementsByTagNameShallow(node, 'img');
	for ( var i = 0; i < nodes.length; i++) {
		var src = nodes[i].src;
		imgs.push(src);
	}
	return imgs;
}  // CollectIMG_src

function getCSSrules(n) {
	if (n < document.styleSheets.length) {
		if (document.styleSheets[0].rules) {
			return document.styleSheets[n].rules; // IE
		} else {
			return document.styleSheets[n].cssRules; // Mozilla
		}
	}
	return null;
}  // getCSSrules

/**
 * Collects all URIs in the present CSS which refer to images, thus allowing for the loadImages
 *  function to check for all images present in a browser neutral way.
 * 
 * If passed null the function creates an empty array of URIs and starts collecting them.
 * This allows for having an images array beforehand and adding other images (from offsite URIs) to the array manually.
 */
function collectCSS_backgroundImages(imgs, selectors) {
	if (imgs === null) {
		imgs = [];
	}

	function addURI(uri) {
		for ( var j = 0; j < imgs.length; j++) {
			if (uri == imgs[j])
				return;
		}
		imgs.push(uri);
	}  // addURI

	function matchSelectors(sel, sels) {
		if (sels === null)
			return true;

		for ( var i = 0; i < sels.length; i++) {
			if (sels[i] == sel)
				return true;
		}
		return false;
	}  // matchSelectors

	var n = 0;
	while (true) {
		var rules = getCSSrules(n);
		if (rules === null)
			break;
		for ( var i = 0; i < rules.length; i++) {
			if (matchSelectors(rules[i].selectorText, selectors)) {
				var uri = rules[i].style.backgroundImage;
				if ((uri != 'none') && (uri.length > 0)) {
					var u = /^url\((.*)\)$/.exec(uri);
					if (u) {
						addURI(u[1]); // Safari has rather strange ideas of URIs in CSS
					}
				}
			}
		}
		n++;
	}
	return imgs;
}  // collectCSS_backgroundImages


/* DBK - unused so far.
 * 
 * Given a bunch of flags this function will sit and wait until all flags go to true.
 * If this happens callback is called, if not after some time the errback will be triggered.
 */
globals.TimeoutError = Divmod.Error.subclass('globals.TimeoutError');

function waitfor(flags, timeout) {
	function flagstrue() {
		for ( var i = 0; i < flags.length; i++) {
			if (!flags[i])
				return false;
		}
		return true;
	}

	var stepcount = 0;
	var steprate = 2; // checks per second
	var waitDeferred = Divmod.Defer.Deferred();
	var checkStep = function() {
		if (stepcount > (timeout * steprate)) {
			self.timer = null;
			// waitDeferred.errback(minimal.common.globals.TimeoutError('timeout...'));
			waitDeferred.errback(globals.TimeoutError('timeout...'));
		} else if (flagstrue()) {
			waitDeferred.callback();
		} else {
			stepcount++;
			self.timer = setTimeout(checkStep, 1000 / steprate);
		}
	};  // checkStep

	self.timer = setTimeout(checkStep, 1000 / steprate);
	return waitDeferred;
}  // waitfor


/**
 * Load image URIs
 */
globals.ImageLoadingError = Divmod.Error.subclass('globals.ImageLoadingError');

/**
 * Load Images
 */
function loadImages(uris) {
	var imgs = [];
	for ( var i = 0; i < uris.length; i++) {
		var img = new Image();
		img.src = uris[i];
		imgs.push(img);
	}  // for loop

	/**
	 * 
	 * @param img
	 * @returns {Boolean}
	 */
	function isImageOk(img) {
		if (!img.complete) {
			return false;
		}
		if (typeof img.naturalWidth != "undefined" && img.naturalWidth === 0) {
			return false;
		}
		return true;
	}  // isImageOK

	/**
	 * 
	 * @returns {Boolean} true if all images are loaded
	 */
	function imgsloaded() {
		for ( var i = 0; i < imgs.length; i++) {
			if (!isImageOk(imgs[i]))
				return false;
		}
		return true;
	}  // imgsloaded

	/**
	 * List the images that have not loaded.
	 * 
	 * @returns {String}
	 */
	function imgsNotloaded() {
		var estr = '';
		for ( var i = 0; i < imgs.length; i++) {
			if (!isImageOk(imgs[i])) {
				if (estr.length > 0)
					estr += '; ';
				estr = estr + imgs[i].src;
			}
		}
		return estr;
	}  // imgsNotloaded

	var stepcount = 0;
	var steprate = 2; // checks per second
	var readyDeferred = Divmod.Defer.Deferred();

	var checkStep = function() {
		if ((stepcount > 120)) {
			self.timer = null;
			// readyDeferred.errback(new minimal.common.globals.ImageLoadingError(
			readyDeferred.errback(new globals.ImageLoadingError(
					'could not load all images: ' + imgsNotloaded()));
		} else if (imgsloaded()) {
			readyDeferred.callback();
		} else {
			stepcount++;
			self.timer = setTimeout(checkStep, 1000 / steprate);
		}
	};  // checkStep

	self.timer = setTimeout(checkStep, 1000 / steprate);
	return readyDeferred;
}  // loadImages


/**
 * 
 */
Divmod.Runtime.theRuntime.addLoadEvent(
	function appStartup() {
		globals.workspace.appStartup();
	}
);

// END DBK
