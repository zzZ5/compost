$(".addEquipment").click(function (){
    console.log("click");
    var add_equipment = $(this);
    $.ajax({
        url: "/addEquipment/",
        method: 'GET',
        dataType: 'text',
        data:{name:add_equipment.attr("name")},
        success:function (result, status) {
            console.log(result);
            if (result == 'ok'){
                add_equipment.hide();
                alert("添加成功！");
            }else {
                alert(result);
            }
        },
        error: function (result){
            alert("dData transmission error！");
        }
    });
});