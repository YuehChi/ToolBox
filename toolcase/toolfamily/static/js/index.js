$(document).ready(function(){

    
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

    // ---------- Enabled Enter To Submit ----------
    $('#index-form').on('keypress', function(e) {
        return e.which !== 13;
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