$("#all_select").click(function () {
    console.log("click");
    $("input[type='checkbox']").prop("checked", true);
});

$("#all_unselect").click(function () {
    console.log("click");
    $("input[type='checkbox']").prop("checked", false);
});