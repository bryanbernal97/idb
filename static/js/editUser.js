$(document).ready(function() {

/* ********************************************************************************************** */
/* ********************************** GAME SELECTOR FORMATTING ********************************** */
/* ********************************************************************************************** */

	// Only allow the user to select a single game at a time, even though it's formatted using
	// multiple selector with bootstrap-select

	var oldSelectedGame = "";
	$("#user-game-edit option:selected").each(function () {
		oldSelectedGame = $(this).text();
	});

	$('#user-game-edit').change(function() {

		var bothSelectedGames = $('option:selected', this).text();
		var newSelectedGame = bothSelectedGames.replace(oldSelectedGame, '');

		$('#user-game-edit option').each(function() {
			if ($(this).text() == newSelectedGame) {
				this.selected = true;
			} else {
				this.selected = false;
			}
		});

		$("#user-game-edit .selectpicker").selectpicker('refresh');

		oldSelectedGame = newSelectedGame;

	});


/* ********************************************************************************************** */
/* ******************************* COMMUNITY SELECTOR FORMATTING ******************************** */
/* ********************************************************************************************** */

	// Only allow the user to select a single community at a time, even though it's formatted using
	// multiple selector with bootstrap-select

	var oldSelectedCommunity = "";
	$("#user-community-edit option:selected").each(function () {
		oldSelectedCommunity = $(this).text();
	});

	$('#user-community-edit').change(function() {

		var bothSelectedCommunities = $('option:selected', this).text();
		var newSelectedCommunity = bothSelectedCommunities.replace(oldSelectedCommunity, '');

		$('#user-community-edit option').each(function() {
			if ($(this).text() == newSelectedCommunity) {
				this.selected = true;
			} else {
				this.selected = false;
			}
		});

		$("#user-community-edit .selectpicker").selectpicker('refresh');

		oldSelectedCommunity = newSelectedCommunity;

	});

/* ********************************************************************************************** */
/* *************************************** FORM HANDLING **************************************** */
/* ********************************************************************************************** */

	// Serialize form to later check if form has changed. *Only covers form elements with name
	// attribute.
	var origForm = $('#edit-user-form').serialize();

	// Hide template fields and show form fields when user clicks the edit button
	$("#user-edit-button").click(function(){

		origForm = $('#edit-user-form').serialize();

		$("#user-name").addClass('hidden');
		$("#user-description").addClass('hidden');
		$("#user-language").addClass('hidden');
		$("#user-views").addClass('hidden');
		$("#user-followers").addClass('hidden');
		$("#user-url").addClass('hidden');
		$("#user-game").addClass('hidden');
		$("#user-community").addClass('hidden');
		$("#user-teams").addClass('hidden');
		$("#user-created").addClass('hidden');
		$("#user-updated").addClass('hidden');
		$("#user-edit-button").addClass('hidden');


		$("#user-name-edit").removeClass('hidden');
		$("#user-description-edit").removeClass('hidden');
		$("#user-language-edit").removeClass('hidden');
		$("#user-views-edit").removeClass('hidden');
		$("#user-followers-edit").removeClass('hidden');
		$("#user-url-edit").removeClass('hidden');
		$("#user-game-edit").removeClass('hidden');
		$("#user-community-edit").removeClass('hidden');
		$("#user-teams-edit").removeClass('hidden');
		$("#user-created-edit").removeClass('hidden');
		$("#user-updated-edit").removeClass('hidden');
		$("#user-edit-submit").removeClass('hidden');
	});

	// Update template fields with form values, update database, hide edit form fields,
	// and show updated template fields with confirmation/failure alert from updating database.
	$("#user-edit-submit").click(function() {

		// Only need to take action if the form values have changed
		if ($('#edit-user-form').serialize() != origForm) {

			var newName = $("#user-name-edit").val();
			$("#site-title").text(newName);											// SITE TITLE
			$("#user-name").text(newName);											// NAME
			$("#user-description").text($("#user-description-edit").val());			// DESCRIPTION
			$("#user-language").text($("#user-language-edit").val());				// LANGUAGE
			$("#user-views").text($("#user-views-edit").val());						// VIEWS
			$("#user-followers").text($("#user-followers-edit").val());				// FOLLOWERS

			// URL formatting as HTML link
			var userUrl = $("#user-url-edit").val();
			var userUrlHtml = "<a href='" + userUrl + "'>" + userUrl + "</a>";
			$("#user-url").html(userUrlHtml);										// URL


			// User game link formatting
			var gameHTML = "";
			$("#user-game-edit option:selected").each(function () {
					var $this = $(this);
					var gameID = $this.val();
					var gameName = $this.text();
					var gameHref = '/games/' + gameID;
					gameHTML = "<a href='" + gameHref + "'><br />" + gameName + "</a>";
			});
			if (gameHTML == "") {
				gameHTML = "<br>None";
			}
			$("#user-game").html(gameHTML);											// GAME (CONNECTION)


			// User community link formatting
			var communityHTML = "";
			$("#user-community-edit option:selected").each(function () {
					var $this = $(this);
					var communityID = $this.val();
					var communityName = $this.text();
					var communityHref = '/communities/' + communityID;
					communityHTML = "<a href='" + communityHref + "'><br />" + communityName + "</a>";
			});
			if (communityHTML == "") {
				communityHTML = "<br>None";
			}
			$("#user-community").html(communityHTML);								// COMMUNITY (CONNECTION)
			

			var teamIds = $("#user-teams-edit").val();
			if (teamIds.length == 1 && teamIds[0] == 'None') {
				$("#user-teams").text('None');
			} else {
				// Teams formatting as HTML links
				var teamsHTML = "";
				$("#user-teams-edit option:selected").each(function () {
					var $this = $(this);
					var teamID = $this.val();
					var teamName = $this.text();
					if (teamID == 'None') {
						$("#user-teams").text('None');
					} else {
						var teamHref = '/teams/' + teamID;
						var teamHTML = "<a href='" + teamHref + "'><br />" + teamName + "</a>";
						teamsHTML += teamHTML;
					}

				});
				$("#user-teams").html(teamsHTML);									// TEAMS (CONNECTION)
			}

			$("#user-created").text($("#user-created-edit").val());					// CREATED
			$("#user-updated").text($("#user-updated-edit").val());					// UPDATED
		}


		// Hide edit form fields and show updated template fields
		$("#user-name-edit").addClass('hidden');
		$("#user-description-edit").addClass('hidden');
		$("#user-language-edit").addClass('hidden');
		$("#user-views-edit").addClass('hidden');
		$("#user-followers-edit").addClass('hidden');
		$("#user-url-edit").addClass('hidden');
		$("#user-game-edit").addClass('hidden');
		$("#user-community-edit").addClass('hidden');
		$("#user-teams-edit").addClass('hidden');
		$("#user-created-edit").addClass('hidden');
		$("#user-updated-edit").addClass('hidden');
		$("#user-edit-submit").addClass('hidden');

		$("#user-name").removeClass('hidden');
		$("#user-description").removeClass('hidden');
		$("#user-language").removeClass('hidden');
		$("#user-views").removeClass('hidden');
		$("#user-followers").removeClass('hidden');
		$("#user-url").removeClass('hidden');
		$("#user-game").removeClass('hidden');
		$("#user-community").removeClass('hidden');
		$("#user-teams").removeClass('hidden');
		$("#user-created").removeClass('hidden');
		$("#user-updated").removeClass('hidden');
		$("#user-edit-button").removeClass('hidden');
	});
});