// console.log('Made it to edit model form')

// Hide form initially

$("#user-name-edit").hide();
$("#user-description-edit").hide();
$("#user-language-edit").hide();
$("#user-views-edit").hide();
$("#user-followers-edit").hide();
$("#user-url-edit").hide();
$("#user-created-edit").hide();
$("#user-updated-edit").hide();
$("#user-edit-submit").hide();



$("#user-edit-button").click(function(){
    $("#user-name").hide();
	$("#user-description").hide();
	$("#user-language").hide();
	$("#user-views").hide();
	$("#user-followers").hide();
	$("#user-url").hide();
	$("#user-created").hide();
	$("#user-updated").hide();
	$("#user-edit-button").hide();


    $("#user-name-edit").show();
	$("#user-description-edit").show();
	$("#user-language-edit").show();
	$("#user-views-edit").show();
	$("#user-followers-edit").show();
	$("#user-url-edit").show();
	$("#user-created-edit").show();
	$("#user-updated-edit").show();
	$("#user-edit-submit").show();
});

$("#user-edit-submit").click(function() {

	// This is where i will make the call to the backend to update the instance
	// Make the value of the form be the value of the normal fields and alert that the update was a success

	$("#user-name-edit").hide();
	$("#user-description-edit").hide();
	$("#user-language-edit").hide();
	$("#user-views-edit").hide();
	$("#user-followers-edit").hide();
	$("#user-url-edit").hide();
	$("#user-created-edit").hide();
	$("#user-updated-edit").hide();
	$("#user-edit-submit").hide();

	$("#user-name").show();
	$("#user-description").show();
	$("#user-language").show();
	$("#user-views").show();
	$("#user-followers").show();
	$("#user-url").show();
	$("#user-created").show();
	$("#user-updated").show();
	$("#user-edit-button").show();
});