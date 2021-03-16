$(document).ready(function(){
    $("#register-button").on("click", function(){
        let userId = $(this).data('userid')
        let eventId = $(this).data('eventid')
        let csrfToken = $(this).data('token')
        
        if (!$(this).hasClass('active')) {
            $(this).hide()
            $('#unregister-trigger').show()

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


        } 
    })

    $('#unregister-button').on('click', function(){
        let userId = $(this).data('userid')
        let eventId = $(this).data('eventid')
        let csrfToken = $(this).data('token')
        $("#register-button").show()
        $('#unregister-trigger').hide()

        $.ajax({
            type: "POST",
            url: `${eventId}/unassoc_event/${userId}/`,
            headers: {'X-CSRFToken': csrfToken},
            success: function(response) {
                console.log(response)
            },
            error: function(e){
                console.log(e)
            }
         });
    })
})

