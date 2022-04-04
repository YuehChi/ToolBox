$(function(){
    $('.tab-list li').click(function(){
        var target = $(this).attr('m');
        $('.tab').children("[c='"+target+"']").removeClass('hide').siblings().addClass('hide')
    });
});