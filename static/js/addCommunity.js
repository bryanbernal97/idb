
/* ********************************************************************************************** */
/* ***************************************** RECAPTCHA ****************************************** */
/* ********************************************************************************************** */

	var onloadCallback = function() {
        grecaptcha.render('g-recaptcha', {
          'sitekey' : '6LdDhSkUAAAAACNeH507j02X8yH-p_QhJEEDJHHm'
        });
      };


/* ********************************************************************************************** */
/* ************************************** FORM VALIDATION *************************************** */
/* ********************************************************************************************** */

    function isImageURL(url) {
    	return(url.match(/\.(jpeg|jpg|gif|png)$/) != null);
	}

	$('#add-community-form').validator({
	    custom: {
	        'positive': function($el) { 
	        	var num = $el.val();
	        	if (num == Math.floor(num)){
	        		if(num < 0) {
	        			return "Please enter a non-negative number"; // this message will not be used because data-error is set on elements
	        		}
	        	}
	    	},
	    	'imageURL': function($el) {
	    		var url = $el.val();
	    		if (!isImageURL(url)) {
	    			return "Please enter a URL that points to an image"; // this message will not be used because data-error is set on elements
    			}
	    		// }
	    	},
	    	'uniqueID': function($el) {
	    		var id = $el.val();
    			if (ids.indexOf(id) != -1) {
    				return "Sorry, that ID is already taken";
				}

	    	}
	    	
		}
	});


$(document).ready(function() {


/* ********************************************************************************************** */
/* ********************************** GAME SELECTOR FORMATTING ********************************** */
/* ********************************************************************************************** */

	// Only allow the user to select a single game at a time, even though it's formatted using
	// multiple selector with bootstrap-select

	var oldSelectedGame = "";
	$("#community-game-add option:selected").each(function () {
		oldSelectedGame = $(this).text();
	});

	$('#community-game-add').change(function() {

		var bothSelectedGames = $('option:selected', this).text();
		var newSelectedGame = bothSelectedGames.replace(oldSelectedGame, '');

		$('#community-game-add option').each(function() {
			if ($(this).text() == newSelectedGame) {
				this.selected = true;
			} else {
				this.selected = false;
			}
		});

		$("#community-game-add .selectpicker").selectpicker('refresh');

		oldSelectedGame = newSelectedGame;

	});

/* ********************************************************************************************** */
/* ********************************* OWNER SELECTOR FORMATTING ********************************** */
/* ********************************************************************************************** */

	// Only allow the user to select a single game at a time, even though it's formatted using
	// multiple selector with bootstrap-select

	var oldSelectedOwner = "";
	$("#community-owner-add option:selected").each(function () {
		oldSelectedOwner = $(this).text();
	});

	$('#community-owner-add select').change(function() {

		var bothSelectedOwners = $('option:selected', this).text();
		var newSelectedOwner = bothSelectedOwners.replace(oldSelectedOwner, '');

		var singleSelected = true;

		$('#community-owner-add option').each(function() {
			if ($(this).text() == newSelectedOwner && singleSelected) {
				this.selected = true;
				singleSelected = false;
			} else {
				this.selected = false;
			}
		});

		$("#community-owner-add .selectpicker").selectpicker('refresh');

		oldSelectedOwner = newSelectedOwner;

	});


	$("#community-add-submit").click(function(e) {
		if(!grecaptcha.getResponse()) {
		    e.preventDefault();
		    alert("Please verify the reCAPTCHA!");
		}
	});


});