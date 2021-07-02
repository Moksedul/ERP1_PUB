
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
   var $select1 = $('#id_collected_from'),
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
{
    $("#id_collected_from").select2({});
    $("#id_collection_to_account").select2({});
    $("#id_sale_voucher_no").select2({});
    $("#id_local_sale_voucher_no").select2({});
});