
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
		$("#game-delete-button").removeClass('hidden');
		$("#g-recaptcha").removeClass('hidden');
	});


	$("#game-edit-submit").click(function(e) {
		var formSerialized =  $('#edit-game-form').serialize();
		formSerialized = formSerialized.substring(0, formSerialized.lastIndexOf('&')); // Gets rid of g-recaptcha form field that wasn't there before edit was hit

		if (formSerialized != origForm) {
			if(!grecaptcha.getResponse()) {
			    e.preventDefault();
			    alert("Please verify the reCAPTCHA!");
			}
		} else {
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
			$("#game-delete-button").addClass('hidden');
			$("#g-recaptcha").addClass('hidden');

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
		}
	});

	$("#game-delete-button").click(function(e){
		if(!grecaptcha.getResponse()) {
		    e.preventDefault();
		    alert("Please verify the reCAPTCHA!");
		}else{
			var result = confirm("Are you sure you want to DELETE this Game?");
			if (result) {
    		//Logic to delete the item
			}
		}	
	});



});