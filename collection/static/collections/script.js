
//for hide and show cheque details
function showChequeDetails() {
  var x = document.getElementById("id_collection_mode").value;
  if (x == "Cheque" || x == "Online" || x == "Pay Order") {
    document.getElementById("demo").style.display = "block";
  }
  else{document.getElementById("demo").style.display = "none";}

}


//for loading image and voucher numbers
$(document).ready(function ()
{
   var $select1 = $('#company'),
       $select2 = $('#id_local_sale_voucher_no'),
       $select3 = $('#id_sale_voucher_no'),
       $options1 = $select2.find('option');
       $options2 = $select3.find('option');
       $select1.on('change',function()
       {
            var url1 = $("#collectionForm").attr("data-vouchers-url2");
            var url2 = $("#collectionForm").attr("data-image-url");
            var url3 = $("#collectionForm").attr("data-vouchers-url1");
            var nameId = $(this).val();
            $.ajax({
                        url: url1,
                        data: {
                          'name': nameId
                        },
                        success: function (data) {
                          $("#id_local_sale_voucher_no").html(data);
                        }
                  });

            $.ajax({
                        url: url3,
                        data: {
                          'name': nameId
                        },
                        success: function (data) {
                          $("#id_sale_voucher_no").html(data);
                        }
                  });

             $.ajax({
                        url: url2,
                        data: {
                          'name': nameId
                        },
                        success: function (data) {
                          $("#person_image").html(data);
                        }
                  });
       }).trigger('change');
});



//for search function in options/selections
$(document).ready(function ()
{   // for collection form
    $("#id_collected_from").select2({});
    $("#company_name").select2({});
    $("#id_sale_voucher_no").select2({});
    $("#id_local_sale_voucher_no").select2({});

    // for collection list
    $("#name").select2({});
    $("#voucher_no").select2({});
    $("#phone_no").select2({});
});

//for search menu hide and show
$(document).ready(function(){
	$("#searchForm").hide();
	$("#showSearch1").hide();

  	$("#showSearch").click(function()
		{   $("#search-form-container").css("height", "auto");
			$("#searchForm").show();
			$("#showSearch").hide();
			$("#showSearch1").show();

		});

	$("#showSearch1").click(function()
		{   $("#search-form-container").css("height", "35px");
			$("#searchForm").hide();
			$("#showSearch").show();
			$("#showSearch1").hide();

		});
});
//for search menu hide and show


//alerts for collection edit and delete
function alertEdit() {
  alert("Can not be edited after Collection Success");
}

function alertDelete() {
  alert("Can not be deleted after Collection Success");
}