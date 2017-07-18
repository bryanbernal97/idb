$(document).ready(function() {

	var ENVIRONMENT = 'http://dev-env.fkmjb3y3r4.us-west-2.elasticbeanstalk.com/';
	var api_user_url = ENVIRONMENT + '/api/user/';

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
		$("#captcha-img").removeClass('hidden');
		$("#captcha-submit").removeClass('hidden');
	});

	// Update template fields with form values, update database, hide edit form fields,
	// and show updated template fields with confirmation/failure alert from updating database.
	$("#user-edit-submit").click(function() {

		// // Only need to take action if the form values have changed
		// if ($('#edit-user-form').serialize() != origForm) {

		// 	var newName = $("#user-name-edit").val();
		// 	var newDescription = $("#user-description-edit").val();
		// 	var newLanguage = $("#user-language-edit").val();
		// 	var newViews = $("#user-views-edit").val();
		// 	var newFollowers = $("#user-followers-edit").val();

		// 	$("#site-title").text(newName);											// SITE TITLE
		// 	$("#user-name").text(newName);											// NAME
		// 	$("#user-description").text(newDescription);							// DESCRIPTION
		// 	$("#user-language").text(newLanguage);									// LANGUAGE
		// 	$("#user-views").text(newViews);										// VIEWS
		// 	$("#user-followers").text(newFollowers);								// FOLLOWERS

		// 	// URL formatting as HTML link
		// 	var newUrl = $("#user-url-edit").val();
		// 	var userUrlHtml = "<a href='" + newUrl + "'>" + newUrl + "</a>";
		// 	$("#user-url").html(userUrlHtml);										// URL


		// 	// User game link formatting
		// 	var gameHTML = "";
		// 	var newGameID = null;
		// 	$("#user-game-edit option:selected").each(function () {
		// 			var $this = $(this);
		// 			newGameID = $this.val();
		// 			var gameName = $this.text();
		// 			var gameHref = '/games/' + newGameID;
		// 			gameHTML = "<a href='" + gameHref + "'><br />" + gameName + "</a>";
		// 	});
		// 	if (gameHTML == "") {
		// 		gameHTML = "<br>None";
		// 	}
		// 	$("#user-game").html(gameHTML);											// GAME (CONNECTION)


		// 	// User community link formatting
		// 	var communityHTML = "";
		// 	var newCommunityID = null;
		// 	$("#user-community-edit option:selected").each(function () {
		// 			var $this = $(this);
		// 			newCommunityID  = $this.val();
		// 			var communityName = $this.text();
		// 			var communityHref = '/communities/' + newCommunityID;
		// 			communityHTML = "<a href='" + communityHref + "'><br />" + communityName + "</a>";
		// 	});
		// 	if (communityHTML == "") {
		// 		communityHTML = "<br>None";
		// 	}
		// 	$("#user-community").html(communityHTML);								// COMMUNITY (CONNECTION)
	

		// 	// User team links formatting
		// 	var teamsHTML = "";
		// 	var newTeamIDS = [];
		// 	$("#user-teams-edit option:selected").each(function () {
		// 		var $this = $(this);
		// 		var teamID = $this.val();
		// 		newTeamIDS.push(parseInt(teamID));
		// 		var teamName = $this.text();
		// 		var teamHref = '/teams/' + teamID;
		// 		var teamHTML = "<a href='" + teamHref + "'><br />" + teamName + "</a>";
		// 		teamsHTML += teamHTML;
		// 	});
		// 	if (teamsHTML == "") {
		// 		teamsHTML = "<br>None";
		// 	}
		// 	$("#user-teams").html(teamsHTML);										// TEAMS (CONNECTION)		

		// 	var newCreated = $("#user-created-edit").val();
		// 	var newUpdated = $("#user-updated-edit").val();
		// 	$("#user-created").text(newCreated);									// CREATED
		// 	$("#user-updated").text(newUpdated);									// UPDATED
		// }

		// /* ************************************************************************************** */
		// /* ********************************** UPDATE DATABASE *********************************** */
		// /* ************************************************************************************** */

		// var userID = $("#user-id-edit").val();
		// var updateURL = api_user_url + userID;

		// // Need to make sure that all the available options from the form are on here
		// var dataObject = {
		// 	'name': newName,
		// 	'description': newDescription,
		// 	'language': newLanguage,
		// 	'views': newViews,
		// 	'followers': newFollowers,
		// 	'url': newUrl,
		// 	'created': newCreated,
		// 	'updated': newUpdated,
		// 	'game_id': newGameID,
		// 	'community_id': newCommunityID,
		// 	'team_ids': newTeamIDS
		// };

		// var headers = {'content-type': 'application/json'};

		// $.ajax({ 
		// 	url: updateURL,
		// 	headers: headers,
		//    	method: "PUT",
		//    	dataType: "json",
		//    	data: JSON.stringify(dataObject),
		//    	success: function(data){        
		//     	alert("Congratulations, the update was successful!");
		//    	},
		//    	error: function(error){        
		//     	console.log("Error: " + error.responseText); // Make an error message.
		//    	}
		// });


		// // Hide edit form fields and show updated template fields
		// $("#user-name-edit").addClass('hidden');
		// $("#user-description-edit").addClass('hidden');
		// $("#user-language-edit").addClass('hidden');
		// $("#user-views-edit").addClass('hidden');
		// $("#user-followers-edit").addClass('hidden');
		// $("#user-url-edit").addClass('hidden');
		// $("#user-game-edit").addClass('hidden');
		// $("#user-community-edit").addClass('hidden');
		// $("#user-teams-edit").addClass('hidden');
		// $("#user-created-edit").addClass('hidden');
		// $("#user-updated-edit").addClass('hidden');
		// $("#user-edit-submit").addClass('hidden');

		// $("#user-name").removeClass('hidden');
		// $("#user-description").removeClass('hidden');
		// $("#user-language").removeClass('hidden');
		// $("#user-views").removeClass('hidden');
		// $("#user-followers").removeClass('hidden');
		// $("#user-url").removeClass('hidden');
		// $("#user-game").removeClass('hidden');
		// $("#user-community").removeClass('hidden');
		// $("#user-teams").removeClass('hidden');
		// $("#user-created").removeClass('hidden');
		// $("#user-updated").removeClass('hidden');
		// $("#user-edit-button").removeClass('hidden');
	});
});