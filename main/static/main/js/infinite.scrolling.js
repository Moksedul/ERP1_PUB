

//for activating infinite scrolling
var table = $('.card-body')
var infinite = new Waypoint.Infinite({
	element: $('.infinite-container')[0],
	context: $('.infinite-trigger'),

	offset: 'bottom-in-view',

	onBeforePageLoad: function () {
		$(table).load("{% include 'main/loader.html' %}");
	},
	onAfterPageLoad: function () {
		$( "#loading" ).remove();
	}
});


//for responsive table container height
$(document).ready(function(){
	var bodyHeight = $("body").height();
	var formHeight = $("#search").height() + 13;
	var footerHeight = $('.footer').height();
	var contentHeight = bodyHeight - formHeight - footerHeight;
	console.log(contentHeight);
	$('.table-container').css('height', contentHeight);
});