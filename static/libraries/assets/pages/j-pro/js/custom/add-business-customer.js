$(document).ready(function(){

    // Phone masking
    $('#phone_number').mask('+99-99999-99999', {placeholder:'x'});
    $('#id_card_no').mask('99999-9999999-9', {placeholder:'_'});

    // Validation
    $( "#j-pro" ).justFormsPro({
        rules: {
            name: {
                required: true
            },
            cea_id_no: {
                required: false
            },
            phone_number: {
                required: true
            },
            address: {
                required: true
            },
            email: {
                required: false
            },
        },
        messages: {
            name: {
                required: "Add business customer name"
            },
            phone_number: {
                required: "Add business customer phone"
            },
            cea_id_no: {
                required: "Add business customer cea reg no"
            },
            address: {
                required: "Add business customer address"
            },
            email: {
                required: "Add business customer email"
            },
        },
        debug: false
    });
});