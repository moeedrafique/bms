$(document).ready(function(){

    // Phone masking
    $('#phone_number').mask('(9999) 999-9999', {placeholder:'x'});
    $('#landline').mask('(9999) 999-9999', {placeholder:'x'});
    $('#id_card_no').mask('99999-9999999-9', {placeholder:'_'});

    // Validation
    $( "#j-pro" ).justFormsPro({
        rules: {
            name_of_shop: {
                required: true
            },
            shop_address: {
                required: true
            },
            phone_number1: {
                required: true
            },
            phone_number2: {
                required: true
            },
            landline1: {
                required: true
            },
            landline2: {
                required: true
            },
            shop_logo: {
                validate: true,
                required: false,
                size: 2,
                extension: "jpg|jpeg|png|gif"
            }
        },
        messages: {
            name_of_shop: {
                required: "Add your shop name"
            },
            phone_number1: {
                required: "Add your phone"
            },
            phone_number2: {
                required: "Add your phone"
            },
            landline1: {
                required: "Add your landline no"
            },
            landline2: {
                required: "Add your landline no"
            },
            shop_address: {
                required: "Add your address"
            },
            shop_logo: {
                size_extension: "File types: jpg/jpeg/png/gif. Size: 2Mb"
            }
        },
        debug: true
    });
});