$(document).ready(function(){

    // Phone masking
    $('#phone_number').mask('(9999) 999-9999', {placeholder:'x'});
    $('#id_card_no').mask('99999-9999999-9', {placeholder:'_'});

    // Validation
    $( "#j-pro" ).justFormsPro({
        rules: {
            name: {
                required: true
            },
            id_card_no: {
                required: true
            },
            country: {
                required: true
            },
            phone_number: {
                required: true
            },
            house_address: {
                required: true
            },
            email: {
                required: false
            },
        },
        messages: {
            name: {
                required: "Add customer name"
            },
            phone_number: {
                required: "Add customer phone"
            },
            id_card_no: {
                required: "Add customer cnic no"
            },
            country: {
                required: "Add customer nationality"
            },
            house_address: {
                required: "Add customer address"
            },
            email: {
                required: "Add customer email"
            },
        },
        debug: false
    });
});