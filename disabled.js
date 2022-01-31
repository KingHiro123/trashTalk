$(function(){
    var usernameValue = $('#item_description').val();
    $('#item_description').change(function(){
        if ($(this).val() != usernameValue){
            $('input.btn-success').prop('disabled', false);
        }
    });
});