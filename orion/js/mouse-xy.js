
// Version	1.0.0

onLoad = init();
function init()
{
	if (!document.all)	// not IE
		document.captureEvents(Event.MOUSEMOVE);
	document.onmousemove = handleMouseMove;
}

function handleMouseMove (e)
{
	var mouseX = e ? e.pageX : window.event.clientX;
	var mouseY = e ? e.pageY : window.event.clientY;

	window.status = 'MouseXY=' + mouseX + ',' + mouseY;
	return false;
}







