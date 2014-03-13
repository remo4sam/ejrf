function makePostRequest(url, data) {
    var jForm = $('<form></form>');
    jForm.attr('action', url);
    jForm.attr('method', 'post');
    for (name in data) {
        var jInput = $("<input/>");
        jInput.attr({'name' : name, 'value': data[name], 'type': 'hidden'});
        jForm.append(jInput);
    }
    var button = $("<input type='submit' style='display: none'/>");
    jForm.append(button);
    $("body").append(jForm);
    button.trigger('click');
}

$(function(){
    $("a[post=true]").each(function () {
        $(this).on('click', function (e) {
            e.preventDefault();
            makePostRequest(
                $(this).attr('phref'),
                JSON.parse($(this).attr('pdata'))
            );
        });
    });
});