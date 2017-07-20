/* ********************************************************************************************** */
/* ***************************************** RECAPTCHA ****************************************** */
/* ********************************************************************************************** */

	var onloadCallback = function() {
        grecaptcha.render('g-recaptcha', {
          'sitekey' : '6LdDhSkUAAAAACNeH507j02X8yH-p_QhJEEDJHHm'
        });
      };


    function isImageURL(url) {
    	return(url.match(/\.(jpeg|jpg|gif|png)$/) != null);
	}

	$('#add-user-form').validator({
	    custom: {
	        'positive': function($el) { 
	        	var num = $el.val();
	        	if(num < 0) {
	        		return "Please enter a non-negative number"; // this message will not be used because data-error is set on elements
	        	}
	    	},
	    	'imageURL': function($el) {
	    		var url = $el.val();
	    		if (!isImageURL(url)) {
	    			return "Please enter a URL that points to an image"; // this message will not be used because data-error is set on elements
    			}
	    		// }
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
	$("#user-game-add option:selected").each(function () {
		oldSelectedGame = $(this).text();
	});

	$('#user-game-add').change(function() {

		var bothSelectedGames = $('option:selected', this).text();
		var newSelectedGame = bothSelectedGames.replace(oldSelectedGame, '');

		$('#user-game-add option').each(function() {
			if ($(this).text() == newSelectedGame) {
				this.selected = true;
			} else {
				this.selected = false;
			}
		});

		$("#user-game-add .selectpicker").selectpicker('refresh');

		oldSelectedGame = newSelectedGame;

	});


/* ********************************************************************************************** */
/* ******************************* COMMUNITY SELECTOR FORMATTING ******************************** */
/* ********************************************************************************************** */

	// Only allow the user to select a single community at a time, even though it's formatted using
	// multiple selector with bootstrap-select

	var oldSelectedCommunity = "";
	$("#user-community-add option:selected").each(function () {
		oldSelectedCommunity = $(this).text();
	});

	$('#user-community-add').change(function() {

		var bothSelectedCommunities = $('option:selected', this).text();
		var newSelectedCommunity = bothSelectedCommunities.replace(oldSelectedCommunity, '');

		$('#user-community-add option').each(function() {
			if ($(this).text() == newSelectedCommunity) {
				this.selected = true;
			} else {
				this.selected = false;
			}
		});

		$("#user-community-add .selectpicker").selectpicker('refresh');

		oldSelectedCommunity = newSelectedCommunity;

	});


	$("#user-add-submit").click(function(e) {
		if(!grecaptcha.getResponse()) {
		    e.preventDefault();
		    alert("Please verify the reCAPTCHA!");
		}
	});

});