$(document).ready(function(){
    if ($('.event-cards .card').length > 5) {
        $('.event-cards').slick({
            slidesToShow:5,
            slidesToScroll:5,
            arrows: true,
            prevArrow:"<i class='far fa-caret-circle-left fa-3x slick-prev'></i>",
            nextArrow:"<i class='far fa-caret-circle-right fa-3x slick-next'></i>",
            responsive: [
                {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                    infinite: true,
                    dots: true
                }
                },
                {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                }
                },
                {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
                }
            ]
        });
    }   
});
