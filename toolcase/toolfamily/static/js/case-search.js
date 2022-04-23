$(document).ready(function(){

    
    getDefault()

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
    $('input:checkbox').on('click', function() {
        var $box = $(this);
        if ($box.is(':checked')) {

          var group = "input:checkbox[name='" + $box.attr("name") + "']";
          $(group).prop("checked", false);
          $box.prop("checked", true);
        } else {
          $box.prop("checked", false);
        }
    });

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
        $('#advanced-search-form').submit();


    });


});

function getDefault(){
    if ($('#get-input-casetype').html() != ""){
        var type_id = 'check-type-'+$('#get-input-casetype').html()

        $('#'+type_id).prop("checked", true);
    }

    if ($('#get-input-casefield').html() != ""){
        var field_id = 'check-field-'+$('#get-input-casefield').html()
        $('#'+field_id).prop("checked", true);
    }

    if ($('#get-input-type').html() != ""){
        var type_id = 'check-type-'+$('#get-input-type').html()
        $('#'+type_id).prop("checked", true);
    }

    
    if ($('#get-input-field').html() != ""){
        var field_id = 'check-field-'+$('#get-input-field').html()
        $('#'+field_id).prop("checked", true);
    }

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

    if ($('#get-input-work').html() == '100000000000000000'){
        $('#radio-workmode-0').prop('checked', true)
    }
    else if ($('#get-input-work').html() == '1'){
        $('#radio-workmode-1').prop('checked', true)
    }
    else if ($('#get-input-work').html() == '2'){
        $('#radio-workmode-2').prop('checked', true)
    }

    if($('#get-input-caselist').html() != ""){

        console.log()
        var str_list = $('#get-input-caselist').html().slice(1,-1).split(', ')
        var str_arr = []
        str_list.forEach(element => str_arr.push(element) );
        
        
        $("#forminput-caselist").val(str_arr)
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

    console.log($('#input-preference').val() == '')
    $('#forminput-constraint').val($('#input-preference').val())
    $('#forminput-location').val($('#input-location').val())

    console.log($('#forminput-type').val())
    console.log($('#forminput-field').val())
    console.log($('#forminput-num').val())
    console.log($('#forminput-date').val())
    console.log($('#forminput-work').val())
    console.log($('#forminput-constraint').val())
    console.log($('#forminput-location').val())
    console.log($("#forminput-caselist").val())
    
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
    var llt_str = llt + '前登入'
    return  llt_str 
}

function convertMS(millisecondes){
    let seconds = millisecondes / 1000
    if(seconds < 60){
        return '不到1分鐘'
    }
    else{
        let minutes = seconds / 60
        if (minutes < 60){
            return Math.floor(minutes).toString() + ' 分鐘'
        }
        else{
            let hours = minutes/60
            if (hours < 24){
                return Math.floor(hours).toString() + ' 小時'
            }
            else{
                let days = hours/24
                if(days < 31){
                    return Math.floor(days).toString() + ' 天'
                }
                else{
                    let months = days/30
                    if(months < 12){
                        return Math.floor(months).toString() + ' 個月'
                    }
                    else{
                        let years = months/12
                        return Math.floor(years).toString() + ' 年'
                    }
                }
            }
        }

    }
    
}