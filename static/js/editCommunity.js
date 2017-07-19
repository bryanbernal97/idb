
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
		$("#community-delete-button").removeClass('hidden');
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

	});

	$("#community-delete-button").click(function(e){
		if(!grecaptcha.getResponse()) {
		    e.preventDefault();
		    alert("Please verify the reCAPTCHA!");
		}else{
			var result = confirm("Are you sure you want to DELETE this Community?");
			if (result) {
    		//Logic to delete the item
			} else {
				e.preventDefault();
			}
		}	
	});


});