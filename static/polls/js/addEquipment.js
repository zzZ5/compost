$(".addEquipment").click(function (){
    console.log("click");
    var add_equipment = $(this);
    var data = {name:add_equipment.attr("name")};
    add_equipment.hide()
    $('#' + data["name"]).show()
    if (add_equipment.hasClass('iconjian1')){
        data["action"] = 'remove'
    } else {
        data["action"] = 'add'
    }
    $.ajax({
        url: "/addEquipment/",
        method: 'GET',
        dataType: 'JSON',
        data: data,
        success:function (result, status) {
            console.log(result);
            if (result['Code'] == 'ok'){
                if(add_equipment.hasClass('iconjian1')){
                    add_equipment.removeClass("iconjian1");
                    add_equipment.addClass("iconjiatianjiakuangxuanduoxuan-8");
                    add_equipment.attr("title","添加到我的设备");
                    alert(result['Message']);
                }else {
                    add_equipment.removeClass("iconjiatianjiakuangxuanduoxuan-8");
                    add_equipment.addClass("iconjian1");
                    add_equipment.attr("title","从我的设备移除");
                    alert(result['Message']);
                }
            }else {
                alert("error: " + result['Code'] + '\n' + result['Message']);
            }
            $('#' + data["name"]).hide()
            add_equipment.show()
        },
        error: function (result){
            alert("Data transmission error！");
        }
    });
});