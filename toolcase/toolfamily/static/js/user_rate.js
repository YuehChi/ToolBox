$(document).ready(function() {
     // --------------- User Rate ---------------
     console.log($('#get-user-rate').html())
     console.log($('#get-user-ratenum').html())
     var rate = $('#get-user-rate').html()
     var rate_html = ''
     let starnum = Math.floor(rate)
     for (var i = 0; i < 5; i++ ) {
         //starnum: 3, 2, 1, 0, -1
         //i      : 0, 1, 2, 3, 4
         if(starnum > 0){
             rate_html = rate_html + '<i class="material-icons star-color">star</i>'
         }
         else if (starnum == 0){
             if(rate % 1 >= 0.5){
                 rate_html = rate_html + '<i class="material-icons star-color">star_half</i>'
             }
             else{
                 rate_html = rate_html + '<i class="material-icons star-color">star_border</i>'
             }
         }
         else{
             rate_html = rate_html + '<i class="material-icons star-color">star_border</i>'
         }
         starnum = starnum - 1 
     }
 
     console.log(rate_html)
     $('#user-rate').html(rate_html)
     $('#user-ratenum').html('('+ $('#get-user-ratenum').html() + ')')
 
 
 
 
     console.log($('#get-user-rate').html())
     console.log($('#get-user-ratenum').html())
});