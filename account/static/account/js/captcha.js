$(".captcha").click(function (){
    console.log("click");
    $.ajax({
        url: "/captcha/refresh/",
        method: 'GET',
        dataType: 'json',
        success: function (result, status) {
            $('.captcha').attr('src', result['image_url']);
            $('#id_captcha_0').val(result['key'])
        }
    });
});
