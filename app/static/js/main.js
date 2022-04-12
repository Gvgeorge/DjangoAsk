console.log('script loaded')


$(document).ready(function (){
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    $("#like-btn").click(function (){
        $.ajax({
            url: $('#like-btn-form').data('url'),
            type: 'POST',
            data: {csrfmiddlewaretoken: csrfToken},
            success: function(xhr){
                console.log(xhr)
                var is_authenticated = xhr.authenticated;
                if (is_authenticated === true) {
                    $("#like-btn").text(xhr.rating)

                    if (xhr.liked == true) {
                        $("#like-btn").css('background-color', 'red')
                    } else {
                        $("#like-btn").css('background-color', 'blue')
                    }
                }
                else{
                    alert( 'Please LOG IN!')
                }
            }

        });

    });

});