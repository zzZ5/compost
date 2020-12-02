$("#all_select").click(function () {
    console.log("click");
    $("input[type='checkbox']").attr("checked", true);
});

$("#all_unselect").click(function () {
    console.log("click");
    $("input[type='checkbox']").attr("checked", false);
});