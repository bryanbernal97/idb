// console.log('Made it to edit model form')

// Hide form initially

$("#user-name-edit").hide();
$("#user-description-edit").hide();
$("#user-language-edit").hide();
$("#user-views-edit").hide();
$("#user-followers-edit").hide();
$("#user-url-edit").hide();
$("#user-game-edit").hide();
$("#user-created-edit").hide();
$("#user-updated-edit").hide();
$("#user-edit-submit").hide();


var origForm = $('#edit-user-form').serialize();

$("#user-edit-button").click(function(){

	origForm = $('#edit-user-form').serialize();
	// console.log('original form= ' + origForm);

    $("#user-name").hide();
	$("#user-description").hide();
	$("#user-language").hide();
	$("#user-views").hide();
	$("#user-followers").hide();
	$("#user-url").hide();
	$("#user-game").hide();
	$("#user-created").hide();
	$("#user-updated").hide();
	$("#user-edit-button").hide();


    $("#user-name-edit").show();
	$("#user-description-edit").show();
	$("#user-language-edit").show();
	$("#user-views-edit").show();
	$("#user-followers-edit").show();
	$("#user-url-edit").show();
	$("#user-game-edit").show();
	$("#user-created-edit").show();
	$("#user-updated-edit").show();
	$("#user-edit-submit").show();
});

$("#user-edit-submit").click(function() {

	if ($('#edit-user-form').serialize() != origForm) {
		// This is where i will make the call to the backend to update the instance
		// Make the value of the normal fields be the values of the form and alert if the update was a success or failure
		$("#user-name").text($("#user-name-edit").val());
		$("#user-description").text($("#user-description-edit").val());
		$("#user-language").text($("#user-language-edit").val());
		$("#user-views").text($("#user-views-edit").val());
		$("#user-followers").text($("#user-followers-edit").val());
		var userUrl = $("#user-url-edit").val();
		var userUrlHtml = "<a href='" + userUrl + "'>" + userUrl + "</a>";
		$("#user-url").html(userUrlHtml);
		var gameID = $("#user-game-edit").val();
		var gameName = $("#user-game-edit option:selected").text();
		var gameHref = '/games/' + gameID;
		var gameHTML = "<a href='" + gameHref + "'>" + gameName + "</a>";
		$("#user-game").html(gameHTML);
		$("#user-created").text($("#user-created-edit").val());
		$("#user-updated").text($("#user-updated-edit").val());
	} else {
		console.log('Form did not change no need to call API');
	}

	$("#user-name-edit").hide();
	$("#user-description-edit").hide();
	$("#user-language-edit").hide();
	$("#user-views-edit").hide();
	$("#user-followers-edit").hide();
	$("#user-url-edit").hide();
	$("#user-game-edit").hide();
	$("#user-created-edit").hide();
	$("#user-updated-edit").hide();
	$("#user-edit-submit").hide();

	$("#user-name").show();
	$("#user-description").show();
	$("#user-language").show();
	$("#user-views").show();
	$("#user-followers").show();
	$("#user-url").show();
	$("#user-game").show();
	$("#user-created").show();
	$("#user-updated").show();
	$("#user-edit-button").show();
});