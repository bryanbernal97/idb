
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



});