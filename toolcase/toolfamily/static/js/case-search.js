$(document).ready(function(){
    $('.dropdown-toggle').dropdown()

    $('#search-keyword').mouseenter(function(){
        $(this).css('background-color', 'white')
    });
    $('#search-keyword').mouseout(function(){
        $(this).css('background-color', 'transparent')
    });
    $('#search-keyword').click(function(){
        $(this).css('background-color', 'white')
    });

});