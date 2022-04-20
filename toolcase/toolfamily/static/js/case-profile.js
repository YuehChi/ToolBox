<<<<<<< HEAD
<<<<<<< HEAD
$(document).ready(function() {

    // --------------- Case Edit Button ---------------
    if($('#get-user-id').html() == $('#get-loginuser-id').html()){
        $('#link-edit').removeClass('d-none')
        $('#case-buttons').addClass('d-none')
    }

    // --------------- Case Status ---------------
    var case_status = $('#get-case-status').html()
    console.log('case_status:' + case_status)
    if(case_status == '徵求'){
        $('#case-status').html('徵求中')
    }



    // --------------- Case Time ---------------
    var enddate =$('#get-case-enddate').html()
    var year = enddate.split('年')[0]
    var month = enddate.split('年')[1].split('月')[0]
    var date =  enddate.split('年')[1].split('月')[1].split('日')[0]
    enddate = new Date(month + '/' + date + '/' + year)
    var currentdate = new Date();

    var remainday = convertMS(Math.abs((enddate.getTime() - currentdate.getTime())))
    //var remainday = enddate.getDate() - currentdate.getDate()

    console.log(enddate)
    console.log(currentdate)
    console.log(remainday)
    enddate = year + '/' + month + '/' + date

    var startdate = $('#get-case-startdate').html()
    var year = startdate.split('年')[0]
    var month = startdate.split('年')[1].split('月')[0]
    var date =  startdate.split('年')[1].split('月')[1].split('日')[0]
    startdate = year + '/' + month + '/' + date





    $('#case-time').html(startdate + ' ~ ' + enddate + ' 還剩' + remainday)



    // --------------- Case Description ---------------
    var description = $('#get-case-description').html()
    description = description.replaceAll('\n', '<br>')
    $('#case-description').html(description)

    // --------------- Case Images ---------------
    var case_images = document.getElementsByClassName('case-img')
    var show_num = 2

    // carousel-inner
    var imgitems_html = ''
    var imgindicator_html = ''
    if(case_images.length != 0){
        imgitems_html = imgitems_html + '<div class="carousel-item active"><div class="row">'
        imgindicator_html = imgindicator_html + '<li data-bs-target="#carousel-case-images" data-bs-slide-to="0" class="active"></li>'
        for (i=0; i<case_images.length; i++){
            // console.log(case_images[i].src)
            // console.log(imgitems_html)

            if(i<show_num){
                // console.log('i<show_num')
                // console.log(imgitems_html)
                imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block show-type" src="' + case_images[i].src + '" alt="Slide Image"></div>'
            }
            else{
                console.log('i>show_num')
                if(i%show_num == 0 && i!=0){
                    // console.log('i%show_num == 0 && i!=0')
                    // console.log(imgitems_html)
                    imgitems_html = imgitems_html + '</div></div>'
                    imgitems_html = imgitems_html + '<div class="carousel-item"><div class="row">'
                    imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block show-type" src="' + case_images[i].src + '" alt="Slide Image"></div>'
                    imgindicator_html = imgindicator_html + '<li data-bs-target="#carousel-case-images" data-bs-slide-to="'+ Math.floor(i/show_num) +'"></li>'
                }
                else{
                    // console.log('i%show_num != 0 || i==0')
                    // console.log(imgitems_html)
                    imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block show-type" src="' + case_images[i].src + '" alt="Slide Image"></div>'
                }
            }
        }
        if(case_images.length %show_num != 0){
            imgitems_html = imgitems_html + '<div class="col padding-none"></div>'
        }
        // console.log(imgitems_html)
        imgitems_html = imgitems_html + '</div></div>'
            
        //     if (i==0){
        //         imgitems_html = '<div class="carousel-item active"><div class="row">'
        //         imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block" src="' + case_images[i].src + '" alt="Slide Image"></div>'
        //         imgindicator_html = imgindicator_html + '<li data-bs-target="#carousel-case-images" data-bs-slide-to="0" class="active"></li>'
        //     }
        //     else if(i%show_num == 1){
        //         imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block" src="' + case_images[i].src + '" alt="Slide Image"></div>'
        //     }
        //     else if(i%show_num == 2){
        //         imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block" src="' + case_images[i].src + '" alt="Slide Image"></div>'
        //     }
        //     else if(i%show_num == 0 && i!=0){
        //         imgitems_html = '<div class="carousel-item"><div class="row">'
        //         imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block" src="' + case_images[i].src + '" alt="Slide Image"></div>'
        //         imgindicator_html = imgindicator_html + '<li data-bs-target="#carousel-case-images" data-bs-slide-to="'+ Math.floor(i/show_num) +'"></li>'
        //         console.log(Math.floor(i/show_num))
        //     }
        // }
        // imgitems_html = imgitems_html + '</div></div>'
    }
    // console.log(imgitems_html)
    // console.log(imgindicator_html)
    $('.carousel-inner').html(imgitems_html)
    $('.carousel-indicators').html(imgindicator_html)





    // console.log(case_images)


    // ------------------------------ User ------------------------------
    $('#user-nickname').html($('#get-user-nickname').html())
    $('#user-department').html($('#get-user-department').html())
    //$('#user-icon').attr('src', $('#get-user-icon').html())
    $('#user-icon').css('background-image', 'url('+$('#get-user-icon').html()+')')
    // $('#user-icon').attr('style', "background-image:" + $('#get-user-icon').html())
    console.log($('#get-user-lastlogintime').html())
    // --------------- User Gender ---------------
    var gender = $('#get-user-gender').html()
    if (gender == 0){
        //genderless
        $('#user-gender').attr('src', '/static/images/gender-male-female.png')
        // console.log(gender)
    }
    else if (gender == 1){
        //male
        $('#user-gender').attr('src', '/static/images/gender-male.png')
        // console.log(gender)
    }
    else if (gender == 2){
        //female
        $('#user-gender').attr('src', '/static/images/gender-female.png')
        // console.log(gender)
    }

    // --------------- User Last Login Time ---------------
    var lastlogin = $('#get-user-lastlogintime').html()
    
    var year = lastlogin.split('年')[0]
    var month = lastlogin.split('年')[1].split('月')[0]
    var date =  lastlogin.split('年')[1].split('月')[1].split('日')[0]
    var hour = lastlogin.split('年')[1].split('月')[1].split('日')[1].split(':')[0]
    var minutes = lastlogin.split('年')[1].split('月')[1].split('日')[1].split(':')[1]
    lastlogin = new Date(year, month-1, date, hour, minutes)


    var llt = convertMS(Math.abs((currentdate.getTime() - lastlogin.getTime())))
    console.log(llt)
    $('#user-lastlogintime').html('上次登入: ' + llt + '前')

    // --------------- User Rate ---------------
    console.log($('#get-user-rate').html())
    console.log($('#get-user-ratenum').html())
    var rate = $('#get-user-rate').html()
    var rate_html = ''
    let starnum = Math.floor(rate)
    for (var i = 0; i < 5; i++ ) {
        //starnum: 3, 2, 1, 0, -1
        //i      : 0, 1, 2, 3, 4
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

    console.log(rate_html)
    $('#user-rate').html(rate_html)
    $('#user-ratenum').html('('+ $('#get-user-ratenum').html() + ')')




    console.log($('#get-case-description').html())
    console.log($('#get-user-department').html())
    console.log($('#get-user-rate').html())
    console.log($('#get-user-ratenum').html())
    console.log($('#get-user-lastlogintime').html())


});

function convertMS(millisecondes){
    let seconds = millisecondes / 1000
    if(seconds < 60){
        return '不到1分鐘'
    }
    else{
        let minutes = seconds / 60
        if (minutes < 60){
            console.log('minutes:' + Math.floor(minutes))
            return Math.floor(minutes).toString() + ' 分鐘'
        }
        else{
            let hours = minutes/60
            if (hours < 24){
                console.log('hours:' + hours)
                return Math.floor(hours).toString() + ' 小時'
            }
            else{
                let days = hours/24
                if(days < 31){
                    console.log('days:' + days)
                    return Math.floor(days).toString() + ' 天'
                }
                else{
                    let months = days/30
                    if(months < 12){
                        console.log('months:' + months)
                        return Math.floor(months).toString() + ' 個月'
                    }
                    else{
                        let years = months/12
                        console.log('years:' + years)
                        return Math.floor(years).toString() + ' 年'
                    }
                }
            }
        }

    }

}
=======
=======
>>>>>>> User-2.0
$(document).ready(function() {

    // --------------- Case Status ---------------
    var case_status = $('#get-case-status').html()
    console.log('case_status:' + case_status)
    if(case_status == '徵求'){
        $('#case-status').html('徵求中')
    }


    // --------------- Case Time ---------------
    var enddate =$('#get-case-enddate').html()
    var year = enddate.split('年')[0]
    var month = enddate.split('年')[1].split('月')[0]
    var date =  enddate.split('年')[1].split('月')[1].split('日')[0]
    enddate = new Date(month + '/' + date + '/' + year)
    var currentdate = new Date();
    var remainday = enddate.getDate() - currentdate.getDate()
    enddate = year + '/' + month + '/' + date

    var startdate = $('#get-case-startdate').html()
    var year = startdate.split('年')[0]
    var month = startdate.split('年')[1].split('月')[0]
    var date =  startdate.split('年')[1].split('月')[1].split('日')[0]
    startdate = year + '/' + month + '/' + date


    $('#case-time').html(startdate + ' ~ ' + enddate + ' 還剩' + remainday + '天')


    // --------------- Case Description ---------------
    var description = $('#get-case-description').html()
    description = description.replaceAll('\n', '<br>')
    $('#case-description').html(description)

    // --------------- Case Images ---------------
    var case_images = document.getElementsByClassName('case-img')
    var show_num = 2

    // carousel-inner
    var imgitems_html = ''
    var imgindicator_html = ''
    if(case_images.length != 0){
        imgitems_html = imgitems_html + '<div class="carousel-item active"><div class="row">'
        imgindicator_html = imgindicator_html + '<li data-bs-target="#carousel-case-images" data-bs-slide-to="0" class="active"></li>'
        for (i=0; i<case_images.length; i++){
            // console.log(case_images[i].src)
            // console.log(imgitems_html)

            if(i<show_num){
                // console.log('i<show_num')
                // console.log(imgitems_html)
                imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block" src="' + case_images[i].src + '" alt="Slide Image"></div>'
            }
            else{
                console.log('i>show_num')
                if(i%show_num == 0 && i!=0){
                    // console.log('i%show_num == 0 && i!=0')
                    // console.log(imgitems_html)
                    imgitems_html = imgitems_html + '</div></div>'
                    imgitems_html = imgitems_html + '<div class="carousel-item"><div class="row">'
                    imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block" src="' + case_images[i].src + '" alt="Slide Image"></div>'
                    imgindicator_html = imgindicator_html + '<li data-bs-target="#carousel-case-images" data-bs-slide-to="'+ Math.floor(i/show_num) +'"></li>'
                }
                else{
                    // console.log('i%show_num != 0 || i==0')
                    // console.log(imgitems_html)
                    imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block" src="' + case_images[i].src + '" alt="Slide Image"></div>'
                }
            }
        }
        if(case_images.length %show_num != 0){
            imgitems_html = imgitems_html + '<div class="col padding-none"></div>'
        }
        // console.log(imgitems_html)
        imgitems_html = imgitems_html + '</div></div>'
            
        //     if (i==0){
        //         imgitems_html = '<div class="carousel-item active"><div class="row">'
        //         imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block" src="' + case_images[i].src + '" alt="Slide Image"></div>'
        //         imgindicator_html = imgindicator_html + '<li data-bs-target="#carousel-case-images" data-bs-slide-to="0" class="active"></li>'
        //     }
        //     else if(i%show_num == 1){
        //         imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block" src="' + case_images[i].src + '" alt="Slide Image"></div>'
        //     }
        //     else if(i%show_num == 2){
        //         imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block" src="' + case_images[i].src + '" alt="Slide Image"></div>'
        //     }
        //     else if(i%show_num == 0 && i!=0){
        //         imgitems_html = '<div class="carousel-item"><div class="row">'
        //         imgitems_html = imgitems_html + '<div class="col padding-none"><img class="w-100 d-block" src="' + case_images[i].src + '" alt="Slide Image"></div>'
        //         imgindicator_html = imgindicator_html + '<li data-bs-target="#carousel-case-images" data-bs-slide-to="'+ Math.floor(i/show_num) +'"></li>'
        //         console.log(Math.floor(i/show_num))
        //     }
        // }
        // imgitems_html = imgitems_html + '</div></div>'
    }
    // console.log(imgitems_html)
    // console.log(imgindicator_html)
    $('.carousel-inner').html(imgitems_html)
    $('.carousel-indicators').html(imgindicator_html)





    // console.log(case_images)


    // ------------------------------ User ------------------------------
    $('#user-nickname').html($('#get-user-nickname').html())
    $('#user-department').html($('#get-user-department').html())
    $('#user-icon').attr('src', $('#get-user-icon').html())
    // $('#user-icon').attr('style', "background-image:" + $('#get-user-icon').html())
    console.log($('#get-user-lastlogintime').html())
    // --------------- User Gender ---------------
    var gender = $('#get-user-gender').html()
    if (gender == 0){
        //genderless
        $('#user-gender').attr('src', '/static/images/gender-male-female.png')
        // console.log(gender)
    }
    else if (gender == 1){
        //male
        $('#user-gender').attr('src', '/static/images/gender-male.png')
        // console.log(gender)
    }
    else if (gender == 2){
        //female
        $('#user-gender').attr('src', '/static/images/gender-female.png')
        // console.log(gender)
    }

    // --------------- User Last Login Time ---------------
    var lastlogin = $('#get-user-lastlogintime').html()

    var year = lastlogin.split('年')[0]
    var month = lastlogin.split('年')[1].split('月')[0]
    var date =  lastlogin.split('年')[1].split('月')[1].split('日')[0]
    var hour = lastlogin.split('年')[1].split('月')[1].split('日')[1].split(':')[0]
    var minutes = lastlogin.split('年')[1].split('月')[1].split('日')[1].split(':')[1]
    lastlogin = new Date(year, month-1, date, hour, minutes)


    function convertMS(millisecondes){
        let seconds = millisecondes / 1000
        if(seconds < 60){
            return '不到1分鐘前'
        }
        else{
            let minutes = seconds / 60
            if (minutes < 60){
                console.log('minutes:' + Math.floor(minutes))
                return Math.floor(minutes).toString() + ' 分鐘前'
            }
            else{
                let hours = minutes/60
                if (hours < 24){
                    console.log('hours:' + hours)
                    return Math.floor(hours).toString() + ' 小時前'
                }
                else{
                    let days = hours/24
                    if(days < 31){
                        console.log('days:' + days)
                        return Math.floor(days).toString() + ' 天前'
                    }
                    else{
                        let months = days/30
                        if(months < 12){
                            console.log('months:' + months)
                            return Math.floor(months).toString() + ' 個月前'
                        }
                        else{
                            let years = months/12
                            console.log('years:' + years)
                            return Math.floor(years).toString() + ' 年前'
                        }
                    }
                }
            }

        }

    }

    var llt = convertMS(Math.abs((currentdate.getTime() - lastlogin.getTime())))
    console.log(llt)
    $('#user-lastlogintime').html('上次登入: ' + llt)

    // --------------- User Rate ---------------
    console.log($('#get-user-rate').html())
    console.log($('#get-user-ratenum').html())
    var rate = $('#get-user-rate').html()
    var rate_html = ''
    let starnum = Math.floor(rate)
    for (var i = 0; i < 5; i++ ) {
        //starnum: 3, 2, 1, 0, -1
        //i      : 0, 1, 2, 3, 4
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

    console.log(rate_html)
    $('#user-rate').html(rate_html)
    $('#user-ratenum').html('('+ $('#get-user-ratenum').html() + ')')




    console.log($('#get-case-description').html())
    console.log($('#get-user-department').html())
    console.log($('#get-user-rate').html())
    console.log($('#get-user-ratenum').html())
    console.log($('#get-user-lastlogintime').html())







});
<<<<<<< HEAD
>>>>>>> origin/Server
=======

>>>>>>> User-2.0
