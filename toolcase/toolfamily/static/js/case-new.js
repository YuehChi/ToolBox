$(document).ready(function() {
  $('#summernote').summernote({
      placeholder: 'Hello Bootstrap 4',
      tabsize: 2,
      height: 100
  });

  $('.option').hover(function(){
    console.log("1")
  })

  $('.datepicker').datepicker({
    startDate:'1d'

  });

  $('#radio-check-enddate').click(function(){
    var source = $(this).attr('src').split("/");
    if(source[source.length -1] == 'check-circle-outline.png'){
      $("#input-enddate").attr('disabled', true);
      $(this).attr('src', '/static/images/check-circle.png')
    }
    else{
      $("#input-enddate").attr('disabled', false);
      $(this).attr('src', '/static/images/check-circle-outline.png')
    }
  
  });

  $('#input-required-NPER').on('input', function() {
    if($(this).val()){

    }
  });




  // var selector = $(location).prop("href").split("/").slice(0,-3).join("/");
  // var selector = selector + "/static/plugin/multiselect-02/colorlib-selector.html"
  // $('.multi-selector').load(selector); 

});