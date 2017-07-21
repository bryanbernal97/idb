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

	$('#add-team-form').validator({
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
	    		if (id == Math.floor(id)) {
	    			var id_int = parseInt(id);
	    			if (ids.indexOf(id_int) != -1) {
	    				return "Sorry, that ID is already taken";
    				}
	    		}
	    	}
	    	
		}
	});

$(document).ready(function() {


/* ********************************************************************************************** */
/* ******************************************* SUBMIT ******************************************* */
/* ********************************************************************************************** */

	$("#team-add-submit").click(function(e) {
		if(!grecaptcha.getResponse()) {
		    e.preventDefault();
		    alert("Please verify the reCAPTCHA!");
		}
	});


});