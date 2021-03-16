$(document).ready(function(){
    $("#register-button").on("click", function(){
        if (!$(this).hasClass('active')) {
            $(this).text("Unregister")
            $(this).removeClass('btn-primary').addClass("btn-danger")
            let userId = $(this).data('userid')
            let eventId = $(this).data('eventid')
            let csrfToken = $(this).data('token')

            $.ajax({
                type: "POST",
                url: `${eventId}/assoc_event/${userId}/`,
                headers: {'X-CSRFToken': csrfToken},
                success: function(response) {
                    console.log(response)
                },
                error: function(e){
                    console.log(e)
                }
            });


        } else {
            $(this).text("Register")
            $(this).removeClass('btn-danger').addClass("btn-primary")
        }
    })
})
