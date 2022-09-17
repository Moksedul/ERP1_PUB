//responsive table container height
$(document).ready(function(){
	var bodyHeight = $("body").height();
	var footerHeight = $('.footer').height();
	var contentHeight = bodyHeight- footerHeight;
	console.log(contentHeight);
	$('.table-container').css('height', contentHeight);
});
