var number = 0
var upload_img_log = []
var upload_img_files = []
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
    enddate = enddate[2] + '-' + enddate[0] + '-' + enddate[1] + ' 23:59:59'
    $('#forminput-enddate').val(enddate)                                 // Ended Datetime
    $('#forminput-startdate').val(startdate)
    $('#forminput-num').val($('#input-num').val())                    // Required Num
    $('#forminput-work').val($('#input-work').val())                  // Work Mode
    $('#forminput-constraint').val($('#input-preference').val())      // Constraint-
    $('#forminput-location').val($('#input-location').val())          // Location
    
    var description = $('#textarea-description').val()

    console.log(upload_img_log)
    var uplod_img_submit = []
    upload_img_log.forEach(function(value, index, object){
      uplod_img_submit.push(value[1])
    });
    
    //$('#forminput-images').attr('files', uplod_img_submit)
    // const iii = document.getElementById('forminput-images')
    // console.log(new fileListItems(uplod_img_submit))
    // iii.files = new fileListItems(uplod_img_submit)
    $('#forminput-images').prop('files', new fileListItems(uplod_img_submit))
    // $('#forminput-images').prop('files', new fileListItems(uplod_img_submit).files)
    console.log($('#forminput-images').prop('files'))
    //console.log($('#test').prop('files'))


    // $('#forminput-images').attr('files', uplod_img_submit)
    // var fileInput = document.getElementById("test");
    // console.log(fileInput.files)
    // console.log($('#forminput-images').val())
    
    postImg()
   // description = description.replaceAll('\n', '<br>')
    $('#forminput-description').val(description) //Description
    // console.log($('#forminput-title').val())
    // console.log($('#forminput-casetype').val())
    // console.log($('#forminput-casefield').val())
    // console.log($('#forminput-num').val())
    // console.log($('#forminput-work').val())
    // console.log($('#forminput-startdate').val())
    // console.log($('#forminput-enddate').val())
    // console.log($('#forminput-constraint').val())
    // console.log($('#forminput-location').val())
    // console.log($('#forminput-description').val())


    $('#case-new-form').submit()


  });


  //---------------------Uploade Image Preview---------------------
  var counter = 1
  $("#input-img").change(function (){
    $('#span-input-file-validation').removeClass('d-block').addClass('d-none')
    // console.log($(this).val())
    // console.log("change!")

    //console.log($(this).prop('files')[0])

    // generate random file name and create new file
    var iname = $(this).prop('files')[0].lastModified.toString() + randomLetter() +'.' + $(this).prop('files')[0].type.split('/')[1]
    console.log(iname)
    const upload_img = new File([$(this).prop('files')[0]], iname , {type: $(this).prop('files')[0].type});
    //console.log(upload_img)
    //var upload_img = $(this).prop('files')[0]
    // console.log(upload_img.size * 	0.000001)

    if(upload_img.size * 	0.000001 > 2) {
      $('#span-input-file-validation').removeClass('d-none').addClass('d-block')
      $(this).val(null);
    }
    else {

      upload_img_log.push([counter, upload_img])
      var reader = new FileReader();

      var target_div_id = 'updiv_' + counter
      var target_img_id = 'upimg_' + counter
      var target_button_id = 'upbutton_' + counter

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
    }
    
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
});

  
function deleteImg(event) {
  console.log(event.target)
  console.log(event.target.id.split('_')[1])
  console.log('updiv_' + event.target.id.split('_')[1])

  var div_id = '#updiv_' + event.target.id.split('_')[1]
  $(div_id).remove();
  number = number - 1;
  console.log(number)
  if (number < 10){
    $("#input-img").prop('disabled', false);
  }

  upload_img_log.forEach(function(value, index, object){
    if(value[0].toString() == event.target.id.split('_')[1]){
      object.splice(index, 1);
    }
  });

}

function postImg(event) {
  var imgs = document.getElementsByClassName('upload-img')
  //console.log(imgs.length)
  for(var i = 0; i < imgs.length; i++){
    //console.log(imgs[i].src)
  }
  
}

function randomLetter(length) {
    var result     = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < 15; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}

/**
 * @params {File[]} files Array of files to add to the FileList
 * @return {FileList}
 */
 function fileListItems (files) {
  var b = new ClipboardEvent("").clipboardData || new DataTransfer()
  for (var i = 0, len = files.length; i<len; i++) b.items.add(files[i])
  return b.files
}

