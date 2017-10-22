function submit_form() {
    
    var url = $("form").attr("action");
    var data = $("form").serialize();
    var type = $("form").attr("method");
    
    $.ajax({
        url : url,
        data : data,
        type : type,
        success : function(json) {
            window.location = $("#cancel").attr("href");
        }
    });
}

$(function() {
    $("#submit").click(submit_form);
});