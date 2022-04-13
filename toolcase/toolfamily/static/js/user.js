$(document).ready(function() {
    $("#id_icon").change(function(){
        //當檔案改變後，做一些事 
        readURL(this);   // this代表<input id="id_icon">
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
    $('.member').click(function(){
        var target = $(this).attr('m');
        $('.tab').children("[c='"+target+"']").removeClass('hide').siblings().addClass('hide');
    });
    $('.list-group-item').click(function(){
        $(this).addClass('bold').siblings().removeClass('bold');
    });

});