var number = 0
var counter = 1
var upload_img_log = []
$(document).ready(function() {
  $('#button-post').click(function(){
    console.log('click')
    $('#forminput-title').val($('#input-title').val())                // Title
    $('#forminput-reward').val($('#input-reward').val())              // Reward
    $('#forminput-casetype').val($('#select-casetype').val())        // Case Field
    $('#forminput-casefield').val($('#select-casefield').val())        // Case Type

    var enddate = $('#input-enddate').val().split('/')
    enddate = enddate[2] + '-' + enddate[0] + '-' + enddate[1]
    $('#forminput-enddate').val(enddate)                                 // Ended Datetime
    $('#forminput-num').val($('#input-num').val())                    // Required Num
    $('#forminput-work').val($('#input-work').val())                  // Work Mode
    $('#forminput-constraint').val($('#input-preference').val())      // Constraint
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

   // description = description.replaceAll('\n', '<br>')
    $('#forminput-description').val(description) //Description
    // console.log($('#forminput-title').val())
    // console.log($('#forminput-casetype').val())
    // console.log($('#forminput-casefield').val())
    console.log($('#forminput-num').val())
    // console.log($('#forminput-work').val())
    // console.log($('#forminput-startdate').val())
    console.log($('#forminput-enddate').val())
    // console.log($('#forminput-constraint').val())
    // console.log($('#forminput-location').val())
    // console.log($('#forminput-description').val())


    //$('#case-new-form').submit()


  });


  //---------------------Case Old Info---------------------
  $('#input-title').val($('#forminput-title').val())                // Title
  $('#input-reward').val($('#forminput-reward').val())              // Reward
  $('#select-casetype').val(parseInt($('#get-casetype').html()))        // Case Field
  $('#select-casefield').val(parseInt($('#get-casefield').html()))        // Case Type
  $('#input-num').val($('#forminput-num').val())                    // Required Num
  $('#input-preference').val($('#get-constraint').html())      // Constraint
  $('#input-location').val($('#get-location').html())          // Location
    
  $('#textarea-description').val($('#get-description').val())

  //---------------------Work Mode---------------------
  console.log($('#forminput-work').val())
  if($('#forminput-work').val() == '1'){
    $('#radio-check-onsite').attr('src', '/static/images/check-circle.png')
    $('#radio-check-online').attr('src', '/static/images/check-circle-outline.png')
    $('#input-work').val('1')
    console.log($('#input-work').val())
  }
  else if($('#forminput-work').val() == '2'){
    $('#radio-check-online').attr('src', '/static/images/check-circle.png')
    $('#radio-check-onsite').attr('src', '/static/images/check-circle-outline.png')
    $('#input-work').val('2')
    console.log($('#input-work').val())
  }

  //---------------------End Date---------------------
  var enddate = $('#get-enddate').html()
  console.log(enddate)
  var year = enddate.split('年')[0]
  var month = enddate.split('年')[1].split('月')[0]
  var date =  enddate.split('年')[1].split('月')[1].split('日')[0]
  if(parseInt(month) < 10){
    month = '0' + month
  }
  enddate = month + '/' + date + '/' + year
  $('#input-enddate').val(enddate)          // Ended Datetime




  //---------------------Images---------------------
  // console.log(document.getElementsByClassName('case-image'))
  var old_case_image = document.getElementsByClassName('case-image')

  for (var i=0; i<old_case_image.length; i++){
    var isplit = old_case_image[i].src.split('/')
    var iname = isplit [isplit .length - 1]

    fetch(old_case_image[i].src)
    .then(res => res.blob())
    .then(blob => {

      const file = new File([blob], iname, blob)
      //console.log(file)
      upload_img_log.push([counter, file])



      var target_div_id = 'updiv_' + counter
      var target_img_id = 'upimg_' + counter
      var target_button_id = 'upbutton_' + counter

      var target_html = '<div class="m-1 w-20 d-inline-block position-relative" id="'+ target_div_id +'">'+
                        '<button class="close position-absolute right-1 top-1 btn-upload-delete" type="button" id="'+ target_button_id +'" onclick="deleteImg(event)"><span aria-hidden="true">×</span></button>' +
                        '<img id="'+ target_img_id+'" class="upload-img d-inline"></div>'
      // console.log(file)
      $('#upload_image').append(target_html)

      var reader = new FileReader();
      reader.onload = function(e) {
        $('#'+target_img_id).attr('src', e.target.result);
      }
      reader.readAsDataURL(file)

      counter = counter + 1
      number = number + 1

      if (number == 10){
        $("input:file").prop('disabled', true);
      }
      console.log(number)
    })

  }


  

  //---------------------Uploade Image Preview---------------------

  $("#input-img").change(function (){
    $('#span-input-file-validation').removeClass('d-block').addClass('d-none')


    // generate random file name and create new file
    var iname = $(this).prop('files')[0].lastModified.toString() + randomLetter() +'.' + $(this).prop('files')[0].type.split('/')[1]
    console.log(iname)
    const upload_img = new File([$(this).prop('files')[0]], iname , {type: $(this).prop('files')[0].type});

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

