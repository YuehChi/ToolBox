$(document).ready(function() {
    var reportModal = document.getElementById('reportModal')
    reportModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var recipient = button.getAttribute('data-bs-whatever')
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    var modalTitle = reportModal.querySelector('.modal-title')

    modalTitle.textContent = recipient
    })
    // // $('#reportDIV').load( 'toolcase\toolfamily\templates\report.html' );
    // $('#reportModal').on('show.bs.modal', function (event) {
    //     alert("QQ");
    //     var button = $(event.relatedTarget) // Button that triggered the modal
    //     var recipient = button.data('whatever') // Extract info from data-* attributes
    //     // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    //     // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    //     var modal = $(this)
    //     modal.find('.modal-title').text(recipient)
    //   })
});