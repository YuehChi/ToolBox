$(document).ready(function(){

    
    getDefault()

    // ---------- Pagination ----------
    $('#select-pagination').on('change', function() {
        console.log($(this).val())
        //advancedSearchSubmit()

        console.log($('#select-pagination option:selected').val())
        $('#forminput-page').val($('#select-pagination option:selected').val())
        getDefault()
        advancedSearchSubmit()
        //$('#forminput-page').val($('#select-pagination option:selected').val())
        console.log($('#select-pagination option:selected').val())

        $('#advanced-search-form').submit()
    })


    // ---------- Second Num Filter ----------
    if ($('#select-num').val() == "3"){
        $('.case-card').each(function(){

            if( parseInt($(this).find('.filter-num').html()) < 5 ){
                console.log($(this).find('.filter-num').html())
                $(this).remove()
            }
    
        })
        recountCaseLength()
    }

    if ($('#select-num').val() == "4"){
        $('.case-card').each(function(){

            if( parseInt($(this).find('.filter-num').html()) < 10 ){
                console.log($(this).find('.filter-num').html())
                $(this).remove()
            }
    
        })
        recountCaseLength()
    }

    // ---------- Single Choice Checkbox ----------
    // $('input:checkbox').on('click', function() {
    //     var $box = $(this);
    //     if ($box.is(':checked')) {

    //       var group = "input:checkbox[name='" + $box.attr("name") + "']";
    //       $(group).prop("checked", false);
    //       $box.prop("checked", true);
    //     } else {
    //       $box.prop("checked", false);
    //     }
    // });

      // ---------- Single Choice Radio ----------
    $('input:radio').on('click', function() {
        var $box = $(this);
        if ($box.is(':checked')) {

          var group = "input:radio[name='" + $box.attr("name") + "']";
          $(group).prop("checked", false);
          $box.prop("checked", true);
        } else {
          $box.prop("checked", false);
        }
      });

    // ---------- Enabled Enter To Submit ----------
    $('#advanced-search-form').on('keypress', function(e) {
        return e.which !== 13;
    });

    // ---------- Advanced Search Submit ----------
    $('#button-advanced-search').click(function(){

        advancedSearchSubmit()
        $('#forminput-page').val('1')

        console.log($('#forminput-status').val())
        $('#advanced-search-form').submit()

    });


});

function appendPageOption(page, total_page){
    console.log(page)
    console.log(total_page)
    for (var i=1; i< total_page+1; i++){
        var page_text = i + ' /' + total_page + '頁'
        if(i != page){
            $('#select-pagination').append($('<option>').val(i).text(page_text));
        }
        else{
            console.log(i)
            $('#select-pagination').append($('<option>').val(i).text(page_text).attr('selected',true));
        }
        
    }


    
}

function paginatorSubmit(){

    
    // // ---------- Caselist ----------
    // if($('#get-input-caselist').html() != "" ){

    //     if($('#get-input-caselist').html() != "['']"){
    //         console.log('emptyyyyyyyyyy')
    //         var str_list = $('#get-input-caselist').html().slice(1,-1).split(', ')
    //         var str_arr = []
    //         str_list.forEach(element => str_arr.push(element));
            
            
    //         $("#forminput-caselist").val(str_arr)
    //     }
    //     else{
    //         $('#get-input-caselist').html('')
    //         $("#forminput-caselist").val()
    //     }   
    // }

    // $('#advanced-search-case-query').val('')

    // // ---------- Num ----------
    // $('#forminput-num').val($('#get-input-num').html())


    // if ($('#get-input-type').html() != ""){
    //     var type_id = 'check-type-'+$('#get-input-type').html()
    //     $('#'+type_id).prop("checked", true);
    // }

    
    // if ($('#get-input-field').html() != ""){
    //     var field_id = 'check-field-'+$('#get-input-field').html()
    //     $('#'+field_id).prop("checked", true);
    // }

    // $('#forminput-date')
    // $('#forminput-work')
    // $('#forminput-constraint')
    // $('#forminput-location')
    // $('#forminput-con')
    // $('#forminput-page')
    //$('#advanced-search-form').submit()




}

function getDefault(){  

    if($('#get-input-page').text() == ""){
        var page = 1
        var total_page = parseInt($('#get-input-total-page').text())
        appendPageOption(page, total_page)
    }
    else{
        var page = parseInt($('#get-input-page').text()) 
        var total_page = parseInt($('#get-input-total-page').text())
        appendPageOption(page, total_page)
    }



    if ($('#get-input-casetype').html() != ""){
        var type_id = 'check-type-'+$('#get-input-casetype').html()

        $('#'+type_id).prop("checked", true);
    }
    else{
        var group = "input:checkbox[name='type']";
        $(group).prop("checked", false);
    }

    if ($('#get-input-casefield').html() != ""){
        var field_id = 'check-field-'+$('#get-input-casefield').html()
        $('#'+field_id).prop("checked", true);
    }
    else{
        var group = "input:checkbox[name='field']";
        $(group).prop("checked", false);
    }

    // if ($('#get-input-type').html() != ""){
    //     var type_id = 'check-type-'+$('#get-input-type').html()
    //     $('#'+type_id).prop("checked", true);
    // }

    // if ($('#get-input-field').html() != ""){
    //     var field_id = 'check-field-'+$('#get-input-field').html()
    //     $('#'+field_id).prop("checked", true);
    // }

    $('.get-input-type').each(function(){
        var type_id = 'check-type-'+$(this).html()
        $('#'+type_id).prop("checked", true);
    })

    $('.get-input-field').each(function(){
        var field_id = 'check-field-'+$(this).html()
        $('#'+field_id).prop("checked", true);
    })

    


    // ---------- Status ----------
    var status = $('#get-input-status').html()
    if (status == "1"){
        $('#select-status option').filter('[value=1]').attr('selected', true)
    }
    else if(status == "2"){
        $('#select-status option').filter('[value=2]').attr('selected', true)
    }
    else if(status == "3"){
        $('#select-status option').filter('[value=3]').attr('selected', true)
    }
    else if(status == "10"){
        $('#select-status option').filter('[value=10]').attr('selected', true)
    }
    else{
        $('#select-status option').filter('[value=0]').attr('selected', true)
    }


    // ---------- Num ----------
    var num = $('#get-input-num').html()
    console.log(num)
    if ( num == "1"){
        $('#select-num option').filter('[value=1]').attr('selected', true)
    }
    else if (num == "5"){
        $('#select-num option').filter('[value=2]').attr('selected', true)
    }
    else if (num == "10"){
        $('#select-num option').filter('[value=3]').attr('selected', true)
    }
    else if (num == "10000"){
        $('#select-num option').filter('[value=0]').attr('selected', true)
    }
    else if (num == "20000"){
        $('#select-num option').filter('[value=4]').attr('selected', true)
    }

    // ---------- Work Mode ----------
    if ($('#get-input-work').html() == '100000000000000000'){
        $('#radio-workmode-0').prop('checked', true)
    }
    else if ($('#get-input-work').html() == '1'){
        $('#radio-workmode-1').prop('checked', true)
    }
    else if ($('#get-input-work').html() == '2'){
        $('#radio-workmode-2').prop('checked', true)
    }

    // ---------- Enddate ----------
    var cd = new Date()
    var ed = $('#get-input-enddate').html()
    cd.setDate(cd.getDate() +4)
    cd = cd.toISOString().substr(0, 10)
    if (cd == ed){
        $('#select-enddate option').filter('[value=1]').attr('selected', true)
    }

    cd = new Date()
    cd.setDate(cd.getDate() +8)
    cd = cd.toISOString().substr(0, 10)
    if (cd == ed){
        $('#select-enddate option').filter('[value=2]').attr('selected', true)
    }

    cd = new Date()
    cd.setMonth(cd.getMonth() +1)
    cd = cd.toISOString().substr(0, 10)
    if (cd == ed){
        $('#select-enddate option').filter('[value=3]').attr('selected', true)
    }

    // ---------- Input: Preference & Location ----------
    if($('#get-input-constraint').html() != 'None'){
        $('#input-preference').val($('#get-input-constraint').html())
    }

    if($('#get-input-location').html() != 'None'){
        $('#input-location').val($('#get-input-location').html())
    }
    
    


    if($('#get-input-caselist').html() != "" ){

        if($('#get-input-caselist').html() != "['']"){
            console.log('emptyyyyyyyyyy')
            var str_list = $('#get-input-caselist').html().slice(1,-1).split(', ')
            var str_arr = []
            str_list.forEach(element => str_arr.push(element));
            
            
            $("#forminput-caselist").val(str_arr)
        }
        else{
            $('#get-input-caselist').html('')
        }
        console.log($('#get-input-caselist').html())
        
    }
    else{
        console.log('is empty')
    }

}

function advancedSearchSubmit(){
    
    // if($('input[name="check-type"]:checked').val() != ""){
    //     $('#forminput-type').val($('input[name="check-type"]:checked').val())
    //     $('#forminput-type').prop("checked", true)
    // }

    // if($('input[name="check-field"]:checked').val() != ""){
    //     $('#forminput-field').val($('input[name="check-field"]:checked').val())
    //     $('#forminput-field').prop("checked", true)
    // }
    // else{
    //     $('#forminput-field').val(null)
    //     $('#forminput-field').prop("checked", true)
    // }
    
    // ---------- Status ----------
    var status = $('#select-status').val()
    if (status == 0){
        $('#forminput-status').val('')
    }
    else if (status == 1){
        $('#forminput-status').val('1')
    }
    else if (status == 2){
        $('#forminput-status').val('2')
    }
    else if (status == 3){
        $('#forminput-status').val('3')
    }
    else  if (status == 10){
        $('#forminput-status').val('10')
    }


    // ---------- Num ----------
    var num = $('#select-num').val()
    if (num == 0){
        $('#forminput-num').val('')
    }
    else if (num == 1){
        $('#forminput-num').val('1')
    }
    else if (num == 2){
        $('#forminput-num').val('5')
    }
    else if (num == 3){
        $('#forminput-num').val('10')
    }
    else{
        $('#forminput-num').val('')
    }

    // ---------- Enddate ----------
    var period = $('#select-enddate').val()
    var enddate = new Date()
    if (period == 0){
        // Unlimited
        $('#forminput-date').val('')
    }
    else if (period == 1){
        // Under 3 days
        enddate.setDate(enddate.getDate() + 4); 
        enddate = enddate.toISOString().substr(0, 10)
        $('#forminput-date').val(enddate)
    }
    else if (period == 2){
        // Under 1 week
        enddate.setDate(enddate.getDate() + 8); 
        enddate = enddate.toISOString().substr(0, 10)
        $('#forminput-date').val(enddate)
    }
    else if (period == 3){
        // Under 1 month
        enddate.setMonth(enddate.getMonth() + 1); 
        enddate = enddate.toISOString().substr(0, 10)
        $('#forminput-date').val(enddate)

    }
    else{
        $('#forminput-date').val('')
    }

    // ---------- Workmode ----------
    if ($('input[name="workmode"]:checked').val()== 0){
        $('#forminput-work').val('')
    }
    else{
        $('#forminput-work').val(parseInt($('input[name="workmode"]:checked').val()))
    }

    // console.log($('#input-preference').val() == '')
    $('#forminput-constraint').val($('#input-preference').val())
    $('#forminput-location').val($('#input-location').val())

    // console.log($('#forminput-type').val())
    // console.log($('#forminput-field').val())
    console.log($('#forminput-num').val())
    // console.log($('#forminput-date').val())
    // console.log($('#forminput-work').val())
    // console.log($('#forminput-constraint').val())
    // console.log($('#forminput-location').val())
    // console.log($("#forminput-caselist").val())
    // console.log($('#forminput-page').val())
    
    if(typeof  $('input[name="field"]:checked').val() === "undefined" && typeof  $('input[name="type"]:checked').val() === "undefined"){
        $('#forminput-con').val('0')
    }
    console.log($('#forminput-con').val())

    $('#advanced-search-case-query').val("")
}

function recountCaseLength(){
    var case_counter = 0
    $('.case-counter').each(function(){

        case_counter += 1

    })

    $('#case-length').html(case_counter)
}

function userRate(rate){

    var rate_html = ''
    let starnum = Math.floor(rate)
    for (var i = 0; i < 5; i++ ) {
        if(starnum > 0){
            rate_html = rate_html + '<i class="material-icons star-color">star</i>'
        }
        else if (starnum == 0){
            if(rate % 1 >= 0.5){
                rate_html = rate_html + '<i class="material-icons star-color">star_half</i>'
            }
            else{
                rate_html = rate_html + '<i class="material-icons star-color">star_border</i>'
            }
        }
        else{
            rate_html = rate_html + '<i class="material-icons star-color">star_border</i>'
        }
        starnum = starnum - 1 
    }

    return rate_html
}

function userLastLogin(lastlogin){
    var currentdate = new Date();
    var year = lastlogin.split('年')[0]
    var month = lastlogin.split('年')[1].split('月')[0]
    var date =  lastlogin.split('年')[1].split('月')[1].split('日')[0]
    var hour = lastlogin.split('年')[1].split('月')[1].split('日')[1].split(':')[0]
    var minutes = lastlogin.split('年')[1].split('月')[1].split('日')[1].split(':')[1]
    lastlogin = new Date(year, month-1, date, hour, minutes)


    var llt = convertMS(Math.abs((currentdate.getTime() - lastlogin.getTime())))
    if($('#language option').filter(':selected').val() == 'en'){
        var llt_str = 'login: ' + llt + ' ago'
    }
    else{
        var llt_str = llt + ' 前登入'
    }
    
    return  llt_str 
}

function convertMS(millisecondes){
    let seconds = millisecondes / 1000
    if(seconds < 60){
        if($('#language option').filter(':selected').val() == 'en'){
            return 'less than 1 min'
        }
        else{
            return '不到1分鐘'
        }
    }
    else{
        let minutes = seconds / 60
        if (minutes < 60){
            if($('#language option').filter(':selected').val() == 'en'){
                return Math.floor(minutes).toString() + ' mins'
            }
            else{
                return Math.floor(minutes).toString() + ' 分鐘'
            }
            
        }
        else{
            let hours = minutes/60
            if (hours < 24){
                if($('#language option').filter(':selected').val() == 'en'){
                    return Math.floor(hours).toString() + ' hours'
                }
                else{
                    return Math.floor(hours).toString() + ' 小時'
                }
                
            }
            else{
                let days = hours/24
                if(days < 31){
                    if($('#language option').filter(':selected').val() == 'en'){
                        return Math.floor(days).toString() + ' days'
                    }
                    else{
                        return Math.floor(days).toString() + ' 天'
                    }
                    
                }
                else{
                    let months = days/30
                    if(months < 12){
                        if($('#language option').filter(':selected').val() == 'en'){
                            return Math.floor(months).toString() + ' months'
                        }
                        else{
                            return Math.floor(months).toString() + ' 個月'
                        }
                        
                    }
                    else{
                        let years = months/12
                        if($('#language option').filter(':selected').val() == 'en'){
                            return Math.floor(years).toString() + ' year'
                        }
                        else{
                            return Math.floor(years).toString() + ' 年'
                        }
                        
                    }
                }
            }
        }

    }
    
}