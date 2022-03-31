$(document).ready(function() {
	$('#test').change(function(){
		// var countries = [];
        // $.each($(".country option:selected"), function(){            
        //     countries.push($(this).val());
        // });
        // alert("You have selected the country - " + countries.join(", "));
		// alert($('a.visible').attr("data-value"));
		alert($(this).val())

	})

});

(function($) {

	"use strict";

	$('.label.ui.dropdown').dropdown();

	$('.no.label.ui.dropdown').dropdown({
		useLabels: false
	});

	

	$('.ui.button').on('click', function () {
		$('.ui.dropdown').dropdown('restore defaults')
		alert("click")
	})

	 
})(jQuery);

