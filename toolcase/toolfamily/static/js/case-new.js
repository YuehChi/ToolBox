var number = 0

$(document).ready(function() {
  $('#button-post').click(function(){
    console.log('click')
    $('#forminput-title').val($('#input-title').val())                // Title
    $('#forminput-reward').val($('#input-reward').val())              // Reward
    $('#forminput-casetype').val($('#select-casetype').val())        // Case Field
    $('#forminput-casefield').val($('#select-casefield').val())        // Case Type

    var startdate = new Date();
    startdate = startdate.getFullYear() + '-' + String(startdate. getMonth() + 1). padStart(2, '0') + '-' + String(startdate. getDate()). padStart(2, '0') +' '+ startdate.getHours() + ":" + startdate.getMinutes() + ":" + startdate.getSeconds();
    var enddate = $('#input-enddate').val().split('/')
    enddate = enddate[2] + '-' + enddate[0] + '-' + enddate[1]
    $('#forminput-enddate').val(enddate)                                 // Ended Datetime
    $('#forminput-startdate').val(startdate)
    $('#forminput-num').val($('#input-num').val())                    // Required Num
    $('#forminput-work').val($('#input-work').val())                  // Work Mode
    $('#forminput-constraint').val($('#input-preference').val())      // Constraint
    $('#forminput-location').val($('#input-location').val())          // Location
    
    var description = $('#textarea-description').val()
   // description = description.replaceAll('\n', '<br>')
    $('#forminput-description').val(description) //Description
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

    //$('#case-new-form').submit()


  });


  //---------------------Uploade Image Preview---------------------
  var counter = 1
  $("input:file").click(function(){
    console.log('click!')

  })
  $("input:file").change(function (){
    console.log("change!")
    console.log($(this).prop('files')[0])

    var upload_img = $(this).prop('files')[0]
    var reader = new FileReader();

    var target_div_id = 'updiv_' + counter
    var target_img_id = 'upimg_' + counter
    var target_button_id = 'upbutton_' + counter

    // var target_html = '<div class="d-block m-3" id="'+ target_div_id +'">'+
    //                   '<img id="'+ target_img_id+'" class="upload-img d-inline">'+
    //                   '<button class="btn btn-upload-delete d-inline" type="button" id="'+ target_button_id +'" onclick="deleteImg(event)">X</button></div>'
    var target_html = '<div class="m-1 w-20 d-inline-block position-relative" id="'+ target_div_id +'">'+
                      '<button class="close position-absolute right-1 top-1 btn-upload-delete" type="button" id="'+ target_button_id +'" onclick="deleteImg(event)"><span aria-hidden="true">×</span></button>' +
                      '<img id="'+ target_img_id+'" class="upload-img d-inline"></div>'
                      

    $('#upload_image').append(target_html)
    

    reader.onload = function(e) {
      $('#'+target_img_id).attr('src', e.target.result);
    }
    reader.readAsDataURL(upload_img)

    counter = counter + 1
    number = number + 1
    $(this).val(null);

    if (number == 10){
      $("input:file").prop('disabled', true);
    }
    console.log(number)
  });



  //---------------------Validation---------------------
 var validator = $('#case-new-form').validate({
        rules:{
          input_title:{required: true, maxlength:30},
          input_reward:{required: true, maxlength:30},
          input_enddate:{required: true, date:true},
          input_num:{required: true, min:1, max:100, digits:true, number:true},
          input_location:{required: true, maxlength:20},
          select_casefield:{required: true},
          select_casetype:{required: true},
          textarea_description:{maxlength:1000},
        },
        messages:{
        }
    });


  //---------------------Datepicker---------------------
  $('.datepicker').datepicker({
    startDate:'1d',
    dateFormat: 'yy-mm-dd'
  });

  $('.option').hover(function(){
    console.log("1")
  })


  //---------------------Location Text & Radio Button---------------------
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

  //---------------------Work Mode Radio Button----------------------
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

  
function deleteImg(event){
  console.log(event.target)
  console.log(event.target.id.split('_')[1])
  console.log('updiv_' + event.target.id.split('_')[1])
  var div_id = '#updiv_' + event.target.id.split('_')[1]
  $(div_id).remove();
  number = number - 1;
  console.log(number)
  if (number < 10){
    $("input:file").prop('disabled', false);
  }
}