$(document).ready(function(){

			// Phone masking
			$('#phone_number').mask('(9999) 999-9999', {placeholder:'x'});
			$('#landline').mask('(9999) 999-9999', {placeholder:'x'});
			$('#id_card_no').mask('99999-9999999-9', {placeholder:'_'});

			// Validation
			$( "#j-pro" ).justFormsPro({
				rules: {
					first_name: {
						required: true
					},
					last_name: {
						required: true
					},
					email: {
						required: true,
						email: true
					},
					phone_number: {
						required: true
					},
					emergency_contact: {
						required: true
					},
					username: {
						required: true
					},
					password: {
						required: true
					},
					id_card_no: {
						required: true
					},
					dob: {
						required: true
					},
					nationality: {
						required: true
					},
					city: {
						required: true
					},
					postal_code: {
						required: true
					},
					house_address: {
						required: true
					},
					position: {
						required: true
					},
					medical_history: {
						required: false
					},
					profile_pic: {
						validate: true,
						required: false,
						size: 2,
						extension: "jpg|jpeg|png|gif"
					}
				},
				messages: {
					first_name: {
						required: "Add your first name"
					},
					last_name: {
						required: "Add your last name"
					},
					email: {
						required: "Add your email",
						email: "Incorrect email format"
					},
					phone_number: {
						required: "Add your phone"
					},
					emergency_contact: {
						required: "Add your emergency contact no"
					},
					username: {
						required: "Add your username"
					},
					password: {
						required: "Add your password"
					},
					id_card_no: {
						required: "Add your cnic no"
					},
					dob: {
						required: "Add your date of birth"
					},
					nationality: {
						required: "Select your country"
					},
					city: {
						required: "Add your city"
					},
					postal_code: {
						required: "Add your postal code"
					},
					house_address: {
						required: "Add your address"
					},
					position: {
						required: "Select desired position"
					},
					medical_history: {
						required: "Add your message"
					},
					profile_pic: {
						size_extension: "File types: jpg/jpeg/png/gif. Size: 2Mb"
					}
				},
				formRedirect: {
					redirect: true,
					address: "http://127.0.0.1:8000/admin-dashboard/"
				},
				debug: false
			});
		});