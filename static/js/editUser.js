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

	// Hide form initially
	$("#user-name-edit").hide();
	$("#user-description-edit").hide();
	$("#user-language-edit").hide();
	$("#user-views-edit").hide();
	$("#user-followers-edit").hide();
	$("#user-url-edit").hide();
	$("#user-game-edit").hide();
	$("#user-community-edit").hide();
	$("#user-teams-edit").hide();
	$("#user-created-edit").hide();
	$("#user-updated-edit").hide();
	$("#user-edit-submit").hide();

	// Serialize form to later check if form has changed. *Only covers form elements with name
	// attribute.
	var origForm = $('#edit-user-form').serialize();

	// Hide template fields and show form fields when user clicks the edit button
	$("#user-edit-button").click(function(){

		origForm = $('#edit-user-form').serialize();

		$("#user-name").hide();
		$("#user-description").hide();
		$("#user-language").hide();
		$("#user-views").hide();
		$("#user-followers").hide();
		$("#user-url").hide();
		$("#user-game").hide();
		$("#user-community").hide();
		$("#user-teams").hide();
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
		$("#user-community-edit").show();
		$("#user-teams-edit").show();
		$("#user-created-edit").show();
		$("#user-updated-edit").show();
		$("#user-edit-submit").show();
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
		$("#user-name-edit").hide();
		$("#user-description-edit").hide();
		$("#user-language-edit").hide();
		$("#user-views-edit").hide();
		$("#user-followers-edit").hide();
		$("#user-url-edit").hide();
		$("#user-game-edit").hide();
		$("#user-community-edit").hide();
		$("#user-teams-edit").hide();
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
		$("#user-community").show();
		$("#user-teams").show();
		$("#user-created").show();
		$("#user-updated").show();
		$("#user-edit-button").show();
	});
});