$(document).ready(function(){

    $('.dropdown-toggle').dropdown()

    //--------------- Hover ---------------
    $('#dropdown-field').hover(function(){
        $('#dropdownlink-field').css('color', '#eee')
    },function(){
        $('#dropdownlink-field').css('color', '#865140')
    });

    $('#dropdown-type').hover(function(){
        $('#dropdownlink-type').css('color', '#eee')
    },function(){
        $('#dropdownlink-type').css('color', '#865140')
    });

    $('#div-search-allcase').hover(function(){
        $('#link-search-allcase').css('color', '#5e4949')
    },function(){
        $('#link-search-allcase').css('color', '#865140')
    });


    $('#search-form').on('keypress', function(e) {
        if ($('#search-keyword').val() != ""){
            $('#forminput-case-query').val($('#search-keyword').val())
            $('#forminput-case-page').val('1')
            $('#search-from').submit()
        }
        else {
            return e.which !== 13;
        }
    });

    $('#link-search-keyword').click(function(){
        if ($('#search-keyword').val() != ""){
            $('#forminput-case-query').val($('#search-keyword').val())
            $('#forminput-case-page').val('1')
            $('#search-from').submit()
        }
    });

    //--------------- Search ---------------
    $('.a-search-field').click(function(){
        console.log($(this).data("value"))
        $('#forminput-case-field').val($(this).data("value"))
        $('#forminput-case-field').prop("checked", true);
        $('#forminput-case-query').val("")
        $('#forminput-case-page').val('1')
        $('#search-form').submit()
    })

    $('.a-search-type').click(function(){
        console.log($(this).data("value"))
        $('#forminput-case-type').val($(this).data("value"))
        $('#forminput-case-type').prop("checked", true);
        $('#forminput-case-query').val("")
        $('#forminput-case-page').val('1')
        $('#search-form').submit()
    })

    $('#link-search-allcase').click(function(){
        document.location.href="/toolfamily/case/search/";
    })

    



});