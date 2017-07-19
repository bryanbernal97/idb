
/* ********************************************************************************************** */
/* ***************************************** RECAPTCHA ****************************************** */
/* ********************************************************************************************** */

	var onloadCallback = function() {
        grecaptcha.render('g-recaptcha', {
          'sitekey' : '6LdDhSkUAAAAACNeH507j02X8yH-p_QhJEEDJHHm'
        });
      };

$(document).ready(function() {


/* ********************************************************************************************** */
/* ********************************** GAME SELECTOR FORMATTING ********************************** */
/* ********************************************************************************************** */

	// Only allow the user to select a single game at a time, even though it's formatted using
	// multiple selector with bootstrap-select

	var oldSelectedGame = "";
	$("#community-game-edit option:selected").each(function () {
		oldSelectedGame = $(this).text();
	});

	$('#community-game-edit').change(function() {

		var bothSelectedGames = $('option:selected', this).text();
		var newSelectedGame = bothSelectedGames.replace(oldSelectedGame, '');

		$('#community-game-edit option').each(function() {
			if ($(this).text() == newSelectedGame) {
				this.selected = true;
			} else {
				this.selected = false;
			}
		});

		$("#community-game-edit .selectpicker").selectpicker('refresh');

		oldSelectedGame = newSelectedGame;

	});


/* ********************************************************************************************** */
/* ********************************* OWNER SELECTOR FORMATTING ********************************** */
/* ********************************************************************************************** */

	// Only allow the user to select a single game at a time, even though it's formatted using
	// multiple selector with bootstrap-select

	var oldSelectedOwner = "";
	$("#community-owner-edit option:selected").each(function () {
		oldSelectedOwner = $(this).text();
	});

	$('#community-owner-edit').change(function() {

		var bothSelectedOwners = $('option:selected', this).text();
		var newSelectedOwner = bothSelectedOwners.replace(oldSelectedOwner, '');

		$('#community-owner-edit option').each(function() {
			if ($(this).text() == newSelectedOwner) {
				this.selected = true;
			} else {
				this.selected = false;
			}
		});

		$("#community-owner-edit .selectpicker").selectpicker('refresh');

		oldSelectedOwner = newSelectedOwner;

	});

/* ********************************************************************************************** */
/* *************************************** FORM HANDLING **************************************** */
/* ********************************************************************************************** */

	// Serialize form to later check if form has changed. *Only covers form elements with name
	// attribute.
	var origForm = $('#edit-community-form').serialize();

	// Hide template fields and show form fields when user clicks the edit button
	$("#community-edit-button").click(function(){

		origForm = $('#edit-community-form').serialize();

		$("#community-name").addClass('hidden');
		$("#community-description").addClass('hidden');
		$("#community-language").addClass('hidden');
		$("#community-rules").addClass('hidden');
		$("#community-game").addClass('hidden');
		$("#community-owner").addClass('hidden');
		$("#community-edit-button").addClass('hidden');


		$("#community-name-edit").removeClass('hidden');
		$("#community-description-edit").removeClass('hidden');
		$("#community-language-edit").removeClass('hidden');
		$("#community-rules-edit").removeClass('hidden');
		$("#community-game-edit").removeClass('hidden');
		$("#community-owner-edit").removeClass('hidden');
		$("#community-edit-submit").removeClass('hidden');
		$("#g-recaptcha").removeClass('hidden');
	});


	// Update template fields with form values, update database, hide edit form fields,
	// and show updated template fields with confirmation/failure alert from updating database.
	$("#community-edit-submit").click(function(e) {

		// alert('response: ' + grecaptcha.getResponse());
		// e.preventDefault();
		if(!grecaptcha.getResponse()) {
		    e.preventDefault();
		    alert("Please verify the reCAPTCHA!");
		}
		// Only need to take action if the form values have changed
		// if ($('#edit-community-form').serialize() != origForm) {

		//	var newName = $("#community-name-edit").val();
		//	$("#site-title").text(newName);												// SITE TITLE
		//	$("#community-name").text(newName);											// NAME
		//	$("#community-description").text($("#community-description-edit").val());	// DESCRIPTION
		//	$("#community-language").text($("#community-language-edit").val());			// LANGUAGE
		//	$("#community-rules").text($("#community-rules-edit").val());				// RULES

		//	// Community game link formatting
		//	var gameHTML = "";
		//	$("#community-game-edit option:selected").each(function () {
		//			var $this = $(this);
		//			var gameID = $this.val();
		//			var gameName = $this.text();
		//			var gameHref = '/games/' + gameID;
		//			gameHTML = "<a href='" + gameHref + "'><br />" + gameName + "</a>";
		//	});
		//	if (gameHTML == "") {
		//		gameHTML = "<br>None";
		//	}
		//	$("#community-game").html(gameHTML);										// GAME (CONNECTION)

		//	// Community owner link formatting
		//	var ownerHTML = "";
		//	$("#community-owner-edit option:selected").each(function () {
		//			var $this = $(this);
		//			var ownerID = $this.val();
		//			var ownerName = $this.text();
		//			var ownerHref = '/users/' + ownerID;
		//			ownerHTML = "<a href='" + ownerHref + "'><br />" + ownerName + "</a>";
		//	});
		//	if (ownerHTML == "") {
		//		ownerHTML = "<br>None";
		//	}
		//	$("#community-owner").html(ownerHTML);										// OWNER (CONNECTION)

		// }

		// $("#community-name-edit").addClass('hidden');
		// $("#community-description-edit").addClass('hidden');
		// $("#community-language-edit").addClass('hidden');
		// $("#community-rules-edit").addClass('hidden');
		// $("#community-game-edit").addClass('hidden');
		// $("#community-owner-edit").addClass('hidden');
		// $("#community-edit-submit").addClass('hidden');

		// $("#community-name").removeClass('hidden');
		// $("#community-description").removeClass('hidden');
		// $("#community-language").removeClass('hidden');
		// $("#community-rules").removeClass('hidden');
		// $("#community-game").removeClass('hidden');
		// $("#community-owner").removeClass('hidden');
		// $("#community-edit-button").removeClass('hidden');

	});


});