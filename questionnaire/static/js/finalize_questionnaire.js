function makePostRequest(url, data) {
    console.log(url);
    console.log(data);
    var jForm = $('<form></form>');
    jForm.attr('action', url);
    jForm.attr('method', 'post');
    for (name in data) {
        var jInput = $("<input>");
        jInput.attr('name', name);
        jInput.attr('value', data[name]);
        jForm.append(jInput);
    }
    //console.log(jForm);
    jForm.submit();
}

$(function(){
    $("a[post=true]").each(function () {
        console.log('here');
        $(this).on('click', function () {
            makePostRequest(
                $(this).attr('phref'),
                JSON.parse($(this).attr('pdata'))
            );
        });
    });
});