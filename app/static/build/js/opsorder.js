function addOrder(crisis_id,action_id)
{
    var SAF = $("#" + action_id + "_SAF")[0].value;
    var SCDF = $("#" + action_id + "_SCDF")[0].value;
    var SPF = $("#" +action_id + "_SPF")[0].value;
    var Cleaner = $("#" +action_id + "_Cleaners")[0].value;
    var Description = document.getElementById("txt_description").value;

    $.ajax({
            type: "GET",
            data: {"crisis_id":crisis_id,"action_id":action_id,"SAF":SAF,"SCDF":SCDF,"SPF":SPF,"Cleaner":Cleaner,"description":Description},
            url: '/addOpsOrder',
            dataType: 'json',
            success: function (data) {
            }
    });
}