
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
		$("#user-delete-button").removeClass('hidden');
		$("#g-recaptcha").removeClass('hidden');


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
	});


	$("#user-edit-submit").click(function(e) {

		// Only need to take action if form values have changed, otherwise there is nothing to update.
		var formSerialized =  $('#edit-user-form').serialize();
		formSerialized = formSerialized.substring(0, formSerialized.lastIndexOf('&')); // Gets rid of g-recaptcha form field that wasn't there before edit was hit
		if (formSerialized != origForm) {
			console.log('origForm = ' + origForm);
			console.log('new form = ' + $('#edit-user-form').serialize());
			if(!grecaptcha.getResponse()) {
			    e.preventDefault();
			    alert("Please verify the reCAPTCHA!");
			}
		} else {
			e.preventDefault();
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
			$("#g-recaptcha").addClass('hidden');


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
		}

	});
});