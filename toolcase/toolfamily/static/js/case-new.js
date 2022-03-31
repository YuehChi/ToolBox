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

  // var selector = $(location).prop("href").split("/").slice(0,-3).join("/");
  // var selector = selector + "/static/plugin/multiselect-02/colorlib-selector.html"
  // $('.multi-selector').load(selector); 

});