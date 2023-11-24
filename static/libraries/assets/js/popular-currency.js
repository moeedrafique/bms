// Add wishlist
$(document).on('click',".btn-success",function(){
    var _pid=$(this).attr('data-product');
    console.log(_pid)
    var _vm=$(this);
    // Ajax
    $.ajax({
        url:"/add-wishlist",
        data:{
            product:_pid
        },
        dataType:'json',
        success:function(res){
            if(res.bool==true){
                console.log("True")
                _vm.addClass('disabled').removeClass('btn-success');
            }
        }
    });
    // EndAjax
});
// End