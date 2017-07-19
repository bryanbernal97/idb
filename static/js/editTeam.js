
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
/* *************************************** FORM HANDLING **************************************** */
/* ********************************************************************************************** */


	// Serialize form to later check if form has changed. *Only covers form elements with name
	// attribute.
	var origForm = $('#edit-team-form').serialize();


	// Hide template fields and show form fields when user clicks the edit button
	$("#team-edit-button").click(function(){

		origForm = $('#edit-team-form').serialize();

		// Hide edit form fields and show updated template fields
		$("#team-name").addClass('hidden');
		$("#team-info").addClass('hidden');
		$("#team-streamers").addClass('hidden');
		$("#team-games").addClass('hidden');
		$("#team-created").addClass('hidden');
		$("#team-updated").addClass('hidden');
		$("#team-edit-button").addClass('hidden');

		$("#team-name-edit").removeClass('hidden');
		$("#team-info-edit").removeClass('hidden');
		$("#team-streamers-edit").removeClass('hidden');
		$("#team-games-edit").removeClass('hidden');
		$("#team-created-edit").removeClass('hidden');
		$("#team-updated-edit").removeClass('hidden');
		$("#team-edit-submit").removeClass('hidden');
		$("#team-delete-button").removeClass('hidden');
		$("#g-recaptcha").removeClass('hidden');

	});

	// Update template fields with form values, update database, hide edit form fields,
	// and show updated template fields with confirmation/failure alert from updating database.
	$("#team-edit-submit").click(function(e){
		if(!grecaptcha.getResponse()) {
		    e.preventDefault();
		    alert("Please verify the reCAPTCHA!");
		}
	});

	$("#team-delete-button").click(function(e){
		if(!grecaptcha.getResponse()) {
		    e.preventDefault();
		    alert("Please verify the reCAPTCHA!");
		}else{
			var result = confirm("Are you sure you want to DELETE this Team?");
			if (result) {
    		//Logic to delete the item
			}
		}

	});


		
		// Only need to take action if the form values have changed
		//if ($('#edit-team-form').serialize() != origForm) {

		//	var newName = $("#team-name-edit").val();
		//	$("#site-title").text(newName);											// SITE TITLE
		//	$("#team-name").text(newName);											// NAME
		//	$("#team-info").text($("#team-info-edit").val());						// INFO

		//	// Team streamers links formatting
		//	var streamersHTML = "";
		//	$("#team-streamers-edit option:selected").each(function () {
		//		var $this = $(this);
		//		var streamerID = $this.val();
		//		var streamerName = $this.text();
		//		var streamerHref = '/user/' + streamerID;
		//		var streamerHTML = "<a href='" + streamerHref + "'><br />" + streamerName + "</a>";
		//		streamersHTML += streamerHTML;
		//	});
		//	if (streamersHTML == "") {
		//		streamersHTML = "<br>None";
		//	}
		//	$("#team-streamers").html(streamersHTML);								// STREAMERS (CONNECTION)
		

		//	// Team games links formatting
		//	var gamesHTML = "";
		//	$("#team-games-edit option:selected").each(function () {
		//		var $this = $(this);
		//		var gameID = $this.val();
		//		var gameName = $this.text();
		//		var gameHref = '/games/' + gameID;
		//		var gameHTML = "<a href='" + gameHref + "'><br />" + gameName + "</a>";
		//		gamesHTML += gameHTML;
		//	});
		//	if (gamesHTML == "") {
		//		gamesHTML = "<br>None";
		//	}
		//	$("#team-games").html(gamesHTML);										// GAMES (CONNECTION)

		//	$("#team-created").text($("#team-created-edit").val());					// CREATED
		//	$("#team-updated").text($("#team-updated-edit").val());					// UPDATED

		//}

});