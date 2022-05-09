$(document).ready(function() {
    $('#reportModal').on('hidden.bs.modal', function () {
        $(this).find('form').trigger('reset');
    })
    var reportModal = document.getElementById('reportModal')
    reportModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget;
    // Extract info from data-bs-* attributes
    var object_info = button.getAttribute('data-bs-whatever');
    // Update the modal's content.
    var modalObj = reportModal.querySelector('#report_obj');
    modalObj.value = object_info;
    })
    // reportModal.addEventListener('show.bs.modal', function (event) {
    //     // Button that triggered the modal
    //     var button = event.relatedTarget;
    //     // Extract info from data-bs-* attributes
    //     var user_info = button.getAttribute('data-user');
    //     var case_info = button.getAttribute('data-case');
    //     // Update the modal's content.
    //     var modaluser = reportModal.querySelector('.reported_user');
    //     modaluser.value = user_info;
    //     var modalcase = reportModal.querySelector('.reported_case');
    //     modalcase.value = case_info;
    //     })

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
            },
            error: function(data) {
                console.log('無法送出');
                alert('無法傳送！');
            }
        })
    });
});
