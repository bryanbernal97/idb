$(document).ready(function() {

/* ********************************************************************************************** */
/* ******************************* ADD / REMOVE GENRES TEXT BOXES ******************************* */
/* ********************************************************************************************** */

	// Here first get the contents of the div with name class copy-fields and add it to before
	// "before-add-more-genres" div class.
	$(".add-more-genre").click(function(){ 
		var html = $(".copy-genre-fields").html();

		// Get the current value of the textbox with add button
		var currentVal = $(".before-add-more-genres input").val();

		// Only need to add another text box if there is something in the current text box
		if (currentVal != "") {
			
			// Move the value to the new element with remove button
			var newHtml = html.replace(/value=".*?"/, 'value="' + currentVal + '"');

			var actualHtml = '<div class="copy-genre-fields">' + newHtml + '</div>';

			// Reset value of textbox with add button
			$(".before-add-more-genres input").val("");

			// Add a new input text box with current value and remove button above the newly empty
			// input text box with add button
			$(".before-add-more-genres").before(actualHtml);
		}

		
	});
	  
	// Here it will remove the current value of the remove button which has been pressed
	$("body").on("click",".remove-genre",function(){ 
		var outer = $(this).parents(".copy-genre-fields");
		outer.children("br").remove();
		$(this).parents(".control-group").remove();
	});

/* ********************************************************************************************** */
/* ***************************** ADD / REMOVE PLATFORMS TEXT BOXES ****************************** */
/* ********************************************************************************************** */

	// Here first get the contents of the div with name class copy-fields and add it to before
	// "before-add-more-platforms" div class.
	$(".add-more-platform").click(function(){ 

		// Inner elements of copy-platform-fields div
		var html = $(".copy-platform-fields").html();
		
		// Get the current value of the textbox with add button
		var currentVal = $(".before-add-more-platforms input").val();

		// Only need to add another text box if there is something in the current text box
		if (currentVal != "") {

			// Move the value to the new element with remove button
			var newHtml = html.replace(/value=".*?"/, 'value="' + currentVal + '"');
			
			// Add the enclosing div back
			var actualHtml = '<div class="copy-platform-fields">' + newHtml + '</div>';

			// Reset value of textbox with add button
			$(".before-add-more-platforms input").val("");

			// Add a new input text box with current value and remove button above the newly empty
			// input text box with add button
			$(".before-add-more-platforms").before(actualHtml);
		}
	});
	  
	// Here it will remove the current value of the remove button which has been pressed
	$("body").on("click",".remove-platform",function(){ 
		var outer = $(this).parents(".copy-platform-fields");
		outer.children("br").remove();
		$(this).parents(".control-group").remove();
	});


/* ********************************************************************************************** */
/* *************************************** FORM HANDLING **************************************** */
/* ********************************************************************************************** */

	// Serialize form to later check if form has changed. *Only covers form elements with name
	// attribute.
	var origForm = $('#edit-game-form').serialize();

	// Hide template fields and show form fields when user clicks the edit button
	$("#game-edit-button").click(function(){

		origForm = $('#edit-game-form').serialize();

		$("#game-name").addClass('hidden');
		$("#game-description").addClass('hidden');
		$("#game-rating").addClass('hidden');
		$("#game-genres").addClass('hidden');
		$("#game-platforms").addClass('hidden');
		$("#game-release-date").addClass('hidden');
		$("#game-streamers").addClass('hidden');
		$("#game-teams").addClass('hidden');
		$("#game-communities").addClass('hidden');
		$("#game-edit-button").addClass('hidden');


		$("#game-name-edit").removeClass('hidden');
		$("#game-description-edit").removeClass('hidden');
		$("#game-rating-edit").removeClass('hidden');
		$("#game-genres-edit").removeClass('hidden');
		$("#game-platforms-edit").removeClass('hidden');
		$("#game-release-date-edit").removeClass('hidden');
		$("#game-streamers-edit").removeClass('hidden');
		$("#game-teams-edit").removeClass('hidden');
		$("#game-communities-edit").removeClass('hidden');
		$("#game-edit-submit").removeClass('hidden');
	});


	// Update template fields with form values, update database, hide edit form fields,
	// and show updated template fields with confirmation/failure alert from updating database.
	$("#game-edit-submit").click(function() {

		// Only need to take action if the form values have changed
		if ($('#edit-game-form').serialize() != origForm) {
			
			var newName = $("#game-name-edit").val();
			$("#site-title").text(newName);										// SITE TITLE
			$("#game-name").text(newName);										// NAME
			$("#game-description").text($("#game-description-edit").val());		// DESCRIPTION
			$("#game-rating").text($("#game-rating-edit").val());				// RATING

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
			$("#game-genres").html(genresHtml);									// GENRES

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
			$("#game-platforms").html(platformsHtml);							// PLATFORMS


			$("#game-release-date").text($("#game-release-date-edit").val());	// RELEASE DATE

			// Game streamer links formatting
			var streamersHTML = "";
			$("#game-streamers-edit option:selected").each(function () {
				var $this = $(this);
				var streamerID = $this.val();
				var streamerName = $this.text();
				var streamerHref = '/users/' + streamerID;
				var streamerHTML = ("<a href='" + streamerHref + "'><br />" +
					streamerName + "</a>");
				streamersHTML += streamerHTML;
			});
			if (streamersHTML == "") {
				streamersHTML = "<br>None";
			}
			$("#game-streamers").html(streamersHTML);							// STREAMERS (CONNECTION)

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
			$("#game-teams").html(teamsHTML);									// TEAMS (CONNECTION)

			// Game community links formatting
			var communitiesHTML = "";
			$("#game-communities-edit option:selected").each(function () {
				var $this = $(this);
				var communityID = $this.val();
				var communityName = $this.text();
				var communityHref = '/communities/' + communityID;
				var communityHTML = ("<a href='" + communityHref + "'><br />" +
					communityName + "</a>");
				communitiesHTML += communityHTML;
			});
			if (communitiesHTML == "") {
				communitiesHTML = "<br>None";
			}
			$("#game-communities").html(communitiesHTML);						// COMMUNITIES (CONNECTION)
		}

		// Hide edit form fields and show updated template fields
		$("#game-name-edit").addClass('hidden');
		$("#game-description-edit").addClass('hidden');
		$("#game-rating-edit").addClass('hidden');
		$("#game-genres-edit").addClass('hidden');
		$("#game-platforms-edit").addClass('hidden');
		$("#game-release-date-edit").addClass('hidden');
		$("#game-streamers-edit").addClass('hidden');
		$("#game-teams-edit").addClass('hidden');
		$("#game-communities-edit").addClass('hidden');
		$("#game-edit-submit").addClass('hidden');

		$("#game-name").removeClass('hidden');
		$("#game-description").removeClass('hidden');
		$("#game-rating").removeClass('hidden');
		$("#game-genres").removeClass('hidden');
		$("#game-platforms").removeClass('hidden');
		$("#game-release-date").removeClass('hidden');
		$("#game-streamers").removeClass('hidden');
		$("#game-teams").removeClass('hidden');
		$("#game-communities").removeClass('hidden');
		$("#game-edit-button").removeClass('hidden');

	});

});