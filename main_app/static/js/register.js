$(document).ready(function(){
    $("#register-button").on("click", function(){
        if (!$(this).hasClass('active')) {
            $(this).text("Unregister")
            $(this).removeClass('btn-primary').addClass("btn-danger")
        } else {
            $(this).text("Register")
            $(this).removeClass('btn-danger').addClass("btn-primary")
        }
    })
})
