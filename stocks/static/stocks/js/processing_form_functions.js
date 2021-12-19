
$(document).ready(function ()
{
    var totalForms = $('#id_{{formset_name}}-TOTAL_FORMS').val(); // for getting total forms number

      for (let i = 0; i < totalForms; i++) {
                $("#id_{{formset_name}}-"+ i +"-product").select2({}); // for enable search in product selection
            }
    $("#id_business_name").select2({}); // for select options search
    
    // for adding add button to last item
   var addMore = $('#add_more')
   var productTitle = $('.product')
   var lastProductTitle = productTitle[productTitle.length-2] // getting las product box
   $(lastProductTitle).append(addMore)

});


// add new empty form for product
$('#add_more').click(function() {
    var form_idx = $('#id_{{formset_name}}-TOTAL_FORMS').val(); // "formset_name" came from context of django view
    $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx)); // replace id prefix of empty form
    $('#id_{{formset_name}}-TOTAL_FORMS').val(parseInt(form_idx) + 1); // changing total number of forms
    var id = "#id_{{formset_name}}-" + form_idx + "-product" // getting the new id of product selection
    $(id).select2({}); // for select options search

    // for creating new title of product box
    var productTitle = $('.product')
    var lastProductTitle = productTitle[productTitle.length-2]
    var textProduct = 'Product-'  + (productTitle.length-1)
    $(lastProductTitle).text(textProduct);
    $(lastProductTitle).append(this)

});


// for complete the post_product and add to finishing stock
function completeProcessing(productID) // this function will be called when "Complete" button will be clicked
{   
    var productID = productID - 1;
    var postStockId = '#id_poststock_set-' +  productID  + '-id';
    var postStock = $(postStockId).val();
    console.log(postStock);
    window.location.href = '/complete_processing/{{processing_stock.id}}/'+postStock+'';
}



// for disable all fields of completed "post_stocks"
$(document).ready(function(){

    var formset = $('.form_set');

    $(formset).each(function(i, obj) {
        var postStockId = '#id_poststock_set-' +  i  + '-id';
        var postStock = $(postStockId).val();
        var isCompleted = false;

        $.ajax({
                url: '/is_completed',
                data: {
                        'post_stock': postStock
                    },
                success: function(response) {
                    isCompleted = response.is_completed;
                    if (isCompleted){
                completeButtonID = i+1
                $(obj).find("input").attr("readonly", true);
                $(obj).find("input").attr("disabled", true);
                $(obj).find("select").attr("readonly", true);
                $(obj).find("select").attr("disabled", true);
                $(obj).find('#complete-'+ completeButtonID +'').remove();
                    }

                },
                failure: function(data) { 
                    alert('Got an error dude');
                }
            }); 

    });
});

// for re-enabled all fields of completed "post_stocks" otherwise new product will not be added
$('#form_submit').click(function() {
    $('#form_set').find("input").attr("readonly", false);
    $('#form_set').find("input").attr("disabled", false);
    $('#form_set').find("select").attr("readonly", false);
    $('#form_set').find("select").attr("disabled", false);

});
