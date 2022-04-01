$(document).ready(function() {
  $('#button-post').click(function(){
    console.log('click')
    $('#forminput-title').val($('#input-title').val())                // Title
    $('#forminput-reward').val($('#input-reward').val())              // Reward
    $('#forminput-casetype').val($('#select-casefield').val())        // Case Field
    $('#forminput-casefield').val($('#select-casetype').val())        // Case Type

    var startdate = new Date();
    startdate = startdate.getFullYear() + '-' + startdate.getMonth() + '-' + startdate.getDay() +' '+ startdate.getHours() + ":" + startdate.getMinutes() + ":" + startdate.getSeconds();
    var enddate = $('#input-enddate').val().split('/')
    enddate = enddate[2] + '-' + enddate[0] + '-' + enddate[1]
    $('#forminput-enddate').val(enddate)                                 // Ended Datetime
    $('#forminput-startdate').val(startdate)
    $('#forminput-num').val($('#input-num').val())                    // Required Num
    $('#forminput-work').val($('#input-work').val())                  // Work Mode
    $('#forminput-constraint').val($('#input-preference').val())      // Constraint
    $('#forminput-location').val($('#input-location').val())          // Location
    $('#forminput-description').val($('#textarea-description').val()) //Description
    console.log($('#forminput-title').val())
    console.log($('#forminput-casetype').val())
    console.log($('#forminput-casefield').val())
    console.log($('#forminput-num').val())
    console.log($('#forminput-work').val())
    console.log($('#forminput-startdate').val())
    console.log($('#forminput-enddate').val())
    console.log($('#forminput-constraint').val())
    console.log($('#forminput-location').val())
    console.log($('#forminput-description').val())

    $('#case-new-form').submit()


  });

  function validation(){
    $('#case-new-form').validate({
        rules:{

        }
    })
  }

  $('.datepicker').datepicker({
    startDate:'1d',
    dateFormat: 'yy-mm-dd'
  });

  $('.option').hover(function(){
    console.log("1")
  })

  var location_temp = ""
  $('#radio-check-location').click(function(){
    var source = $(this).attr('src').split("/");
    
    console.log($(this).val());
    if(source[source.length -1] == 'check-circle-outline.png'){
      location_temp = $('#input-location').val()
      $("#input-location").attr('disabled', true);
      $("#input-location").val('不限');
      $(this).attr('src', '/static/images/check-circle.png')
    }
    else{
      $("#input-location").attr('disabled', false);
      $("#input-location").val(location_temp);
      $(this).attr('src', '/static/images/check-circle-outline.png')
    }
  
  });


  $('.radio-workmode').click(function(){
    var source = $(this).attr('src').split("/");
    if(source[source.length -1] == 'check-circle-outline.png'){
      if($(this).attr('id') == 'radio-check-onsite'){
        $('#radio-check-onsite').attr('src', '/static/images/check-circle.png')
        $('#radio-check-online').attr('src', '/static/images/check-circle-outline.png')
        $('#input-work').val('1')
        console.log($('#input-work').val())
      }
      else{
        $('#radio-check-online').attr('src', '/static/images/check-circle.png')
        $('#radio-check-onsite').attr('src', '/static/images/check-circle-outline.png')
        $('#input-work').val('2')
        console.log($('#input-work').val())
      }
    }
  });


  //--------------------------垃圾桶--------------------------
  
  // let options = {
  //   componentRestrictions: { country: 'tw' } // 限制在台灣範圍
  // };
  // var autocomplete = new google.maps.places.Autocomplete($("#input-location")[0], options);
  // google.maps.event.addListener(autocomplete, 'place_changed', function() {
  //     var place = autocomplete.getPlace();
  //     console.log(place.address_components);
  // });

  // var selector = $(location).prop("href").split("/").slice(0,-3).join("/");
  // var selector = selector + "/static/plugin/multiselect-02/colorlib-selector.html"
  // $('.multi-selector').load(selector);
  
    // $('#summernote').summernote({
  //     placeholder: 'Hello Bootstrap 4',
  //     tabsize: 2,
  //     height: 100
  // });
});