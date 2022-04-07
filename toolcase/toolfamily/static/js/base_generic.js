$(document).ready(function() {

    $('#button-case-new').click(function(){
        window.location.href = "{% url 'case-new'%}";
    });

});
