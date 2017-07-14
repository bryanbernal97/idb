$(document).ready(function() {

	// Here first get the contents of the div with name class copy-fields and add it to after "after-add-more" div class.
	$(".add-more-genre").click(function(){ 
		var html = $(".copy-genre-fields").html();

		// Get the current value of the textbox with add button
		var currentVal = $(".before-add-more-genres input").val();

		// Only need to add another text box if there is something in the current text box
		if (currentVal != "") {
			// Move the value to the new element with remove button
			var newHtml = html.replace(/value=".*?"/, 'value="' + currentVal + '"');
			// var newHtml = html.replace('value="*"', 'value="' + currentVal + '"');

			var actualHtml = '<div class="copy-genre-fields">' + newHtml + '</div>';


			// Reset value of textbox with add button
			$(".before-add-more-genres input").val("");

			$(".before-add-more-genres").before(actualHtml);
		}

		
	});
	  
	// Here it will remove the current value of the remove button which has been pressed
	$("body").on("click",".remove-genre",function(){ 
		var outer = $(this).parents(".copy-genre-fields");
		// console.log(outer.children("br"));
		outer.children("br").remove();
		$(this).parents(".control-group").remove();
	});


	// Here first get the contents of the div with name class copy-fields and add it to after "after-add-more" div class.
	$(".add-more-platform").click(function(){ 
		var html = $(".copy-platform-fields").html();
		
		// Get the current value of the textbox with add button
		var currentVal = $(".before-add-more-platforms input").val();

		// Only need to add another text box if there is something in the current text box
		if (currentVal != "") {
			// Move the value to the new element with remove button
			var newHtml = html.replace(/value=".*?"/, 'value="' + currentVal + '"');
			// var newHtml = html.replace('value="(*)"', 'value="' + currentVal + '"');

			var actualHtml = '<div class="copy-platform-fields">' + newHtml + '</div>';

			// Reset value of textbox with add button
			$(".before-add-more-platforms input").val("");

			$(".before-add-more-platforms").before(actualHtml);
		}
	});
	  
	// Here it will remove the current value of the remove button which has been pressed
	$("body").on("click",".remove-platform",function(){ 
		// console.log("This on remove click: " + $(this).parents(".copy-platform-fields").html());
		var outer = $(this).parents(".copy-platform-fields");
		// console.log(outer.children("br"));
		outer.children("br").remove();
		// console.log("This parents on remove click: " + $(this).parents(".control-group").parents(".copy-platform-fields").children("br").html());
		$(this).parents(".control-group").remove();
	});





	// Hide form initially
	$("#game-name-edit").hide();
	$("#game-description-edit").hide();
	$("#game-rating-edit").hide();
	$("#game-genres-edit").hide();
	$("#game-platforms-edit").hide();
	$("#game-release-date-edit").hide();
	$("#game-streamers-edit").hide();
	$("#game-teams-edit").hide();
	$("#game-communities-edit").hide();
	$("#game-edit-submit").hide();
 


	// // Make sure cannot select None and other streamers for multi select on game edit form
	// $('#game-streamers-edit select').change(function() {
	// 	if ($('option:first', this).is(':selected')) {
	// 		$('option:not(:first)', this).prop('selected', false);
	// 	}
	// 	$(this).selectpicker('refresh');
	// });


	// // Make sure cannot select None and other teams for multi select on game edit form
	// $('#game-teams-edit select').change(function() {
	// 	if ($('option:first', this).is(':selected')) {
	// 		$('option:not(:first)', this).prop('selected', false);
	// 	}
	// 	$(this).selectpicker('refresh');
	// });


	// // Make sure cannot select None and other communities for multi select on game edit form
	// $('#game-communities-edit select').change(function() {
	// 	if ($('option:first', this).is(':selected')) {
	// 		$('option:not(:first)', this).prop('selected', false);
	// 	}
	// 	$(this).selectpicker('refresh');
	// });


	var origForm = $('#edit-game-form').serialize();


	$("#game-edit-button").click(function(){

		origForm = $('#edit-game-form').serialize();

		$("#game-name").hide();
		$("#game-description").hide();
		$("#game-rating").hide();
		$("#game-genres").hide();
		$("#game-platforms").hide();
		$("#game-release-date").hide();
		$("#game-streamers").hide();
		$("#game-teams").hide();
		$("#game-communities").hide();
		$("#game-edit-button").hide();


		$("#game-name-edit").show();
		$("#game-description-edit").show();
		$("#game-rating-edit").show();
		$("#game-genres-edit").show();
		$("#game-platforms-edit").show();
		$("#game-release-date-edit").show();
		$("#game-streamers-edit").show();
		$("#game-teams-edit").show();
		$("#game-communities-edit").show();
		$("#game-edit-submit").show();
	});


	$("#game-edit-submit").click(function() {

		if ($('#edit-game-form').serialize() != origForm) {
			// This is where i will make the call to the backend to update the instance
			// Make the value of the normal fields be the values of the form and alert if the update was a success or failure
			$("#game-name").text($("#game-name-edit").val());
			$("#game-description").text($("#game-description-edit").val());

			$("#game-rating").text($("#game-rating-edit").val());

			var genresHtml = "";
			$('input[name="genres[]"]').each(function() {
				genre = $(this).val();
				if (genre != '') {
					genresHtml += "<br>" + $(this).val();
				}
			});
			if (genresHtml == "") {
				genresHtml = "<br>None";
			}
			$("#game-genres").html(genresHtml);

			var platformsHtml = "";
			$('input[name="platforms[]"]').each(function() {
				platform = $(this).val();
				if (platform != "") {
					platformsHtml += "<br>" + $(this).val();
				}
			});
			if (platformsHtml == "") {
				platformsHtml = "<br>None";
			}
			$("#game-platforms").html(platformsHtml);


			$("#game-release-date").text($("#game-release-date-edit").val());

			// Game streamer links formatting
			var streamersHTML = "";
			$("#game-streamers-edit option:selected").each(function () {
				console.log('Inside options for streamers');
				var $this = $(this);
				var streamerID = $this.val();
				var streamerName = $this.text();
				var streamerHref = '/users/' + streamerID;
				var streamerHTML = "<a href='" + streamerHref + "'><br />" + streamerName + "</a>";
				streamersHTML += streamerHTML;
			});
			if (streamersHTML == "") {
				streamersHTML = "<br>None";
			}
			$("#game-streamers").html(streamersHTML);

			// Game team links formatting
			var teamsHTML = "";
			$("#game-teams-edit option:selected").each(function () {
				var $this = $(this);
				var teamID = $this.val();
				var teamName = $this.text();
				var teamHref = '/teams/' + teamID;
				var teamHTML = "<a href='" + teamHref + "'><br />" + teamName + "</a>";
				teamsHTML += teamHTML;
			});
			if (teamsHTML == "") {
				teamsHTML = "<br>None";
			}
			$("#game-teams").html(teamsHTML);

			// Game community links formatting
			var communitiesHTML = "";
			$("#game-communities-edit option:selected").each(function () {
				var $this = $(this);
				var communityID = $this.val();
				var communityName = $this.text();
				var communityHref = '/communities/' + communityID;
				var communityHTML = "<a href='" + communityHref + "'><br />" + communityName + "</a>";
				communitiesHTML += communityHTML;
			});
			if (communitiesHTML == "") {
				communitiesHTML = "<br>None";
			}
			$("#game-communities").html(communitiesHTML);
		}

		$("#game-name-edit").hide();
		$("#game-description-edit").hide();
		$("#game-rating-edit").hide();
		$("#game-genres-edit").hide();
		$("#game-platforms-edit").hide();
		$("#game-release-date-edit").hide();
		$("#game-streamers-edit").hide();
		$("#game-teams-edit").hide();
		$("#game-communities-edit").hide();
		$("#game-edit-submit").hide();

		$("#game-name").show();
		$("#game-description").show();
		$("#game-rating").show();
		$("#game-genres").show();
		$("#game-platforms").show();
		$("#game-release-date").show();
		$("#game-streamers").show();
		$("#game-teams").show();
		$("#game-communities").show();
		$("#game-edit-button").show();


	});





});