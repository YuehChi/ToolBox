$(document).ready(function() {
    $('#reportModal').on('hidden.bs.modal', function () {
        $(this).find('form').trigger('reset');
    })
    var reportModal = document.getElementById('reportModal')
    reportModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget;
    // Extract info from data-bs-* attributes

    if(button.getAttribute('data-user')){
        var user_info = button.getAttribute('data-user');
        var user_name = button.getAttribute('user-name');
        var userObj = reportModal.querySelector('#report_user');
        userObj.value = user_info;
        var usertext = reportModal.querySelector('#text-user');
        usertext.value = user_name;
    }
    if(button.getAttribute('data-case')){
        // alert(button.getAttribute('data-case'));
        var case_info = button.getAttribute('data-case');
        var case_name = button.getAttribute('case-name');
        var caseObj = reportModal.querySelector('#report_case');
        caseObj.value = case_info;
        var casetext = reportModal.querySelector('#text-case');
        casetext.value = case_name;
    }


    // Update the modal's content.
    // var modalObj = reportModal.querySelector('#report_obj');
    // modalObj.value = object_info;
    })

    //需要在 modal 顯示時就填入要檢舉的 case 與 user 資訊!!!

    $('#reportModal .modal-footer button.btn-primary').on('click', function(e){
        e.preventDefault(); //阻止頁面跳轉

        var theForm = $(this).parents('.modal-footer')
            .siblings('.modal-body').children('form');
        var formData = theForm.serialize();
        console.log('submit the form in modal:', formData);

        $.ajax({
            url: theForm.attr('action'),
            type: "POST",
            data: formData,
            success: function(data) {
                console.log('成功送出', data);
                alert('已成功送出舉報！');
                theForm.parents('.modal').modal('hide');
                window.location.reload();
            },
            error: function(error) {
                console.log(error);
                if(error.responseJSON.error){
                    console.log('檢舉失敗:', error.responseJSON.error);
                    alert('檢舉失敗 (' + error.responseJSON.error + ')');
                }else{
                    console.log('檢舉失敗');
                    alert('檢舉失敗（不明原因）');
                }
            }
        })
    });
});
