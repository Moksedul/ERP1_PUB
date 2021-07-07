//for search function in options/selections
$(document).ready(function ()
{

    $("#name").select2({});
    $("#company").select2({});


});

//for search menu hide and show
$(document).ready(function(){
	$("#formFields").hide();
	$("#showSearch1").hide();

  	$("#showSearch").click(function()
		{   $("#search-form-container").css("height", "auto");
			$("#formFields").show();
			$("#showSearch").hide();
			$("#showSearch1").show();

		});

	$("#showSearch1").click(function()
		{   $("#search-form-container").css("height", "35px");
			$("#formFields").hide();
			$("#showSearch").show();
			$("#showSearch1").hide();

		});
});
//for search menu hide and show