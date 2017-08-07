
// Version	2.0.0

// var ss_trackingScript = 'http://localhost/~stonestreem.com/cgi-bin/track.cgi';
var ss_trackingScript = 'http://stonestreem.com/cgi-bin/track.cgi';

var ss_trackURL = ss_trackingScript + '?' + document.referrer;
document.writeln ('<script type="text/javascript" src="' + ss_trackURL + '"></script>');


onclick = clickTrace;				// route all click events
function clickTrace(e)
{
	var trackURL = "";

	if (!e) 
	{ 
		var e = window.event;		// IE
		var elmClick = e.srcElement;
		var mouseX = window.event.clientX;
		var mouseY = window.event.clientY;
	}
	else
	{ 
		var elmClick = e.target;	// FF
		var mouseX = e.pageX;
		var mouseY = e.pageY;
	}

	trackURL = ss_trackingScript + '?OnClick=' + elmClick + elmClick.nodeName + '&MouseXY=' + mouseX + ',' + mouseY;

	ss_img = new Image();
	ss_img.src = trackURL;

	return true;				// pass back to originating object
}


onunload = unloadTrace;				// route the unload events
function unloadTrace()
{
	var trackURL = "";

	trackURL = ss_trackingScript + '?OnUnload=TRUE';

	ss_img = new Image();
	ss_img.src = trackURL;

	return true;				// pass back to originating object
}


