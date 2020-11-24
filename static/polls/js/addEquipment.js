$(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

$(".addEquipment").click(function (){
    console.log("click");
    $.ajax({
        url: "/addEquipment/",
        method: 'GET',
        dataType: 'json',
        data:{name:$(this).attr("name")},
        success: function (result, status) {
            if (result=='ok'){
                console.log("ok");
                $(this).hide()
            }else {
                alert(result);
            }
        }
    });
});