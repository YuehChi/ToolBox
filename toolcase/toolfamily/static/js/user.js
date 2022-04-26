$(document).ready(function() {
    //image preview
    $("#id_icon").change(function(){
        //file changed
        readURL(this);   // this: <input id="id_icon">
     });
    function readURL(input){
        if(input.files && input.files[0]){
            const reader = new FileReader();
            reader.onload = function (e) {
                $("#preview_img").attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    //sidebar font-weight
    $('.member').click(function(){
        var target = $(this).attr('m');
        $('.tab').children("[c='"+target+"']").removeClass('hide').siblings().addClass('hide');
    });
    $('.list-group-item').click(function(){
        $(this).addClass('bold').siblings().removeClass('bold');
    });

});
